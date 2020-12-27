# this is a file in which all the behind the scene process work

# here i'm importing all the module which required
import pandas as pd
import pickle
import sklearn

# here i'm declaring global variable
data = None
model = None
model_data_frame = None

# here i'm loading usefule artifacts
def load_artifacts():
    global data, model, model_data_frame # here i'm using a global variable
    data = pd.read_csv("artifacts/cleaned_data.csv") # here i'm reading a cleaned data frame which was cleaned while data analysis and model building
    model_data_frame = pd.read_csv("artifacts/model_data.csv", index_col="name") # here i'm reading model_data file which is 0,1 matrics or categorical feature matrix or pivot table which is use to get a recommendation
    with open("artifacts/model.pickle", "rb") as f:
        model = pickle.load(f) # here i'm opening pickle file which have stored recommendation model

# here i'm returning dish and diet values
def get_dishes_name():
    global data # here i'm using a gloabl variable
    dishes_name = data.name.to_list() # here i'm getting a name of dish from data data frame
    diet_of_dishes = data.diet.to_list()  # here i'm getting diet of dish from data data frame
    return dishes_name, diet_of_dishes  # here i'm returning dish_name and diet of dishes

# here i'm returning diet wise dise diet can be vegetarian or non-vegetarian
def get_diet_wise_dishes(diet):
    global data # here i'm using global variable

    if diet == "vegetarian":
        df = data.loc[data.diet == diet, ["name", "diet"]] # here i'm getting those dish name which has vegetarian diet
        return df.name, df.diet
    elif diet == "non-vegetarian":
        df = data.loc[data.diet == diet, ["name", "diet"]] # here i'm getting those dish name which has non-vegetarian diet
        return df.name, df.diet
    else:
        return get_dishes_name() # here i'm getting all the dishes name

# here i'm returning state names
def get_state_name():
    global data # here i'm using global variable
    return list(data.state.unique()) # here i'm getting all the state name from data data frame

# here i'm returning a state wise dishes
def get_state_wise_dishes(state, diet):
    global data # here i'm using global variable
    verify_state = state in data.state.to_list() # here i'm verifying the state name
    if diet == "vegetarian" or diet == "non-vegetarian": # here i'm returning those dishes which have either vegetarian diet or non-vegetarian diet
        if verify_state: # if state is verified means state is in my record only then i will send a data according to state other wise i will send all data
            if state == "All State": # here if value of state is all state then i will send all data
                return get_diet_wise_dishes(diet)
            else: # other wise i will send a data base on state names
                df = data.loc[(data.state == state) & (data.diet == diet), ["name", "diet"]]
                return df.name, df.diet # here i'm returning name of dish and diet of dish
        else: # other wise i will return all state data base on diet
            return get_diet_wise_dishes(diet)
    else: # other wise i will send all data base on state not a diet
        if verify_state: # here if state is verified only then i will send a data base on state otherwise i will send all state data
            if state == "All State":
                return get_dishes_name()
            else:
                df = data.loc[data.state == state,["name", "diet"]]
                return df.name, df.diet
        else:
            return get_dishes_name()

# here i'm returning region wise dishes
def get_region_wise_dishes(region, diet):
    global data # here i'm using global variable
    verify_region = region.title() in data.region.to_list() # here i'm verifying region name
    if diet == "vegetarian" or diet == "non-vegetarian": # here i'm returning those dishes which have either vegetarian diet or non-vegetarian diet
        if verify_region: # if region is verified means region is in my record only then i will send a data according to region other wise i will send all data
            df = data.loc[(data.region == region.title()) & (data.diet == diet), ["name", "diet"]]
            return df.name, df.diet
        else:
            return get_diet_wise_dishes(diet)
    else:# other wise i will send all data base on region not a diet
        if verify_region:
            df = data.loc[data.region == region.title(), ["name", "diet"]]
            return df.name, df.diet
        else:
            return get_dishes_name()

# here i'm returning recipe id
def get_recipe(dish):
    global data # here i'm using global variable
    # here i'm returning unique youtube id of recipe of particular dish
    return data.loc[data.name == dish, ["recipe"]].values[0][0]

# here i'm generate recommendation base on particular dish
def get_recommendation(dish):
    global model, model_data_frame # here i'm using global variable

    X = model_data_frame[model_data_frame.index == dish] # here i'm getting a record of particular dish
    # here i put that record to my recommendation model and getting 13 recommended dish means n_neighbors = 13
    distance, cuisine_index = model.kneighbors(X, n_neighbors = 13)  # here model return two things distance and index of dishes which is index of model_data data frame

    recommendation_result = [] # here i will append recommendation result in this list
    for c in cuisine_index.flatten(): # here i'm converting 2D array to 1D array using flatten() method of numpy
        recommended_dish = model_data_frame.index[c] # here i'm getting index name of particular index and index name is basically dish name
        if recommended_dish == dish: # here if dish name is recommended_dish then i will ignore here
            continue
        recommendation_result.append(recommended_dish) # here i'm appending a result to list

    return recommendation_result[:12] # here i'm returning first 12 recommended dishes name

