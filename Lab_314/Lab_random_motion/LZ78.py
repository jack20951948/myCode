class node:
    def __init__(self, val=7):
        self.action = None
        self.val = val
        self.zero = 1
        self.two = 1
        self.three = 1
        self.four = 1
        self.five = 1
        self.six = 1

    def insert_Zero(self):
        if self.zero == 1:
            self.zero = node()
            self.val += self.zero.val - 1
        
    def insert_One(self, action):
        if self.one == 1:
            self.one = node()
            self.val += self.one.val



def compress(message):
    tree_dict, m_len, i = {}, len(message), 0
    while i < m_len:
        # case I
        if message[i] not in tree_dict.keys():
            yield (0, message[i])
            tree_dict[message[i]] = len(tree_dict) + 1
            i += 1
        # case III
        elif i == m_len - 1:
            yield (tree_dict.get(message[i]), '')
            i += 1
        else:
            for j in range(i + 1, m_len):
                # case II
                if message[i:j + 1] not in tree_dict.keys():
                    yield (tree_dict.get(message[i:j]), message[j])
                    tree_dict[message[i:j + 1]] = len(tree_dict) + 1
                    i = j + 1
                    break
                # case III
                elif j == m_len - 1:
                    yield (tree_dict.get(message[i:j + 1]), '')
                    i = j + 1

    print("message:", message, "\ntree dict:", tree_dict)

def uncompress(packed):
    unpacked, tree_dict = '', {}
    for index, ch in packed:
        if index == 0:
            unpacked += ch
            tree_dict[len(tree_dict) + 1] = ch
        else:
            term = tree_dict.get(index) + ch
            unpacked += term
            tree_dict[len(tree_dict) + 1] = term
    return unpacked

def main():
    messages = ['ABBCBCABABCAABCAAB', 'BABAABRRRA', 'AAAAAAAAA']
    for m in messages:
        pack = compress(m)
        unpack = uncompress(pack)

if __name__ == '__main__':
    main()


# def compress(uncompressed):
#     """Compress a string to a list of output symbols."""

#     # Build the dictionary.
#     dict_size = 256
#     dictionary = dict((chr(i), chr(i)) for i in range(dict_size))

#     w = ""
#     result = []
#     for c in uncompressed:
#         wc = w + c
#         if wc in dictionary:
#             w = wc
#         else:
#             result.append(dictionary[w])
#             # Add wc to the dictionary.
#             dictionary[wc] = dict_size
#             dict_size += 1
#             w = c

#     # Output the code for w.
#     if w:
#         result.append(dictionary[w])
#     return result


# def decompress(compressed):
#     """Decompress a list of output ks to a string."""
#     from io import StringIO

#     # Build the dictionary.
#     dict_size = 256
#     dictionary = dict((chr(i), chr(i)) for i in range(dict_size))

#     # use StringIO, otherwise this becomes O(N^2)
#     # due to string concatenation in a loop
#     result = StringIO()
#     w = compressed.pop(0)
#     result.write(w)
#     for k in compressed:
#         if k in dictionary:
#             entry = dictionary[k]
#         elif k == dict_size:
#             entry = w + w[0]
#         else:
#             raise ValueError('Bad compressed k: %s' % k)
#         result.write(entry)

#         # Add w+entry[0] to the dictionary.
#         dictionary[dict_size] = w + entry[0]
#         dict_size += 1

#         w = entry
#     return result.getvalue()

# def main():
#     from io import StringIO
#     # How to use:
#     compressed = compress('TOBEORNOTTOBEORTOBEORNOT')
#     print (compressed)
#     decompressed = decompress(compressed)
#     print (decompressed)

#     print(dict((i, i) for i in range(256)))

# if __name__ == "__main__":
#     main()