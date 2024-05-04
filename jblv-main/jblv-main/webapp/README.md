# Web App

# SQL Functions
## Query 1: Reservations
* To create a reservation, we must have a hotel ID as well as a check in and checkout date. We send this data into our function via the forms in q1_reservations.html and return the available room types at the hotel to reserve along with the average cost per night if that reservation were to be made.
* We first got the available rooms at the hotel by excluding reservations where the checkin and checkout date are in the range of the given datas (left join).
* Then, we got the room type of the available rooms to get the base price of the cost per night and joined the seasonal discount, daily discount, and guest discount, which are all unique to the hotel, to account for the true average price of the room.
* Right now, the season is set to spring, and the guest category is set to VIP


## Query 2: Checking In
* To check in, we must get the available rooms per the reservations room type. In this case, we just get the available double rooms for a specific check in date, given by the user
* We first get the reservations that do not have an assigned room to their booking, and filter out the ones that do not have the room type of 'Double Suite'
* We also make sure that the room is clean and not occupied to ensure it is available to reserve.

## Query 3: Checking Out
* The function generates a billing statement for a guest upon checkout.
* It takes in the parameters for guest first name, last name, and the checkout date.
* The billing statement is a table that includes information such as  reservation ID, check-in and check-out dates, days stayed, room number, room price, discounted price, service price, and total amount due.
* We then retrieve the check in and check out dates for the given guest, calculate the days stayed, and find the season discount for those days, along with the guest category discount.
* Then, for each day of the guest's stay, we iterate, calculating the room price and applying that day's discount to the room price along with the season discount and guest category discount, accumulated into a total discounted price variable.
* Lastly, the total price is calculated by retrieving all the service costs associated with that stay and adding with the discounted price to get the total amount due, which is returned in a table along with other information for the bill.
* Upon clicking the "check out" button, the user triggers the corresponding tables to update their information needed to checkout a guest, such as the actual checkout date, occupied status of room, clean status, etc.

## Query 4: Special Feature (Spa)
* Our hotels special feature is a spa! This function takes in a max price that the guest wants to spend on their service and filters out all of the services that exceed this price.
* We first get the services that match the category 'Spa', as well as the service selected by the user in q4_special_feature.html, and then filter out the services that are too expensive.
* Our services are identified by a hotel, so we must specify first which hotel we are looking at, then the specific service id to match our 'Spa' service. 

# Running the flask app
* flask --app app run
* Flask and psychopg must be imported; if a .venv file is present, run source .venv/bin/activate
* app is the name of the application we want to run, in this case app.py
