# **Super Duper AES (250pts)**
Passo a passo de como o desafio foi solucionado
Link para o desafio [aqui](https://ctftime.org/task/9330).
## O desafio

#### Question
>The Advanced Encryption Standard (AES) has got to go. Spencer just invented the Super Duper Advanced Encryption Standard (SDAES), and it's 100% unbreakable. AES only performs up to 14 rounds of substitution and permutation, while SDAES performs 10,000. That's so secure, SDAES doesn't even use a key!
#### Hint
>Spencer used this video as inspiration for Super Duper AES: [Link](https://www.youtube.com/watch?v=DLjzI5dX8jc)

## Análise do código original
#### A utilidade da Dica
No vídeo da dica é explicado sobre como funcionaria esse sistema de criptografia, porém no vídeo fica clara a importância de uma chave, enquanto o código do CTF não possui uma.
Também no vídeo, o autor explica que, sem a chave, basta apenas fazer os passos reversos da criptografia para obter a resposta.

#### Cada passo da criptografia
```
def round(hexMessage):
    numBlocks = len(hexMessage)//8
    substitutedHexMessage = ""
    for i in range(numBlocks):
        substitutedHexMessage += substitute(hexMessage[8*i:8*i+8])
    permutedHexMessage = ""
    for i in range(numBlocks):
        permutedHexMessage += permute(substitutedHexMessage[8*i:8*i+8])
    return permutedHexMessage
```
Uma mensagem em hexadecimal é enviada para essa função, onde primeiro tem seus digitos substituídos e depois permutados (pela main, isso é feito 10.000x)

A substituição é feita pela função:
```
def substitute(hexBlock):
    substitutedHexBlock = ""
    substitution =  [8, 4, 15, 9, 3, 14, 6, 2, 
                    13, 1, 7, 5, 12, 10, 11, 0]
    for hexDigit in hexBlock:
        newDigit = substitution[int(hexDigit, 16)]
        substitutedHexBlock += hex(newDigit)[2:]
    return substitutedHexBlock
```
Essa função basicamente substitui cada valor hexadecimal x do bloco pelo valor que está na posição x do vetor "substitutedHexBlock". Ex: 0 será trocado por 8, D será trocado por A.

Já a permutação é feita pela função:
```
def permute(hexBlock):
    permutation =   [6, 22, 30, 18, 29, 4, 23, 19,
                    15, 1, 31, 11, 28, 14, 25, 2,
                    27, 12, 21, 26, 10, 16, 0, 24,
                     7, 5, 3, 20, 13, 9, 17, 8]
    block = int(hexBlock, 16)
    permutedBlock = 0
    for i in range(32):
        bit = (block & (1 << i)) >> i # verifica se cada bit está ativo
        permutedBlock |= bit << permutation[i] # move o bit ativo para a posição indicada em "permutation"
    return hexpad(hex(permutedBlock)[2:])
```
Ela transforma um bloco hexa em binário e verifica, bit a bit, se este está ativo e o troca de lugar de acordo com o vetor permutation.

## Fazendo tudo ao contrário
Para a solução, basta inverter a ordem da função round, para primeiro permutar e depois fazer a substituição:
```
def deround(hexMessage):
    numBlocks = len(hexMessage)//8
    permutedHexMessage = ""
    for i in range(numBlocks):
        permutedHexMessage += permute(hexMessage[8*i:8*i+8])
    substitutedHexMessage = ""
    for i in range(numBlocks):
        substitutedHexMessage += substitute(permutedHexMessage[8*i:8*i+8])
    return substitutedHexMessage
```
Para a função, basta reestruturar os vetores, usando uma lógica reversa, que decodifique esse array de maneira que, por exemplo: se 6 está na posição 0, então no array decodificado a posição 6 terá valor 0.

Substituição:


|Posição| 0| 1|  2| 3| 4|  5| 6| 7|  8| 9|10|11| 12| 13| 14|15|
|--|--|--|---|--|--|---|--|--|---|--|--|--|---|---|---|--|
|Valor Antigo| 8| 4| 15| 9| 3| 14| 6| 2| 13| 1| 7| 5| 12| 10| 11| 0|

|Posição| 0| 1|  2| 3| 4|  5| 6| 7|  8| 9|10|11| 12| 13| 14|15|
|--|--|--|---|--|--|---|--|--|---|--|--|--|---|---|---|--|
|Novo Valor|15| 9| 7| 4| 1| 11| 6| 10| 0| 3| 13| 14| 12| 8| 5| 2|



Nova função de substituição:
```
def substitute(hexBlock): #substituição invertida
    substitutedHexBlock = ""
    substitution =  [15, 9, 7, 4, 1, 11, 6, 10,
                     0, 3, 13, 14, 12, 8, 5, 2]
    for hexDigit in hexBlock:
        newDigit = substitution[int(hexDigit, 16)]
        substitutedHexBlock += hex(newDigit)[2:]
    return substitutedHexBlock
```

Permutação:


| Posição |  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  | 10  | 11  | 12  | 13  | 14  | 15 |16 |17 |18 |19 |20 |21 |22 |23 |24 |25 |26 |27 |28 |29 |30 |31 |
|---------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| Valor Antigo  |  8  |  4  | 15  |  9  |  3  | 14  |  6  |  2  | 13  |  1  |  7  |  5  | 12  | 10  | 11  |  0  | 27  | 12  | 21  | 26  | 10  | 16  |  0  | 24  |  7  |  5  |  3  | 20  | 13  |  9  | 17  |  8  |

| Posição |  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  | 10  | 11  | 12  | 13  | 14  | 15 |16 |17 |18 |19 |20 |21 |22 |23 |24 |25 |26 |27 |28 |29 |30 |31 |
|---------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| Novo Valor | 22  |  9  | 15  | 26  |  5  | 25  |  0  | 24  | 31  | 29  | 20  | 11  | 17  | 28  | 13  |  8  | 21  | 30  |  3  |  7  | 27  | 18  |  1  |  6  | 23  | 14  | 19  | 16  | 12  |  4  |  2  | 10  |



Nova função de permutação:
```
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
```
## Código final e a Flag
```
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
```
Rodando este código, obtemos a flag:

>nactf{5ub5t1tut10n_p3rmutat10n_n33d5_a_k3y}

E realmente, o método de substituição precisa de uma chave :))
