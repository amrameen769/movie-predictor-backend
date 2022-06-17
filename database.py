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
  

  

