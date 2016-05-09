import bs4 as BeautifulSoup
import urllib
from urllib import request
import os.path


class RecipeParse(object):
    def __init__(self, url):
        self.url = url
        self.soup = self.lets_get_soup()
        self.title = ''
        self.img_url = ''
        self.recipe_yield = ''
        self.ingredients = {}
        self.instructions = []

    def __str__(self):
        ingredients_table = ''
        instruction_list = ''

        for ingredient, amount in self.ingredients.items():
            ingredients_table += "|" + ''.join(amount) + "|" + \
                                 ingredient + "|\n"

        for step in self.instructions:
            instruction_list += "\n\n* " + step

        return "#[{}]({})\n![alt text]({})\n###Ingredients\n|Quantity|Ingredient|" \
               "\n----------:|:-------\n{}\n###Instructions{}".format(
            self.title, self.url, self.img_url, ingredients_table, instruction_list
        )

    def lets_get_soup(self):
        """
        Gets BeautifulSoup object from url
        :return: False or BeautifulSoup object
        """
        try:
            # pretend to be Firefox
            req = urllib.request.Request(self.url,
                                         headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as url_file:
                url_byte = url_file.read()
        except urllib.request.HTTPError as e:  # HTTP status code
            print(e.__str__())
            return False
        except urllib.request.URLError as e:  # General Error
            print(e.__str__())
            return False
        except urllib.error.ContentTooShortError as e:
            # not all data retrieved
            print(e.__str__())
            return False
        except OSError as e:  # Vauge Error
            print(e.__str__())
            return False
        except Exception as e:  # Anything
            print(e.__str__())
            return False

        try:
            url_string = url_byte.decode('UTF-8')
        except UnicodeDecodeError as e:
            print(e.__str__())
            return False
        except Exception as e:
            print(e.__str__())
            return False
        return BeautifulSoup.BeautifulSoup(url_string, "html.parser")

    def set_recipe_title(self):
        """
        Gets recipe title from recipe
        :return: None
        """

    def set_recipe_img(self):
        """
        Sets recipe image using url
        :return: None
        """

    def set_recipe_yield(self):
        """
        Gets recipe yield (serving size) from Food52 recipe
        :return: None
        """

    def set_ingredients(self):
        """
        Sets ingredient dict from Food52.com {"ingredient": "quantity"}
        :return: None
        """

    def set_instructions(self):
        """
        Sets instructions for Food52.com recipe
        :return:
        """

    def set_recipe_contents(self):
        """
        Sets all recipe elements
        :return:
        """

    def make_markup(contents, title):
        try:
            title = ''.join(c for c in title if 0 < ord(c) < 127)
            x = str(os.path.dirname(os.path.dirname(__file__)) +
                    "/Recipes/" + title + ".md")
            file = open(x, "w")
            file.write(contents)
        except IOError as e:
            raise IOError
        file.close()
        return True


class Food52Parse(RecipeParse):
    def __init__(self, url):
        super(Food52Parse, self).__init__(url)

    def set_recipe_title(self):
        """
        Gets recipe title from Food52.com recipe
        :return: None
        """
        self.title = self.soup.find("h1", {"class": "article-header-title"}).text.strip()

    def set_recipe_img(self):
        """
        Sets recipe image using url
        :return: None
        """
        self.img_url = "https:" + self.soup.find(
            "figure", {"class": "photo-frame first"}).find("img")['src']

    def set_recipe_yield(self):
        """
        Gets recipe yield (serving size) from Food52 recipe
        :return: None
        """
        self.recipe_yield =self.soup.find("p", itemprop="recipeYield")

    def set_ingredients(self):
        """
        Sets ingredient dict from Food52.com {"ingredient": "quantity"}
        :return: None
        """
        # find all for multi-part recipes
        for div in self.soup.findAll("ul", {"class": "recipe-list"}):
            # find all ingredient <li> elements
            for element in div.findAll("li", itemprop="ingredients"):
                # find all ingredient names
                for ingredient in element.findAll(
                        "span", {"class": "recipe-list-item-name"}):
                    # if ingredient is already present in dict
                    if ingredient.text.strip() in self.ingredients.keys():
                        self.ingredients[
                            ingredient.text.strip()
                        ].append(
                            element.find(
                                "span", {"class": "recipe-list-quantity"}
                            ).text.strip()
                        )
                    # if ingredient is not present in dict or None
                    if ingredient.text is not None and ingredient.text.strip()\
                            not in self.ingredients.keys():
                        self.ingredients[ingredient.text.strip()] = []
                        self.ingredients[
                            ingredient.text.strip()
                        ].append(
                            element.find(
                                "span", {"class": "recipe-list-quantity"}
                            ).text.strip()
                        )

    def set_instructions(self):
        """
        Sets instructions for Food52.com recipe
        :return:
        """
        self.instructions = [
            step.text.strip() for step in self.soup.findAll(
                "li", itemprop="recipeInstructions")
            ]

    def set_recipe_contents(self):
        self.set_recipe_title()
        self.set_recipe_img()
        self.set_recipe_yield()
        self.set_ingredients()
        self.set_instructions()


class AllRecipesParse(RecipeParse):
    def __init__(self, url):
        super(AllRecipesParse, self).__init__(url)
        self.ingredients = []

    def __str__(self):
            ingredients_table = ''
            instruction_list = ''

            for ingredient in self.ingredients:
                ingredients_table += "|" + ''.join(ingredient) +  "|\n"

            for step in self.instructions:
                instruction_list += "\n\n* " + step

            return "#[{}]({})\n![alt text]({})\n###Ingredients\n|Ingredient|" \
                   "\n|:-------|\n{}\n###Instructions{}".format(
                self.title, self.url, self.img_url, ingredients_table, instruction_list
            )

    def set_recipe_title(self):
        """
        Gets recipe title from Food52.com recipe
        :return: None
        """
        self.title = self.soup.find(
            "h1", {"class": "recipe-summary__h1"}).text.strip()

    def set_recipe_img(self):
        """
        Sets recipe image using url
        :return: None
        """
        self.img_url = self.soup.find(
            "img", {"class": "rec-photo"})['src']

    def set_ingredients(self):
        """
        Sets ingredient dict from Food52.com {"ingredient": "quantity"}
        :return: None
        """
        # find all for multi-part recipes
        self.ingredients = [
            ingredient.text.strip() for ingredient in self.soup.findAll(
                "span", {"class": "recipe-ingred_txt added"})
                ]

    def set_instructions(self):
        """
        Sets instructions for Food52.com recipe
        :return:
        """
        self.instructions = [
            step.text for step in self.soup.findAll(
                "span", {"class": "recipe-directions__list--item"}) if step.text
            ]

    def set_recipe_contents(self):
        """
        Sets all class variables.
        :return: None
        """
        self.set_recipe_title()
        self.set_recipe_img()
        self.set_ingredients()
        self.set_instructions()


link = "http://allrecipes.com/recipe/7958/pumpkin-chocolate-chip-muffins/"

thisrecipe = AllRecipesParse(link)
thisrecipe.set_recipe_contents()
print(thisrecipe.__str__())

#file = "/Users/brooke/Desktop/recipes.txt"
#with open(file, 'r') as f:
#    content = f.read().splitlines()

#for url in content:
#    thisrecipe = Food52Parse(url)
#    thisrecipe.set_recipe_contents()
#    try:
#        thisrecipe.make_markup(thisrecipe.__str__(), thisrecipe.title)
#    except IOError as e:
#        print(thisrecipe.title, "\tFILE NOT CREATED:\t", e.__str__())
