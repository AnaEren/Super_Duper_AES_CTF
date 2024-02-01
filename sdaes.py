import sys
from binascii import hexlify

def substitute(hexBlock): #substituição invertida
    substitutedHexBlock = ""
    substitution =  [15, 9, 7, 4, 1, 11, 6, 10,
                     0, 3, 13, 14, 12, 8, 5, 2]
    for hexDigit in hexBlock:
        newDigit = substitution[int(hexDigit, 16)]
        substitutedHexBlock += hex(newDigit)[2:]
    return substitutedHexBlock

def pad(message): # blocos multiplos de 4
    numBytes = 4-(len(message)%4) 
    return message + numBytes * chr(numBytes)

def hexpad(hexBlock):
    numZeros = 8 - len(hexBlock)
    return numZeros*"0" + hexBlock

def permute(hexBlock): #função inversa - inverte do mesmo jeito que a substituição
    permutation =   [22, 9, 15, 26, 5, 25, 0, 24,
                     31, 29, 20, 11, 17, 28, 13, 8,
                     21, 30, 3, 7, 27, 18, 1, 6,
                     23, 14, 19, 16, 12, 4, 2, 10]
    block = int(hexBlock, 16)
    permutedBlock = 0
    for i in range(32):
        bit = (block & (1 << i)) >> i
        permutedBlock |= bit << permutation[i]
    return hexpad(hex(permutedBlock)[2:])

def round(hexMessage):
    numBlocks = len(hexMessage)//8
    substitutedHexMessage = ""
    for i in range(numBlocks):
        substitutedHexMessage += substitute(hexMessage[8*i:8*i+8])
    permutedHexMessage = ""
    for i in range(numBlocks):
        permutedHexMessage += permute(substitutedHexMessage[8*i:8*i+8])
    return permutedHexMessage

def deround(hexMessage):
    numBlocks = len(hexMessage)//8
    permutedHexMessage = ""
    for i in range(numBlocks):
        permutedHexMessage += permute(hexMessage[8*i:8*i+8])
    substitutedHexMessage = ""
    for i in range(numBlocks):
        substitutedHexMessage += substitute(permutedHexMessage[8*i:8*i+8])
    return substitutedHexMessage


if __name__ == "__main__":
    cypher = 'd59fd3f37182486a44231de4713131d20324fbfe80e91ae48658ba707cb84841972305fc3e0111c753733cf2'

    for i in range(10000):
        cypher = deround(cypher)

    hexMessage = bytes.fromhex(cypher)
    print(hexMessage.decode('utf-8'))

#Flag: nactf{5ub5t1tut10n_p3rmutat10n_n33d5_a_k3y}