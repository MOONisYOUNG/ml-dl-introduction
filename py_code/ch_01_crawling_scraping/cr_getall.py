from bs4 import BeautifulSoup
from urllib.request import *
from urllib.parse import *
from os import makedirs
import os.path, time, re

# 처리된 파일명 데이터 저장하는 용도
proc_files = {}

# HTML 내부에 있는 링크 추출
def enum_links(html, base):
    soup = BeautifulSoup(html, "lxml")
    links = soup.select("link[rel='stylesheet']")
    links += soup.select("a[href]")
    result = []
    for a in links:
        href = a.attrs['href']
        url = urljoin(base, href)
        result.append(url)
    return result

# 파일 다운로드
def download_file(url):
    o = urlparse(url)
    savepath = "./" + o.netloc + o.path
    if re.search(r"/$", savepath):
        savepath += "index.html"
    savedir = os.path.dirname(savepath)
    
    # 이미 path에 존재하는 파일명이라면 return으로 종료
    if os.path.exists(savepath):
        return savepath
    
    # path에 없는 폴더명이라면 새로 폴더 만들기
    if not os.path.exists(savedir):
        print("mkdir =", savedir)
        makedirs(savedir)
    
    try:
        print("download =", url)
        urlretrieve(url, savepath)
        time.sleep(1)
        return savepath
    except:
        print("다운 실패 :", url)
        return None
    
# html 페이지 대상으로 재귀적 분석 진행
def analyze_html(url, root_url):
    savepath = download_file(url)
    
    # savepath가 없거나 이미 처리된 파일의 경우에는 analyze를 중단
    if savepath is None:
        return
    if savepath in proc_files:
        return
    
    proc_files[savepath] = True
    print("analyze_html =", url)
    html = open(savepath, 'r', encoding="utf-8").read()
    links = enum_links(html, url)

    for link_url in links:
        # link_url의 맨 앞 부분이 root_url로 시작하지 않는 경우
        if link_url.find(root_url) != 0:
            # css 파일이 아닌 경우에 continue로 무시
            if not re.search(r".css$", link_url):
                continue
        # html 파일인 경우, 재귀적으로 analyze를 진행
        if re.search(r".(html|htm)$", link_url):
            analyze_html(link_url, root_url)
            continue
        download_file(link_url)

if __name__ == "__main__":
    url = "https://docs.python.org/3.5/library/"
    analyze_html(url, url)