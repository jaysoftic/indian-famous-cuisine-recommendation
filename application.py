from flask import Flask, request, render_template, redirect
from flask_jsglue import JSGlue # this is use for url_for() working inside javascript which is help us to navigate the url
import util
import difflib # for finding searching keyword which are closer to our dishes list

application = Flask(__name__)

# JSGlue is use for url_for() working inside javascript which is help us to navigate the url
jsglue = JSGlue() # create a object of JsGlue
jsglue.init_app(application) # and assign the app as a init app to the instance of JsGlue

util.load_artifacts() # this function is load some of the artifacts such as csv pickle etc

# here at initially i am getting dishes names bcz this dishes name will be send to web page and use it as a search suggestion
dishes, diet_of_dishes = util.get_dishes_name()
search_dishes = dishes # this search dish will be pass to the web app and this will help me to suggest a dishes to search box

# here is my home page route
@application.route("/")
def home():
    dishes, diet_of_dishes = util.get_dishes_name() # here i'm getting dishes names along with it's diet, diet can be veg or non veg

    # pagination logic
    total_pages = round(len(dishes) / 28) + 1
    dishes= dishes[0: 28]
    diet_of_dishes = ["all_diet"] * 28

    # here i zip two list and make a dictionary of dishes as key and diet of a that dishes as a value
    final_dishes = dict(zip(dishes, diet_of_dishes))

    return render_template("home.html", dishes = final_dishes, total_pages = total_pages, current_page = 1, page_type = "main", nav_active_home = "active", search_dishes = search_dishes)
    # dishes is a dish name and diet in the form of dict is pass to the web page
    # here total_pages is a total pages of records,
    # current_page is current requested page by client, page_type is indicates that which page is active like main page or diet page so it will help me to navigate a url according to that page
    # nav_active_home is used to activate a navbar of home tab basically is use for css purpose
    # search_dishes is a list of dishes is later on use on front end as a search box suggestion


# here is page route of home page
@application.route("/page/<int:pagenum>")
def page(pagenum):
    dishes, diet_of_dishes = util.get_dishes_name() # here i'm getting dishes names along with it's diet, diet can be veg or non veg

    # pagination logic
    total_pages = round(len(dishes) / 28) # here i divided total pages by 28 so i will show only 28 records per page
    reminder = len(dishes) % 28 # here find a module it will help me to add extra page, basically if reminder is 0 means i need to send even num records(28) and if it is 1 then i need to send odd num record(29)
    if reminder != 0:
        total_pages += 1 # if reminder is not 0 then i am increment a page

    dishes = dishes[28 * (pagenum - 1): 28 * pagenum] # here i slicing a records base on page num and 28 records
    # here i'm putting value as all_diet so it's basically mean that when user open site it show all diet data in gold color and when user click on veg or non veg it will show the data according to that and there will be shown either green or red color border
    diet_of_dishes = ["all_diet"] * len (dishes) # so this is a only page url that's why all type of diet dishes will show

    # here i zip two list and make a dictionary of dishes as key and diet of a that dishes as a value
    final_dishes = dict(zip(dishes, diet_of_dishes))

    return render_template("home.html", dishes = final_dishes, total_pages = total_pages, current_page = pagenum, page_type = "main" , nav_active_home = "active", search_dishes = search_dishes)
    # dishes is a dish name and diet in the form of dict is pass to the web page
    # here total_pages is a total pages of records,
    # current_page is current requested page by client, page_type is indicates that which page is active like main page or diet page so it will help me to navigate a url according to that page
    # nav_active_home is used to activate a navbar of home tab basically is use for css purpose
    # search_dishes is a list of dishes is later on use on front end as a search box suggestion


