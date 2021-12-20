# -*- coding: utf-8 -*-
"""
Script para scrapear imágenes de Google Images a partir de un CSV 
utilizando la librería GoogleImageScrapper encontrada en 
https://github.com/ohyicong/Google-Image-Scraper .

Para ejecutar este script, NECESITAS TENER INSTALADO
GOOGLE CHROME EN WINDOWS.
"""
# Import libraries
from GoogleImageScrapper import GoogleImageScraper
import os
import pandas as pd

### Function definition
def string_combination(list_a, list_b, separator=" "):
    """
    Takes 2 collections of strings.

    Returns a list of strings with all combinations between items in the collections.
    """
    list_to_return = []

    for term_a in list_a:
        for term_b in list_b:
            list_to_return.append(term_a + separator + term_b)
            list_to_return.append(term_b + separator + term_a)

    return list_to_return


def download_all_items_in_collection(
    collection,
    webdriver_path,
    image_path,
    number_of_images,
    headless,
    min_resolution,
    max_resolution,
    name_separator=None,
    fragmented_folders=False,
):
    """
    Takes a collection of strings.

    Downloads all items in collection.
    """
    for item in collection:
        search_term = item
        save_path = image_path

        if fragmented_folders:
            temp_list = item.split(name_separator)
            save_path = image_path + "\\" + temp_list[0] + "\\" + temp_list[1]
            del temp_list

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

    del image_scrapper


###

### Parameter definition
"""
SEARCH_ITEMS_CSV_PATH 
    Location of the csv file with the seach items.
KEYWORDS (List of Strings)
    List of keywords to generate the combinations with SEARCH_ITEMS_CSV_PATH collection (every element
    in the last one will be joined with the first one).
IMAGE_DIR_PATH (String)
    Directory where the scrapped images will be saved.
WEBDRIVER_PATH (String)
    Directory of the webdriver.
NUMBER_OF_IMAGES (Int)
    Number of images to download, per search term.
HEADLESS (Boolean)
    A weird-ass Chromium parameter. No idea what it does. Keep as False.
MIN_RESOLUTION (Tuple of ints)
    Minimmum resolution of the images to download.
MAX_RESOLUTION (Tuple of ints)
    Maximmum resolution fo the images to download.
"""
SEARCH_ITEMS_CSV_PATH = "./pueblosUTF.csv"
KEYWORDS = ["textil", "prenda", "telar"]
WEBDRIVER_PATH = os.path.normpath(os.getcwd() + "\\webdriver\\chromedriver.exe")
IMAGE_PATH = os.path.normpath(os.getcwd() + "\\photos")
NUMBER_OF_IMAGES = 5
HEADLESS = False
MIN_RESOLUTION = (0, 0)
MAX_RESOLUTION = (9999, 9999)
###

### Main program

print("Starting download")

df = pd.read_csv(SEARCH_ITEMS_CSV_PATH)
search_terms = df.iloc(0)
del df

search_terms = string_combination(search_terms, KEYWORDS)
download_all_items_in_collection(
    search_terms,
    WEBDRIVER_PATH,
    IMAGE_PATH,
    NUMBER_OF_IMAGES,
    HEADLESS,
    MIN_RESOLUTION,
    MAX_RESOLUTION,
    name_separator=" ",
    fragmented_folders=True,
)

print("All Done!")
###
