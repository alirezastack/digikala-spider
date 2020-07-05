from digispider.utils import singleton
from mongoengine import connect


@singleton
class MongoConnection:
    def __init__(self, cfgs):
        self.client = connect(**cfgs)

        # The ismaster command is cheap and does not require auth.
        # ConnectionFailure/ServerSelectionTimeoutError will be raised if MongoDB is not reachable
        self.client.admin.command('ismaster')

    def __str__(self):
        return self.client
