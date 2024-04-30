
from codec import ArithmeticCodec


def main():
    imgs = ['quadrado_ascii','baboon_ascii', 'lena_ascii']
    e = ArithmeticCodec()
    encoding_block_dims = [(2,2),(4,4), (8,8),(16, 16)]
    for encoding_block_dim in encoding_block_dims:
        for file in imgs:
            e.encode(f"imgs\\{file}.pgm", encoding_block_dim)
            output_file = f"{file}_{encoding_block_dim[0]}_{encoding_block_dim[1]}"
            mse = e.decode(f"results\\{output_file}.txt",
                 f"results\\{output_file}.json", f"imgs\\{file}.pgm")
            e.show_compression_rate(f"imgs\\{file}.pgm",
                                    [f"results\\{output_file}.txt",
                                     f"results\\{output_file}.json"], encoding_block_dim, mse)

if __name__ == "__main__":
    main()