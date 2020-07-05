from json import JSONDecodeError
from digispider import config
import requests


class RequestWrapper:
    _ALLOWED_METHODS = ['get', 'post']

    def __init__(self, url, headers=None, payload=None, cookies=None):
        self.url = url
        self.headers = headers if headers else {}
        self.payload = payload if payload else {}
        self.cookies = cookies if cookies else {}

    def call(self, method):
        assert method in self._ALLOWED_METHODS, \
            f"Invalid method given: {method}"
        s = requests.Session()
        res = getattr(s, method)(url=self.url,
                                 data=self.payload,
                                 headers=self.headers,
                                 cookies=self.cookies)
        return s, res


def login(operation=None):
    """
    operation: type of login order/invoice/...
    :return: login response with requests' session
    """

    urls = {
        'invoices': f"{config['base_url']}/account/login/?_back=https://seller.digikala.com/sellerinvoice/",
        'orders': f"{config['base_url']}/account/login/?_back=https://seller.digikala.com/orders/"
    }

    headers = {
        'Host': 'seller.digikala.com',
        'Connection': 'keep-alive',
        'Content-Length': '115',
        'Cache-Control': 'max-age=0',
        'Origin': 'https://seller.digikala.com',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/78.0.3904.108 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,'
                  'application/xml;q=0.9,'
                  'image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Referer': urls[operation],
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8'
    }

    rw = RequestWrapper(url=urls[operation], headers=headers, payload=config['credential'])
    return rw.call('post')


def parse_parameters(params):
    if not params:
        return {}

    parsed_params = {}
    params = map(lambda x: x.split('='), params.split('&'))
    for part in params:
        parsed_params[part[0]] = part[1]

    return parsed_params


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance
