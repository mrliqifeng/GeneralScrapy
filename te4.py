from selenium import webdriver
from selenium.webdriver.chrome.options import Options
print("启动动态引擎*********************")
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.set_page_load_timeout(1)
driver.get("https://nj.lianjia.com/ershoufang/103103451388.html")
print(driver.page_source)