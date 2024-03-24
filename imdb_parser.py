# importing required libraries
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# defining browser
options = Options()
options.add_experimental_option("detach", True)  # to leave the browser open
# options.add_argument("--headless=new")  # to make the browser invisible; delete it if needed
options.add_argument("--mute-audio")  # mute audio of the browser
driver = webdriver.Chrome(options=options)

url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'  # top 250 IMDB
driver.maximize_window()  # maximize the window
driver.get(url)  # open the URL
driver.implicitly_wait(20)  # maximum time to load the link

# finding all movies
movies = driver.find_elements(By.XPATH, "//*[contains(@class, 'ipc-title-link-wrapper')]")

data = []  # list, where data will be stored

# traversing through movies array
for index, movie in enumerate(movies):
    if index == 250:  # stop when number of movies reaches 250
        break
    try:  # handling page not loading and other cases
        movie_url = movie.get_attribute("href")

        # Open the movie link in a new tab
        driver.execute_script(f"window.open('{movie_url}', '_blank');")
        driver.implicitly_wait(10)

        # Switch to the newly opened tab
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)

        # Get information from the current page
        movie_name = driver.find_element(By.XPATH, "//*[contains(@class, 'hero__primary-text')]").text
        movie_summary = driver.find_element(By.XPATH, "//*[contains(@class, 'sc-466bb6c-3 fOUpWp')]").text

        # traverse through genres
        movie_genres = driver.find_elements(By.XPATH, "//*[contains(@class, 'ipc-chip__text')]")
        genre_list = []
        for genre in movie_genres:
            genre_list.append(genre.text)

        # store all data
        data.append({
            'movie_name': movie_name,
            'summary': movie_summary,
            'genre': genre_list
        })

        time.sleep(1)

        # Close the new tab
        driver.close()

        # Switch back to the main tab
        driver.switch_to.window(driver.window_handles[0])
    except:
        driver.close()

        # Switch back to the main tab or window
        driver.switch_to.window(driver.window_handles[0])

df = pd.DataFrame(data)  # creating a DataFrame
df.to_csv('movie_summary.csv')  # exporting

driver.quit()
