from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

import time
import sys
import os
import ast
import json

# get problem
def scrape():
    title_slug = input("Title slug of the problem: ")
    num = int(input("# of the problem: "))

    file_path = f'cache/problems/{title_slug}.json'
    cache = ""
    meta_content = ""
    difficulty = ""
    if os.path.exists(file_path):
        # if problem was already scraped, then use it
        with open(file_path, 'r', encoding='utf-8') as f:
            cache = json.load(f)
        meta_content = cache["meta_content"]
        difficulty = cache["difficulty"]
    else:
        # scrape with Selenium
        defaultURL = "https://leetcode.com/problems/" + title_slug
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get(defaultURL)

        # wait for website fully loaded and extract information
        time.sleep(7)
        meta_tag = driver.find_element(By.NAME, 'description')
        meta_content = meta_tag.get_attribute('content')

        # get difficulty of the problem
        class_names = [
            "text-difficulty-easy",
            "text-difficulty-medium",
            "text-difficulty-hard"
        ]

        for class_name in class_names:
            try:
                difficulty_element = driver.find_element(By.CLASS_NAME, class_name)
                difficulty = difficulty_element.get_attribute('innerHTML').strip()
                break
            except NoSuchElementException:
                continue
    
        # save meta_content
        output = {}
        directory = 'cache/problems'
        if not os.path.exists(directory):
            os.makedirs(directory)

        output["meta_content"] = meta_content
        output["difficulty"] = difficulty
        with open(f'cache/problems/{title_slug}.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=4)

    # edit information
    placeholder = "Can you solve this real interview question? "
    pos1 = meta_content.find('-')
    pos2 = meta_content.find("Example 1")
    pos3 = meta_content.find("Input")
    pos4 = meta_content.find("Output")
    pos5 = meta_content.find("Explanation")
    pos6 = meta_content.find("Example 2")
    if pos6 == -1:
        pos6 = len(meta_content) - 1
    if pos1 == -1 or pos2 == -1 or pos3 == -1 or pos4 == -1:
        sys.exit("Title or description or example not found.")

    title = meta_content[:pos1-1].replace(placeholder, "")
    description = meta_content[pos1+2:pos2].rstrip().replace("\n", " ")
    inp = meta_content[pos3+5:pos4]
    if inp.startswith(':'):
        inp = inp[1:]
    inp = inp.strip()
    outp = ""
    if pos5 == -1:
        outp = meta_content[pos4+6:pos6]
    else:
        outp = meta_content[pos4+6:pos5]
    if outp.startswith(':'):
        outp = outp[1:]
    outp = outp.strip()
    example = meta_content[pos3:pos6].rstrip()

    # convert input into Python dictionary format
    # example = inp.replace(" = ", ":")
    # start = 0
    # end = -3
    # while start != 1:
    #     end = example.find(":", end + 3)
    #     example = example[:start] + "'" + example[start:end] + "'" + example[end:]
    #     start = example.find(", ", start + 1) + 2

    # # convert output into Python and append into dictionary
    # example = "{" + example + ", 'answer':" + outp + "}"
    print(example)
    dict_example = example
    # dict_example = ast.literal_eval(example)

    return title, title_slug, description, example, dict_example, num, difficulty


