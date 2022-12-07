# The scraper

THe scrape function gets the URL for the annenburg website, and it only runs if today's menu is not yet up. When it does run, it scrapes the menu for the current date (which we get with the datetime import) for breakfast, lunch, and dinner. The scrape function uses Selenium to identify where the menu dishes are located in the HTML document. Once it is done getting all of the scraped results, it sends the name of the dish, category of the dish, and meal (breakfast, lunch, or dinner) to the food table in blog.db.

The get_menu functions first checks to see if there is any data in the food table for the current date. If nothing is in there, then it runs the scrape function. The get_menu function then returns the requested menu for the current day. That way, the scrape function is only ran once per day, which helps limit delay.

# The application

The index function gives us the menu for a certain day, and it lets you choose between lunch, breakfast, and dinner. Once a choice of menu is selected, the get_menu function from scraper.py will return data for the current day's selected menu. The index function will then pass the data into the index.html template, so that it can be displayed on the front-end.

The profile function gives us the reviews that the logged in user has given, and it also displays the average rating that the user has given. It works by querying the database for all reviews written by the user logged in, calculating the average rating that the reviewer has given along the way. It then passes this into the profile.html template to be displayed on the front-end. You can also delete posts by pressing the delete button, which is linked to each post's post_id. Once the delete button is clicked, we delete the post with the post_id that we get from the delete button from the POSTS table in blog.db.

The upload function lets you give your own rating and review for that day's menu. It works by giving you a text area and a selector that lets you choose integers from 1-5. Once the submit button is clicked, it sends a post request to the POSTS database to add your new post.

The feed page shows everybody else's ratings and reviews. It works by querying the database for all reviews ever. It also gives you the average rating for today. The way we got that was by querying the database for the average of all ratings written on or after the current date (since posts follow the current_timestamp, most posts will be "after the current date" e.g. 2022-12-06 < 2022-12-06 07:33:06)

# The SQL (blog.db)

We created three SQL tables that we utilize throughout app.py and its corresponding HTML pages.

Our first table, 'Posts', we created a table that stores information on a given meal, which includes the name of the food, the time when the post is uploaded, the rating a user gives the meal, the id of the post, and the text input for a user comment. We utilize the text input, the id of the post, the rating, and the time stamp in our post pages. Sorted meals and names of dishes did not come to fruition in the posting aspect of our website, although dishes are sorted by meal in the menu part of our website and the given name of the dish could likely be included within the user's text comment, reviewing the meal.

Our second table, 'users', includes a user text entry to store a username, a password text entry to store a user's hashed password, and an autoincremented user_id that recognizes the user in relation to this username and passwords when they re-enter the website.

Our third table, 'Food', works directly to store information attained from our scraper algorithm for given dishes and meals. The scraper algorithm, on the first time anyone user it on a particular day, runs and collects data off of annenberg's online website, and stores the different data types to corresponding sql values in 'portal'. 'meal' will store the meal as a text. 'name' will store the name of a given dish and 'category' will give each a text category it fits in. For example, a dish named 'black beans' would have a category of 'Salad bar' . All of these data types are text entries. Each dish also has a primary key autoincremented id number that makes it unique and recognizable for the program to match it with the rest of the data points in the table.

# HTML

Now we will move on to the HTML templates. All of these templates will be using and applying elements from the SQL tables and being manipulated by jinja and python to become dynamic, changing pages based on user input.

apology.html flashes an error message(need more detail here)

layout.html acts as our basis for all other html pages outside of apology, where it makes the basic outline for our ‘Annenberg Review’ button in the top left corner of the screen, as well as setting the navigation bar. Layout.html also directly link the different html pages to one another. Every other html page on this website ‘extends layout.html’

login.html is the first page we see extend layout.html on the website. Login is our default page once a user enters our website url in the search bar. This page includes some of the same structural features of layout.html, which include a navbar with buttons: a ‘register’ button, that links us to a page that allows a new user to create an account, and a ‘login’ button, which, if we are in the registration page, allows us to switch from registering a new user to getting to the login page. Within the login page, we have post methods that take text entries of ‘username’ and ‘password’, which are then sent into the code to see if they match the registration page usernames and passwords entered. If they are a match, then the page sends us into index.html, and if they are wrong, an error message is displayed.

register.html is structured very similarly to login.html. The only differences between the two pages is that register.html takes in two password entries and that it utilizes the javascript page register.js to actually register a new user in the database of user in the system. Once a user is registered(barring they do not enter either a username or password or a username is already used, which would result in an error message), we will then be shifted to the login page.

