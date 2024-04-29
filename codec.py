import json
import os
import imageio.v2 as imageio
import numpy as np

from image import Image

class ArithmeticCodec:
    
    def encode(self, filename: str, encode_block_dim: tuple = (8,8), quantization_levels: int = 256):
        img = Image.read_from_file(filename)
        nickname = f"{img.name}_{encode_block_dim[0]}_{encode_block_dim[1]}_{quantization_levels}"
        delta = 256 / quantization_levels
        prob_table = self.calculate_probability_table(img, quantization_levels)
        self.write_info_to_json(prob_table, quantization_levels, encode_block_dim, f"encoded_files\\{nickname}.json")
        encrypted_code_file = f"encoded_files\\{nickname}.txt"
        f = open(encrypted_code_file, "w")
        img.divide_array_in_blocks(encode_block_dim)
        for block in img.blocks:
            cryptogram = self.encode_block(block, prob_table, delta)
            f.write(str(cryptogram)+'\n')
        f.close()
        
    def encode_block(self, block: np.ndarray, prob_table: dict, delta: float) -> float:
        low, high = 0., 1.
        flattened_symbols = block.flatten()
        for symb in flattened_symbols:
            prev_low, prev_high = low, high
            level = symb // delta
            low = prev_low + (prev_high-prev_low) * prob_table[level][0]
            high = prev_low + (prev_high-prev_low) * prob_table[level][1]
        return low 
    
    def calculate_probability_table(self, img: Image, quantization_levels: int):
        delta = 256 / quantization_levels
        level_population = {}
        
        for i in range(quantization_levels):
            level_population[i] = 0 
        for line in img.array:
            for elmt in line:
                level = elmt // delta
                level_population[level] += 1
        low = 0
        for i in range(quantization_levels):
            level_population[i] /= img.array.size
            high = low+ level_population[i]
            level_population[i] = (low, high)
            low = high
        return level_population
    
    def calculate_compression_rate():
        pass
    
    def write_info_to_json(self, prob_table, quantization_levels, block_dim, filename):
        content = {"prob_table": prob_table, "quantization_levels": quantization_levels, "block_dim": block_dim}
        f = open(filename, 'w')
        json.dump(content, f, indent=4)
        f.close()
        
    def read_info_from_json(self,filename):
        f = open(filename)
        return json.load(f)
    
    def decode(self, coded_filename, code_info_filename):
        code_info = self.read_info_from_json(code_info_filename)
        
    
e = ArithmeticCodec()
e.encode("imgs\\lena_ascii.pgm")