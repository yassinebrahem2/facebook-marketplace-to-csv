from playwright.sync_api import sync_playwright
# The os library is used to get the environment variables.
import os
# The time library is used to add a delay to the script.
import time
# The BeautifulSoup library is used to parse the HTML.
from bs4 import BeautifulSoup
# For saving results in CSV format
import csv
# For generating random numbers and delays
import random
# For handling arrays and deduplication
import numpy as np

# Headers used for the CSV file
csv_headers = ['title', 'price', 'location', 'link', 'image']
# Facebook login credentials
EMAIL = "FACEBOOK_EMAIL_OR_PHONE_NUMBER_HERE"
PASSWORD = "FACEBOOK_PASSWORD_HERE"

# Declare the page variable globally for access across functions
page = None

# Sleep for a random time between a and b seconds
def randomTimeDelay(a, b):
    time.sleep(random.uniform(a, b))

# Log in to Facebook using the provided credentials
def loginFacebook():
    initial_url = "https://www.facebook.com/login/device-based/regular/login/"
    page.goto(initial_url)
    randomTimeDelay(3, 4)
    print("LOGGING IN")
    try:
        # Fill in email and password fields
        email_input = page.wait_for_selector('input[name="email"]').fill(EMAIL)
        password_input = page.wait_for_selector('input[name="pass"]').fill(PASSWORD)
        time.sleep(1)
        # Click the login button
        login_button = page.wait_for_selector('button[name="login"]').click()
        randomTimeDelay(5, 6)
        input("Press Enter To Start")
    except:
        # Return 1 if any error occurs during login
        return 1
    return 0

# Extracts product info from a single listing
def getItemListing(listing):
    try:
        # Get the item image URL
        image = listing.find('img', class_='x168nmei x13lgxp2 x5pf9jr xo71vjh xt7dq6l xl1xv1r x6ikm8r x10wlt62 xh8yej3')['src']
    except:
        image = ""
    try:
        # Get the item title
        title = str(listing.find('span', 'x1lliihq x6ikm8r x10wlt62 x1n2onr6').text)
        title = title.replace("\n", " ")
    except:
        title = ""
    try:
        # Get the item price
        price = listing.find('span', 'x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1tu3fi x3x7a5m x1lkfr7t x1lbecb7 x1s688f xzsf02u').text
    except:
        price = ""
    try:
        # Get the link to the item
        post_url = listing.find('a', class_='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xkrqix3 x1sur9pj x1s688f x1lku1pv')['href']
    except:
        post_url = ""
    try:
        # Get the location info of the item
        location = listing.find('span', 'x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft').text
    except:
        location = ""
    # Return all extracted data as a tuple
    return tuple(str(i) for i in (title, price, location, post_url, image))

# Parses listings on the current page and scrolls to load more
def getParsedItems(page, depth):
    parsed = []
    for i in range(depth):
        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')
        # Find all product listing elements
        listings = soup.find_all('div', class_='x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24')
        endReached = True
        for listing in listings:
            item = getItemListing(listing)
            if item != ('', '', '', '', ''):
                if not item in parsed:
                    endReached = False
                parsed.append(item)
        # If all listings are duplicates, stop early
        if endReached:
            break;
        # Scroll down to load more listings
        page.keyboard.press('End')
        randomTimeDelay(2, 3)
    # Return parsed items as a numpy array
    return np.array(list(parsed))

# Removes duplicate entries from a numpy array
def removeDuplicates(data):
    view = data.view(dtype=[('f{}'.format(i), data.dtype) for i in range(data.shape[1])]) 
    _, idx = np.unique(view, return_index=True)
    return data[idx]

# Main scraping function for marketplace
def crawlFacebookMarketplace(cities, queries, max_price, depth=10, isHeadless=True):
    global page

    # Start a Playwright session
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=isHeadless)  # Launch browser with GUI
        page = browser.new_page()
        randomTimeDelay(2, 3)
        loginFacebook()  # Log into Facebook
        data = np.empty((0, 5))  # Initialize empty data array
        print("FIND LISTINGS")
        for city in cities:
            for query in queries:
                # Build URL with city, search query and max price
                marketplace_url = f'https://www.facebook.com/marketplace/{city}/search/?query={query}&maxPrice={max_price}&sortBy=price_descend'
                print(f"CITY: {city}, QUERY: {query}, maxprice: {max_price}")
                page.goto(marketplace_url)
                randomTimeDelay(2, 4)
                items = getParsedItems(page, depth)
                data = np.vstack((data, items))  # Add new items to data array
        
        print("CLOSING BROWSER")
        browser.close()  # Close browser when done
    print(f"DATA LENGTH: {len(data)}")
    return data

# Save collected data to a CSV file
def saveProducts(data, filename):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = csv_headers
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)  # Write header row
            writer.writerows(data)       # Write item rows
    except Exception as e:
        print(f"Error saving data to CSV: {e}")

# Generate a unique filename to avoid overwriting existing files
def getUniqueFilename(base_name="Data", extension=".csv"):
    counter = 0
    while True:
        filename = f"{base_name}{counter}{extension}"
        if not os.path.exists(filename):
            return filename
        counter += 1

# Entry point of the script
def main():
    # List of Facebook marketplace city IDs or Name
    cities = ["New York, New York", "Philadelphia, Pennsylvania"]
    # Search queries to run
    queries = ["iphone 14 pro max", "iphone 15 pro max"]
    # Number of scrolls per query and city
    depth = 3
    # Maximum price for filtering
    price = "4000"
    # Whether to run the browser in headless mode (True = no UI, False = show browser)
    isHeadless = True

    # Perform the crawl
    data = crawlFacebookMarketplace(cities, queries, price, depth, isHeadless)
    # Get a unique filename
    filename = getUniqueFilename("data", ".csv")
    # Save the results
    saveProducts(data, filename)

# Run the script if it's executed directly
if __name__ == "__main__":
    main()