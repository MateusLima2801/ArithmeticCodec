from __future__ import annotations
import math
import numpy as np

class Image:
    dim: tuple[int]
    max: int
    array: np.ndarray[int]
    separator = '  '
    name: str
    blocks: np.ndarray
    
    def __init__(self, dim, max, array, name):
        self.dim = dim
        self.max = max
        self.array = array
        self.name = name
        
    @staticmethod
    def read_from_file(filename:str) -> Image:
        f = open(filename, "r")
        lines = f.readlines()
        f.close()
        name = filename.split('\\')[-1].split('.')[0]
        info_dim = lines[2][:-1].split(Image.separator)
        max = int(lines[3][:-1])
        dim = (int(info_dim[0]), int(info_dim[1]))
        array = np.zeros(dim)
        i = 0
        for line in lines[4:]:
            info = line[:-1].split(Image.separator)
            for elmt in info:
                row = math.floor(i/dim[0])
                array[row, i-row*dim[0]] = int(elmt)
                i+=1
        return Image(dim, max, array, name)
    
    def divide_array_in_blocks(self, dim_block: tuple):
        blocks = []
        for i in range(0, self.dim[0], dim_block[0]):
            for j in range(0, self.dim[1], dim_block[1]):
                block = self.array[i:i+dim_block[0], j:j+dim_block[1]]
                blocks.append(block)
        self.blocks = blocks
        
        

