Let us go through the scraping.py file first.

THe scrape function gets the URL for the annenburg website, and it only runs if today's menu is not yet up.
The get_menu functions returns the requested menu for the current date, and if the data is not yet there, then it calls the scrape function.

Let us go through app.py
  The index page gives us the menu for a certain day, and it lets you choose between lunch, breakfast, and dinner.
  The Profile page gives us the reviews that the logged in user has given, and it also displays the average rating that the user has given. You can also delete your own posts.
  The Upload page lets you give your own rating and review for that day's menu.
  The Feed page shows everybody else's ratings and reviews.
