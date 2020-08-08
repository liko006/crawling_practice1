# 다나와 웹사이트에서 상품정보 다운받아 엑셀에 저장
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from tqdm import tqdm_notebook
import pandas as pd

driver = webdriver.Chrome('chromedriver.exe')
driver.implicitly_wait(2)

def get_prod_items(prod_items):
    
    prod_data = []
    for prod_item in prod_items:
        try:  
            # 상품정보 가져오기
            title = prod_item.select('p.prod_name')[0].text.strip()
        except:
            title = ''
    
        try:
            # 상품 상세정보 가져오기
            spec_list = prod_item.select('div.spec_list')[0].text.strip()
        except:
            spec_list = ''

        try:
            # 가격정보 가져오기
            price = prod_item.select('li.rank_one > p.price_sect > a > strong')[0].text.strip()
        except:
            price = ''
            
        prod_data.append([title, spec_list, price])
        
    return prod_data

def get_search_page_url(keyword, page):
    return 'http://search.danawa.com/dsearch.php?query={}&volumeType=allvs&page={}&limit=40&sort=saveDESC&list=list&boost=true&addDelivery=N&tab=goods'.format(keyword, page)

keyword = '무선청소기'
total_page = 10
prod_data_total = []

for page in tqdm_notebook(range(1, total_page+1)):
    driver.get(url)
    url = get_search_page_url(keyword, page)
    time.sleep(3)
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    prod_items = soup.select('div.main_prodlist > ul.product_list > li.prod_item')
    prod_item_list = get_prod_items(prod_items)
    
    prod_data_total = prod_data_total + prod_item_list
    

# 데이터 저장    
data = pd.DataFrame(prod_data_total)

data.columns = ['상품명', '스펙 목록', '가격']

data.to_excel('./0802/danawa_crawling_result.xlsx', index=False)

# 크롤링 결과(저장된 파일의 데이터) 호츨
data = pd.read_excel('./0802/danawa_crawling_result.xlsx')
data.info()
print('-'*80)
data.head()

