import redis
import json
from os import getenv

from service.SentAnalysis import SentAnalysis
from database.Database import Database


class ListenerService:
    def __init__(self):
        self.CHANNEL_NAME = getenv('REDIS_CHANNEL')
        # self.svc = SentAnalysis()
        self.redis = redis.Redis()
        self.database = Database()

        self.pubsub = self.redis.pubsub()
        self.pubsub.psubscribe(self.CHANNEL_NAME)
        self.run()

    def run(self):
        for message in self.pubsub.listen():
            if message["type"]  == 'pmessage':
                data = json.loads(message["data"])
                id = data["id"]
                review = data["review"]
                print(id, review)
                self.database.update(id, review)
                print("Is the right channel", message["data"])
