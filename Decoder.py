from bitarray import bitarray

from Huffman import Huffman_Decoding

class Decoder:
    signature = bytearray('Ъь', 'utf-8')
    version = 0
    algo_compression_with_context = None
    algo_compression_without_context = None
    algo_loss_protection = None
    encryption = None

    def get_meta_data(self, file_meta_data):
        self.signature = file_meta_data[0:4]
        self.version = file_meta_data[4:6]
        self.algo_compression_without_context = file_meta_data[8]
        self.algo_compression_with_context = file_meta_data[9]
        self.algo_loss_protection = file_meta_data[10]
        self.encryption = file_meta_data[11]

    def decode(self, file_name):
        file = open(file_name, 'rb')
        file_bytes = file.read()
        file.close()
        archived_files_data = file_bytes[12::]

        self.get_meta_data(file_bytes[0:12])

        if self.signature != bytearray('Ъь', 'utf-8'):
            exit('Сигнатура не совпадает')

        while archived_files_data:
            file_data_size = int.from_bytes(archived_files_data[0:8], 'big')
            file_code_info_size = int.from_bytes(archived_files_data[8:16],'big')
            file_data_bits_offset = int.from_bytes(archived_files_data[16:17], 'big')
            file_code_bits_offset = int.from_bytes(archived_files_data[17:18], 'big')
            file_name_size = int.from_bytes(archived_files_data[18:20], 'big')

            file_data_info_size = file_data_size + file_code_info_size + file_name_size

            file_bytes = archived_files_data[20 : 20 + file_data_info_size]
            idx = file_bytes.find(bytes('|', 'utf-8'))
            file_name = file_bytes[:idx]

            data_start_idx = idx + 1
            data_end_idx = idx + 1 + file_data_size
            file_data = file_bytes[data_start_idx:data_end_idx]
            file_code = file_bytes[data_end_idx:data_end_idx + file_code_info_size]
            file_name = file_name.decode('utf-8')

            file_output_data = file_data if self.algo_compression_without_context == 0 else self.decompression(file_data, file_data_bits_offset, file_code, file_code_bits_offset)
            my_file = open(f'output/{file_name}', 'wb')
            my_file.write(file_output_data)
            # print(result_byte_code)
            my_file.close()

            archived_files_data = archived_files_data[20 + file_data_info_size:]
    
    def decompression(self, data: bytearray, data_bits_offset: int, codes: bytearray, codes_bits_offset: int):
        data_offseted = bitarray()
        data_offseted.frombytes(data)
        data_offseted = data_offseted[data_bits_offset:]

        codes_offseted = bitarray()
        codes_offseted.frombytes(codes)
        codes_offseted = codes_offseted[codes_bits_offset:]

        return Huffman_Decoding(data_offseted, codes_offseted)





