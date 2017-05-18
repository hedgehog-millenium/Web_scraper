import scraper

url = 'https://metanit.com/python/tutorial/8.2.php'
sitemap_url = 'https://metanit.com/sitemap.xml'
html = scraper.download(url,user_agent='BadCrawler')
print(html)