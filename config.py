URL = 'https://congbothongtin.ssc.gov.vn/'
DRIVER_PATH = './chromedriver.exe'
DELAY = 10
FROM_DATE_XPATH = '/html/body/div[2]/form/div[3]/div[2]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div/div[1]/div/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/input'
TO_DATE_XPATH = '/html/body/div/form/div[3]/div[2]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div/div[1]/div/table/tbody/tr/td[2]/table/tbody/tr[4]/td[2]/input'
SEARCH_XPATH = '/html/body/div/form/div[3]/div[2]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div/div[1]/div/table/tbody/tr/td[3]/table/tbody/tr[3]/td[2]/span/div[1]/a'
LINKBCTCXPATH = '//*[@id="pt9:t1::db"]/table/tbody/tr[{index}]/td[2]/span/a'
NEXTXPATH = '/html/body/div/form/div[3]/div[2]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div/div[3]/div/div[5]/table/tbody/tr/td/table/tbody/tr/td[9]/a'

FILE_DOWNLOAD ='F:\CrawlerSSC\BCTC'
DOWNLOAD_XPATH ='/html/body/div[1]/form/div[2]/div[3]/div/div[1]/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/div/div/div[1]/div/table/tbody/tr/td/table/tbody/tr[3]/td[2]/div/div[2]/table/tbody/tr[5]/td[3]/span/div[2]/div[2]/span/a[1]'

TYPEBCTC_XPATH = '//*[@id="pt2:pt1::tabh::cbc"]/div[{index}]/div/div[1]/a'
SCROLLBCTC_XPATH = '/html/body/div[1]/form/div[2]/div[3]/div/div[1]/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div'
SCROLLBCTC_ID = 'pt2:pgl1s'

MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
MONGO_DATABASE = "BCTC"
MONGO_COLLECTION = "BCTC_collection"
