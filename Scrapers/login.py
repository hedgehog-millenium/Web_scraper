from urllib import request,parse
import lxml.html
from http.cookiejar import CookieJar

LOGIN_EMAIL = 'hedgehog.millenium@gmail.com'
LOGIN_PASSWORD = 'SaQo2017'
LOGIN_URL = 'https://www.list.am/login'


def login_basic():
    """fails because not using formkey
    """
    data = {'email': LOGIN_EMAIL, 'password': LOGIN_PASSWORD}
    encoded_data = parse.urlencode(data).encode("utf-8")
    req = request.Request(LOGIN_URL, encoded_data)
    response = request.urlopen(req)
    print(response.geturl())


def login_formkey():
    """fails because not using cookies to match formkey
    """
    html = request.urlopen(LOGIN_URL).read()
    data = parse_form(html)
    data['email'] = LOGIN_EMAIL
    data['password'] = LOGIN_PASSWORD
    encoded_data = parse.urlencode(data).encode("utf-8")
    req = request.Request(LOGIN_URL, encoded_data)
    response = request.urlopen(req)
    print(response.geturl())


def login_cookies():
    """working login
    """
    cj = CookieJar()
    opener = request.build_opener(request.HTTPCookieProcessor(cj))
    html = opener.open(LOGIN_URL).read()
    data = parse_form(html)
    data['your_email'] = LOGIN_EMAIL
    data['password'] = LOGIN_PASSWORD
    encoded_data = parse.urlencode(data).encode('utf-8')
    req = request.Request(LOGIN_URL, encoded_data)
    response = opener.open(req)
    print(response.geturl())
    return opener


def parse_form(html):
    """extract all input properties from the form
    """
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data


if __name__ == '__main__':
    login_cookies()