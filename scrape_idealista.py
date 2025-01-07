from util import json_write_file

average_price = "12,966 eur/m²"

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

# Set up the Selenium WebDriver (Make sure you have the appropriate driver installed)
# Replace 'chromedriver' with the path to your ChromeDriver executable if necessary
driver = uc.Chrome()

# URL to scrape
urls = ["https://www.idealista.it/en/aree/vendita-case/?shape=%28%28i%7EmtGi%60aw%40kk%40%3F%3Fi%7E%40rj%40bAVd%7C%40%29%29",
       "https://www.idealista.it/en/aree/vendita-case/lista-2?shape=%28%28i%7EmtGi%60aw%40kk%40%3F%3Fi%7E%40rj%40bAVd%7C%40%29%29",
       "https://www.idealista.it/en/aree/vendita-case/lista-3?shape=%28%28i%7EmtGi%60aw%40kk%40%3F%3Fi%7E%40rj%40bAVd%7C%40%29%29"]

properties = {}
for url in urls:
    # Open the webpage
    driver.get(url)

    # Wait for the page to load
    # Adjust time if the website takes longer to load
    time.sleep(5)

    # TODO for article tag with item as the class in it.
    articles = driver.find_elements(By.TAG_NAME, "article")
    for article in articles:
        if "adv" in article.get_attribute("class"):
            continue


        link = article.find_element(By.CLASS_NAME, "item-link")
        href = link.get_attribute("href")
        name = link.text

        # get class name item-price for price
        price = article.find_element(By.CLASS_NAME, "item-price").text.replace("€", "").replace(",", "")
        # from span item-detail-char get the second span item
        features = article.find_element(By.CLASS_NAME, "item-detail-char").find_elements(By.TAG_NAME, "span")

        rooms = features[0].text.replace(" rooms", "")
        square_footage = features[1].text.replace(" m²", "")
        floor = features[2].text

        print(price, square_footage, href)
        print(int(price) / int(square_footage), int(price), int(square_footage))
        price_footage = int(price) / int(square_footage)
        properties[href] = {"name": name, "price": price, "m2": square_footage, "price/m2": price_footage,
                            "rooms": rooms, "floor": floor, "href": href}


# Close the driver
driver.quit()

# Save hrefs to a JSON file
output_file = "properties.json"
json_write_file(output_file, properties)

print(f"Found {len(properties)} properties in '{output_file}'.")