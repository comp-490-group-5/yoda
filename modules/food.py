import random
import sys

if sys.version_info[0] >= 3:
    from urllib.parse import quote
else:
    from urllib import quote

import click
import requests

API_KEY = 'PssDzQz9vE51CseZKIKtUc76g-nFf5Xmv-Ha0_SGBowyEME0YNxG9iGMDsQ722rAPHLLupyUlMWHRdqaCCnrp-RAFLGVYIWfOAuB2Wn-5C0aR-1bnA5Csu4PGDCMXHYx'
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'


@click.group()
def food():
    """
    Food module... yum
    Suggest recipes for food, drinks, and restaurants
    """

@food.command()
def suggest_recipes():
    """
    Get a suggested recipe.
    """

    suggester("meals")

@food.command()
def suggest_drinks():
    """
    Get suggested a random drink recipe from the Cocktail DB API.
    """
    suggester("drinks")



@food.command()
def suggest_restaurant():
    """
    Get a suggested restaurant in your city.
    """
    if sys.version_info[0] >= 3:
        city = input('What city are you in? ')
        cuisine = input('What type of food are you interested in? ')
    else:
        city = raw_input('What city are you in? ')
        cuisine = raw_input('What type of food are you interested in? ')
    yelp_url = '{0}{1}'.format(API_HOST, quote(SEARCH_PATH.encode('utf8')))
    url_params = {
        'term': 'restaurant+' + cuisine,
        'categories': cuisine,
        'location': city.replace(' ', '+'),
        'limit': 50
    }
    req = requests.get(yelp_url, headers={'Authorization': 'Bearer ' + API_KEY}, params=url_params)
    if req.status_code == 200:
        parsed_response = req.json()
        businesses = parsed_response['businesses']
        if len(businesses) == 0:
            click.echo('Could not find any restaurants like that in your city :(')
        else:
            restaurant = random.choice(businesses)
            click.echo()
            click.echo("Why don't you try THIS restaurant tonight!")
            click.echo()
            click.echo(restaurant['name'] + ' on ' + restaurant['location']['address1'])
            click.echo('Book a table at ' + restaurant['phone'])
    else:
        click.echo('Could not process your request.')



def suggester(subjectAsString):
    """
    Get a suggested restaurant in your city.
    """

    if type(subjectAsString) != str:
        raise TypeError("subjectAsString must be of type string")

    if subjectAsString == 'meals':
        recipeRandomURL = "https://www.themealdb.com/api/json/v1/1/random.php"
        recipeLookupURL = "https://www.themealdb.com/api/json/v1/1/search.php?s="
        flavorString = "In need of a recipe you look. Hmmmmmmmm."
        JSONKey = "strMeal"
    elif subjectAsString == 'drinks':
        recipeRandomURL = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
        recipeLookupURL = "https://www.thecocktaildb.com/api/json/v1/1/search.php?s="
        flavorString = "Like you need a drink you look.  Hmmmmmm."
        JSONKey = "strDrink"
    else:
        raise ValueError("\'subjectAsString\' needs to be either \'meals\' or \'drinks\'")



    def getRecipeSuggestion():
        request = requests.get(recipeRandomURL)
        parsed_response = request.json()
        recipeInfoJSON = parsed_response[subjectAsString]
        recipeStr = recipeInfoJSON[0][JSONKey]

        click.echo(flavorString)
        click.echo("---------------------" + recipeStr + "---------------------")
        getIngredients(recipeStr)
        getRecipeInstructions(recipeStr)

    def getIngredients(recipeStr):
        request = requests.get(recipeLookupURL+recipeStr)
        parsed_response = request.json()
        recipeInfoJSON = parsed_response[subjectAsString]
        recipeInstructions = recipeInfoJSON[0]["strInstructions"]
        click.echo("Instructions: " + recipeInstructions)
    def getRecipeInstructions(recipeStr):
        request = requests.get(recipeLookupURL + recipeStr)
        parsed_response = request.json()
        recipeInfoJSON = parsed_response[subjectAsString]
        click.echo("Ingredients: ")
        for ingNumber in range(1, 16):
            ingredient = recipeInfoJSON[0]["strIngredient" + str(ingNumber)]
            qty = recipeInfoJSON[0]["strMeasure" + str(ingNumber)]
            if ingredient:
                if not qty:
                    output_str = "{} (as needed)".format(ingredient)
                else:
                    #
                    output_str = ingredient + ' ' + qty

                click.echo(output_str)
                recipeInfoJSON.append(ingredient)

    getRecipeSuggestion()

