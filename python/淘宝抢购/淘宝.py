from selenium import webdriver
from selenium.webdriver.chrome.service import Service
if __name__=='__main__':
    # s=Service(r"C:\Users\ChuZhk\Desktop\CZK\python\chromedriver.exe")
    # webdriver=webdriver.Chrome(service=s)
    webdriver = webdriver.Chrome(r"C:\Users\ChuZhk\AppData\Local\Chromium\Application\Chromium.exe")
    webdriver.get("https://www.taobao.com/")
