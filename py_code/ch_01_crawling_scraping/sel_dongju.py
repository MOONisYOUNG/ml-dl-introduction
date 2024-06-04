from bs4 import BeautifulSoup
import urllib.request as req

url = "https://ko.wikipedia.org/wiki/%EC%9C%A4%EB%8F%99%EC%A3%BC"
res = req.urlopen(url)
soup = BeautifulSoup(res, "lxml")

# 화살표 있으나 없으나 결과는 동일 (물론 화살표 있는 게 가독성은 더 좋음)
a_list = soup.select("#mw-content-text > div.mw-content-ltr.mw-parser-output > ul:nth-child(58) > li")
# a_list = soup.select("#mw-content-text div.mw-content-ltr.mw-parser-output ul:nth-child(58) li")

for a in a_list:
    name = a.text
    print("-", name.split('—')[0])