import os
import sys
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scrape:
    def __init__(self, user, pwd, drive_path):
        """
        Summary:
        The Scrape class initializes a Selenium Chrome browser interface to
        scrape submission information from LeetCode. Used in conjunction with
        my other project to record my LeetCode submissions.

        The class's primary methods will login, write a .py submission file from
        the LeetCode submission page, and append the solutions to the Markdown table
        of my README file within the target repository.

        For an example of how this would look. See the Python table @ https://github.com/jpal91/leetcode

        Parameters:
        user String: LeetCode username
        pws String: LeetCode password
        drive_path String: Absolute path to Chrome WebDriver on local stystem ex. C:/User/Programs/chromedriver

        Returns:
        None
        """

        self.title = ""
        self.file_name = ""
        self.challenge_url = ""
        self.user = user
        self.pwd = pwd
        self.drive_path = drive_path
        

    def login(self):
        """
        Summary:
        Logs into LeetCode using username and password and creates a WebDriver to be used when
        creating new submissions files.

        Parameters
        None

        Returns: None
        """
        self.driver = webdriver.Chrome(self.drive_path)
        self.driver.implicitly_wait(10)

        self.driver.get("https://leetcode.com/accounts/login/")

        login = self.driver.find_element(By.CSS_SELECTOR, "input#id_login")
        login.send_keys(self.user)

        password = self.driver.find_element(By.CSS_SELECTOR, "input#id_password")
        password.send_keys(self.pwd)

        password.send_keys(Keys.RETURN)

        # Waits until after the login redirect to continue
        # If credentials aren't correct, exit
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.url_changes(self.driver.current_url))
        except:
            self.close()
            sys.exit('Could not log in. Please check credentials and try again')
        return

    def _copy(self):
        """
        Summary
        Copies code from the submission to be used within the write_solution method

        Parameters: None

        Returns
        solution: A webdriver datatype that contains all of the text from the solution code box on the submission page
        """

        solution = self.driver.find_elements(By.CSS_SELECTOR, "div.ace_line_group")
        return solution

    def write_solution(self, url, sol_dir):
        """
        Summary
        Goes to the targetted submission page via the submission's url. Once there,
        it will take the proper title of the challenge (as the URL only has an id#) and
        assigns it to the self.title variable to add to the README, then creates a standard
        file name in lower-case joined by "-"

        A new file is then written to the targtted directory and the README is appended with
        the new solution infomration.

        Parameters

        url String: The target submission page on the LeetCode website Ex. https://leetcode.com/submissions/detail/8302286/
        sol_dir String: Absolute or relative path to the directory where the solution will be added Ex: C:/User/Project/Solutions/ or ../Solutions/

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
        text = self._copy()
        self.file_name = title_text + ".py"
        with open(sol_dir + self.file_name, "w") as file:
            for t in text:
                file.write(t.text + "\n")

    def write_readme(self, rm_path):
        """
        Summary
        Appends a new line to the end of the README in MD table format. The
        table has 3 rows - Solution, LeetCode (link to challenge), and Screenshot.
        This class appends the solution code from the solution page, a link to the
        file within the repository, and the challenge's url on LeetCode

        Parameters
        
        rm_path String: Absolute or relative path to the README file Ex: C:/Users/Project/README.md or ../README.md

        Returns: None
        """
        with open(rm_path, "a") as file:
            string = "\n|[{}](/Python/{})|[LC]({})||".format(
                self.title, self.file_name, self.challenge_url
            )
            file.write(string)

    def close(self):
        """
        Summary
        Closes the WebDriver once we're done with it.

        Paramters: None

        Returns: None
        """
        self.driver.close()
        return


if __name__ == "__main__":
    # pending.txt is used as a queue for new solutions that I've added
    # and want to include in the leetcode repository.
    #
    # The items are read off and the "queue" is cleared by writing over the file
    # The list created is then stripped of whitespace and given to the class
    # instance which will create a new WebDriver/Scrape instance and run each url
    # one by one until complete
    #
    # Environment Variables:
    # When running this program from the command line, a .env file can be present with the variables listed below.
    # This is optional and if not provided, you will be prompted to enter the required info before proceeding
    # USER: LeetCode username
    # PASSWORD: LeetCode password
    # DRIVE_PATH: Absolute path to the Chrome Webdriver
    # Q_PATH: An absolute or relative path to the "queue" (.txt file) that you will use to specify which solutions you want to be processed
    # RM_PATH: An absolute or relative path to the README.md file
    # SOL_PATH: An absolute or relative path to the directory which will have the new solution added

    check = input('Is your queue list up to date? -> y/n: ')

    if check != 'y':
        sys.exit('Update your queue!')

    load_dotenv()

    args = [
        os.getenv("USER"),
        os.getenv("PASSWORD"),
        os.getenv("DRIVE_PATH"),
        os.getenv("Q_PATH"),
        os.getenv("RM_PATH"),
        os.getenv("SOL_PATH")
    ]

    if not all(args):
        for i in range(6):
            if args[i]:
                continue

            match i:
                case 0:
                    args[0] = input('Enter LeetCode username ')
                case 1:
                    args[1] = input('Enter LeetCode password ')
                case 2:
                    args[2] = input('Enter absolute path to Chrome Webdriver ')
                case 3:
                    args[3] = input('Enter absolute or relative path to queue .txt file ')
                case 4:
                    args[4] = input('Enter absolute or relative path to README file ')
                case 5:
                    args[5] = input('Enter absolute or relative path to your solutions directory ')

    if not all(args):    
        sys.exit("Required env variables are not present. Please see https://github.com/jpal91/lc_bot for instructions.")

    with open(args[3], "r") as file:
        lines = file.readlines()
    with open(args[3], 'w') as file:
        file.write('')

    urls = [l.strip() for l in lines]

    drive = Scrape(args[0], args[1], args[2])

    drive.login()

    for url in urls:
        drive.write_solution(url, args[5])
        drive.write_readme(args[4])

    drive.close()
