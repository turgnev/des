from unittest import TestCase
from bitstring import BitArray
from des import DES


class TestDES(TestCase):
    def test_add_padding(self):
        des = DES()
        text = BitArray(b'223')
        expected = BitArray(bin='0011001000110010001100111000000000000000000000000000000000000000')

        des.add_padding(text)

        self.assertEqual(text, expected)

    def test_add_padding64(self):
        des = DES()
        text = BitArray(b'22334432')
        expected = BitArray(
            bin='00110010001100100011001100110011001101000011010000110011001100101000000000000000000000000000000000000000000000000000000000000000')

        des.add_padding(text)

        self.assertEqual(text, expected)

    def test_remove_padding(self):
        des = DES()
        expected = BitArray(b'22334432')
        text = BitArray(
            bin='00110010001100100011001100110011001101000011010000110011001100101000000000000000000000000000000000000000000000000000000000000000')

        text = des.remove_padding(text)

        self.assertEqual(text, expected)

    def test_add_bit(self):
        text = BitArray(bin='001100100011001')
        expected = BitArray(bin='00110010001100110')

        DES.add_bit(text, 1)
        DES.add_bit(text, 0)

        self.assertEqual(text, expected)

    def test_permute(self):
        des = DES()
        text = BitArray(bin='0101011011101001100111101010110011011110010111111111010010110001')
        expected = BitArray(bin='0111001111110101011111011010001011011110110010100011111000110101')

        res = des.permute(text, des.IP)

        self.assertEqual(res, expected)

    def test_expand(self):
        des = DES()
        text = BitArray(bin='11011110110010100011111000110101')
        expected = BitArray(bin='111011111101011001010100000111111100000110101011')

        res = des.expand(text, des.E)

        self.assertEqual(res, expected)

    def test_substitution(self):
        des = DES()
        test = BitArray(bin='100111011011011100111001011110011101111011110111')
        expected = BitArray(bin='010000100110001101100011010001100001111101011100')
        res = des.substitution(test)

        self.assertEqual(res, expected)


    def test_generate_keys(self):
        key = BitArray(bin='1101111100010000100111010101100011101001101001001010011100110001')
        expected = BitArray(bin='010000100110001101100011010001100001111101011100')
        print(expected.len)
        des = DES()

        keys = des.generate_keys(key)
        print(len(keys))
        print(keys)
        print(keys[0].len)
        self.assertEqual(keys[0], expected)