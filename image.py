from __future__ import annotations
import math
import numpy as np

class Image:
    dim: tuple[int]
    max: int
    array: np.ndarray[int]
    name: str
    blocks: np.ndarray
    
    def __init__(self, dim, max, array, name):
        self.dim = dim
        self.max = max
        self.array = array
        self.name = name
        
    @staticmethod
    def read_from_pgm_file(filename:str) -> Image:
        f = open(filename, "r")
        lines = f.readlines()
        f.close()
        name = filename.split('\\')[-1].split('.')[0]
        info_dim = lines[2][:-1].split()
        max = int(lines[3][:-1])
        dim = (int(info_dim[0]), int(info_dim[1]))
        array = np.zeros(dim)
        i = 0
        for line in lines[4:]:
            info = line[:-1].split()
            for elmt in info:
                row = math.floor(i/dim[0])
                array[row, i-row*dim[0]] = int(elmt)
                i+=1
        return Image(dim, max, array, name)
    
    def write_to_pgm_file(self, filename: str):
        f = open(filename, "w")
        f.write("P2\n")
        f.write(f"# CREATED FROM {self.name} BY MATEUS LIMA\n")
        f.write(f"{self.dim[0]} {self.dim[1]}\n")
        f.write(f"{self.max}\n")
        flat = self.array.flatten()
        i = 0
        line = ""
        for elmt in flat:
            if i == 16:
                line+="\n"
                f.write(line)
                line = ""
                i = -1
            line += f'{int(elmt)} '
            i+=1
        f.close()
        
    def divide_array_in_blocks(self, dim_block: tuple):
        blocks = []
        for i in range(0, self.dim[0], dim_block[0]):
            for j in range(0, self.dim[1], dim_block[1]):
                block = self.array[i:i+dim_block[0], j:j+dim_block[1]]
                blocks.append(block)
        self.blocks = blocks
        
    @staticmethod
    def compose_arr_from_blocks(blocks: np.ndarray, dim: tuple):
        array = np.zeros(dim)
        dim_block = blocks[0].shape
        n_blocks_row = dim[0] // dim_block[0]
        for b, block in enumerate(blocks):
            row = b // n_blocks_row
            col = b % n_blocks_row
            for i in range(len(block)):
                for j in range(len(block[0])):
                    array[row*dim_block[0]+i,col*dim_block[1]+j] = block[i,j]
        return array
    
    def copy(self) -> Image:
        return Image(self.dim, self.max, self.array.copy(), self.name)
        
        
        

