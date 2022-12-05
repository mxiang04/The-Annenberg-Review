import datetime
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from cs50 import SQL

driver = webdriver.Chrome(ChromeDriverManager().install())
db = SQL("sqlite:///blog.db")
# Get time when running program
now = datetime.datetime.now()
date = now.strftime("%m-%d-%Y")

meal_matcher = {
    "Breakfast": 0,
    "Lunch": 1,
    "Dinner": 2,
}

# Gets menu for specific day


def scrape(meal):
    URL = "http://www.foodpro.huds.harvard.edu/foodpro/menu_items.asp?date={}&type=30&meal={}".format(
        date, meal_matcher[meal])
    MENU_XPATH = "/html/body/div/div[3]/div[1]/form/table[3]/tbody/tr"
    # Go to Annenburg Site
    driver.get(URL)

    table_data = driver.find_elements(By.XPATH, MENU_XPATH)
    categories = {}
    cur_category = None
    for row in table_data:
        try:
            # Only first piece of data i.e. the name of the category or dish matters
            data = row.find_elements(By.XPATH, "./td")[0]

            if "category" in row.get_attribute('class').split():
                cur_category = data.text
                categories[cur_category] = []
                continue

            if cur_category is None:
                continue

            menu_item = data.find_element(By.XPATH, "./div[1]/span/a").text
            categories[cur_category].append(menu_item)
        except:
            pass

    for category, items in categories.items():
        for item in items:
            db.execute(
                "INSERT INTO FOOD (category, name, meal) VALUES (?, ?, ?)", category, item, meal)


def get_menu(meal):
    cur_date = now.strftime("%Y-%m-%d")
    rows = db.execute("SELECT * FROM FOOD WHERE date = ?", cur_date)
    if len(rows) == 0:
        for key, value in meal_matcher.items():
            scrape(key)

    data = db.execute(
        "SELECT category, name FROM FOOD WHERE meal = ? AND date = ?", meal, cur_date)
    return data
