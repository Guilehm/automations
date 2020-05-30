import requests
from requests import RequestException

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

    def _validate_request(self, platform, username):
        url = self.base_url.format(
            platform=platform,
            username=username,
        )
        response = requests.get(url)
        try:
            response.raise_for_status()
        except RequestException:
            raise
        self._response = response
