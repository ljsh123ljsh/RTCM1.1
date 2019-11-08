from redis import StrictRedis
r = StrictRedis(host='49.233.166.39', port=6379, db=10, decode_responses=True)
from json import loads
# def singal_type(rtcm, IDlist):
#     r1074 =
rtcm1074 = r.hgetall('rtcm1074')
rtcm1084 = r.hgetall('rtcm1084')
rtcm1094 = r.hgetall('rtcm1094')
rtcm1124 = r.hgetall('rtcm1124')

Nsig_id = [2, 10, 23]
rtcmtype = 1074
DIC = eval('rtcm'+str(rtcmtype))
print(DIC[str(3)])
mm = DIC[str(3)]
print(type(loads(mm)))
Nsig_id = [loads(DIC[str(x)])['FrequencyBand'] for x in Nsig_id]
print(Nsig_id)
