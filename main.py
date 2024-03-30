import json

from playwright.sync_api import Playwright, sync_playwright
from rich import print


def run(playwright: Playwright) -> None:
    start_url = "https://www.bhphotovideo.com/c/buy/Digital-Cameras/ci/9811/N/4288586282"
    # select chromium browser
    chrome = playwright.chromium
    # launch the chromium browser in headfull mode
    browser = chrome.launch(headless=False)
    # open a new page
    page = browser.new_page(color_scheme='dark')
    # navigate to the url
    page.goto(start_url)

    while True:
        # capture all links from te list page
        links = page.locator('a[data-selenium="miniProductPageProductNameLink"]').all()[:1]
        for link in links:
            # open new page for product page
            p = browser.new_page(base_url="https://www.bhphotovideo.com/")
            url = link.get_attribute('href')
            if url is not None:
                p.goto(url)  # navigate to the product page
            data = p.locator('script[type="application/ld+json"]').nth(1).text_content()
            json_data = json.loads(data)
            print(json_data["name"])
            p.close()
        # capture page number
        page_numbers = page.locator('span[class="paginationText"]').text_content()
        print("page_numbers:", page_numbers)
        if int(page_numbers[0] == page_numbers[2]):
            print("No more pages")
            break
        else:
            page.locator('a[data-selenium="listingPagingPageNext"]').click()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
