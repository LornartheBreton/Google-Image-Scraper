# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:02:06 2020

@author: OHyic

"""
# Import libraries
from GoogleImageScrapper import GoogleImageScraper
import os
import pandas as pd

df = pd.read_csv("./pueblosUTF.csv")

if __name__ == "__main__":
    # Define file pathn
    webdriver_path = os.path.normpath(os.getcwd() + "\\webdriver\\chromedriver.exe")
    image_path = os.path.normpath(os.getcwd() + "\\photos")

    # Add new search key into array ["cat","t-shirt","apple","orange","pear","fish"]
    pueblos = df["PUEBLO"]
    keywords = ["textil", "prenda", "telar"]

    # Parameters
    number_of_images = 5
    headless = False
    min_resolution = (0, 0)
    max_resolution = (9999, 9999)

    # Main program
    for pueblo in pueblos:
        for keyword in keywords:
            search_term = pueblo + " " + keyword
            save_path = image_path + "\\" + pueblo + "\\" + keyword
            image_scrapper = GoogleImageScraper(
                webdriver_path,
                image_path,
                search_term,
                number_of_images,
                headless,
                min_resolution,
                max_resolution,
            )
            image_urls = image_scrapper.find_image_urls()
            image_scrapper.save_images(image_urls)

    # Release resources
    del image_scrapper
