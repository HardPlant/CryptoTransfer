'''
LEA Algorithm
See : https://seed.kisa.or.kr/html/egovframework/iwt/ds/ko/ref/LEA%20A%20128-Bit%20Block%20Cipher%20Datasheets-Korean.pdf


'''
def BitToInt(x):
    assert(type(x) == bytearray)
    assert(len(x) == 32)
    sum = 0
    currentbin = 1
    for item in reversed(x):
        sum = item * currentbin
        currentbin *= 2
    return sum

def IntToBit(x):
    pass
def KeySechdule_enc(key):
    pass
def KeySechedule_dec(key):
    pass

def ROL(X):
    pass
def ROR(x):
    pass
def round_enc():
    pass
def round_dec():
    pass


# Nr

round = (24,28,32)
