from bitstring import BitArray
from des import DES

des = DES()
key = BitArray('0x1234567890123456')


filename = input('filename: ')
with open("./files/" + filename, 'rb') as file:
    input_bytes = file.read()

inputbits = BitArray(input_bytes)
outputbits = des.cipher_text(inputbits, key)
res = BitArray.tobytes(outputbits)

with open("./files/ciph_" + filename, 'wb') as file:
    file.write(res)






with open("./files/ciph_" + filename, 'rb') as file:
    input_bytes = file.read()

inputbits = BitArray(input_bytes)
outputbits = des.decipher_text(inputbits, key)
res = BitArray.tobytes(outputbits)

with open("./files/deciph_" + filename, 'wb') as file:
    file.write(res)