# In this file i'm going to scrap image of appropriate dishes using bing image downloader

from bing_image_downloader import downloader # here is the being image downloader library which is used bing search engine
import pandas as pd
import os

data = pd.read_csv("cleaned_data.csv") # here i read clearned data frame
name = data.name # here i getting name of dishes

for n in name: # here i iterate through each dishes name with appropriate keyword
    path = "./image_dataset/" + n + " indian food"

    if os.path.exists(path): # here i check whether that image is already have in our file or not if it is than i will skip it
        continue
    query_string = n + " indian food" # here 's the query string, search string or name of the dishes with appropriate name
    downloader.download(query_string, limit=5, output_dir='static/image_dataset',
                        adult_filter_off=True, force_replace=False, timeout=60*5)
    # above downloader will download the image to dataset folder