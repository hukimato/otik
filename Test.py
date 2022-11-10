from LZ77Compressor import LZ77Compressor

comp = LZ77Compressor()

with open('test1.txt', 'rb') as file:
    data = file.read()
    print(data)
    compressed = comp.compress(data)
    print(compressed)
    decompressed = comp.decompress(compressed)

    print(decompressed)
