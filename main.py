from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
import re

chrome_options = Options()
chrome_options.add_argument("--lang=zh-CN")

# 创建一个Chrome浏览器实例
driver = webdriver.Chrome(options=chrome_options)


# driver.maximize_window()

class TmpMail:
    window = None
    email = None
    code = None
    refreshButton = None

    def __init__(self):
        driver.execute_script("window.open('https://mail.itcp.site/', '_blank');")

        self.window = driver.window_handles[-1]
        driver.switch_to.window(self.window)
        self.refreshButton = driver.find_element(By.CSS_SELECTOR, "#app > div > section > main > form > div > "
                                                                  "div.el-form-item__content > div.el-button-group > "
                                                                  "button:nth-child(1)")

    def getEmail(self):
        driver.switch_to.window(self.window)
        self.email = driver.find_element(By.CSS_SELECTOR, "#app > div > section > main > div:nth-child(3) > "
                                                          "div:nth-child(2) > span > span").text
        # print(self.email)
        return self.email

    def getCode(self):
        driver.switch_to.window(self.window)
        self.getEmail()
        match = False
        code = ""
        while not match:
            self.refreshButton.click()
            time.sleep(2)
            tbody = driver.find_element(By.CSS_SELECTOR, "#app > div > section > main > div:nth-child(4) > div > "
                                                         "div.el-table__inner-wrapper > div.el-table__body-wrapper > "
                                                         "div >"
                                                         "div.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default > "
                                                         "div >"
                                                         "table > tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                tds = row.find_elements(By.TAG_NAME, "td")
                for td in tds:
                    print(td.text)
                    match = re.match(r"联梦AI邮箱验证邮件", td.text)
                    if match:
                        row.find_element(By.TAG_NAME, "button").click()
                        print("进入邮件")
                        time.sleep(5)
                        emailBody = driver.find_element(By.CSS_SELECTOR, ".el-card__body")
                        code = emailBody.find_element(By.CSS_SELECTOR, "strong").text
                        break
                if match:
                    break
            if match:
                break

        button = driver.find_element(By.CSS_SELECTOR, "#el-drawer__title > button")
        button.click()

        button = driver.find_element(By.CSS_SELECTOR, "#app > div > section > main > form > div > "
                                                      "div.el-form-item__content > div.el-button-group > "
                                                      "button:nth-child(3)")
        button.click()
        return self.email, code


class OneApi:
    baseUrl = None
    window = None

    def __init__(self, baseUrl="https://ai.lra.cn"):
        self.baseUrl = baseUrl

    def register(self, email):
        if self.window is not None:
            driver.switch_to.window(self.window)
            driver.get(self.baseUrl + "/register")
        else:
            driver.execute_script("window.open('" + self.baseUrl + "/register', '_blank');")
            self.window = driver.window_handles[-1]
            driver.switch_to.window(self.window)

        time.sleep(10)

        inputData = driver.find_element(By.CSS_SELECTOR, "#root > div.ui.container.main-content > div > div > form")
        allInput = inputData.find_elements(By.TAG_NAME, "input")
        print(len(allInput))

        parts = email.split("@")
        username = parts[0] + "LMAPI"

        for i in allInput:
            i.send_keys(username)

        inputEmail = driver.find_element(By.CSS_SELECTOR, "#root > div.ui.container.main-content > div > div > form > "
                                                          "div >"
                                                          "div:nth-child(4) > div > input[type=email]")

        # 清空输入框内容
        inputEmail.send_keys(Keys.CONTROL + "a")  # 选中全部内容
        inputEmail.send_keys(Keys.BACKSPACE)  # 删除选中的内容

        inputEmail.send_keys(email)

        button = driver.find_element(By.CSS_SELECTOR, "#root > div.ui.container.main-content > div > div > form > div "
                                                      "> div:nth-child(4) > div > button")
        button.click()

        return username

    def putCode(self, code):
        driver.switch_to.window(self.window)
        inputCode = driver.find_element(By.CSS_SELECTOR, "#root > div.ui.container.main-content > div > div > form > "
                                                         "div >"
                                                         "div:nth-child(5) > div > input[type=text]")
        # 清空输入框内容
        inputCode.send_keys(Keys.CONTROL + "a")  # 选中全部内容
        inputCode.send_keys(Keys.BACKSPACE)  # 删除选中的内容
        inputCode.send_keys(code)

        button = driver.find_element(By.CSS_SELECTOR, "#root > div.ui.container.main-content > div > div > form > div "
                                                      "> button")
        button.click()
        time.sleep(5)

    def login(self, username, passwd):
        if self.window is not None:
            driver.switch_to.window(self.window)
            driver.get(self.baseUrl + "/login")
        else:
            driver.execute_script("window.open('" + self.baseUrl + "/login', '_blank');")
            self.window = driver.window_handles[-1]
            driver.switch_to.window(self.window)

        inputData = driver.find_element(By.CSS_SELECTOR, "#root > div.ui.container.main-content > div > div > form > "
                                                         "div > div:nth-child(1) > div > input[type=text]")
        inputData.send_keys(username)

        inputData = driver.find_element(By.CSS_SELECTOR, "#root > div.ui.container.main-content > div > div > form > "
                                                         "div > div:nth-child(2) > div > input[type=password]")
        inputData.send_keys(passwd)

        button = driver.find_element(By.CSS_SELECTOR, "#root > div.ui.container.main-content > div > div > form > div "
                                                      "> button")
        button.click()
        time.sleep(5)

    def get_key(self, name, token):
        if self.window is not None:
            driver.get(self.baseUrl + "/token/add")
        else:
            print("error: 未登录")
            return

        driver.switch_to.window(self.window)
        inputName = driver.find_element(By.CSS_SELECTOR, "#root > div.ui.container.main-content > div > form > "
                                                         "div:nth-child(1) > div > div > input[type=text]")
        inputName.send_keys(name)

        inputToken = driver.find_element(By.CSS_SELECTOR, "#root > div.ui.container.main-content > div > form > "
                                                          "div:nth-child(5) > div > div > input[type=number]")
        # 清空输入框内容
        inputToken.send_keys(Keys.CONTROL + "a")  # 选中全部内容
        inputToken.send_keys(Keys.BACKSPACE)  # 删除选中的内容
        inputToken.send_keys(token)

        button = driver.find_element(By.CSS_SELECTOR, "#root > div.ui.container.main-content > div > form > "
                                                      "button.ui.positive.button")
        button.click()

        driver.get(self.baseUrl + "/token")

        while True:
            time.sleep(10)
            tbody = driver.find_element(By.CSS_SELECTOR, "#root > div.ui.container.main-content > div > table > tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                tds = row.find_elements(By.TAG_NAME, "td")
                for td in tds:
                    if td.text == name:
                        # print("找到了")
                        button = row.find_element(By.CSS_SELECTOR, ".ui.small.positive.button")
                        button.click()
                        # 获取剪贴板内容
                        clipboard_content = pyperclip.paste()

                        # 打印剪贴板内容
                        print("key:" + clipboard_content)

                        # 获取当前网站的域名
                        domain = driver.execute_script("return document.domain")

                        # 删除指定域名下的所有Cookie
                        driver.delete_cookie(domain)

                        return clipboard_content


tmpMail = TmpMail()
oneApi = OneApi()

# email, code = tmpMail.getCode()
# print(email, code)

while True:
    email = tmpMail.getEmail()
    print(email)

    username = oneApi.register(email)

    email, code = tmpMail.getCode()
    print(email, code)
    oneApi.putCode(code)

    oneApi.login(username, username)
    key = oneApi.get_key("aaa", "100000")

    # time.sleep(5)
    # 打开文件以追加模式
    file_path = "example.txt"
    with open(file_path, "a") as file:
        # 追加一行内容
        line = email + "   " + username + "    " + username + "   " + key + "api地址:"+oneApi.baseUrl+"\n"
        file.write(line)

    time.sleep(10)
time.sleep(60)

# 关闭浏览器
driver.quit()
