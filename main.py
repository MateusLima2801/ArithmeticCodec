
from codec import ArithmeticCodec


def main():
    e = ArithmeticCodec()
    e.encode("imgs\\baboon_ascii.pgm")
    e.decode("encoded_files\\baboon_ascii_8_8_256.txt","encoded_files\\baboon_ascii_8_8_256.json")

if __name__ == "__main__":
    main()