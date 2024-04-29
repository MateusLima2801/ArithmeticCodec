import os
import imageio.v2 as imageio
import numpy as np

class ArithmeticalEncoder:
    
    def read_img(self, filename: str):
        return imageio.imread(filename)      
    
    def encode(self, filename: str, batch_size: int, quantization_levels: int = 256):
        img = self.read_img(filename)
        delta = 256 / quantization_levels
        pixel_stream = img.flatten().reshape((img.size//batch_size,batch_size))
        prob_table = self.calculate_probability_table(img, quantization_levels)
        f = open(f"encoded_files\\{filename}_{batch_size}.txt", "w")
        for batch in pixel_stream:
            cryptogram = self.encode_batch(batch, prob_table, delta)
            f.write(cryptogram)
            
        
    def encode_batch(self, symbols: list[int], prob_table: dict, delta: float) -> float:
        low, high = 0., 1.
        for symb in symbols:
            prev_low, prev_high = low, high
            level = symb // delta
            low = prev_low + (prev_high-prev_low) * prob_table[level][0]
            high = prev_low + (prev_high-prev_low) * prob_table[level][1]
        return low 
    
    def calculate_probability_table(self, img: np.array, quantization_levels: int):
        delta = 256 / quantization_levels
        level_population = {}
        
        for i in range(quantization_levels):
            level_population[i] = 0 
        for line in img:
            for elmt in line:
                level = elmt // delta
                level_population[level] += 1
        low = 0
        for i in range(quantization_levels):
            level_population[i] /= img.size
            high = low+ level_population[i]
            level_population[i] = (low, high)
            low = high
        return level_population
    
    def calculate_compression_rate():
        pass
    
e = ArithmeticalEncoder()
e.encode("imgs\\baboon_ascii.pgm", 2, 256)