# 📦 Facebook Marketplace to CSV

A Python script that automates scraping of listings from Facebook Marketplace using Playwright and BeautifulSoup. The script logs into Facebook, searches specified queries in selected cities, and extracts product info like title, price, location, image, and link — all saved in a CSV file.

## 🙏 Credits

This project is based on the work by **[Harminder Singh Nijjar](https://github.com/passivebot)**.  
Original repo: [facebook-marketplace-scraper](https://github.com/passivebot/facebook-marketplace-scraper)

---

## ⚙️ Features

- 🔐 Automated Facebook login
- 🔎 Search by multiple cities and queries
- 💰 Price filtering
- 📄 Extracts:
  - Title
  - Price
  - Location
  - Link
  - Image
- 📁 Saves data to a CSV file

## 📦 Requirements

- Python 3.7 or newer
- [Playwright](https://playwright.dev/python/)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- NumPy

### Install dependencies:

```bash
pip install -r requirements.txt
```

## 🧠 Usage
### 1.Set your Facebook credentials in the script:

```bash
EMAIL = "FACEBOOK_EMAIL_OR_PHONE_NUMBER_HERE"
PASSWORD = "FACEBOOK_PASSWORD_HERE"
```
### 2.Modify search settings in the main() function:
- cities: List of location names (e.g., ["New York, New York"])

- queries: Keywords to search (e.g., ["iphone 14 pro max"])

- price: Maximum price filter

- depth: How many scrolls/pages to load per query

- isHeadless: Set to False to see the browser in action

### 3.Run the script:

```bash
python main.py
```

### 4.A CSV file like data0.csv will be generated in the project folder.

## ⚠️ Disclaimer
This tool is for educational purposes only.
Scraping Facebook may violate their Terms of Service.
Use at your own risk.
