from bs4 import BeautifulSoup
import urllib.request as req

url = "https://finance.naver.com/"
res = req.urlopen(url)

soup = BeautifulSoup(res, "html.parser")

price = soup.select_one("#content > div.article > div.section2 > div.section_stock_market > div.section_stock > div.kospi_area.group_quot.quot_opn > div.heading_area > a > span > span.num").string
print("오늘의 코스피 : {}".format(price))