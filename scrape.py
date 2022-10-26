import asyncio
import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
load_dotenv()

class Scrape:
    def __init__(self):
        """
        Summary: 
        The Scrape class initializes a Selenium Chrome browser interface to
        scrape submission information from LeetCode. Used in conjunction with
        my other project to record my LeetCode submissions.

        The class's primary methods will login, write a .py submission file from
        the LeetCode submission page, and append the solutions to the Markdown table
        of my README file within the target repository

        Parameters:
        None

        Returns:
        None
        """
        
        self.title = ""
        self.file_name = ""
        self.challenge_url = ""
        self.driver = webdriver.Chrome(os.getenv('PATH'))
        self.driver.implicitly_wait(10)

    async def login(self):
        """
        Summary:
        Logs into LeetCode using username and password. The method is async to
        simulate some time needed to complete the login process on the LeetCode side
        before it proceeds to the individual submissions

        Parameters: None

        Returns: None
        """
        self.driver.get("https://leetcode.com/accounts/login/")
        login = self.driver.find_element(By.CSS_SELECTOR, "input#id_login")
        login.send_keys("jpal91")
        password = self.driver.find_element(By.CSS_SELECTOR, "input#id_password")
        password.send_keys(os.getenv('PASSWORD'))
        password.send_keys(Keys.RETURN)
        time.sleep(5)
        return

    def copy(self):
        """
        Summary:
        Copies code from the submission to be used within the write_solution method

        Parameters: None
        
        Returns: 
        solution: A webdriver datatype that contains all of the text from the solution code box on the submission page
        """
        
        solution = self.driver.find_elements(By.CSS_SELECTOR, "div.ace_line_group")
        return solution

    def write_solution(self, url):
        """
        Summary:
        Goes to the targetted submission page via the submission's url. Once there,
        it will take the proper title of the challenge (as the URL only has an id#) and
        assigns it to the self.title variable to add to the README, then creates a standard
        file name in lower-case joined by "-"

        A new file is then written to the targtted directory and the README is appended with 
        the new solution infomration.

        Parameters:
        url String: The target submission page on the LeetCode website

        Returns:
        None
        """
        self.driver.get(url)
        title = self.driver.find_element(By.CSS_SELECTOR, "h4 a.inline-wrap").text
        
        # Keeps the actual title of the challenge for use in the write_readme module
        # ex: "Two Sum"
        self.title = title

        # After, we move all letters to lowercase and join by "-" to use as a file name
        # ex: "two-sum"
        # Since this is also the same format of the challenge urls on leetcode, simply
        # use this newly created string as the direct link to the challenge page within the
        # write_readme method
        title = title.lower().split(" ")
        title_text = "-".join(title)
        self.challenge_url = "https://leetcode.com/problems/" + title_text

        # If the length is over 25 (arbitrary), we truncate the file name by moving backwards
        # through the string until we reach the next "-" to avoid slicing through a word
        # ex: "first-unique-character-in-a-string" -> "first-unique-character"
        n = len(title_text)

        if n > 25:
            for i in range(24, -1, -1):
                if title_text[i] != "-":
                    continue
                else:
                    title_text = title_text[:i]
                    break
        
        # copy() method is called to return the actual code text from the submission page
        # File name from above is joined by .py and written to a new file line by line 
        # to maintain formatting
        text = self.copy()
        self.file_name = title_text + ".py"
        with open("../leetcode/Python/" + self.file_name, "w") as file:
            for t in text:
                file.write(t.text + '\n')

    def write_readme(self):
        """
        Summary:
        Appends a new line to the end of the README in MD table format. The
        table has 3 rows - Solution, LeetCode (link to challenge), and Screenshot.
        This class appends the solution code from the solution page, a link to the
        file within the repository, and the challenge's url on LeetCode

        Parameters: None

        Returns: None
        """
        with open("../leetcode/README.md", "a") as file:
            string = "\n|[{}](/Python/{})|[LC]({})||".format(
                self.title, self.file_name, self.challenge_url
            )
            file.write(string)
    
    def close(self):
        """
        Summary:
        Closes the WebDriver once we're done with it.

        Paramters: None
        
        Returns: None
        """
        self.driver.close()
        return


if __name__ == '__main__':
    async def run_urls(urls):
        drive = Scrape()
        await drive.login()

        for url in urls:
            drive.write_solution(url)
            drive.write_readme()
        drive.close()
    
    # pending.txt is used as a queue for new solutions that I've added
    # and want to include in the leetcode repository.
    #
    # The items are read off and the "queue" is cleared by writing over the file
    # The list created is then stripped of whitespace and given to the run_urls
    # function which will create a new WebDriver/Scrape instance and run each url
    # one by one until complete

    with open('../leetcode/pending.txt', 'r') as file:
        lines = file.readlines()
    with open('../leetcode/pending.txt', 'w') as file:
        file.write('')
    asyncio.run(run_urls([l.strip() for l in lines]))