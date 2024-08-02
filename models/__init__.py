from .engine.file_storage import FileStorage
from .engine.db_storage import DBStorage
from os import getenv

storage_type = getenv('HBNB_TYPE_STORAGE')

if storage_type == "db":
    storage = DBStorage()
    storage.reload()
else:
    storage = FileStorage()
    storage.reload()
