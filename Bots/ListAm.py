from Scrapers.downloader import Downloader


class ListAmBot:
    __LOGIN_EMAIL = 'firstbot1990@gmail.com'
    __LOGIN_PASSWORD = 'firstbot1990'
    __LOGIN_URL = 'https://www.list.am/login'

    def add_flat_announcement(self):
        data_dict = {'your_email': self.__LOGIN_EMAIL, 'password': self.__LOGIN_PASSWORD}
        proxy = '61.5.207.102:80'
        opener = Downloader.login_cookies(self.__LOGIN_URL, data_dict, proxy)
        add_page_html = opener.open('https://www.list.am/add/58').read()
        form = Downloader.parse_form(add_page_html)
        for k in form:
            print(k, ' : ', form[k])


if __name__ == "__main__":
    from Scrapers.proxy_manager import ProxyManager
    mgr = ProxyManager()
    mgr.get_proxy_list()

    # bot = ListAmBot()
    # bot.add_flat_announcement()
