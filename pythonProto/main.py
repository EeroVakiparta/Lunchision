import requests
from bs4 import BeautifulSoup
import pandas as pd

# https://lounaspori.fi/ravintolat/lounasravintolat/

def download_and_parse(lounasporiURL, favDishes):
    start_url = lounasporiURL

    # Download the HTML from start_url
    downloaded_html = requests.get(start_url)

    # Parse the HTML with Beautifulsoup and create a soup object
    soup = BeautifulSoup(downloaded_html.text, features="html.parser")

    # save a local copy, NOTE: , newline='',encoding="utf-8" added because of UnicodeEncodeError charmap cant encode
    with open('downloaded.html', 'w', newline='', encoding="utf-8") as file:
        file.write(soup.prettify())

    # select all item-inner divs
    item_inners = soup.find_all("div", {"class": "item-inner"})

    # make a dictionary of all the restaurants and their lunchtext
    restaurant_dict = {}
    for item_inner in item_inners:
        restaurant_name = item_inner.find("h2").text
        # get the lunchtext part of the item_inner
        lunchtext = item_inner.find("div", {"class": "dow-menu-data"})

        restaurant_dict[restaurant_name] = lunchtext

    # print(restaurant_dict)

    # find all the restaurants from the dictionary of lists which have the word included in favDishes in their lunchtext
    # give one point for each word found to the restaurant
    restaurant_points = {}
    for restaurant in restaurant_dict:
        restaurant_points[restaurant] = 0
        for dish in favDishes:
            if dish in restaurant_dict[restaurant].text:
                restaurant_points[restaurant] += 1

    # print top 3 restaurants and their points and words found
    print("Top 3 restaurants:")
    for restaurant in sorted(restaurant_points, key=restaurant_points.get, reverse=True)[:3]:
        print(restaurant, restaurant_points[restaurant])
    # print(best_restaurants.keys())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # lista of favorite dishes
    favorite_dishes = ["lohi", "aurajuusto", "aura", "tulinen", "spicy", "pekoni", "kebab", "lohta", "pizza", "tofu"]
    # ask user if they want to add more dishes to the list
    add_more = input("Do you want to add more dishes to the list? (y/n)")
    if add_more == "y":
        while add_more == "y":
            new_dish = input("Enter a new dish: ")
            favorite_dishes.append(new_dish)
            add_more = input("Do you want to add more dishes to the list? (y/n)")
    else:
        pass

    download_and_parse('https://lounaspori.fi/ravintolat/lounasravintolat/', favorite_dishes)