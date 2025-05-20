from pygments import highlight
from pygments.lexers import CppLexer
from pygments.formatters import HtmlFormatter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

def export_img(cpp_code, title):
    print("Rendering code to image...")

    # Highlight the code with 2-space indentation
    formatter = HtmlFormatter(full=True, style='colorful', linenos=False, nowrap=False)
    highlighted_code = highlight(cpp_code, CppLexer(), formatter)

    # Add CSS for 2-space indentation and wrapping
    css = """
    <style>
    pre {
        white-space: pre-wrap;       /* CSS3 */
        white-space: -moz-pre-wrap;  /* Firefox */
        white-space: -pre-wrap;      /* Opera <7 */
        white-space: -o-pre-wrap;    /* Opera 7 */
        word-wrap: break-word;       /* IE */
        tab-size: 2;                 /* Set tab size to 2 spaces */
    }
    </style>
    """
    highlighted_code = css + highlighted_code

    # Save the highlighted code to an HTML file
    with open('cache/code.html', 'w') as f:
        f.write(highlighted_code)

    directory = 'cache/generated-img'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Configure Selenium options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize WebDriver with WebDriverManager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Load the HTML file
        driver.get(f"file://{os.getcwd()}/cache/code.html")

        # Set the window size
        driver.set_window_size(405, 720)

        # Take a screenshot of the page
        driver.save_screenshot(f"cache/generated-img/{title}.png")
        print(f"Code image saved as {title}.png")
    finally:
        # Quit the driver
        driver.quit()
        print("ChromeDriver stopped.")