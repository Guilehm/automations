from databases.mongo import get_db


class BaseSpider:
    def __init__(self, base_url, db_name=None):
        self.base_url = base_url
        self._response = None
        self.response = None
        self.db = get_db(db_name) if db_name else None

    def save_data(self, data, collection):
        collection = self.db[collection]
        many = not isinstance(data, dict) and len(data) > 1
        if many:
            return collection.insert_many(data)
        return collection.insert_one(data)
