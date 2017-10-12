from CustomCrypto.LEA import LEA


def getMAC(pt, key, PKCSPadding = True):
    if pt is None:
        raise AttributeError('Improprt pt')
    lea = LEA(key)

    buffer = LEA.to_bytearray(pt)
    chain_vec = buffer[0:16]
    offset = 0
    mac = bytearray()

    len_x16 = len(buffer)-16
    while offset <= len_x16:
        chain_vec = lea.encrypt(LEA.xorAr(chain_vec, buffer[offset:offset+16]))

        offset+= 16

    if PKCSPadding:
        more = len(buffer) - offset
        buffer += bytearray([more])*more

    chain_vec = lea.encrypt(LEA.xorAr(chain_vec, buffer[offset:offset+16]))

    return chain_vec






def is_vailid(ct, mac):
    pass









