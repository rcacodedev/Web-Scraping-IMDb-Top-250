import csv
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

def scrape_imdb(url, item_selector):
    try:
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        items = soup.select(item_selector)

        if not items:
            print("No items found on the page.")
            return []

        print(f"Found {len(items)} items on the page.")

        data = []
        for item in items:
            title = item.select_one("h3[class*='ipc-title__text']")
            year = item.select_one("span[class*='cli-title-metadata-item']")

            if title and year:
                title_text = title.text.strip()
                year_text = year.text.strip("()") or "N/A"

                rating = item.select_one("span[class*='ratingGroup--imdb-rating']")
                rating_text = rating.text.strip() if rating else "N/A"

                item_data = {
                    "Title": title_text,
                    "Year": year_text,
                    "Rating": rating_text,
                }

                data.append(item_data)

        return data

    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return []

def export_data(data, filename, export_format):
    if export_format == "CSV":
        export_to_csv(data, filename)
    elif export_format == "JSON":
        export_to_json(data, filename)
    else:
        print("Invalid export format. Please choose either CSV or JSON.")

def export_to_csv(data, filename):
    if not data:
        print("No data to export.")
        return

    keys = data[0].keys()

    with open(f"{filename}.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

def export_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file, ensure_ascii=False, indent=4)

try:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    choice = input("Choose what type of TOP250 you want to watch (FILMS/TV)?: ").upper()
    if choice not in ["FILMS", "TV"]:
        print("Invalid choice. Please choose either FILMS or TV.")
        driver.quit()
        exit()

    export_format = input("Choose export format (CSV/JSON)?: ").upper()

    if export_format not in ["CSV", "JSON"]:
        print("Invalid export format. Please choose either CSV or JSON.")
        driver.quit()
        exit()

    if choice == "FILMS":
        url_films = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
        films_data = scrape_imdb(url_films, "div[class='sc-43986a27-0 gUQEVh cli-children']")
        export_data(films_data, "films_data", export_format)

    elif choice == "TV":
        url_tv = "https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250"
        tv_data = scrape_imdb(url_tv, "div[class='sc-43986a27-0 gUQEVh cli-children']")
        export_data(tv_data, "tv_data", export_format)

finally:
    driver.quit()
