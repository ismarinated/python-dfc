import random as rnd

def expanding_function(K):
    KS = 'DA06C80ABB1185EB4F7C7B5757F5958490CFD47D7C19BB42158D9554F7B46BCE'
    
    PK = [(K + KS[len(K):])[i: i + 8] for i in range (0, 64, 8)]
    
    OA1 = PK[0] + PK[7]
    OB1 = PK[4] + PK[3]
    EA1 = PK[1] + PK[6]
    EB1 = PK[5] + PK[2]

    KA2 = 'B7E151628AED2A6A'
    KA3 = 'BF7158809CF4F3C7'
    KA4 = '62E7160F38B4DA56'
    KB2 = 'A784D9045190CFEF'
    KB3 = '324E7738926CFBE5'
    KB4 = 'F4BF8D8D8C31D763'

    OA2 = hex(int(OA1, base=16) ^ int(KA2, base=16)).upper()[2::]
    OB2 = hex(int(OB1, base=16) ^ int(KB2, base=16)).upper()[2::]
    EA2 = hex(int(EA1, base=16) ^ int(KA2, base=16)).upper()[2::]
    EB2 = hex(int(EB1, base=16) ^ int(KB2, base=16)).upper()[2::]

    OA3 = hex(int(OA1, base=16) ^ int(KA3, base=16)).upper()[2::]
    OB3 = hex(int(OB1, base=16) ^ int(KB3, base=16)).upper()[2::]
    EA3 = hex(int(EA1, base=16) ^ int(KA3, base=16)).upper()[2::]
    EB3 = hex(int(EB1, base=16) ^ int(KB3, base=16)).upper()[2::]

    OA4 = hex(int(OA1, base=16) ^ int(KA4, base=16)).upper()[2::]
    OB4 = hex(int(OB1, base=16) ^ int(KB4, base=16)).upper()[2::]
    EA4 = hex(int(EA1, base=16) ^ int(KA4, base=16)).upper()[2::]
    EB4 = hex(int(EB1, base=16) ^ int(KB4, base=16)).upper()[2::]

    Kt1 = OA1 + OB1 + OA2 + OB2 + OA3 + OB3 + OA4 + OB4
    Kt2 = EA1 + EB1 + EA2 + EB2 + EA3 + EB3 + EA4 + EB4

    return Kt1, Kt2

def trunc6(x):
    return bin(int(x, base=16))[2:8]

def round_table(x):
    table = ['B7E15162', '8AED2A6A', 'BF715880', '9CF4F3C7',
             '62E7160F', '38B4DA56', 'A784D904', '5190CFEF',
             '324E7738', '926CFBE5', 'F4BF8D8D', '8C31D763',
             'DA06C80A', 'BB1185EB', '4F7C7B57', '57F59584',
             '90CFD47D', '7C19BB42', '158D9554', 'F7B46BCE',
             'D55C4D79', 'FD5F24D6', '613C31C3', '839A2DDF',
             '8A9A276B', 'CFBFA1C8', '77C56284', 'DAB79CD4',
             'C2B3293D', '20E9E5EA', 'F02AC60A', 'CC93ED87',
             '4422A52E', 'CB238FEE', 'E5AB6ADD', '835FD1A0',
             '753D0A8F', '78E537D2', 'B95BB79D', '8DCAEC64',
             '2C1E9F23', 'B829B5C2', '780BF387', '37DF8BB3',
             '00D01334', 'A0D0BD86', '45CBFA73', 'A6160FFE',
             '393C48CB', 'BBCA060F', '0FF8EC6D', '31BEB5CC',
             'EED7F2F0', 'BB088017', '163BC60D', 'F45A0ECB',
             '1BCD289B', '06CBBFEA', '21AD08E1', '847F3F73',
             '78D56CED', '94640D6E', 'F0D3D37B', 'E67008E1']
    
    RT_x = int(trunc6(x), base=2)

    return table[RT_x]

def round_function(Ki, m):

    a, b = Ki[:16], Ki[16:32]
    
    x = hex(((int(a, base=16) * int(m, base=16) + int(b, base=16)) % (2**64 + 13)) % 2**64).upper()[2::]
    
    x1, x2 = x[:8], x[8:16]

    KC = 'EB64749A'
    KD = '86D1BF275B9B241D'

    y = hex((int((hex((int(round_table(x1), base=16) ^ int(x2, base=16))).upper()[2::] + hex(int(x1, base=16) ^ int(KC, base=16)).upper()[2::]), base=16) + int(KD, base=16)) % 2**64).upper()[2::]
    
    return y

def block_composer(key, m, c = 0):
    L = m[:16]
    R = m[16:32]

    K = expanding_function(key)
    
    count = 0
    while(count < 7):
        if (c % 2 == 1 and (count + 1) % 2 == 1) or ((count + 1) % 2 == 0 and c == 0):
            Ki = K[0]
        else: Ki = K[1]

        Ki = [Ki[i: i + 32] for i in range (0, 128, 32)]

        if c > 0:
            Ki.reverse()

        result_RF = round_function(Ki[count // 2], L)

        buf = L
        L = hex(int(result_RF, base=16) ^ int(R, base=16)).upper()[2::]
        R = buf

        count += 1
        if c > 0:
            c += 1

    if c > 0:
        Ki = K[1]
        Ki = [Ki[i: i + 32] for i in range (0, 128, 32)]
        Ki.reverse()

        result_RF = round_function(Ki[3], L)

    else:
        Ki = K[0]
        Ki = [Ki[i: i + 32] for i in range (0, 128, 32)]

        result_RF = round_function(Ki[3], L)
   
    R = hex(int(result_RF, base=16) ^ int(R, base=16)).upper()[2::]

    return L + R

source = 'CFCED0CED8C8CDC0FCEC0DEC8D8CDC0C'
key = '0000CCC0D0C8CDC0'

# Шифрование
e = block_composer(key, source)

# Дешифрование
d = block_composer(key, e, 1)

print(f"Исходное значение - {source}, ключ - {key}\nШифрование - {e}\nДешифрование - {d}")