import requests
from bs4 import BeautifulSoup
import re
import webbrowser
import tkinter as tk
from tkinter import messagebox
import threading

def download_and_process_pages():
    base_url = "https://www.olx.pl/oferty/q-Kia-Niro/?page="
    all_html_content = []
    page_number = 1
    while True:
        url = f"{base_url}{page_number}"
        response = requests.get(url)
        if response.status_code != 200:
            break
        all_html_content.append(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        next_button = soup.find("a", {"data-cy": "pagination-forward"})
        if not next_button:
            break
        page_number += 1

    combined_html_content = "\n".join(all_html_content)
    with open("combined_pages.html", "w", encoding="utf-8") as f:
        f.write(combined_html_content)

    combined_html_path = "combined_pages.html"
    offers_txt_path = "offers.txt"
    pattern = r'"http[^"]*/oferta/[^"]*"'
    matched_fragments = []
    with open(combined_html_path, "r", encoding="utf-8") as file:
        content = file.read()
        matches = re.findall(pattern, content)
        matched_fragments.extend(matches)

    with open(offers_txt_path, "w", encoding="utf-8") as file:
        for fragment in matched_fragments:
            file.write(f"{fragment}\n")

    remove_duplicates("offers.txt", "offers_unique.txt")

def remove_duplicates(input_file_path, output_file_path=None):
    seen_lines = set()
    with open(input_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    unique_lines = []
    for line in lines:
        if line not in seen_lines:
            seen_lines.add(line)
            unique_lines.append(line)
    if output_file_path is None:
        output_file_path = input_file_path
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.writelines(unique_lines)

def open_urls_with_brave(keyword):
    brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
    webbrowser.register('brave', None, webbrowser.BackgroundBrowser(brave_path))
    file_path = "offers_unique.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = file.readlines()
    urls = [url.strip().strip('"') for url in urls]
    opened_count = 0
    for url in urls:
        try:
            if keyword.lower() in url.lower():
                webbrowser.get('brave').open(url)
                opened_count += 1
        except Exception as e:
            print(f"Failed to open {url}: {e}")
    messagebox.showinfo("Search Complete", f"Opened {opened_count} URLs containing the keyword '{keyword}'")

def search_button_click():
    keyword = keyword_entry.get()
    if not keyword:
        messagebox.showerror("Error", "Please enter a keyword")
        return
    
    search_button.config(state=tk.DISABLED)
    status_label.config(text="Downloading and processing pages...")
    
    def search_thread():
        download_and_process_pages()
        open_urls_with_brave(keyword)
        search_button.config(state=tk.NORMAL)
        status_label.config(text="Ready")
    
    threading.Thread(target=search_thread, daemon=True).start()

root = tk.Tk()
root.title("OLX Search")
root.geometry("300x150")

keyword_label = tk.Label(root, text="Enter keyword:")
keyword_label.pack(pady=10)

keyword_entry = tk.Entry(root, width=30)
keyword_entry.pack()

search_button = tk.Button(root, text="Search", command=search_button_click)
search_button.pack(pady=10)

status_label = tk.Label(root, text="Ready")
status_label.pack()

root.mainloop()
