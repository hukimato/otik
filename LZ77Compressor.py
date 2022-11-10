import math
from bitarray import bitarray


class LZ77Compressor:
    """
    A simplified implementation of the LZ77 Compression Algorithm
    """
    MAX_WINDOW_SIZE = 400

    def __init__(self, window_size=400):
        self.window_size = min(window_size, self.MAX_WINDOW_SIZE)
        self.lookahead_buffer_size = 15  # length of match is at most 4 bits

    def compress(self, data):
        i = 0
        output_buffer = bitarray(endian='big')
        # print(data)


        while i < len(data):
            # print(i)

            match = self.findLongestMatch(data, i)

            if match:
                # Add 1 bit flag, followed by 12 bit for distance, and 4 bit for the length
                # of the match
                (bestMatchDistance, bestMatchLength) = match

                output_buffer.append(True)
                output_buffer.frombytes(bytes([bestMatchDistance >> 4]))
                output_buffer.frombytes(bytes([((bestMatchDistance & 0xf) << 4) | bestMatchLength]))

                i += bestMatchLength

            else:
                # No useful match was found. Add 0 bit flag, followed by 8 bit for the character
                output_buffer.append(False)
                output_buffer.frombytes(bytes([data[i]]))

                i += 1

        # fill the buffer with zeros if the number of bits is not a multiple of 8
        output_buffer.fill()

        return output_buffer

    def decompress(self, data):
        """
        Given a string of the compressed file path, the data is decompressed back to its
        original form, and written into the output file path if provided. If no output
        file path is provided, the decompressed data is returned as a string
        """
        output_buffer = []

        while len(data) >= 9:

            flag = data.pop(0)

            if not flag:
                byte = data[0:8].tobytes()

                output_buffer.append(byte)
                del data[0:8]
            else:
                byte1 = ord(data[0:8].tobytes())
                byte2 = ord(data[8:16].tobytes())

                del data[0:16]
                distance = (byte1 << 4) | (byte2 >> 4)
                length = (byte2 & 0xf)

                for i in range(length):
                    output_buffer.append(output_buffer[-distance])
        out_data = b''.join(output_buffer)

        return out_data

    def findLongestMatch(self, data, current_position):
        """
        Finds the longest match to a substring starting at the current_position
        in the lookahead buffer from the history window
        """
        # Индекс последнего символа подстроки, которую пытаемся заменить
        end_of_buffer = min(current_position + self.lookahead_buffer_size, len(data) + 1)

        best_match_distance = -1
        best_match_length = -1

        # Начиная с длины подстроки 2 до максимальной длины подстроки
        for j in range(current_position + 2, end_of_buffer):

            # Индекс начала окна, где ищем совпадающую подстроку
            start_index = max(0, current_position - self.window_size)
            substring = data[current_position:j]

            # Начиная с левого конца окна, где ищем совпадающую подстроку
            for i in range(start_index, current_position):

                # Сколько раз подстрока текущей длины уместится в оставшуюся часть окна
                repetitions = len(substring) // (current_position - i)

                # Сколько символов останется
                last = len(substring) % (current_position - i)

                matched_string = data[i:current_position] * repetitions + data[i:i + last]

                if matched_string == substring and len(substring) > best_match_length:
                    best_match_distance = current_position - i
                    best_match_length = len(substring)

        if best_match_distance > 0 and best_match_length > 0:
            return (best_match_distance, best_match_length)
        return None



