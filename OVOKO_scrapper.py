import re
import time
import random
import urllib.parse
import tkinter as tk
from tkinter import messagebox
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException

class CloudflareBypasser:
    def __init__(self, driver, max_retries=5):
        self.driver = driver
        self.max_retries = max_retries

    def bypass(self):
        for _ in range(self.max_retries):
            if self.is_cloudflare_challenge():
                self.solve_challenge()
            else:
                return True
        print("Failed to bypass Cloudflare challenge after maximum retries.")
        return False

    def is_cloudflare_challenge(self):
        return "cloudflare" in self.driver.title.lower() or "just a moment" in self.driver.title.lower()

    def solve_challenge(self):
        try:
            iframe = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='challenges']"))
            )
            self.driver.switch_to.frame(iframe)
            
            checkbox = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "cf-stage"))
            )
            
            self.move_mouse_to_element(checkbox)
            checkbox.click()
            
            self.driver.switch_to.default_content()
        except Exception as e:
            print(f"Error solving challenge: {e}")

    def move_mouse_to_element(self, element):
        action = uc.ActionChains(self.driver)
        action.move_to_element_with_offset(element, 5, 5)
        action.perform()

def setup_driver(brave_path):
    options = uc.ChromeOptions()
    options.binary_location = brave_path
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=VizDisplayCompositor")

    driver = uc.Chrome(options=options)
    return driver

def get_next_page_url(current_url, current_page):
    return current_url + str(current_page + 1) 

def scrape_links(url, output_file, brave_path, start_page=1, end_page=1000):
    driver = setup_driver(brave_path)
    bypasser = CloudflareBypasser(driver)
    
    try:
        all_links = set()
        for page_num in range(start_page, end_page + 1):
            print(page_num)
            if page_num == 1:
                page_url = url
            page_url = get_next_page_url(url, page_num - 1)
            driver.get(page_url)
            
            if not bypasser.bypass():
                continue
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
            )
            for attempt in range(3):   
                try:
                    links = driver.find_elements(By.TAG_NAME, "a")
                    for link in links:
                        href = link.get_attribute("href")
                        all_links.add(href)
                    break  
                except Exception as e:
                    break
            
    finally:
        driver.quit()

    with open(output_file, "a") as f:
            for link in all_links:
                print(link, file=f)

def cut(file_path, keyword):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return
    except IOError as e:
        print(f"Error reading the file {file_path}: {e}")
        return
    
    filtered_lines = [line for line in lines if keyword in line]
    seen = set()
    unique_lines = []
    for line in filtered_lines:
        if line not in seen:
            seen.add(line)
            unique_lines.append(line)

    try:
        with open(file_path, "w") as file:
            file.writelines(unique_lines)
    except IOError as e:
        print(f"Error writing to the file {file_path}: {e}")

def start_scraping():
    url = url_entry.get()
    brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    link_pattern = pattern_entry.get()
    output_file = output_file_entry.get()
    
    
    if not url or not link_pattern or not output_file or not brave_path:
        messagebox.showerror("Error", "All fields are required.")
        return

    try:
        scrape_links(url, output_file, brave_path, start_page=1, end_page=int(number_URLS.get()))
        cut(output_file, link_pattern)
        messagebox.showinfo("Complete", "Scraping and processing complete!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("Web Scraper")

tk.Label(root, text="URL:").grid(row=0, column=0, padx=10, pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Link Pattern:").grid(row=1, column=0, padx=10, pady=5)
pattern_entry = tk.Entry(root, width=50)
pattern_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Output File:").grid(row=2, column=0, padx=10, pady=5)
output_file_entry = tk.Entry(root, width=50)
output_file_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="N.o. URL's:").grid(row=3, column=0, padx=10, pady=5)
number_URLS = tk.Entry(root, width=50)
number_URLS.grid(row=3, column=1, padx=10, pady=5)

start_button = tk.Button(root, text="Start", command=start_scraping)
start_button.grid(row=4, column=1, padx=10, pady=10)

root.mainloop()
