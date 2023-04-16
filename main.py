from tkinter import E
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import config
from time import sleep
from datetime import datetime 
from bs4 import BeautifulSoup 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pymongo
from selenium.webdriver.common.action_chains import ActionChains

class CrawlerSSC:
    #Khởi tạo đối tựơng 
    def __init__(self,date = datetime.now().strftime('%d/%m/%Y'), browser= None):
        self.date = date
        self.results = []
        self.browser = browser

    #chờ cho đến khi load xong footer thi chay tiep
    def wait(self, id):
        try:
            element_present = EC.presence_of_element_located((By.ID, id))
            WebDriverWait(self.browser, config.DELAY).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")

    # lay ra tong so bản ghi
    def getTotalRecord(self):
        sleep(config.DELAY)
        page_source = BeautifulSoup(self.browser.page_source, 'html.parser')
        totalRecords = page_source.find('span', id = 'pt9:it4').contents[0]
        total = int(totalRecords.split(':')[1])
        return total

    # lay dữ liệu từ table
    def extract_table(self, rows):
        final_list = [] 
        for tr in rows:
            intermediate_list = []
            for td in tr.findAll("td"):
                intermediate_list.append(td.findNext(text=True))
            final_list.append(intermediate_list)
        return final_list

    # lay dư liệu từ header
    def extract_header(self, source):
        headings = []
        for th in source[len(source)-1].contents:
            # get title
            title = th.find_all("span")[0].contents[0]#.find_all("div")[len(th.find_all("div"))-1]#.find_all("span")[0].contents[0]
            headings.append(title)
        return headings

    # gôp header với data
    def add_header_data(self, header ,data, type):
        ret = []
        for i in range(len(data)):
            result = {}
            if(type == 1):
                if self.date not in data[i][4]:
                    continue
            for j in range(len(header)):
                if header[j] != 'Tải về':
                    result[header[j]] = data[i][j]
            ret.append(result)
        return ret

    # 
    def getDataPage(self, page_source):
        table_th = page_source.find("table", attrs={"class": "x14z"})
        table_th_field = table_th.tbody.findChildren("tr", recursive = False)
        headings = self.extract_header(table_th_field)

        # print(headings)
        table_data = page_source.find("table", attrs={"class": "x14q"}) 
        rows = table_data.findAll('tr')
        # data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]
        data = self.extract_table(rows)
        
        return self.add_header_data(headings, data, 1)

    def getDataBCTC(self, page_source):
        ret = {}
        table = page_source.find_all("table", attrs={"class": "x14q"})
        table_field = table[0].tbody.findChildren("tr", recursive = False)
        for i in range(1, len(table_field)):
            tr = table_field[i]

        table_th = page_source.find("table", attrs={"class": "x14z"})
        table_th_field = table_th.tbody.findChildren("tr", recursive = False)

        # get header bctc
        headings = []
        for th in table_th_field[len(table_th_field)-1].contents:
            # get title
            title = th.find_all("div")[0].contents[0]#.find_all("div")[len(th.find_all("div"))-1]#.find_all("span")[0].contents[0]
            headings.append(title)
        # get data bctc
        
        rows = table[1].findAll('tr')
        data = self.extract_table(rows)
        bctc = self.add_header_data(headings, data, 2)
        return bctc

    def process(self):
        try:
            # truy cập trang web 
            self.browser.get(config.URL)
            #input search from date
            self.browser.find_element(By.XPATH, config.FROM_DATE_XPATH).send_keys(self.date)
            #input search to date
            self.browser.find_element(By.XPATH, config.TO_DATE_XPATH).send_keys(self.date)
            #click search submit
            WebDriverWait(self.browser,config.DELAY).until(EC.element_to_be_clickable((By.XPATH, config.SEARCH_XPATH))).click()
            # self.browser.find_element(By.XPATH, config.SEARCH_XPATH).click()
            #get number of records
            totalRecords = self.getTotalRecord()
            record = 0
            while True:
                page_source = BeautifulSoup(self.browser.page_source, 'html.parser')
                dataPage = self.getDataPage(page_source)
                lsSTT = [item["STT"] for item in dataPage]
                for i in range(len(lsSTT)):
                    #click next page
                    if i != 0 :
                        for x in range(record//15):
                            WebDriverWait(self.browser,config.DELAY).until(EC.element_to_be_clickable((By.XPATH, config.NEXTXPATH))).click()
                            sleep(1)
                    #click link get all page bctc 
                    WebDriverWait(self.browser,config.DELAY).until(EC.element_to_be_clickable((By.XPATH, config.LINKBCTCXPATH.format(index = (int(lsSTT[i]))-record)))).click()
                    #download bctc
                    # WebDriverWait(self.browser,config.DELAY).until(EC.element_to_be_clickable((By.XPATH, config.DOWNLOAD_XPATH))).click()
                    print("STT: " ,(i + record + 1))
                    for j in range(4):
                        if j != 0:
                            #click type of bctc
                            WebDriverWait(self.browser,config.DELAY).until(EC.element_to_be_clickable((By.XPATH, config.TYPEBCTC_XPATH.format(index= j+1)))).click()
                            sleep(2)
                        else:
                            # scroll div 
                            WebDriverWait(self.browser,config.DELAY).until(EC.element_to_be_clickable((By.XPATH, config.SCROLLBCTC_XPATH))).click()
                            target = self.browser.find_element(By.XPATH, config.SCROLLBCTC_XPATH)
                            ActionChains(self.browser).move_to_element(target).perform()
                            
                        #get data bctc
                        bctc_html = BeautifulSoup(self.browser.page_source, 'html.parser')
                        bctc = self.getDataBCTC(bctc_html)
                        if j == 0:
                            dataPage[i]["bcdkt"] = bctc
                        elif j == 1:
                            dataPage[i]["kqkd"] = bctc
                        elif j == 2:
                            dataPage[i]["lctt-tt"] = bctc
                        else:
                            dataPage[i]["lctt-gt"] = bctc
                        
                    #back to previous page with back()
                    self.browser.back()
                    #self.wait('pt9:footer')
                
                record += 15
                self.results.extend(dataPage)
                if(record > totalRecords):
                    break
                # next page
                for x in range(record//15):
                    WebDriverWait(self.browser,config.DELAY).until(EC.element_to_be_clickable((By.XPATH, config.NEXTXPATH))).click()
                sleep(config.DELAY)
                    # self.browser.find_element(By.XPATH, config.NEXTXPATH).click()
        except Exception as e:    
            print("Error: ", e)
        # Xóa driver và giai phong bộ nhớ
        self.browser.quit()
        # add data db
        self.addDB()

    def addDB(self):
        myclient = pymongo.MongoClient(config.MONGO_CONNECTION_STRING)

        mydb = myclient[config.MONGO_DATABASE]
        mycol = mydb[config.MONGO_COLLECTION]
        x = mycol.insert_many(self.results)

        #print list of the _id values of the inserted documents:
        print(x.inserted_ids)
        pass
        

def main():
    # Khởi tạo webdriver
    options = Options()
    # open gui 
    options.headless = False
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920,1200")
    options.add_argument("start-maximized")
    # download directory
    options.add_experimental_option("prefs", {
        "download.default_directory": config.FILE_DOWNLOAD,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
    })
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options= options,executable_path=config.DRIVER_PATH)
    crawler = CrawlerSSC(date = '05/09/2022', browser= browser)
    crawler.process()
    del crawler
    

if __name__ == '__main__':
    main()