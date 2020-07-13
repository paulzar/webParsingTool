import os, requests
from bs4 import BeautifulSoup as bsp
from datetime import datetime, date
#from pathlib import Path


# copy the url that loads once request with all necessary parameters has been submitted

# website = 'https://auto.drom.ru/toyota/hilux_pick_up/'

# TODO_1: Paste the link to the request get function as argument, check for load errors

# TODO_2: Scrape the values from the block marked as <a class = "b-advItem"></>
# in a list of dicts called 'var':
# "link", "model_year", "config", "engine", "transmission", "fuel", "mileage", "price", "city", "date"

# TODO_2.1 Use decorator to process the exeptions AttributeError: 'NoneType' object has no attribute 'text'
# when block does not contain a certain specific attribute or attribute contains no value

def convert_date(date_bid):
       ru_month = ('января', 'февраля', 'марта',
                   'апреля', 'мая', 'июня', 'июля',
                   'августа', 'сентября', 'октября',
                   'ноября', 'декабря')
       # TODO_1: if date_bid contains 'назад' return today
       if 'назад' in date_bid:
              conv_date = date.today()
       else:
              db_mi = ru_month.index(date_bid.split()[1]) + 1
              conv_date = date(date.today().year, db_mi, int(date_bid.split()[0])) 

       return conv_date.isoformat()

def request_res(website: str) -> list:
    res = requests.get(website)
    res.raise_for_status()

    #def soup_parser(html_page):
    dromSoup = bsp(res.text, 'html.parser') #not 'parser.html'

    advItem_list = [] # list for <a> containers with all items except "date"
    date_list = []

    for x in dromSoup.findAll('a', {'class': 'b-advItem'}):
        advItem_list.append(x)

        # Exception for blocks with no mileage 
        ma = x.select('div[data-ftid="sales__bulls-item_mileage"]')
        if ma == []:
                 mileage = '0'
        else: mileage = ma[0].text.split('\xa0')[0]

        # Exception for blocks with no config
        conf = x.select('div[class="b-advItem__cmp"]')
        if conf == []:
            config = None
        else: config = conf[0].text.strip()

        var = [] # a list collect the sets of "key": value pairs with all parameters
        for x in advItem_list:
            var.append({"link": x["href"], #
                        "model_year": x.find('div', {'class': 'b-advItem__title'})
                            .text
                            .split(", ")[1],
                        "config": config,
                        "engine": x.find('div', {'class': 'b-advItem__params'})
                            .text
                            .split('\n')[1],
                        "transmission": x.find('div', {'class': 'b-advItem__params'})
                            .text
                            .split('\n')[3],
                        "fuel": x.find('div', {'class': 'b-advItem__params'})
                            .text
                            .split('\n')[2],
                        "mileage": mileage,
                        "price": x.find('div', {'class': 'b-advItem__price'})
                            .text
                            .strip()
                            .replace('\xa0', '')
                            .replace('q', ''),
                        "city": x.find('div', {'class': 'b-advItem__params b-text-gray'})
                            .text
                            .strip(),
                        "date_bid": None})

    # find the 'date' blocks because they are somehow outside of <a> containers
    for y in dromSoup.findAll('div', {'data-ftid': 'sales__bulls-item_date'}): 
        db_item = y.text.strip().replace('\xa0', ' ')
        x = convert_date(db_item)
        date_list.append(x)

    # try zip(var, date_list)
    for i in range(len(date_list)):
        var[i]["date_bid"] = date_list[i]

    return var

#request_res(website)

# TODO_3: Transform the date in from relative to unified date format

# TODO_4: Repeat for the next pages of the feed

# TODO_5: Save the results as .csv file

# TODO_N: Print the saved file destination

