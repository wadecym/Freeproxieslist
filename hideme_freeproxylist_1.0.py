'''
作者 : wade chen
測試日期 : 2019/3/8
'''
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class FreeProxiesList():
    def __init__(self):
        # 設定chromedriver路徑
        driver_path = r'D:\chromedriver\chromedriver.exe'
        self.driver = webdriver.Chrome(driver_path)
        # country=國家代碼,多選國家代碼直接連在一起(ex:日本台灣美國); type=類型代碼直接連在一起(http:h,https:s); anon=匿名性(higeh:4)
        self.url = 'https://hidemyna.me/en/proxy-list/?country=JPTWUS&type=hs&anon=4'
        self.proxieslist=[]

    def run(self):
        self.driver.get(self.url)
        # 剛連接網頁時會等五秒再轉向的javascript語法,需等待要抓的關鍵數據出現
        element = WebDriverWait(driver=self.driver, timeout=10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'proxy__t'))
        )
        source = self.driver.page_source
        self.parse_data(source)

        print('self.proxieslist :',self.proxieslist)
        return self.proxieslist

    def parse_data(self,source):
        html = etree.HTML(source)
        data = html.xpath('//table[@class="proxy__t"]/tbody/tr')

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

            proxiesdata = str(ip) + ':' + str(port)
            self.proxieslist.append(proxiesdata)


if __name__ == '__main__':
    spider=FreeProxiesList()
    spider.run()