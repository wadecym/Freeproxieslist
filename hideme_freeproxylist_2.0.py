'''
作者 : wade chen
測試日期 : 2019/3/10
'''
import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#導入無介面模式
from selenium.webdriver.chrome.options import Options


class FreeProxiesList():
    def __init__(self):
        # 設定chromecriver路徑
        driver_path = r'D:\chromedriver\chromedriver.exe'

        # 設定無介面模式
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(driver_path,chrome_options=options)

        # country=國家代碼,多選國家代碼直接連在一起(ex:選擇日本台灣美國); type=類型代碼直接連在一起(http:h,https:s); anon=匿名性(higeh:4)
        self.url = 'https://hidemyna.me/en/proxy-list/?country=JPTWUS&type=hs&anon=4'
        self.proxieslist=[]
        self.currentpage = 1
        self.maxpage = 1

    def parse_data(self,source):
        html = etree.HTML(source)
        data = html.xpath('//table[@class="proxy__t"]/tbody/tr')
        self.maxpage=html.xpath('//div[@class="proxy__pagination"]/ul/li[last()]/a/text()')[0]
        self.currentpage=html.xpath('//div[@class="proxy__pagination"]/ul/li[@class="is-active"]/a/text()')[0]
        data = html.xpath('//table[@class="proxy__t"]/tbody/tr')
        print("當前頁數 : %s ; 共 %s 組數據 " %(self.currentpage,len(data)))

        for i in range(0, len(data)):
            ip = data[i].xpath('./td[1]/text()')[0]
            port = data[i].xpath('./td[2]/text()')[0]
            country = data[i].xpath('./td[3]/div/text()')[0].strip()
            speed = data[i].xpath('./td[4]//p/text()')[0]
            type = data[i].xpath('./td[5]/text()')[0]
            anon = data[i].xpath('./td[6]/text()')[0]
            lastcheck = data[i].xpath('./td[7]/text()')[0]
            print('第%s組數據IP:%s/Port:%s/國家:%s/速度:%s/類型:%s/匿名性:%s/最後檢查時間:%s' % (
                i+1, ip, port, country, speed, type, anon, lastcheck))
            # 將IP:port加入列表中
            proxiesdata = str(ip) + ':' + str(port)
            self.proxieslist.append(proxiesdata)

    def run(self):
        self.driver.get(self.url)

        # 剛連接網頁時會等五秒再轉向的javascript語法,需等待要抓的關鍵數據出現
        WebDriverWait(driver=self.driver, timeout=10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'proxy__t'))
        )
        source = self.driver.page_source
        self.parse_data(source)
        time.sleep(5)

        # 多頁切換頁面
        if self.currentpage < self.maxpage:
            try:
                for i in range(2, int(self.maxpage) + 1):
                    next_url = self.url + "&start={}".format((int(self.currentpage[0])) * 64)
                    self.driver.get(next_url)
                    WebDriverWait(driver=self.driver, timeout=10).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, 'proxy__t'))
                    )
                    source = self.driver.page_source
                    self.parse_data(source)
                    time.sleep(5)
            except Exception as e:
                print(e)

        print('proxieslist 共有 %s  組數據 : %s' % (len(self.proxieslist), self.proxieslist))
        self.driver.close()
        return self.proxieslist

if __name__ == '__main__':
    spider=FreeProxiesList()
    spider.run()