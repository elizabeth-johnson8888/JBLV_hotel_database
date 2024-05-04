We used faker to generate our data.

## SQL files:
* load.sql --loads csv data into jblv database
* create.sql --creates the tables in the database
* alter.sql --creates the primary and foreign keys for the tables in jblv


To load the data into the database:
``` sh
psql < create.sql
psql < load.sql
psql < alter.sql
```


## CSV files:
* admin.csv --data of administrators with their employee_id and department_id
* bills.csv --guest bill data (guest_id,bill_id,total,reservation_id)
* cleaning.csv --data of cleaning employees with their employee_id, department_id, and the schedule_id of what cleaning schedule they're responsible for
* cleaning_schedule.csv --(employee_id,department_id,schedule_id) -- holds the schedules for employees on the current day
* employee.csv --data of hotel employees with their (employee_id,first_name,last_name,job_title,department_id,hotel_id) --hotelid identifies the hotel that the employee works for
* day_discount.csv --holds the daily discounts for hotel rooms (weekday,discount,hotel_id)
* guest_categories.csv --for each hotel, holds guest categories and discounts for each guest(hotel_id,guest_id,category,discount)
* guest.csv --data of guests that have stayed at a hotel(guest_id,first_name,last_name,mobile_phone,home_phone,id_type,id_number)
* hotel_features.csv --data of the features belonging to each hotel such as airport shuttle or pet friendly(hotel_id,name)
* hotel_phones.csv --data of phone numbers associated with the Front Desk, Kitchen, and Housekeeping of each hotel(hotel_id,name,number)
* hotels.csv --data of the hotel (hotel_id,name,addess)
* occupants.csv --occupant data for each reservation(reservation_id,name) --hotel reserver guests
* reservation.csv --data of every reservation for the hotels (reservation_id,guest_id,checkin_date,checkout_date,room_num,type_id,actual_checkin,actual_checkout,hotel_id)
* review.csv --data of every review for every hotel(guest_id,display_name,rating,comment,date)
* room.csv --data of hotel rooms
* room_features.csv --data of the features belonging to each room type(type_id,name,hotel_id)
* room_type.csv --data of room types along with the hotel_id for which hotels offer certain room types(type_id,price,capacity,sq_ft,hotel_id)
* seasons.csv --data of different seasons that can affect the price of hotels(season_id,season_name,start_date,end_date,discount,hotel_id)
* services.csv --data of the services offered at each hotel(service_id,name,price,guest_id,hotel_id)
* spa_services.csv --hold information for specific spa services and their prices


# Database
## Data Generation
* NOTE: When making each model, it is helpful to have your most updated model to reference the necessary attributes for each entity.
* Install Faker – pip install Faker
* Import Faker and random into your file to help generate fake/random data – from faker import Faker
* Make a faker object to call various methods on – fake = Faker(); fake.city()
* Create an object for all entities in your diagram, we used a list, and append each attribute to
* For random numbers, such as years, price, capacity, etc.
* For attributes such as names, addresses, and locations, use Faker to generate fake data

## Base Providers
* In our case, we wanted to make a special fake data generator for animal names. To do this you can import a BaseProvider and extend it to be your own class.
* Providers are packages of generator properties that we can import and add to our 'fake' object – from faker.providers import internet; fake.add_provider(inernet)
* To create your own class of properties, import baseProvider and extend it – class NewProvider(BaseProvider)
* Create properties of the provider by defining methods in your class. We had an 'animal' method that returned a randomly selected element of a list of animals
* Don't forget to add the provider to your 'fake' object using add_provider()

