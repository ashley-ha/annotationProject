import numpy as np
import pandas as pd
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from tqdm import tqdm
import warnings

warnings.filterwarnings("ignore")

# Enter your path to the chromedriver on your machine here
path = r"/Library/ChromeDriver/chromedriver_mac_arm64/chromedriver"
driver = webdriver.Chrome(path)


# Enter URL for the movie (make sure that you are under the "User Reviews" tab)
urls = ['https://www.imdb.com/title/tt0241527/reviews?ref_=tt_sa_3',
        'https://www.imdb.com/title/tt2527338/reviews/?ref_=tt_ql_2',
        'https://www.imdb.com/title/tt0372784/reviews/?ref_=tt_ql_2']
max_reviews_per_movie = 500

movie_titles = ['Harry Potter', 'Star Wars', 'Batman']

final_df = pd.DataFrame(columns=['Movie', 'Review'])

# Loop through the URLs and scrape the reviews for each movie. We need time.sleep() to allow the page to load properly
# and to avoid getting blocked by the website
for url, movie_title in zip(urls, movie_titles):
    time.sleep(1)
    driver.get(url)
    time.sleep(1)
    print(driver.title)
    time.sleep(1)
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    body.send_keys(Keys.PAGE_DOWN)

    sel = Selector(text=driver.page_source)
    review_counts = sel.css('.lister .header span::text').extract_first().replace(',', '').split(' ')[0]
    more_review_pages = int(min(int(review_counts), max_reviews_per_movie))

    for i in tqdm(range(more_review_pages)):
        try:
            css_selector = 'load-more-trigger'
            driver.find_element(By.ID, css_selector).click()

        except:
            pass

    review_list = []
    error_url_list = []
    error_msg_list = []
    reviews = driver.find_elements(By.CSS_SELECTOR, 'div.review-container')
    # Loop through the reviews and extract the text
    for d in tqdm(reviews[:max_reviews_per_movie - len(review_list)]):
        try:
            sel2 = Selector(text=d.get_attribute('innerHTML'))
            try:
                review = sel2.css('.text.show-more__control::text').extract_first()
            except:
                review = np.NaN

            review_list.append(review)

        except Exception as e:
            error_url_list.append(url)
            error_msg_list.append(e)
    # Create a dataframe for each movie and concatenate it with the final dataframe
    movie_df = pd.DataFrame({
        'Movie': movie_title,
        'Review': review_list,
    })

    final_df = pd.concat([final_df, movie_df], axis=0)

# Reset index and print the final dataframe
final_df = final_df.reset_index(drop=True)
print(final_df)
final_df.to_csv('reviews_to_annotate.csv', index=False)
