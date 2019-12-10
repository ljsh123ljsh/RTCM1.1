from stable.Map import Map
from stable import Tool
from stable.CellContent import CellContent
from stable.ConvertDecimal import ConvertDecimal as cd
from stable.ClientReceiver import ClientReceiver as cr
from json import loads
import DATABASE as db
r = db.REDIS



class RTCM:

    def MSM4(self, data, rtcmtype):
        rtcm1074 = r.hgetall('rtcm1074')
        rtcm1084 = r.hgetall('rtcm1084')
        rtcm1094 = r.hgetall('rtcm1094')
        rtcm1124 = r.hgetall('rtcm1124')
        # 12bits参考站ID； 30bitsGNSS历元； 1bit多点文标志； 7bits保留位； 2bits时钟校准标志； 2bits拓展时钟标志； 1bitGNSS平滑类型标志； 3bitsGNSS平滑区间  共61bits省略
        ID = data[12:24]
        print("参考站ID = {}".format(cd(ID).convertdecimal()))
        gnss_liyuan = data[24:24+30]
        print("GNSS历元 = {}".format(cd(gnss_liyuan).convertdecimal()))
        gnss_sta = data[73:74 + 64]  # 卫星掩码64bits
        sat = Map('1', gnss_sta)
        Nsat = sat.map_amount()  # 卫星数
        # print(Nsat)
        Nsat_id = sat.map_id()
        gnss_sig = data[137:137 + 32]  # 信号掩码32bits
        sig = Map('1', gnss_sig)
        Nsig = sig.map_amount()  # 信号数
        # print(Nsig)
        Nsig_id = sig.map_id()
        print(Nsig_id)
        DIC = eval('rtcm'+rtcmtype)
        Nsig_id = [loads(DIC[str(x)])['FrequencyBand'] for x in Nsig_id]

        '''
        加入信号类型
        '''
        print("信号类型：{}".format(Nsig_id))

        X = Nsat * Nsig
        gnss_x = data[169:169 + X]  # 单元掩码X bits
        Ncell = Map('1', gnss_x).map_amount()  # 单元掩码数
        # print(Ncell)
        print("卫星数：{}; 信号数：{}; 单元数：{}".format(Nsat, Nsig, Ncell))


        # -----------卫星数据data2------------
        data2 = data[169 + X:]
        pse11 = CellContent(Nsat, 11)
        pse11_li = pse11.ReturnContent(data2)

        data22 = pse11.RestContent()
        pse12 = CellContent(Nsat, 12)
        pse12_li = pse12.ReturnContent(data22)

        gnss = Tool.extend_satli(pse11_li, pse12_li, gnss_x, Nsig)
        # -----------信号数据datan------------
        datan = pse12.RestContent()
        dic = {}
        i = 1
        while i <= 5:
            p = CellContent(Ncell, i)
            p.ReturnContent(datan)  # 1精确伪距,2相位距离,3相位距离锁定时间标志,4半周模糊度标志,5信噪比CNR
            p_ll = p.ConvertContent(gnss_x)  # 列表与单元掩码融合后
            # print(p_ll)
            if i == 1:  # 精确伪距处理
                p_ll = p.ConvertDecimal(least=24, symbol=True)

            elif i == 2:
                p_ll = p.ConvertDecimal(least=24, symbol=True)
                print('载波相位：{}'.format(p_ll))
            elif i == 5:  # 信噪比处理
                p_ll = p.ConvertDecimal()
            dic[i] = p_ll
            datan = p.RestContent()
            i += 1


    def rtcm1005(self, data):
        ID = data[12:24]
        X = cd(data[34: 34+38], symbol=True).convertdecimal()/1000
        Y = cd(data[74: 74+38], symbol=True).convertdecimal()/1000
        Z = cd(data[114:114+38], symbol=True).convertdecimal()/1000
        BLH = Tool.XYZ2BLH(X, Y, Z)
        gnss = data[30:33] + data[73]
        print("参考站ID = {}".format(cd(ID).convertdecimal()))
        print("GNSS系统 = {}".format(Tool.gnss_system_server(gnss)))
        print('X = {:.4f}\nY = {:.4f}\nZ = {:.4f}'.format(X, Y, Z))
        print('B={0:.9f}\nL={1:.9f}\nH={2:.9f}'.format(BLH[0], BLH[1], BLH[2]))

    def rtcm1007(self, data):
        ID = data[12:24]
        print("参考站ID = {}".format(cd(ID).convertdecimal()))
        n = cr(data[24:32])
        print("天线标识符 = {}".format(n.Getcontent()))
        rdata = n.Restcontent()
        print("天线设置序列 = {}".format(int(rdata[0:8]+'0')))

    def rtcm1008(self, data):
        ID = data[12:24]
        print("参考站ID = {}".format(cd(ID).convertdecimal()))
        n = cr(data[24:32])
        print("天线标识符 = {}".format(n.Getcontent()))
        rdata = n.Restcontent()
        print("天线设置序列 = {}".format(int(rdata[0:8] + '0')))
        # rtcm1008
        m = int(data[40+8 * n:48+8 * n])
        char2_b = data[48+8 * n:48+8 * n + 8 * m]
        char2 = Tool.bin2ascii(char2_b)
        print("天线序列号 = {}".format(char2))

    def rtcm1033(self, data):
        ID = data[12:24]
        print("参考站ID = {}".format(cd(ID).convertdecimal()))
        n = cr(data[24:32])
        print("天线标识符 = {}".format(n.Getcontent()))
        rdata = n.Restcontent()
        print("天线设置序列 = {}".format(int(rdata[0:8]+'0')))
        rdata = rdata[8:]
        li = ['天线序列号', '接收机类型', '接收机固件版本', '接收机序列号']
        for i in range(4):
            cr1 = cr(rdata)
            print(li[i]+"= {}".format(cr1.Getcontent()))
            rdata = cr1.Restcontent()


