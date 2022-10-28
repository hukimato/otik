from itertools import groupby

def rle_encode(file_data):

    list_of_byte_count = [(k, sum(1 for _ in g)) for k,g in groupby(file_data)]

    list_of_byte_count_new = []
    index = 0
    while index < len(list_of_byte_count):
        if list_of_byte_count[index][1] > 127:
            for i in range(list_of_byte_count[index][1] // 127):
                list_of_byte_count_new.append([list_of_byte_count[index][0], 127])
            list_of_byte_count_new.append([list_of_byte_count[index][0], list_of_byte_count[index][1] % 127])
        else:
            list_of_byte_count_new.append(list_of_byte_count[index])
        index += 1

    result_bytearray = bytearray()
    buffer_bytearray = bytearray()
    for pair in list_of_byte_count:
        if pair[1] >= 3:
            if len(buffer_bytearray) > 127:
                buffers = [buffer_bytearray[x:x+127] for x in range(0, len(buffer_bytearray),127)]
                for buffer in buffers:
                    result_bytearray.extend((len(buffer)).to_bytes(1, 'big'))
                    result_bytearray.extend(buffer)
            elif len(buffer_bytearray) != 0:
                result_bytearray.extend((len(buffer_bytearray)).to_bytes(1, 'big'))
                result_bytearray.extend(buffer_bytearray)
            buffer_bytearray = bytearray()

            result_bytearray.extend((128 + pair[1]).to_bytes(1, 'big'))
            result_bytearray.extend((pair[0]).to_bytes(1, 'big'))
        else:
            for i in range(pair[1]):
                buffer_bytearray.extend((pair[0]).to_bytes(1, 'big'))

    if len(buffer_bytearray) != 0:
        if len(buffer_bytearray) > 127:
            buffers = [buffer_bytearray[x:x + 127] for x in range(0, len(buffer_bytearray), 127)]
            for buffer in buffers:
                result_bytearray.extend((len(buffer)).to_bytes(1, 'big'))
                result_bytearray.extend(buffer)
        else:
            result_bytearray.extend((len(buffer_bytearray)).to_bytes(1, 'big'))
            result_bytearray.extend(buffer_bytearray)

    return result_bytearray


def rle_decode(data):
    result = bytearray()
    counter = 0
    index = 0

    while index < len(data)-1:
        if data[index] > 128:
            for i in range(data[index] - 128):
                result.extend((data[index+1]).to_bytes(1, 'big'))
            index += 1
        else:
            idx = index
            for i in range(data[idx]):
                index += 1
                if index >= len(data):
                    break
                result.extend((data[index]).to_bytes(1, 'big'))
        index += 1
    return result


