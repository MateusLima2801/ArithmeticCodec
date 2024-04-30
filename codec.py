import json
import math
import os
import numpy as np
from image import Image
import matplotlib.pyplot as plt

class ArithmeticCodec:
    
    def encode(self, filename: str, encode_block_dim: tuple = (8,8)):
        img = Image.read_from_pgm_file(filename)
        nickname = f"{img.name}_{encode_block_dim[0]}_{encode_block_dim[1]}"
        prob_table = self.calculate_probability_table(img)
        self.write_info_to_json(prob_table, encode_block_dim, img.dim, img.max,f"results\\{nickname}.json")
        encrypted_code_file = f"results\\{nickname}.txt"
        f = open(encrypted_code_file, "w")
        img.divide_array_in_blocks(encode_block_dim)
        for block in img.blocks:
            cryptogram = self.encode_block(block, prob_table)
            f.write(str(cryptogram)+'\n')
        f.close()
    
    def decode(self, coded_filename: str, code_info_filename:str, input_file_name:str):
        code_info = self.read_info_from_json(code_info_filename)
        f = open(coded_filename, "r")
        code_stream = f.readlines()
        f.close()
        blocks = []
        for code in code_stream:
            block = self.decode_block(code_info["block_dim"], code_info["prob_table"], float(code[:-1]))
            blocks.append(block)
        arr = Image.compose_arr_from_blocks(blocks, tuple(code_info["dim"]))
        # plt.imshow(arr, cmap='gray')
        # plt.axis('off')  
        # plt.savefig(f'{coded_filename.split(".")[0]}.png', bbox_inches='tight', pad_inches=0)
        # plt.show(block=False)
        
        original_img = Image.read_from_pgm_file(input_file_name)
        encoded_img = original_img.copy()
        encoded_img.array = arr
        encoded_img.write_to_pgm_file(f'results\\{encoded_img.name}_{code_info["block_dim"][0]}_{code_info["block_dim"][1]}-rec.pgm')
        return self.evaluate_MSE(original_img.array,arr)
    
    def evaluate_MSE(self, original_arr: np.ndarray, generated_arr: np.ndarray):
        mse = 0
        row, col = original_arr.shape
        for i in range(row):
            for j in range(col):
                mse += math.pow(original_arr[i,j]-generated_arr[i,j],2.)
        return math.sqrt(mse/(row*col))
    
    def encode_block(self, block: np.ndarray, prob_table: dict) -> float:
        low, high = 0., 1.
        flattened_symbols = block.flatten()
        for symb in flattened_symbols:
            prev_low, prev_high = low, high
            low = prev_low + (prev_high-prev_low) * prob_table[symb][0]
            high = prev_low + (prev_high-prev_low) * prob_table[symb][1]
        return low 
    
    def decode_block(self, block_dim, prob_table:dict, code: float):
        low, high = 0., 1.
        n_symbols = block_dim[0]*block_dim[1]
        decoded_info = []
        i = 0
        level = 0
        while i < n_symbols:
            for kvp in prob_table.items():
                if code >= kvp[1][0] and code <= kvp[1][1]:
                    level = kvp[0]
                    decoded_info.append(int(level))
                    break
            low = prob_table[level][0]
            high = prob_table[level][1]
            code = (code - low)/(high - low)
            i+=1
        decoded_block = np.zeros(block_dim)
        for i in range(len(decoded_info)):
            decoded_block[i // block_dim[1], i % block_dim[1]] = decoded_info[i]
        return decoded_block
    
    def calculate_probability_table(self, img: Image):
        level_population = {}
        
        for i in range(img.max+1):
            level_population[i] = 0 
        for line in img.array:
            for elmt in line:
                level_population[elmt] += 1
        low = 0
        for i in range(img.max+1):
            level_population[i] /= img.array.size
            high = low+ level_population[i]
            level_population[i] = (low, high)
            low = high
        return level_population
    
    def write_info_to_json(self, prob_table, block_dim, dim, max, filename):
        content = {"prob_table": prob_table, "block_dim": block_dim, "dim": dim, "max": max}
        f = open(filename, 'w')
        json.dump(content, f, indent=4)
        f.close()
        
    def read_info_from_json(self,filename):
        f = open(filename)
        return json.load(f)
    
    def calculate_compression_rate(self, input_filename: str, output_filenames: list[str]):
        input_size = os.path.getsize(input_filename)
        output_size = 0
        for file in output_filenames:
            output_size += os.path.getsize(file)
        return input_size / output_size, input_size, output_size
    
    def show_compression_rate(self, input_filename: str, output_filenames: list[str], encoding_block_dim: tuple[int], mse: float):
        rate, original_size, encoded_size = self.calculate_compression_rate(input_filename, output_filenames)
        filename = input_filename.split("\\")[-1]
        print(f'The encoding for \"{filename}\" using:')
        print(f'-> Original Size (KB): {round(original_size/1024, 3)}')
        print(f'-> Encoding Block Dimension: {encoding_block_dim}')
        print(f'resulted in:')
        print(f'-> Compression Rate: {round(rate,3)}')
        print(f'-> Encoded Files Size (KB): {round(encoded_size/1024, 3)}')
        print(f'-> MSE: {round(mse, 3)}\n')
        