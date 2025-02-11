import json
import requests
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options



URL = "https://www.imdb.com/search/title/?groups=top_100&sort=user_rating,desc"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
r = requests.get(URL, headers=headers)
soup = BeautifulSoup(r.content, 'html5lib')
movie_url = []
table = soup.find('ul', attrs = {'class':'ipc-metadata-list ipc-metadata-list--dividers-between sc-748571c8-0 gFCVNT detailed-list-view ipc-metadata-list--base'})
for row in table.find_all('div', attrs={'class': 'sc-300a8231-0 gTnHyA'}) :
    movie_url.append(row.a['href'])





options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors=yes')

driver = webdriver.Chrome(options=options)


movies = []


for movie in movie_url:
        
        url = str("https://www.imdb.com"+movie)
        print(url)
        driver.get(url)

        
        driver.implicitly_wait(10)

        
        film_name = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/h1/span').text
        film_year = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[1]/a').text
        film_duration = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[3]').text
        film_rating = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[1]/div/div[1]/a/span/div/div[2]/div[1]/span[1]').text
        film_genre = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[1]/div[2]/a[1]/span').text
        film_director = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[2]/div/ul/li[1]/div/ul/li/a').text
        film_main_star = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[2]/div/ul/li[3]/div/ul/li[1]/a').text
        film_plot = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/p/span[1]').text
        film_image = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[1]/div[1]/div/a').get_attribute('href')

        movies.append({
            'name': film_name,
            'year': film_year,
            'duration': film_duration,
            'rating': film_rating,
            'genre': film_genre,
            'director': film_director,
            'main_star': film_main_star,
            'plot': film_plot,
            'image': film_image
        })
         
driver.quit()
       


def write_to_json_file(file_name, data):
    with open(file_name, "w") as fp:
        json.dump(data, fp, indent=4)


file_name = "movies.json"
write_to_json_file(file_name, movies)

df = pd.read_json("movies.json")


df.to_csv("movies.csv", index=False, encoding="utf-8")
