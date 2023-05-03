import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the Google Sheets API credentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)

# Define the URL of the Big Basket website
url = 'https://www.bigbasket.com/'

# Define a list of 5 categories to scrape from
categories = ['Fruits & Vegetables', 'Foodgrains, Oil & Masala', 'Bakery, Cakes & Dairy',
              'Beverages', 'Personal Care']

# Define a dictionary to store the scraped data
data = {'Category': [], 'Subcategory': [], 'Product': [], 'Price': [], 'Quantity': []}

# Set up the web driver (in this case, using Google Chrome)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Loop through each category and scrape 10 products from each subcategory
for category in categories:
    # Navigate to the category page on Big Basket
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'input'))).send_keys(category)
    driver.find_element(By.CLASS_NAME, 'btn.btn-default.bb-search-btn').click()
    time.sleep(5)
    
    # Get a list of all subcategories for the current category
    subcategories = driver.find_elements(By.XPATH, "//div[@class='uiv2-tool__option']/a")
    
    # Loop through each subcategory and scrape 10 products
    for subcategory in subcategories:
        # Navigate to the subcategory page on Big Basket
        subcategory_url = subcategory.get_attribute('href')
        driver.get(subcategory_url)
        time.sleep(5)
        
        # Get a list of all products for the current subcategory
        products = driver.find_elements(By.XPATH, "//div[@qa='product_name']")
        
        # Loop through each product and extract the relevant data
        for i in range(10):
            try:
                product_name = products[i].text
                product_price = driver.find_elements(By.XPATH, "//span[@qa='product_price']")[i*2+1]
                product_quantity = driver.find_elements(By.XPATH, "//span[@qa='product_price']")[i*2]
                
                # Add the data to the dictionary
                data['Category'].append(category)
                data['Subcategory'].append(subcategory.text)
                data['Product'].append(product_name)
                data['Price'].append(product_price.text)
                data['Quantity'].append(product_quantity.text)
            except:
                pass

# Create a new Google Sheet and add the data to it
sheet_name = 'Big Basket Sample Data'
sheet = client.create(sheet_name)
worksheet = sheet.add_worksheet(title='Data', rows=len(data), cols=len(data.keys()))
header = list(data.keys())
worksheet.insert_row(header, 1)
row = 2
for i in range(len(data['Category'])):
    values = list(data.values())
    worksheet.insert_row(values[i], row)
    row += 1

# Close the web driver
driver
