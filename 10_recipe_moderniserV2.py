# modules to be used...

import csv
import re


# ****** Functions ******

def not_blank(question, error_msg, num_ok):
    error = error_msg

    valid = False
    while not valid:
        response = input(question)
        has_errors = ""

        if num_ok != "yes":
            # look at each character in string and if it's a number, complain
            for letter in response:
                if letter.isdigit() == True:
                    has_errors = "yes"
                    break

        if response == "":
            print(error)
            continue
        elif has_errors != "":
            print(error)
            continue
        else:
            return response


# Number check function (number must be a float that is more than 0)
def num_check(question):
    error = "Please enter a number that is more than zero"

    valid = False
    while not valid:
        response = input(question)

        if response.lower() == "xxx":
            return "xxx"

        else:
            try:
                response = float(reponse)
                if response <= 0:
                    print(error)
                else:

                    return response

            except ValueError:
                print(error)


def get_sf():
    serving_size = num_check("What is the recipe serving size?  ")

    # Main Routine goes here
    dodgy_sf = "yes"
    while dodgy_sf == "yes":

        desired_size = num_check("How many servings are needed? ")

        scale_factor_ = desired_size / serving_size

        if scale_factor_ < 0.25:
            dodgy_sf = input("Warning: this scale factor is very small and you"
                             "might struggle to accurately weigh the ingredients.  \n"
                             "Do you want to fix this and make more servings? ").lower()
        elif scale_factor_ > 4:
            dodgy_sf = input("Warning: This scale factor is quite large - "
                             "you might have issues with mixing bowl volumes and oven space. "
                             "\ndo you want to fix this and make a smaller batch? ").lower()
        else:
            dodgy_sf = "no"

    return scale_factor_


# Function to get (and check amount, unit and ingredient)
def get_all_ingredients():
    all_ingredients = []

    stop = ""
    print("Please enter ingredients one line at a time. press 'xxx' to when "
          "you are done.")
    while stop != "xxx":
        # Ask user for ingredient (via not blank function)
        get_recipe_line = not_blank("Recipe Line: ",
                                    "This can't be blank",
                                    "yes")

        # Stop looping if exit code is typed and there are more
        # than 2 ingredients...
        if get_recipe_line.lower() == "xxx" and len(all_ingredients) > 1:
            break

        elif get_recipe_line.lower() == "xxx" and len(all_ingredients) < 2:
            print("You need at least two ingredients in the list.  "
                  "Please add more ingredients.")

        # If exit code is not entered, add ingredient to list
        else:
            all_ingredients.append(get_recipe_line)

    return all_ingredients


# Conversion Function...


# Functions go here
def general_converter(how_much, lookup, dictionary, conversion_factor):
    if lookup in dictionary:
        mult_by = dictionary.get(lookup)
        how_much = how_much * float(mult_by) / conversion_factor
        converted = "yes"

    else:
        converted = "no"

    return [how_much, converted]


def unit_checker(unit_to_check):

    # abbreviations lists
    teaspoon = ["tsp", "teaspoon", "t", "teaspoons"]
    tablespoon = ["tbs", "tablespoon", "T", "tbsp", "tablespoons"]
    cup = ["c", "C", "cup", "CUP", "cups"]
    ounce = ["ounce", "OZ", "ounces"]
    pint = ["pint, pt", "P", "pints"]
    quart = ["qt", "q", "quart", "quarts"]
    pound = ["lb", "pound", "pounds"]
    litre = ["L", "litre", "litres"]
    grams = ["g", "gram", "grams"]
    milliliter = ["mls", "ml", "millimetre", "millimeter"]

    if unit_to_check == "":
        print("you chose {}".format(unit_to_check))
        return unit_to_check

    elif unit_to_check.lower() in grams:
        return "g"
    elif unit_to_check == "T" or unit_to_check.lower() in tablespoon:
        return "tbs"
    elif unit_to_check.lower() in teaspoon:
        return "tsp"
    elif unit_to_check.lower() in cup:
        return "cup"
    elif unit_to_check.lower() in ounce:
        return "ounce"
    elif unit_to_check.lower() in pint:
        return "pint"
    elif unit_to_check.lower() in quart:
        return "pint"
    elif unit_to_check.lower in pound:
        return "pound"
    elif unit_to_check.lower() in litre:
        return "litre"
    elif unit_to_check.lower() in milliliter:
        return "milliliter"
    else:
        return unit_to_check


