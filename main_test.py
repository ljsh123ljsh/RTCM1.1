from RTCM import RTCM
from stable import Tool
from stable.Map import Map

x = '''
e8 6a 64 fb da 61 0c 45 ba 77 2a 1c 08 00 45 04
01 59 20 ac 40 00 75 06 70 67 78 cc ca 65 c0 a8
6f ad 21 f3 cb 59 d4 bc 77 f9 69 69 f5 49 50 18
01 fd 17 b0 00 00 d3 00 82 43 20 01 42 c4 f4 e2
2c 00 24 05 04 84 00 00 00 00 20 20 01 00 6d b6
f9 3d 25 19 0d 39 2d 35 2a cb 1d dc 9c 0d 91 53
50 0d 80 21 f2 63 64 a0 d8 95 af b8 02 b0 00 c0
68 00 b8 47 e9 10 89 20 ff b7 f7 6f 97 f2 27 ff
b7 81 79 3d ad e5 a4 9f b9 c1 3f 02 5b 00 b6 f4
08 ec 18 13 51 60 59 e8 85 53 be 1a 14 a8 68 26
9e c2 0c fa a4 87 dd dd dd dd dd dd dd c0 00 29
9b 2b 70 bb 4c 6c a6 9a ee b2 70 b9 cf 6b d3 00
49 3f 40 01 3c 55 cd 02 00 a4 3f 71 4f 82 54 b6
c2 2d 84 07 30 69 9e b1 98 70 16 83 44 20 a3 0d
b0 93 31 03 30 13 92 6c 62 26 53 05 0d db f8 6b
ac 23 98 40 88 fe 15 bb 17 0a 12 0f b7 90 00 50
cb 08 ae 10 47 02 39 1e c6 60 71 5f f5 d3 00 13
3e d0 01 03 f9 61 c7 78 69 8a dd 08 9e 84 07 a3
1f b1 9f 92 cc da d3 00 05 3e f0 01 00 00 c2 7e
5c d3 00 30 40 90 01 00 00 00 0d 54 52 49 4d 42
4c 45 20 42 44 39 39 30 10 35 2e 33 36 2c 32 30
2f 4a 55 4e 2f 32 30 31 38 0a 35 38 32 35 43 30
30 35 35 32 40 aa 90
'''

def map_d30(content):
    header = 'd30'
    content = content.replace('\n', '').replace(' ', '')
    while 1:
        index = Map(header, content).map_first()
        if index is None:
            break
        index = index.span()
        length = int(content[index[1]:index[1]+3], base=16)
        data = content[index[1]:index[1]+3+length*2]
        yield data
        content = content[index[1] + 3 + length*2:]

def main():
    data_gen = map_d30(x)
    '''
    每条信息不包括d30，从d30后的长度开始解析
    '''
    while 1:
        try:
            data = next(data_gen)
        except StopIteration:
            print("——" * 30)
            print('COMPLETE')
            break
        length = int(data[0:3], base=16)
        data = data[3:]
        supp = Tool.supplehead(data[0])
        data = supp + bin(int(data, base=16))[2:]
        rtcm_type = data[0:12]  # 差分电文类型12bis
        print( "——"*30)
        print("RTCM格式：{}".format(int(rtcm_type, base=2)))
        print("比特数：{};\t字节数:{}".format(length * 8, length))
        if int(rtcm_type, base=2) in [1074, 1084, 1094, 1114, 1124]:  # 1074-GPS, 1084-GLONASS, 1094-GALILEO, 1114-QZZSS, 1124-BDS
            RTCM().MSM4(data)
        elif int(rtcm_type, base=2) == 1005:
            RTCM().rtcm1005(data)
        elif int(rtcm_type, base=2) == 1007:
            RTCM().rtcm1007(data)
        elif int(rtcm_type, base=2) == 1033:
            RTCM().rtcm1033(data)
        else:
            print("暂不支持")
            continue

if __name__ == '__main__':
    main()


