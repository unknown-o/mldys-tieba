from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json,time,os

# 设置 Chrome WebDriver 的路径（根据实际情况修改）
CHROME_DRIVER_PATH = 'chromedriver.exe'

# 创建 Chrome WebDriver 的选项
chrome_options = Options()
#chrome_options.add_argument('--headless')  # 启用无头模式
chrome_options.add_argument('--disable-gpu')  # 禁用 GPU 加速
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=chrome_options)
cookie_string = ''

def cookie_str2dict(cookie_string):
    cookie = cookie_string.replace(" ", "").split(";")
    cookies = []
    for i in cookie:
        cookies.append({
            "name":i.split("=")[0],
            "value":i.split("=")[1],
            "path": "/"
        })
    return cookies

def cookies():
    for item in cookie_str2dict(cookie_string):
        driver.delete_all_cookies
        driver.add_cookie(item)
    driver.refresh()

driver.get("https://tieba.baidu.com/f?kw=%E8%BF%B7%E8%B7%AF%E7%9A%84%E7%89%99%E5%88%B7")

cookies()
def get_tieba_link(url = "https://tieba.baidu.com/f?kw=%E8%BF%B7%E8%B7%AF%E7%9A%84%E7%89%99%E5%88%B7"):
    driver.get(url)
    tieba_link = next_page_link = driver.find_elements(By.CLASS_NAME, "j_th_tit")
    links = []
    for item in tieba_link:
        if(item.get_attribute('href') == None):
            continue
        if('/p/' not in item.get_attribute('href')):
            continue
        links.append(item.get_attribute('href'))
    next_page_link = ""
    return links, ""

def take_screenshot(url):
    try:
        os.makedirs(os.path.basename(url))
    except:
        pass
    driver.get(url)
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    print(total_height)
    driver.set_window_size(1200, total_height)
    time.sleep(5)
    driver.save_screenshot(f'{os.path.basename(url)}/screenshot.png')
    with open(f'{os.path.basename(url)}/page-source.html', 'w',encoding="UTF-8") as f:
        f.write(driver.page_source)
    driver.set_window_size(1200,1200)

tieba_a = get_tieba_link(f"https://tieba.baidu.com/f?kw=%E8%BF%B7%E8%B7%AF%E7%9A%84%E7%89%99%E5%88%B7&ie=utf-8&pn=500")
print(tieba_a[0])
for j in tieba_a[0]:
    take_screenshot(j)
# print(take_screenshot("https://tieba.baidu.com/p/5331464580"))
# time.sleep(4000)









# 关闭浏览器
#driver.quit()
