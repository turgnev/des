from bitstring import BitArray

class DES(object):
    INITIAL_PERMUTE = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17, 9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]

    FINAL_PERMUTE = [40, 8, 48, 16, 56, 24, 64, 32,
            39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30,
            37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28,
            35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26,
            33, 1, 41, 9, 49, 17, 57, 25]

    EXPAND_FEISTEL = [32, 1, 2, 3, 4, 5,
         4, 5, 6, 7, 8, 9,
         8, 9, 10, 11, 12, 13,
         12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21,
         20, 21, 22, 23, 24, 25,
         24, 25, 26, 27, 28, 29,
         28, 29, 30, 31, 32, 1]

    S_BOX = [
        [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
         ],

        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
         ],

        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
         ],

        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
         ],

        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
         ],

        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
         ],

        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
         ],

        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
         ]
    ]


    FEISTEL_PERMUTE = [16, 7, 20, 21, 29, 12, 28, 17,
         1, 15, 23, 26, 5, 18, 31, 10,
         2, 8, 24, 14, 32, 27, 3, 9,
         19, 13, 30, 6, 22, 11, 4, 25]

    CD_1 = [57, 49, 41, 33, 25, 17, 9,
            1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27,
            19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29,
            21, 13, 5, 28, 20, 12, 4]

    # 16 сдвигов - 16 ключей по 56 бит
    SHIFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    # Преобразование всех 16 ключей, состоящих из
    # 56 бит в 16 ключей по 48
    CD_2 = [14, 17, 11, 24, 1, 5, 3, 28,
            15, 6, 21, 10, 23, 19, 12, 4,
            26, 8, 16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55, 30, 40,
            51, 45, 33, 48, 44, 49, 39, 56,
            34, 53, 46, 42, 50, 36, 29, 32]

    @staticmethod
    def add_bit(bit_arr, bit):
        bit_arr.append(1)
        bit_arr[bit_arr.len-1] = bit


        # Дополнение исходного текста до размера, кратного 64-м битам
    def add_padding(self, text):
        temp = BitArray(text)
        temp.append(1)
        temp[temp.len - 1] = 1

        pad_len = 64 - (temp.len % 64)
        if pad_len != 0:
            temp.append(pad_len)
        return temp


    def remove_padding(self, text):
        last1 = 0
        for i in range(text.len):
            if text[i] == 1:
                last1 = i
        return text[:last1]


        # Осуществляет перестановки в блоке block по таблице table
    def permute(self, block, table):
        temp = BitArray()
        for i in range(len(table)):
            if block[table[i] - 1] == 1:
                DES.add_bit(temp, 1)
            else:
                DES.add_bit(temp, 0)
        return temp


        # Расширяет block по table
    def expand(self, block, table):
        temp = BitArray()
        for i in range(len(table)):
            if block[table[i] - 1] == 1:
                DES.add_bit(temp, 1)
            else:
                DES.add_bit(temp, 0)

        return temp

    def left_shift(self, block, n):
        return block[n:] + block[:n];

        # 48-битов в 32
    def substitution(self, block):
        res = BitArray()
        for i in range(8):

            cur = block[i*6:(i+1)*6]

            a = BitArray()
            a.append(cur[::5])

            b = BitArray()
            b.append(cur[1:5])

            sres = BitArray(uint=DES.S_BOX[i][a.uint][b.uint], length=4)
            #print(cur.bin, "a= ", a.uint, " b=", b.uint)
            res.append(sres)
        return res


    def key_parity_bit(self, key):
        res = BitArray()
        for i in range(8):
            cur = key[i * 7:(i + 1) * 7]
            sum = 0
            for b in cur:
                sum += b
            if sum % 2 == 0:
                DES.add_bit(cur, 1)
            else:
                DES.add_bit(cur, 0)
            res.append(cur)
        return res

    def generate_keys(self, key):
        keys = []
        key = self.permute(key, self.CD_1)
        for i in self.SHIFT:
            key = self.left_shift(key, i)
            cur_key = self.expand(key, self.CD_2)
            keys.append(cur_key)
        return keys


    def feistel(self, Ri, ki):
        temp48 = self.expand(Ri, self.EXPAND_FEISTEL)
        temp48 = temp48^ki
        temp32 = self.substitution(temp48)
        temp32 = self.permute(temp32, self.FEISTEL_PERMUTE)
        return temp32


    def cipher_block(self, block64, key):
        block64 = self.permute(block64, self.INITIAL_PERMUTE)
        keys = self.generate_keys(key)

        left = block64[:32]
        right = block64[32:]

        for i in range(16):
            temp = right
            right = left^self.feistel(right, keys[i])
            left = temp

        res = left + right
        res = self.permute(res, self.FINAL_PERMUTE)
        return res


    def decipher_block(self, block64, key):
        block64 = self.permute(block64, self.INITIAL_PERMUTE)
        keys = self.generate_keys(key)

        left = block64[:32]
        right = block64[32:]

        for i in range(16):
            temp = left#При расшировке Левый заменяется на правый и наооборот
            left = right^self.feistel(left, keys[15-i])# И ключи идут в обратном порядке
            right = temp

        res = left + right
        res = self.permute(res, self.FINAL_PERMUTE)
        return res

    def getiblock(self, text, i):
        return text[i*64:(i+1)*64]

    def cipher_text(self, text, key):
        temp = self.add_padding(text)
        res = BitArray()

        print("ciphering")
        nblocks = temp.len // 64
        for i in range(nblocks):
            if i%100 == 0:
                print(i+1," out of ", nblocks)
            cur = self.cipher_block(self.getiblock(temp, i), key)
            res.append(cur)

        return res


    def decipher_text(self, text, key):
        res = BitArray()

        print("deciphering")
        nblocks = text.len // 64
        for i in range(nblocks):
            print(i+1," out of ", nblocks)
            cur = self.decipher_block(self.getiblock(text, i), key)
            res.append(cur)

        res = self.remove_padding(res)
        return res