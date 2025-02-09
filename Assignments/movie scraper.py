from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import json

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()
URL = "https://www.imdb.com/search/title/?groups=top_250"
driver.get(URL)
time.sleep(2)

# List to store all movie details
movie_data = []

def close_popups(driver):
    """Close any popups that might appear on the page."""
    try:
        popup = driver.find_element(By.CSS_SELECTOR, "div[data-testid='promptable']")
        close_button = popup.find_element(By.CSS_SELECTOR, "svg.ipc-icon--clear")
        close_button.click()
        time.sleep(1)  
    except Exception:
        pass  

try:
    # Scrape movies from the current page
    while True:
        list_of_titles = driver.find_elements(By.CSS_SELECTOR, 'h3.ipc-title__text')
        list_of_ratings = driver.find_elements(By.CSS_SELECTOR, 'span.ipc-rating-star--rating')
        list_of_summaries = driver.find_elements(By.CSS_SELECTOR, 'div.ipc-html-content-inner-div')
        list_of_items = driver.find_elements(By.CSS_SELECTOR, 'span.sc-300a8231-7.eaXxft.dli-title-metadata-item')
        
        for i in range(len(list_of_titles)):
            # Extract title
            title = list_of_titles[i].text if i < len(list_of_titles) else "N/A"

            # Extract rating
            rating = list_of_ratings[i].text if i < len(list_of_ratings) else "N/A"

            # Extract summary
            summary = list_of_summaries[i].text if i < len(list_of_summaries) else "N/A"

            # Extract year and duration
            year, duration = "N/A", "N/A"
            for element in list_of_items:
                text = element.text
                if text.isdigit() and len(text) == 4:
                    year = text
                elif 'h' in text and 'm' in text:
                    duration = text

            # Click "More Info" button for genres and directors
            try:
                info_buttons = driver.find_elements(By.CSS_SELECTOR, "button.ipc-icon-button.dli-info-icon")
                if i < len(info_buttons):
                    info_button = info_buttons[i]
                    driver.execute_script("arguments[0].scrollIntoView(true);", info_button)
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ipc-icon-button.dli-info-icon"))
                    ).click()

                    # Extract genres
                    genre_elements = driver.find_elements(By.XPATH, "//ul[contains(@class, 'ipc-inline-list--show-dividers')]//li")
                    genre_list = [genre.text.strip() for genre in genre_elements]

                    # Extract directors
                    director_elements = driver.find_elements(By.XPATH, "//div[@data-testid='p_ct_dr']//a")
                    director_list = [director.text for director in director_elements]

                    # Close the modal
                    close_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.ipc-icon--clear"))
                    )
                    close_button.click()
                    time.sleep(1)  
                else:
                    genre_list = []
                    director_list = []

            except Exception as e:
                print(f"Error extracting genres/directors for movie {i + 1}: {e}")
                genre_list, director_list = [], []

            # Store all details in a dictionary
            movie = {
                "index": i + 1,
                "name": title,
                "duration": duration,
                "rating": rating,
                "release_year": year,
                "summary": summary,
                "genres": genre_list,
                "directors": director_list
            }
            movie_data.append(movie)

        # Move to the next page
        try:
            next_page_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.ipc-see-more__button'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
            next_page_button.click()
            time.sleep(random.uniform(3, 5))  
        except Exception as e:
            print(f"No next page or error: {e}")
            break  

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    driver.quit()

# Save the movie data to a JSON file
json_data = json.dumps(movie_data, indent=4)
with open("movies.json", "w") as outfile:
    outfile.write(json_data)

print("Scraping complete. Data saved to movies.json.")
