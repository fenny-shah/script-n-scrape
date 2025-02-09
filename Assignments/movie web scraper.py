from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

driver = webdriver.Chrome()
driver.maximize_window()
URL = "https://www.imdb.com/search/title/?groups=top_250"
driver.get(URL)
time.sleep(2)

movie_names = []
ratings = []
summaries = []
durations = []
years = []
genres = []
directors = []

def close_popups(driver):
    try:
        popup = driver.find_element(By.CSS_SELECTOR, "div[data-testid='promptable']")
        close_button = popup.find_element(By.CSS_SELECTOR, "svg.ipc-icon--clear")
        close_button.click()
        time.sleep(1)  
    except Exception:
        pass  

try:
    while True:
        list_of_titles = driver.find_elements(By.CSS_SELECTOR, 'h3.ipc-title__text')
        list_of_ratings = driver.find_elements(By.CSS_SELECTOR, 'span.ipc-rating-star--rating')
        list_of_summaries = driver.find_elements(By.CSS_SELECTOR, 'div.ipc-html-content-inner-div')
        list_of_items = driver.find_elements(By.CSS_SELECTOR, 'span.sc-300a8231-7.eaXxft.dli-title-metadata-item')
        list_of_genres = driver.find_elements(By.XPATH, "//ul[contains(@class, 'ipc-inline-list--show-dividers')]//li")
        list_of_directors = driver.find_elements(By.XPATH, "//div[@data-testid='p_ct_dr']//a")

        for title in list_of_titles:
            movie_names.append(title.text)
        for rating in list_of_ratings:
            ratings.append(rating.text)
        for summary in list_of_summaries:
            summaries.append(summary.text)
        for element in list_of_items:
            text = element.text
            if text.isdigit() and len(text) == 4:
                years.append(text)
            elif 'h' in text and 'm' in text:
                durations.append(text)

        try:
            next_page_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button.ipc-see-more__button'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
            time.sleep(1)  
            driver.execute_script("arguments[0].click();", next_page_button)
            time.sleep(random.uniform(3, 5))  
        except Exception as e:
            print(f"No next page or error: {e}")
            break  
    back_to_top_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Back to top']"))
    )
    back_to_top_button.click()
    time.sleep(random.uniform(1, 2)) 
    
    info_buttons = driver.find_elements(By.CSS_SELECTOR, "li-info-icon") 
    for movie_index in range(250):  
        try:
            
            close_popups(driver)
            if movie_index >= len(info_buttons):
                print(f"No 'More Info' button for movie {movie_index + 1}")
                continue

            info_button = info_buttons[movie_index]

            driver.execute_script("arguments[0].scrollIntoView(true);", info_button)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ipc-icon-button.dli-info-icon"))
            ).click()

            genre_elements = driver.find_elements(By.XPATH, "//ul[contains(@class, 'ipc-inline-list--show-dividers')]//li")
            genres.append([genre.text.strip() for genre in genre_elements])

            director_elements = driver.find_elements(By.XPATH, "//div[@data-testid='p_ct_dr']//a")
            directors.append([director.text for director in director_elements])

            close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "button[contains(@title, 'Close Prompt')]"))
            )
            close_button.click()
            time.sleep(1)  

        except Exception as e:
            print(f"Error with movie {movie_index + 1}: {e}")
            driver.refresh()  
            time.sleep(2)

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    driver.quit()
print("Movie Names:", movie_names)
print("Ratings:", ratings)
print("Summaries:", summaries)
print("Durations:", durations)
print("Years:", years)
print("Genres:", genres)
print("Directors:", directors)

import json
from textwrap import indent
from matplotlib.font_manager import json_dump

movie_data=[]
for i in range(len(movie_names)):
    movie = {
        "index" : i,
        "name" : movie_names[i],
        "duration" : durations[i],
        "rating" : ratings[i],
        "release_year" : years[i],
        "summary" : summaries[i],
    }
    movie_data.append(movie)

json_data = json.dumps(movie_data,indent=4)
with open("movies.json", "w") as outfile:
  outfile.write(json_data)
