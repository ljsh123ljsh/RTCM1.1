from redis import StrictRedis as r
r = r(host='49.233.166.39', port=6379, db=12)

async def inp(content):
    r.lset()

