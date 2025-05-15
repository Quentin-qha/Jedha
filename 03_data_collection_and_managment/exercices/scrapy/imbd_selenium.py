from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

# Setup
driver = webdriver.Chrome()
driver.get("https://www.imdb.com/chart/top/?ref_=nv_mv_250")

# Scroll (ou simule plusieurs pages si besoin)
movies_data = []

for i in range(20):  # faire 3 pages (tu peux augmenter)
    time.sleep(2)
    movies = driver.find_elements(By.CSS_SELECTOR, '.ipc-metadata-list')

    for movie in movies:
        try:
            title = movie.find_element(By.CSS_SELECTOR, '.ipc-title__text').text
            #url = movie.find_element(By.CSS_SELECTOR, '.ipc-title-link-wrapper').get_attribute('href')
            #rating = movie.find_element(By.CSS_SELECTOR, '.ipc-rating-star--rating').text
            #try:
                #votes = movie.find_element(By.CSS_SELECTOR, '.ipc-rating-star--voteCount').text
            #except:
                #votes = None

            movies_data.append({
                "title": title,
                #"url": url,
                #"rating": rating,
                #"nb_voters": votes
            })
        except:
            continue

    # Aller à la page suivante
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'a.lister-page-next')
        next_button.click()
    except:
        break

driver.quit()

# Sauvegarder
with open("01-Become_a_movie_director/imdb_all_movies_scroll.json", "w") as f:
    json.dump(movies_data, f, indent=2)