index.html is the homepage of our website. As soon as this page is opened, a bootstrap feature of our website that pops up instructions as to how to use the website appears. This can be exited by clicking the x in the top right corner, which is a button that makes it vanish. This page also extends layout and its navbar structure, but the navbar that appears has different buttons than the login and register pages. This navbar has buttons named ‘upload’, ‘your posts’ and ‘feed’, which correspond to ‘upload.html’, ‘profile.html’, and ‘feed.html’. Pressing any of these buttons will take us to these pages. Additionally, we can see a ‘logout’ button on the right side of the navbar, which leads us to the login page. Other than the navbar, we also have another bootstrap feature in index.html, which is a dropdown menu that allows the user to select a meal: breakfast, lunch, or dinner. After the user selects one of these, there is a select menu button underneath the dropdown menu button, which actually allows the menu to appear. This is where scraper.py compiles and displays the data it scrapes for the website if it is being used for the first time on that day. This aspect of the page will vary based on the day and meal selected.

upload.html has the exact same navbar as index.html, but has different features within the page. Namely, it includes multiple features that contribute to creating an actual post. These are a textbox and a dropdown list that allows the user to rate a given review from 1 to 5. These two features together will be uploaded and transferred to both the ‘your posts’ page and the ‘feed’ page when the user hits the upload button under the two features of this page.

The first interesting feature of profile.html is that when a post is uploaded and the user is transferred to this page, a text will flash the word ‘submitted’ at the top of the screen. The your posts page has the same navbar and structure as index, but it features a bootstrap structure of a table, the user will be able to see the details of all of their individual reviews created from upload.html. This will include a ‘review’ column, which details the text entry from upload, a ‘rating’ column, displaying the rating the user puts out of 5, as well as a ‘time’ column, which displays when the post was created. Additionally, each review has a ‘delete’ button on the righthand row of each post, which allows the user to delete said entry. At the top of the page, there is a ‘Your average rating:’ text displayed will a number following it. That number is the mean of the sum of a given user’s total post ratings(ie a user with 2 total posts with ratings of 1 and 3 would get a 2 average rating).

feed.html also has the same navbar that the other pages other than login and register have, and resembles the table in profile.html very much, but has one additional column called username. This page essentially takes all of the uploads from each individual user and displays all of them into one single page, where all user reviews from all time can be viewed. The only different features this page has from profile.html is that a user cannot delete posts from this page and the average rating section of the page sums the ratings of all user reviews on that given day, and then takes their mean. This way, a user can see the overall rating for annenberg on that given day.

register.js
This function checks whether or not the username is taken or not by using the check function to see if that username is available or not within the table. If it is not, then it reprompts the user to type it in again.

# The Styling

Let us go through the styling of our website!

Title, Background, and Navbar:
For our title and background, we made the class "red", which connects to the title, and the tag "body", which connects to the background of the website, red in our CSS file. Specifically for the title, we changed the font to cursive by changing the font-family to Brush Script MT for the class "red" as well and increased the font-size to 50px to ensure that our title stood out.

    For our navbar, instead of using CSS, we used bootstrap's color "warning" which is really just yellow to make our navbar yellow when we implemented the navbar in layout.html. We also made the navbar extra large in our CSS by making the font-size extra extra large. For the specific names of each item in the navbar, we also decided to change their font to Impact in order to highlight the different aspects of our website. I did this by creating ids for upload, profile, feed, register, login, and logout and then, using CSS, changed their font-family to Impact, made their color black, and made their font-weight bold using CSS.

Index/Menu Page:
Right one goes to the index/menu page of our website, they are greeted by a popout menu on the side that teaches users how what the website is about and how to use it. We implemented this by adapting the "offcanvas" feature from boostrap to our own website in the index.html page. In addition, we also made the select menu button a primary (blue) button from boostrap.

Upload Page:
For the upload page, we made several unqiue designs. First of all, we made a ratings and a comments portion of this page with both titles in the font type Brush Script MT, made their color white, made the font size 50px, and made the font-style bold by making these changes to our h2 tag in CSS. For the ratings box, we used the "select" tag in our upload.html to create a dropdown menu for the difference ratinsgf rom 1-5 one could give for the food of the day. For the comments box, we used the "textarea" tag to create a box with the dimensions 4 by 50 for the user to input any comment they'd like. We made the upload button using bootstrap by picking the primary (blue) buttton for this page in html.

Profile and Feed Pages:
For the profile and feed pages, we also made many styling choices. First, we made the titles and averages at the top white and in italics by changing the h1 and h3 tags in CSS. Then, we made the table headers white as well by making the color of the class th white in CSS. One feature we thought was especially interesting that we also implemented into both pages was the tr:hover feature in our CSS page, which basically makes a row in our table of reviews white whenever someone's mouse hovers over it. We implemented this in CSS by making tr:hover's background color white.

Footer:
Subtle but still there, the footer at the end of our website was originally a light grey and couldn't be seen so we changed the color to black by putting the footer in an "ins" tag and then in CSS, making this tag's color black.
