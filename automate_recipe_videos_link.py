# this file is for fetching recipe video of particular dishes from youtube

from youtubesearchpython import SearchVideos # here i used this library
import pandas as pd

data = pd.read_csv("artifacts/cleaned_data.csv") # here i read csv file of cleaned data

if "recipe" not in data.columns:
    data["recipe"] = "empty" # here i created a recipe column with empty string

try:
    for i in range(data.shape[0]): # here is the for loop iterate through size of rows

        if data.loc[i, "recipe"] == "empty": # if there is unique id available then it's not going to run again
            dish = data.loc[i, "name"]   # here i get a name of dish base on index from loop

            # below i'm getting unique video id using keyword search which will be use later on for showing video on web app
            search = SearchVideos(dish + " indian recipe in english", offset = 1, mode = "dict", max_results = 1)
            print(i, dish) # here i print dish for confirmation

            # below i store a recipe video unique id to appropriate index
            data.loc[i, "recipe"] = search.result()["search_result"][0]["link"].split("=")[1]

            # here again save a csv file which contain all data and recipe's unique youtube id
            data.to_csv("artifacts/cleaned_data.csv", index = False)
except:
    print("----------------------------")
    print("API limit exceed try to run again.")
