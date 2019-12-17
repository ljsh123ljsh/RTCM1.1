from RTCM_ANALYSE.Analyse import analyse
from stable.Tool import segment_d30
from stable.Tool import map_d30
from threading import Thread
import time

content = 'd300b743200172ffe1623f8041d0811200000000202001007dfedbf4b47444f484d504950da7f31f42de8e4e2301456033706b30c2e5714a837adcf5cbe8789b2136a263fb46f6329557296d95f7227eb5fd6bbab4c298049f09bc084bf81f3740716c056c8a12fecff35bbfdebe7f6222136b9849faa12751fb7b2bed41f872a1c17d26793fc9e39c07ba045ef7b67bf5a60567e012d4e0485e7ffffffffffffffffffffff800000aabbf1b74cb5aa8b2eb299a68adbf2a26ac61e523d3004143c001ae92c6223f800003400000000000204000007e82867fa862925929a25986314c0892e0241413b428451aa18b42862b8e138388518d9fffffe06fbe9a6ba081916dd3006844600172ffe1623f802001004200000000080101007ffa72d2c275650654befe656cc1597d3d69fb78f771cddb9c9f3b5e091c0cb812fa6ccfecd01fb4c8dfa49d7f01effc6ab7db093fbe17ff1a69f089e7c3baff0e177fffffffffff80063a6724d3cf555761781092add3010d46400172ff06a03f807bfc000000000000208200007ffffffffbdbf3d3fc23c3f40bda624422933a76d0e4dacea2436fa21828ad704e9066609bb55569d2d23c2a584dd092f169a29b44f87cb8f747eefce841b6b36e81cfc2ed05b0ca8d8f6322703ce05640bc3195e219c4a4163c25304bae231c51f8c981132c0370c00be4fe93bdfaa8a9e973d82804c09b4b0258480a9de02df740a36eff0f61fb2eafedaf4224c78899b223b7f01b1100695a81ccade2d3bf8d12be3b308285d00b82183017be3c3ef8b5d7e5a4c82232e0967f828975f2140fc8859f278affffffffffffffffffffffffffffffffffff8000000005d7e145775b7e14db6c92cd7e79d775d4d35d97e18e99e3b6d34f4078ff00d300133ed00103f957745f928ad2b2f3b007a8c6ce3f7da1b3d300053ef0010000c27e5cd300304090010000000d5452494d424c4520424439393010352e33362c32302f4a554e2f323031380a3538323543303035353240aa90'

content_lis = segment_d30(content)

if __name__ == '__main__':
    t1 = time.time()
    thread_list = []
    print(len(content_lis))
    for data in content_lis:
        thr = Thread(target=analyse, args=(data, ))
        thread_list.append(thr)
    for l in thread_list:
        l.start()
    for l in thread_list:
        l.join()
    t2 = time.time()
    gen = map_d30(content)
    i = 1
    while i:
        try:
            data = next(gen)
            analyse(data)
            i += 1
        except StopIteration:
            break
    print(i)
    t3 = time.time()
    print("seg:{};  gen:{}".format(t2-t1, t3-t2))
    print(t2-t1)
    print(t3-t2)