from config import settings
from motor.motor_asyncio import AsyncIOMotorClient

class MotorDB():
  def __init__(self):
    self.mongodb_client = AsyncIOMotorClient(settings.CLUSTER_URL)
    self.mongodb = None
  
  async def close_connection(self):
    self.mongodb_client.close()

  async def connect_db(self, db_name: str):
    self.mongodb = self.mongodb_client[settings.DB_PREFIX + db_name]
  
  async def get_collection(self, col_name: str):
    return self.mongodb[settings.COL_PREFIX + col_name]

  async def get_all_collections(self):
    if self.mongodb is not None: return await self.mongodb.list_collection_names()
    else: return False
  


# ObjectID Override

from bson import ObjectId

class PyObjectId(ObjectId):
  @classmethod
  def __get_validators__(self):
    yield self.validate
  
  @classmethod
  def validate(self, value):
    if not ObjectId.is_valid(value):
      raise ValueError("Invalid ObjectID")
    
    return ObjectId(value)
  
  @classmethod
  def __modify_schema__(self, field_schema):
    field_schema.update(type="string")