# here is a route of diet of dishes in home page url
@application.route("/diet", defaults = {"name": "all", "pagenum": 1})
@application.route("/diet/<name>", defaults = {"pagenum": 1})
@application.route("/diet/<name>/<int:pagenum>") # here i'm excpecting url as a diet diet name (veg or non veg) and page (page num)
def diet(name, pagenum):
    dishes, diet_of_dishes = util.get_diet_wise_dishes(name)  # here i'm getting dishes names along with it's diet according to diet it can be veg or non veg
    # pagination logic
    total_pages = round(len(dishes) / 28)
    reminder = len(dishes) % 28
    if reminder != 0:
        total_pages += 1

    dishes = dishes[28 * (pagenum - 1): 28 * pagenum]

    # here if the url request is given for vegetarian or non-vegetarian then it will return this data other wise it will return all dishes data
    if name == "vegetarian" or name == "non-vegetarian":
        diet_of_dishes = diet_of_dishes[28 * (pagenum - 1): 28 * pagenum]
    else:
        diet_of_dishes = ["all_diet"] * len(dishes)

    # here i zip two list and make a dictionary of dishes as key and diet of a that dishes as a value
    final_dishes = dict(zip(dishes, diet_of_dishes))

    return render_template("home.html", dishes=final_dishes, current_diet = name, total_pages = total_pages, current_page = pagenum, page_type = "diet", nav_active_home = "active", search_dishes = search_dishes)
    # dishes is a dish name and diet in the form of dict is pass to the web page
    # here total_pages is a total pages of records,
    # here current_diet means diet name which has been requested from client side it can be vegetarian or non-vegetarian
    # current_page is current requested page by client, page_type is indicates that which page is active like main page or diet page so it will help me to navigate a url according to that page
    # nav_active_home is used to activate a navbar of home tab basically is use for css purpose
    # search_dishes is a list of dishes is later on use on front end as a search box suggestion

# here is a route of state page
@application.route("/state", defaults = {"name": "Gujarat", "diet": "all", "pagenum": 1})
@application.route("/state/<name>", defaults = {"diet": "all","pagenum": 1})
@application.route("/state/<name>/<diet>", defaults = {"pagenum": 1})
@application.route("/state/<name>/<diet>/<int:pagenum>") # here it expect state, name of the state, diet of dish and page num
def state(name, diet, pagenum):
    state = util.get_state_name() # here i'm getting all the state name which is use to show at the front end side
    selected_state = name # here is selcted state name by default it is Gujarat
    dishes, diet_of_dishes = util.get_state_wise_dishes(name, diet) # here i'm getting dishes name and it's diets according to state name and diet

    # pagination logic
    total_pages = round(len(dishes) / 28)
    reminder = len(dishes) % 28
    if reminder != 0:
        total_pages+= 1

    dishes = dishes[28 * (pagenum - 1): 28 * pagenum]

    # here if the url request is given for vegetarian or non-vegetarian then it will return this data other wise it will return all dishes data
    if diet == "vegetarian" or diet == "non-vegetarian":
        diet_of_dishes = diet_of_dishes[28 * (pagenum - 1): 28 * pagenum]
    else:
        diet_of_dishes = ["all_diet"] * len(dishes)

    # here i zip two list and make a dictionary of dishes as key and diet of a that dishes as a value
    final_dishes = dict(zip(dishes, diet_of_dishes))

    return render_template("state.html", state = state, selected_state = selected_state, dishes = final_dishes, current_diet = diet, total_pages = total_pages, current_page = pagenum, nav_active_state = "active", search_dishes = search_dishes)
    # state is return state names, selected_state is a state which is selected by user
    # dishes is a dish name and diet in the form of dict is pass to the web page
    # here total_pages is a total pages of records,
    # here current_diet means diet name which has been requested from client side it can be vegetarian or non-vegetarian
    # current_page is current requested page by client
    # nav_active_state is used to activate a navbar of state tab basically is use for css purpose
    # search_dishes is a list of dishes is later on use on front end as a search box suggestion


