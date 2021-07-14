from typing import Optional


class TestAPP:
    def __init__(self, id_query: Optional[str] = None, api: Optional[str] = None):
        self.id_query = id_query
        self.api = api
        self.data_login = {
            'email': 'wera.watcharapon@gmail.com',
            'password': 'kane!@#$',
            'remember': ['remember'],
        }
        self.data = {
            'id': '',
            'name': 'watcharapon',
            'email': 'admin@gmail.com',
            'company': 'mango consultant',
            'tel': '034155123',
            'product': 'Construction',
            'other': 'Real Estate',
            'message': 'Please try to contract me',
            'userId': 'Ud4101d790dacbc5458dbdb68414a0089',
            'email_private': 'wera.watcharaopn@gmail.com',
            'profile': 'watcharapon',
            'picture': 'https://compare-price-mango.herokuapp.com/receive',
            'channel': 'LINE',
            'authUser': {
                'uid': 'kane',
            },
            'tag': ['noting', 'success'],
            'date': '',
            'time': ''
        }

    def query_data(self, **query) -> dict:
        for key in query:
            self.data[key] = query[key]
        return self.data

    def api_include(self, include: Optional[str] = '') -> str:
        return self.api + include

    @staticmethod
    def response_json(response):
        response['id'] = ''
        response['date'] = ''
        response['time'] = ''
        return response
