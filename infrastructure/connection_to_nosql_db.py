import pymongo
from bson.binary import UuidRepresentation

uri = "mongodb://curvex-ddd-d3-group208-int:1yxggqBk8TfmwCeIybGH6UBNYT7OkqX72fBGwK3Rkg3FTkvr9xp8n3ulzTIn6oJyfdHA7wya7qMvUsKV7P42pg==@curvex-ddd-d3-group208-int.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@curvex-ddd-d3-group208-int@"
client = pymongo.MongoClient(uri, uuidRepresentation='standard')

database_api = client.curvex.curvex001

