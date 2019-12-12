from redis import StrictRedis
from DB import redis
REDIS = StrictRedis(host=redis['host'], port=int(redis['port']), password=redis['password'], db=redis['db'])