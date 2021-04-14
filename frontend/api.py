import requests
from json import loads, dumps
from types import SimpleNamespace

URL = "http://127.0.0.1:8000"
API_LISTS_LIST = "api/lists/"
API_LISTS_CREATE = "api/lists/"
API_LISTS_READ = "lists/{0}/"
API_LISTS_UPDATE = "lists/{0}/"
API_LISTS_PARTIAL_UPDATE = "lists/{0}/"
API_LISTS_DELETE = "lists/{0}/"
API_TOKEN = "api/token/"

CODE_SUCCESS = 200
JSON_HEADERS = {'content-type': 'application/json', 'accept': 'application/json'}

get_api = lambda x: URL + "/" + x
dump = lambda x: bytes(dumps(x), encoding="utf-8")

class User(object):

    def __init__(self):
        pass

    def auth(self, user, passwd):
        url = get_api(API_TOKEN)
        data = dump({"username": f"{user}", "password": f"{passwd}"})
        code, self.token = User.post(url=url, data=data, headers=JSON_HEADERS)
        return code
    
    def list(self):
        return User.get(
            url=get_api(API_LISTS_LIST), 
            headers=self._authorised_())
    
    def create(self, title="Untitled"):
        return User.post(
            url=get_api(API_LISTS_CREATE), 
            data=dump({"title": title}), 
            headers=self._authorised_())
    
    def read(self, id):
        return User.post(
            url=get_api(API_LISTS_READ).format(id), 
            headers=self._authorised_())
    
    def update(self, id, title="Untitled"):
        return User.__request__(
            func=requests.put,
            data=dump({"title": title}),
            url=get_api(API_LISTS_UPDATE).format(id), 
            headers=self._authorised_())
            
    def partial_update(self, id, title="Untitled"):
        return User.__request__(
            func=requests.patch,
            data=dump({"title": title}),
            url=get_api(API_LISTS_PARTIAL_UPDATE).format(id), 
            headers=self._authorised_())
    
    def delete(self, id):
        return User.__request__(
            func=requests.delete,
            url=get_api(API_LISTS_DELETE).format(id), 
            headers=self._authorised_())
    
    def _authorised_(self, headers=JSON_HEADERS):
        if not hasattr(self, "token"):
            raise RuntimeError("Authosization required for requested operation!")
        headers = headers.copy()
        headers['Authorization'] = f'Bearer {self.token.access}'
        return headers
    
    @staticmethod
    def get(**argv):
        return User.__request__(requests.get, **argv)
        
    @staticmethod
    def post(**argv):
        return User.__request__(requests.post, **argv)
        
    @staticmethod
    def __request__(func, verbose=True, **argv):
        with func(**argv) as r:
            if r.status_code == CODE_SUCCESS:
                data = loads(r.text)
                if type(data) is dict:
                    data = SimpleNamespace(**data)
            else:
                data = None
            return r.status_code, data