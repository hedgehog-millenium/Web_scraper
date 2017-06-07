from urllib import request,parse
import lxml.html
from http.cookiejar import CookieJar

LOGIN_EMAIL = 'firstbot1990@gmail.com'
LOGIN_PASSWORD = 'firstbot1990'
LOGIN_URL = 'https://www.list.am/login'


def login_cookies(data_dict={'email':'email@gmail.com','passwor':'password'},proxy=None):
    """working login
    """
    cj = CookieJar()
    opener = request.build_opener(request.HTTPCookieProcessor(cj))

    if proxy:
        print("proxy = ",proxy)
        proxy_params = {parse.urlparse(LOGIN_URL).scheme: proxy}
        opener.add_handler(request.ProxyHandler(proxy_params))

    html = opener.open(LOGIN_URL).read()
    data = parse_form(html)
    for k in data_dict:
        data[k] = data_dict[k]
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
    for e in tree.cssselect('form input,form textarea'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data


if __name__ == '__main__':
    data_dict = {'your_email': LOGIN_EMAIL, 'password': LOGIN_PASSWORD}
    opener = login_cookies(data_dict)
    add_page_html = opener.open('https://www.list.am/add/58').read()
    form = parse_form(add_page_html)
    for k in form:
        print(k, ' : ', form[k])