# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 13:01:02 2020

@author: OHyic
"""
#import selenium drivers
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#import helper libraries
import time
import urllib.request
import shutil
import os
import requests

class GoogleImageScraper():
    def __init__(self,webdriver_path,image_path, search_key="cat",number_of_images=1,headless=False):
        #check parameter types
        if (type(number_of_images)!=int):
            print("GoogleImageScraper Error: Number of images must be integer value.")
            return
        if not os.path.exists(image_path):
            print("GoogleImageScraper Notification: Image path not found. Creating a new folder.")
            os.makedirs(image_path)
        self.search_key = search_key
        self.number_of_images = number_of_images
        self.webdriver_path = webdriver_path
        self.image_path = image_path
        self.url = "https://www.google.com/search?q=%s&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_AUoAXoECBUQAw&biw=1920&bih=947"%(search_key)
        self.headless=headless
    def find_image_urls(self):
        """
            This function search and return a list of image urls based on the search key.
            Example:
                google_image_scraper = GoogleImageScraper("webdriver_path","image_path","search_key",number_of_photos)
                image_urls = google_image_scraper.find_image_urls()
                
        """
        options = Options()
        if(self.headless):
            options.add_argument('--headless')
        
        driver = webdriver.Chrome(self.webdriver_path, chrome_options=options)
        driver.get(self.url)
        time.sleep(5)
        image_urls=[]
        try:
            for indx in range (1,self.number_of_images+1):
                #find and click image
                imgurl = driver.find_element_by_xpath('//div//div//div//div//div//div//div//div//div//div[%s]//a[1]//div[1]//img[1]'%(str(indx)))
                imgurl.click()
                
                #select image from the popup
                time.sleep(3)
                images = driver.find_elements_by_class_name("n3VNCb")
                print(indx)
                for image in images:
                    
                    #only download images that ends with jpg/png/jpeg extensions
                    if (image.get_attribute("src")[-3:].lower() in ["jpg","png","jpeg"]):
                        print(image.get_attribute("src"))
                        image_urls.append(image.get_attribute("src"))
                        
                #scroll page to load next image
                driver.execute_script("window.scrollTo(0, "+str(indx*150)+");")
                time.sleep(3)
        except Exception:
            print("GoogleImageScraper Error: System Crashed. Returning saved image urls.")
            driver.close()
            return image_urls     
        
        driver.close()
        return image_urls
    
    def save_images(self,image_urls):
        #save images into file directory
        """
            This function takes in an array of image urls and save it into the prescribed image path/directory.
            Example:
                google_image_scraper = GoogleImageScraper("webdriver_path","image_path","search_key",number_of_photos)
                image_urls=["https://example_1.jpg","https://example_2.jpg"]
                google_image_scraper.save_images(image_urls)
                
        """
        for indx,image_url in enumerate(image_urls):
            try:
                filename = self.search_key+str(indx)+'.jpg'
                image_path = os.path.join(self.image_path, filename)
                image = requests.get(image_url)
                if image.status_code == 200:
                    with open(image_path, 'wb') as f:
                        f.write(image.content)
            except Exception:
                print("GoogleImageScraper Error: %s failed to be downloaded."%(image_url))
                pass
        print("GoogleImageScraper Notification: Download Completed.")
    

