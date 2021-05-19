import redis
from data import channels


# DB configurations
HOST = "localhost"
# HOST = "db-redis"
PORT = 6379


def connect_db(database=0):
    '''Create conection to DB'''
    conexion = redis.StrictRedis(host=HOST, port=PORT, db=database, charset="utf-8", decode_responses=True)
    # if(conexion.ping()):
    #     print("Conectado a servidor de redis")
    # else:
    #     print("error")
    return conexion

# DB Acceses
conexion = connect_db()
client = conexion.pubsub()

def DBInit():
    '''Reset and init DB '''
    conexion.flushall()
    for channel in channels:
        conexion.rpush("channels", channel)


def getChannels():
    '''return list of channel (name, subscribers)'''
    channels = conexion.lrange("channels", 0, -1)
    channels_list = []
    for channel in channels:
        channels_list.append({"name": channel, "subscribers": 0})
    return channels_list


def updateNumberOfSubscribers(channel):
    ''' get the channel dict and set value of subscribers key'''
    channel['subscribers'] = conexion.pubsub_numsub(channel['name'])[0][1]


def publishInChannels(channels, message):
    '''publish message in channels'''
    for channel in channels:
        conexion.publish(channel, message)


def subscribeToChannels(channels, pubsub):
    for channel in channels:
        pubsub.subscribe(channel)


def unsubscribeToChannels(channels, pubsub):
    for channel in channels:
        pubsub.unsubscribe(channel)