# Main routine goes here

# dictionaries go here
unit_central = {
    "ml": 1,
    "tsp": 5,
    "tbs": 15,
    "cup": 237,
    "ounce": 28.35,
    "pint": 473,
    "quart": 946,
    "pound": 454,
    "litre": 1000,
}

# Generate Food dictionary
# open file
groceries = open('01_ingredients_ml_to_g.csv')

# Read data into a list
csv_groceries = csv.reader(groceries)

# Create a dictionary to hold the data
food_dictionary = {}

# Add the data from the list into the dictionary
# (first item in row is key, next is definition)

for row in csv_groceries:
    food_dictionary[row[0]] = row[1]

# print(food_dictionary)

# Get items etc

# set up list to hold 'modernised ingredients
modernised_recipe = []
# Ask user for recipe name and check its not blank
recipe_name = not_blank("What is the recipe name? ",
                        "The recipe name can't be blank and cant contain numbers, ",
                        "no")
# Ask user where the recipe is originally from
source = not_blank("Where is the recipe from?",
                   "The recipe source can't be blank",
                   "yes")

# Get serving sizes and scale factor
scale_factor = get_sf()

# Get amounts, units and ingredients from user...
full_recipe = get_all_ingredients()

# Spilt each line of the recipe into amount, unit and ingredient...
mixed_regex = "\d{1,3}\s\d{1,3}\/\d{1,3}"

for recipe_line in full_recipe:
    recipe_line = recipe_line.strip()
    # Get Amount...
    if re.match(mixed_regex, recipe_line):

        # Get mixed number by matching the regex
        pre_mixed_num = re.match(mixed_regex, recipe_line)
        mixed_num = pre_mixed_num.group()

        # Replace space with a + sign
        amount = mixed_num.replace(" ", "+")
        # Change the string into a decimal
        amount = eval(amount)
        amount = amount * scale_factor

        # Get unit and ingredient...
        compile_regex = re.compile(mixed_regex)
        unit_ingredient = re.split(compile_regex, recipe_line)
        unit_ingredient = (unit_ingredient[1]).strip()  # remove extra white space from unit

    else:
        get_amount = recipe_line.split(" ", 1)  # spilt line at first space

        try:
            amount = eval(get_amount[0])  # convert amount to float if possible
            amount = amount * scale_factor
        except NameError:
            amount = get_amount[0]
            modernised_recipe.append(recipe_line)
            continue

        unit_ingredient = get_amount[1]

    get_unit = unit_ingredient.split(" ", 1)  # Splits text at first space

    unit = get_unit[0]
    # convert in ml
    num_spaces = recipe_line.count(" ")
    if num_spaces > 1:
        # item has unit and ingredient
        unit = get_unit[0]
        ingredient = get_unit[1]
        unit = unit_checker(unit)
        # convert in g

        # if unit is already in grams, add it to list
        if unit == "g":
            modernised_recipe.append("{:.0f} g {}".format(amount, ingredient))
            continue

        # convert to mls if possible...
        amount = general_converter(amount, unit, unit_central, 1)

        # If we're in mls try to convert to grams
        if amount[1] == "yes":
            amount_2 = general_converter(amount[0], ingredient, food_dictionary, 250)

            # if the ingredient is in the list, convert it
            if amount_2[1] == "yes":
                modernised_recipe.append("(:.0f) g ()". format(amount_2[0], ingredient))
            # if the ingredient is not in the list, leave the unit as ml
            else:
                modernised_recipe.append("{:.0f} {}".format(amount, unit_ingredient))
                continue


    # Item only has ingredient (no unit)
    else:
        modernised_recipe.append("{:.0f} {}".format(amount, unit_ingredient))



# put updated ingredient in list

print()
print()
print("**** () ****".format(recipe_name))
print("Source: {}".format(source))
print()

# output ingredient list
for item in modernised_recipe:
    print(item)


