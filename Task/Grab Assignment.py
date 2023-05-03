from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Launch the Chrome browser with the Grab Food URL
driver = webdriver.Chrome()
driver.get("https://food.grab.com/ph/en/")

# Find the input box for location and enter a place in Manila
location_input = driver.find_element_by_xpath("//input[@placeholder='Enter your location']")
location_input.send_keys("Makati City")

# Wait for the page to load and for the search results to appear
wait = WebDriverWait(driver, 10)
search_results = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "searchResultContent")))

# Keep clicking the "Load More" button until all restaurants are displayed
while True:
    try:
        load_more_button = driver.find_element_by_xpath("//button[text()='Load More']")
        driver.execute_script("arguments[0].click();", load_more_button)
        wait.until(EC.staleness_of(load_more_button))
    except:
        break

# Find all the restaurants on the page and extract their latitude and longitude
restaurants = driver.find_elements_by_xpath("//div[@class='searchResult__itemWrapper']")
for restaurant in restaurants:
    name = restaurant.find_element_by_xpath(".//div[@class='name__1ISUI']")
    print(name.text)
    address = restaurant.find_element_by_xpath(".//div[@class='address__2P9RT']")
    print(address.text)
    latitude = restaurant.get_attribute("data-lat")
    print(latitude)
    longitude = restaurant.get_attribute("data-lng")
    print(longitude)
    print('\n')

# Close the browser
driver.quit()
