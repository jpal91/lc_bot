from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Scrape:
    def __init__(self, url):
        self.title = ""
        self.file_name = ""
        self.driver = webdriver.Chrome("C:/Users/User1/OneDrive/Desktop/chromedriver")
        self.login(url)
        self.write_solution()
        self.write_readme(url)
        self.driver.close()
        return

    def login(self, url):
        self.driver.get(url)
        login = self.driver.find_element(By.CSS_SELECTOR, "input#id_login")
        login.send_keys("jpal91")
        password = self.driver.find_element(By.CSS_SELECTOR, "input#id_password")
        password.send_keys("Just!n21")
        self.driver.implicitly_wait(10)
        password.send_keys(Keys.RETURN)

    def copy(self):
        solution = self.driver.find_elements(By.CSS_SELECTOR, "div.ace_line_group")
        self.driver.implicitly_wait(10)
        return solution

    def write_solution(self):
        title = self.driver.find_element(By.CSS_SELECTOR, "h4 a.inline-wrap").text
        self.title = title
        title = title.lower().split(" ")
        title_text = "-".join(title)

        n = len(title_text)

        if n > 25:
            for i in range(24, -1, -1):
                if title_text[i] != "-":
                    continue
                else:
                    title_text = title_text[:i]
                    break

        text = self.copy()
        self.file_name = title_text + ".py"
        with open("../leetcode/Python/" + self.file_name, "w") as file:
            for t in text:
                file.write(t.text + '\n')

    def write_readme(self, url):
        with open("../leetcode/README.md", "a") as file:
            string = "\n|[{}](/Python/{})|[LC]({})||".format(
                self.title, self.file_name, url
            )
            file.write(string)


url = "https://leetcode.com/submissions/detail/830038320/"
drive = Scrape(url)