# here is a route of region page
@application.route("/region", defaults = {"name": "all regions", "diet": "all", "pagenum": 1})
@application.route("/region/<name>", defaults = {"diet": "all", "pagenum": 1})
@application.route("/region/<name>/<diet>", defaults = {"pagenum": 1})
@application.route("/region/<name>/<diet>/<int:pagenum>") # it excpect a region, name of region, diet and page number
def region(name, diet, pagenum):
    selected_region = name # selected_region region which is selected by user
    dishes, diet_of_dishes = util.get_region_wise_dishes(name, diet) # here i'm getting dishes and it's diet according to region and diet arguments

    # pagination logic
    total_pages = round(len(dishes) / 28)
    reminder = len(dishes) % 28
    if reminder != 0:
        total_pages += 1

    dishes = dishes[28 * (pagenum - 1): 28 * pagenum]

    # here if the url request is given for vegetarian or non-vegetarian then it will return this data other wise it will return all dishes data
    if diet == "vegetarian" or diet == "non-vegetarian":
        diet_of_dishes = diet_of_dishes[28 * (pagenum - 1): 28 * pagenum]
    else:
        diet_of_dishes = ["all_diet"] * len(dishes)

    # here i zip two list and make a dictionary of dishes as key and diet of a that dishes as a value
    final_dishes = dict(zip(dishes, diet_of_dishes))

    return render_template("region.html", dishes = final_dishes, selected_region = selected_region, current_diet = diet, total_pages = total_pages, current_page = pagenum, nav_active_region = "active", search_dishes = search_dishes)
    # selected_region is return selected region name which was selected by user
    # dishes is a dish name and diet in the form of dict is pass to the web page
    # here total_pages is a total pages of records,
    # here current_diet means diet name which has been requested from client side it can be vegetarian or non-vegetarian
    # current_page is current requested page by client
    # nav_active_region is used to activate a navbar of region tab basically is use for css purpose
    # search_dishes is a list of dishes is later on use on front end as a search box suggestion

# here is route of recipe
@application.route("/recipe", defaults = {"name": "all"})
@application.route("/recipe/<name>") # it except a recipe and dish name of the recipe
def recipe(name):
    if name == "all": # here if dish name didn't get then by default it will be all and it will redirect to home page
        return redirect("/")
    name = name.lower() # here i convert dish name to lower case
    all_dishes = dishes # here i'm storing all dishes
    if name in all_dishes: # here i'm checking if the dish name in my records only then i will return recipe and recommendation for that dish
        recommended_dishes = util.get_recommendation(name) # here i'm getting recommendation for that dish
        recipe_id = util.get_recipe(name) # here i'm getting unique id of youtube recipe for particular dish

        return render_template("recipe.html", current_dish = name, recommended_dishes = recommended_dishes, recipe_id = recipe_id, search_dishes = search_dishes)
        # here current_dish is a request dish for recipe and recommendation
        # recommended_dishes is a recommendation dish for requested dish
        # recipe id is a unique id of youtube video regarding to recipe of particular dish
        # search_dishes is a list of dishes is later on use on front end as a search box suggestion

    return render_template("recipe.html") # if that condition is not satisfy then herr i will redirect to home page

# here is route of search functionality it expected search query argument from get request
@application.route("/search", methods = ["GET"])
def search():
    if request.method == "GET": # here if request is get only then below code work
        search_query = request.args.get("searchquery") # here is a search keyword or dish which will be getting from user side
        search_result = difflib.get_close_matches(search_query.lower(), search_dishes) # here i finding closest match of searchquery in my dishes list or records using difflib module of python
        if len(search_result) > 0: # if i found records in search result then below code work
            return render_template("search.html", dishes = search_result , search_dishes = search_dishes, current_search = search_query)
        else: # other wise it will show no record found message
            return render_template("search.html", dishes = search_result , search_dishes = search_dishes, current_search = search_query, no_record_found = True)
    else: # if i didn't get a GET request then i will redirect it to home page
        return redirect("/")

# here is route of 404 means page not found error
@application.errorhandler(404)
def page_not_found(e):
    # here i created my own 404 page which will be redirect when 404 error occured in this web app
    return render_template("404.html", search_dishes = search_dishes), 404

if __name__ == "__main__":
    application.run()