from stable import Tool
from stable.Map import Map
from RTCM import RTCM

if __name__ == '__main__':

    file = open('g1.txt', 'r', encoding='utf-8')
    content = file.read()
    content = content.replace('\n', '').replace(' ', '')
    header = 'D30'
    header_ = 'd30'
    indexlist = Map(header, content).map_id(add=False)
    # print(indexlist)
    try:
        content_list = Tool.split_content(content, indexlist)
    except TypeError:
        indexlist = Map(header_, content).map_id(add=False)
        content_list = Tool.split_content(content, indexlist)

    for data in content_list:
        try:
            length = int(data[3:6], base=16)
        except:
            continue
        data = data[6:6 + length * 2]
        # print(len(data))
        if 2 * length > len(data):  # 实际长度小于理论长度时，校验不通过
            continue
        supp = Tool.supplehead(data[0])
        data = supp + bin(int(data, base=16))[2:]
        rtcm_type = data[0:12]  # 差分电文类型12bis
        print("--------------------------------------------------------------------------------------------------------")
        print("RTCM格式：{}".format(int(rtcm_type, base=2)))
        print("比特数：{};字节数:{}".format(length*8, length))
        if int(rtcm_type, base=2) in [1074, 1084, 1094, 1114, 1124]:    # 1074-GPS, 1084-GLONASS, 1094-GALILEO, 1114-QZZSS, 1124-BDS
            print(data)
            RTCM().MSM4(data)
        elif int(rtcm_type, base=2) == 1005:
            RTCM().rtcm1005(data)
        elif int(rtcm_type, base=2) == 1007:
            RTCM().rtcm1007(data)
        elif int(rtcm_type, base=2) == 1033:
            RTCM().rtcm1033(data)
        else:
            continue

