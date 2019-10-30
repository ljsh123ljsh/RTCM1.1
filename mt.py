from RTCM import RTCM
from stable import Tool

'''
解析d30
'''


def analyse(data):
    '''
    :param data: d30开始的报文
    :return: 解析
    '''
    data = data[3:]
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

