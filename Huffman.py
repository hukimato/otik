from bitarray import bitarray

# A Huffman Tree Node
class Node:
    def __init__(self, prob, symbol, left=None, right=None):
        # probability of symbol
        self.prob = prob

        # symbol 
        self.symbol = symbol

        # left node
        self.left = left

        # right node
        self.right = right

        # tree direction (0/1)
        self.code = ''

""" A helper function to print the codes of symbols by traveling Huffman Tree"""
codes = dict()

def Calculate_Codes(node, val=''):
    # huffman code for current node
    newVal = val + str(node.code)

    if(node.left):
        Calculate_Codes(node.left, newVal)
    if(node.right):
        Calculate_Codes(node.right, newVal)

    if(not node.left and not node.right):
        codes[node.symbol] = bitarray(newVal)
         
    return codes        

""" A helper function to calculate the probabilities of symbols in given data"""
def Calculate_Probability(data):
    symbols = dict()
    for element in data:
        if symbols.get(element) == None:
            symbols[element] = 1
        else: 
            symbols[element] += 1     
    return symbols

""" A helper function to obtain the encoded output"""
def Output_Encoded(data, coding):
    return bitarray(''.join(list(map(lambda x: coding[x].to01(), data))))
        
""" A helper function to calculate the space difference between compressed and non compressed data"""    
def Total_Gain(data, coding):
    before_compression = len(data) * 8 # total bit space to stor the data before compression
    after_compression = 0
    symbols = coding.keys()
    for symbol in symbols:
        count = data.count(symbol)
        after_compression += count * len(coding[symbol]) #calculate how many bit is required for that symbol in total
    print("Space usage before compression (in bits):", before_compression)    
    print("Space usage after compression (in bits):",  after_compression)  

def prepare_dict(codes_dict):
    dict_bitarray = bitarray()
    for byte, code in codes_dict.items():
        dict_bitarray.frombytes(len(code).to_bytes(1, 'big'))
        dict_bitarray.extend(code)
        dict_bitarray.frombytes(byte.to_bytes(1, 'big'))
    
    return dict_bitarray

 
def Huffman_Encoding(data):
    symbol_with_probs = Calculate_Probability(data)
    symbols = symbol_with_probs.keys()
    
    nodes = []
    
    # converting symbols and probabilities into huffman tree nodes
    for symbol in symbols:
        nodes.append(Node(symbol_with_probs.get(symbol), symbol))
    
    while len(nodes) > 1:
        # sort all the nodes in ascending order based on their probability
        nodes = sorted(nodes, key=lambda x: x.prob)
    
        # pick 2 smallest nodes
        right = nodes[0]
        left = nodes[1]
    
        left.code = 0
        right.code = 1
    
        # combine the 2 smallest nodes to create new node
        newNode = Node(left.prob+right.prob, left.symbol+right.symbol, left, right)
    
        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)
            
    huffman_encoding = Calculate_Codes(nodes[0])
    encoded_output = Output_Encoded(data,huffman_encoding)
    dict_bitarray = prepare_dict(huffman_encoding)

    codes.clear()
    return encoded_output, dict_bitarray

def find_dict_key_by_val(dict, search_val):
    for key, val in dict.items():
        if val == search_val:
            return key

def decode_dict(dict_bitarray: bitarray):
    i = 0

    codes_dict = dict()
    while i < len(dict_bitarray):
        size = int(dict_bitarray[i:i+8].to01(), 2)
        code = dict_bitarray[i+8:i+8+size]
        byte = int(dict_bitarray[i+8+size:i+8+size+8].to01(), 2)
        codes_dict[byte] = code
        i = i+8+size+8
    
    return codes_dict

def Huffman_Decoding(data: bitarray, huffman_dict_bitarray):
    huffman_dict = decode_dict(huffman_dict_bitarray)
    decoded = bitarray()

    current_code = bitarray('')
    for bit in data.to01():
        current_code.extend(bit)

        if (current_code in huffman_dict.values()):
            decoded.frombytes(find_dict_key_by_val(huffman_dict, current_code).to_bytes(1, 'big'))
            current_code = bitarray()
    
    return decoded.tobytes()      
