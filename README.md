# Janative1: Take a seat | Visual booking system
#### Video Demo:  https://youtu.be/fxQIhqxlqGY

### Description:
The Take a seat is a site which allows you see, which seats in your office are free or taken on any chosen day through simple graphical interface (floorplan).
By clicking on any seat, you can simply book it for that day, or even for a  longer period of time. You can insert booking details also directly through a form.
If the seat is taken (either by you or anybody else), error message appears. There are also other error handling measures, such as start date vs end date logic.
In order to maintain your bookings, you are asked to register before doing anything on the website. After the login, you can see all you current booking entries in the list.
Each booking can be cancelled by hitting cancel button, followed by a modal prompt to reconfirm the decision.

#### Application.py
Controller of the whole application. Controls the interactions of HTML, CSS, JS files and SQL database.

#### Static
repository of static resources, such as svg graphics, favicon, styles.css and background picture.

#### Templates (HTML)
apology.html - site with generated erroe message based on error type.
book.html - site enabling user to pass their input re booking
index.html - history of the booking
layout.html - unified look and feel for all html pages
login.html - for users to enter their credentials
register.html - registering page for users
seating.html - providing visual representation of taken and free seats. Status of each seat is checked against SQL database.

#### database.db
sql database where all the bookings, users and history is stored.

#### helpers.py
it contains helping Python functions

#### requirements.txt
the lsit of needed libraries.

#### Error handling
Application is made in a way that is checks possible errors  - missing or already taken username, missing dates, start date older then end date, seat already taken etc.
