from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from settings import (
    CACHE_PROBLEMS_DIR,
    DIFFICULTY_CLASSES,
    LEETCODE_BASE_URL,
    PAGE_LOAD_WAIT_S,
)
import json
import logging
import os
import time

log = logging.getLogger(__name__)


def _scrape_from_web(title_slug: str) -> tuple[str, str]:
    """Scrape meta description and difficulty from LeetCode using Selenium."""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    try:
        driver.get(LEETCODE_BASE_URL + title_slug)
        time.sleep(PAGE_LOAD_WAIT_S)

        meta_tag = driver.find_element(By.NAME, "description")
        meta_content = meta_tag.get_attribute("content")

        difficulty = ""
        for class_name in DIFFICULTY_CLASSES:
            try:
                element = driver.find_element(By.CLASS_NAME, class_name)
                difficulty = element.get_attribute("innerHTML").strip()
                break
            except NoSuchElementException:
                continue
    finally:
        driver.quit()

    return meta_content, difficulty


def _parse_meta_content(meta_content: str) -> tuple[str, str, str, str]:
    """Extract title, description, raw example, and input from LeetCode meta content."""
    placeholder = "Can you solve this real interview question? "

    pos_dash = meta_content.find(" - ")
    pos_ex1 = meta_content.find("Example 1")
    pos_input = meta_content.find("Input")
    pos_output = meta_content.find("Output")

    if -1 in (pos_dash, pos_ex1, pos_input, pos_output):
        raise ValueError("Could not parse title, description, or example from page meta content.")

    pos_ex2 = meta_content.find("Example 2")
    if pos_ex2 == -1:
        pos_ex2 = len(meta_content) - 1

    title = meta_content[:pos_dash].replace(placeholder, "").strip()
    description = meta_content[pos_dash + 3:pos_ex1].rstrip().replace("\n", " ")
    example = meta_content[pos_input:pos_ex2].rstrip()
    inp = meta_content[pos_input + 5:pos_output].lstrip(":").strip()

    return title, description, example, inp


def scrape() -> tuple[str, str, str, str, str, int, str]:
    """Prompt the user for a problem slug and number, then scrape or load from cache.

    Returns:
        title, title_slug, description, example, example_dict, number, difficulty
    """
    title_slug = input("Title slug of the problem: ").strip()
    num = int(input("Problem number: "))

    cache_path = f"{CACHE_PROBLEMS_DIR}/{title_slug}.json"

    if os.path.exists(cache_path):
        log.info("Loading cached problem data from %s", cache_path)
        with open(cache_path, "r", encoding="utf-8") as f:
            cached = json.load(f)
        meta_content = cached["meta_content"]
        difficulty = cached["difficulty"]
    else:
        log.info("Scraping %s from LeetCode...", title_slug)
        meta_content, difficulty = _scrape_from_web(title_slug)
        os.makedirs(CACHE_PROBLEMS_DIR, exist_ok=True)
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump({"meta_content": meta_content, "difficulty": difficulty}, f, indent=4)
        log.info("Problem cached to %s", cache_path)

    title, description, example, _ = _parse_meta_content(meta_content)
    log.info("Loaded: %s (%s)", title, difficulty)

    return title, title_slug, description, example, example, num, difficulty
