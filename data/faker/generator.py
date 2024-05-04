from faker import Faker
from faker.providers import BaseProvider
import random
import csv

from datetime import datetime, timedelta

# Current date is April 1, 2024
# CUR_DATE = datetime(2024, 4, 1)
CUR_DATE = datetime.now()


class AnimalProvider(BaseProvider):
    # may have to think about possible repeats since we are randomly selecting and not removing
    def animal(self):
        animals = []
        with open("faker/animals.txt", "r") as file:
            # with open("faker\\animals.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                animals.append(line.strip())
        return self.random_element(animals)


fake = Faker()
fake.add_provider(AnimalProvider)

# make 20 hotels


def make_hotels():
    hotels = [[] for _ in range(20)]
    for i in range(20):
        hotels[i].append(i)  # hotel id
        hotels[i].append(fake.animal() + "Hotel")  # hotel name
        hotels[i].append(fake.address())  # hotel address
    return hotels


season_information = [
    # name       start date           end date             discount
    ["Winter", datetime(2024, 1, 1), datetime(2024, 3, 20), .1],
    ["Spring", datetime(2024, 3, 21), datetime(2024, 6, 20), .2],
    ["Summer", datetime(2024, 6, 21), datetime(2024, 9, 22), 1],
    ["Fall", datetime(2024, 9, 23), datetime(2024, 12, 20), .4],
    ["Christmas", datetime(2024, 12, 21), datetime(2024, 12, 31), 1],
    ["New Year", datetime(2025, 1, 1), datetime(2025, 1, 7), 1],
    ["Valentine's Day", datetime(2024, 2, 14), datetime(2024, 2, 14), 1],
    ["Spring Break", datetime(2024, 3, 15), datetime(2024, 3, 31), .15],
    ["Independence Day", datetime(2024, 7, 4), datetime(2024, 7, 4), .50],
    ["Labor Day", datetime(2024, 9, 1), datetime(2024, 9, 1), .05]
]

season_id_set = set()
# assigns at least 3 seasons per hotel


def make_seasons(hotel):
    seasons = []
    for i in range(random.randint(3, 9)):
        season = []
        seasons_id = random.randint(0, 10000)
        while seasons_id in season_id_set:  # make sure the season_id is unique
            seasons_id = random.randint(0, 10000)
        season.append(seasons_id)
        # prevents duplicate seasons for hotels
        season.extend(season_information[i])
        season.append(hotel[0])
        seasons.append(season)
        season_id_set.add(seasons_id)
    return seasons

# hotels have multiple different kinds of phone numbers

def populate_phone():
    num = fake.phone_number()
    while phones.__contains__(num):
        num = fake.phone_number()
    phones.add(num)
    return num

def make_hotel_phones(hotel):
    hotel_phones = []
    #                    hotel_id   name         number
    hotel_phones.append([hotel[0], "Front Desk", populate_phone()])
    hotel_phones.append([hotel[0], "Kitchen", populate_phone()])
    hotel_phones.append([hotel[0], "Housekeeping", populate_phone()])
    return hotel_phones


# make at least 5 room types for the given hotel
def make_room_types(hotel):
    room_types = []
    #                  type_id(str)     price               capacity       sq_ft            hotel_id
    room_types.append(["Queen 1 Bed", 
        70, 2, random.randint(200, 250), hotel[0]])
    room_types.append(["Queen 2 Bed", 
        110, 4, random.randint(251, 300), hotel[0]])
    room_types.append(["King 1 Bed", 
        80, 3, random.randint(251, 325), hotel[0]])
    room_types.append(["Double Suite", 
        120, 8, random.randint(325, 450), hotel[0]])
    room_types.append(["King Suite",
        150, 3, random.randint(350, 450), hotel[0]])
    return room_types

# changes price of the room types based on the day of the week

def make_day_discounts():
    return [[1, .10, 0], [2, .15, 0], [3, .15, 0], [4, .20, 0], [5, .50, 0], [6, .65, 0], [0, .50, 0]]


room_number_set = set()  # use to prevent duplicate room numbers
# At least 3 rooms of each room type; the distribution of the other room types does not matter.
# hotel_room_types holds all room type info for a specific hotel


def make_room(hotel, hotel_room_types):
    rooms = []
    for room_type in hotel_room_types:
        for i in range(20):
            room_num = random.randint(0, 10000)
            while room_num in room_number_set:  # loop until you get a unique room number
                room_num = random.randint(0, 10000)
            #              room_num                   floor_num            is_clean   type_id   is_occupied
            rooms.append([room_num, random.randint(
                1, 5), True, room_type[0], False, hotel[0]])
            room_number_set.add(room_num)
    return rooms

# make 200 guests


def make_guests():
    guests = []
    for i in range(200):
        guests.append([i, fake.first_name(), fake.last_name(),
                       fake.phone_number(), fake.phone_number(),
                       random.choice(
                           ["Passport", "Driver's license", "State ID", "Student ID", "Military ID"]),
                       fake.random_number(digits=9)])
    return guests


# guest category and discounts
guest_categories = [
    ["VIP", .25],
    ["Military", .15],
    ["Government", .1],
    ["Senior", .65]
]

# make employees
employee_id_set = set()


def make_employees(hotel):
    employees = []
    for _ in range(10):
        employee_id = random.randint(1, 10000)
        while employee_id in employee_id_set:  # prevents employee_id duplication
            employee_id = random.randint(1, 10000)
        employee_id_set.add(employee_id)
        employees.append([employee_id, fake.first_name(),
                          fake.last_name(), fake.job(),
                          random.randint(1, 10000), hotel[0]])
    return employees

# half of the employees per hotel


def make_admin(employee):
    admins = []
    admins.append([employee[0], employee[4]])
    return admins

# half of employees per hotel


def make_cleaning(employee, cleaning_schedule):
    housekeepers = []
    housekeepers.append([employee[0], employee[4], cleaning_schedule[0]])
    # print(housekeepers)
    return housekeepers

# make a cleaning schedule is generated for the day


def make_cleaning_schedule(schedule_id):
    cleaning_schedule = []
    cleaning_schedule.append([schedule_id, CUR_DATE])

    return cleaning_schedule, schedule_id


def make_hotel_features(hotel):
    return [hotel[0], random.choice(hotel_features)]


def make_room_features(room_type):
    room_features = []
    for type in room_type:
        room_features.append([type[0], random.choice(room_feature),type[4]])
    return room_features


def make_bills(reservations):
    # guest id, bill_id, total
    bills = []
    for reservation in reservations:
        guest_id = reservation[1]
        type_id = reservation[5]
        hotel_id = 0
        total = 0

        for type in room_types:
            if type[0] == type_id:
                hotel_id = type[4]

                total = type[1]  # price of the room type

        for service in services:
            # search thru services to match guest/hotel id
            if guest_id == service[3] and hotel_id == service[4]:
                total += service[2]
        bill_id = fake.unique.random_number(digits=9)
        bills.append([guest_id, bill_id, total, reservation[0]])
    return bills


def make_services(reservations):
    services = []
    for reservation in reservations:
        guest_id = reservation[1]
        # type_id = reservation[5]
        hotel_id = 0
        # for type in room_types:
        #     if type[0] == type_id:
        #         hotel_id = type[4]

        # print("hotel", hotel_id)
        for _ in range(3):
            s, price = random.choice(service)
            services.append([fake.unique.random_number(
                digits=9), s, price, guest_id, hotel_id])
    return services

def make_guest_categories(hotel):
    guest_cats = []
    i = 0
    for guest in guests:
        i = i % len(guest_categories)
        name, discount = guest_categories[i]
        guest_cats.append([hotel[0], guest[0], name, discount])
        i += 1
    return guest_cats


def make_reservations(hotel):
    id = 0
    hotel_id = hotel[0]
    reservations = []
    for guest in guests:
        guest_id = guest[0]
        reservation = []
        if id < 25:
            # past
            checkin = fake.date_between_dates(CUR_DATE - timedelta(days=random.randint(
                100, 500)), CUR_DATE - timedelta(days=random.randint(10, 99)))
            checkout = fake.date_between_dates(
                checkin + timedelta(days=random.randint(1, 7)))
            room = random.choice(rooms)
            room_num = room[0]
            room_type = room[3]
            actual_checkin = fake.date_between_dates(
                checkin, checkin + timedelta(days=random.randint(0, 1)))
            actual_checkout = fake.date_between_dates(
                actual_checkin, actual_checkin + timedelta(days=random.randint(0, 7)))
            reservation = [id, guest_id, checkin, checkout,
                           room_num, room_type, actual_checkin, actual_checkout, hotel_id]
            reservations.append(reservation)
        elif id < 50:
            # past and multiple rooms/reservations
            for _ in range(2):
                checkin = fake.date_between_dates(CUR_DATE - timedelta(days=random.randint(
                    100, 500)), CUR_DATE - timedelta(days=random.randint(10, 99)))
                checkout = fake.date_between_dates(checkin,
                                                   checkin + timedelta(days=random.randint(1, 7)))
                room = random.choice(rooms)
                room_num = room[0]
                room_type = room[3]
                actual_checkin = fake.date_between_dates(
                    checkin, checkin + timedelta(days=random.randint(0, 1)))
                actual_checkout = fake.date_between_dates(
                    actual_checkin, actual_checkin + timedelta(days=random.randint(0, 7)))
                reservation = [id, guest_id, checkin, checkout,
                               room_num, room_type, actual_checkin, actual_checkout, hotel_id]
                reservations.append(reservation)
                id += 1
        elif id < 80:
            # current
            checkin = fake.date_between_dates(
                CUR_DATE - timedelta(days=random.randint(1, 5)), CUR_DATE)
            checkout = fake.date_between_dates(
                checkin, checkin + timedelta(days=random.randint(5, 10)))
            room = random.choice(rooms)
            room[2] = False     # room is not clean
            room[4] = True      # room is occupied
            room_num = room[0]
            room_type = room[3]
            actual_checkin = fake.random_element([checkin, None])
            actual_checkout = None
            reservation = [id, guest_id, checkin, checkout,
                           room_num, room_type, actual_checkin, actual_checkout, hotel_id]
            reservations.append(reservation)
        else:
            # future
            # room # is null
            checkin = fake.date_between_dates(CUR_DATE + timedelta(days=random.randint(
                5, 10)), CUR_DATE + timedelta(days=random.randint(10, 400)))
            checkout = fake.date_between_dates(
                checkin, checkin + timedelta(days=random.randint(5, 10)))
            room = None
            room_type = fake.random_element(types)
            actual_checkin = fake.random_element([checkin, None])
            actual_checkout = None
            reservation = [id, guest_id, checkin, checkout,
                           room_num, room_type, actual_checkin, actual_checkout, hotel_id]
            reservations.append(reservation)
        # add occupants to reservation
        id += 1
    return reservations


def make_occupants(reservations):
    occupants = []
    seen_guests = set()
    for reservation in reservations:
        reserver = 0
        # Dont occupy future reservations
        if reservation[2] < CUR_DATE.date():
            # Add a guest to ensure that we make one for each reservation
            if not seen_guests.__contains__(reservation[1]):
                seen_guests.add(reservation[1])
                # When a new guest is seen, we want to occupy the first reservation with capacity - 1 (since the reserving guest takes up one spot)
                reserver = 1

            for type in room_types:
                # only for hotel 0
                if type[0] == reservation[5] and type[4] == 0:
                    # add occupants to the reservation (capacity - 1 for reserving guest)
                    for _ in range(type[2] - reserver):
                        occupants.append([reservation[0], fake.name()])
    return occupants


# creates 5 reviews per hotel
# currently not hotel specific since there's only reservations for hotel 0
def make_reviews(hotels, guests):
    reviews = []
    for hotel in hotels:
        for guest in range(6):
            review = []
            guest = random.choice(guests)
            review.append(guest[0])              # guest_id
            review.append(guest[1] + guest[2])   # display_name = first + last
            review.append(random.randint(1, 5))  # rating from 1 to 5 stars
            review.append(fake.text())           # comment
            # date of review before current date and after April 1, 1999
            review.append(fake.date_between(datetime(1999, 4, 1), CUR_DATE))
            reviews.append(review)
    return reviews


# creates 5 reviews for a given hotel
def make_specific_reviews(hotel_id, reservations):
    reviews = []
    # filters reservations to only list a specific hotel's reservations along
    # with only reservations that have actually happened
    fil_res = list(filter(lambda x: x[8] == hotel_id and x[7] != None,
                          reservations))
    for val in range(6):
        review = []
        reservation = random.choice(fil_res)
        review.append(reservation[1])  # guest_id
        review.append(fake.word())  # display_name
        review.append(random.randint(1, 5))  # rating from 1 to 5 stars
        review.append(fake.text())           # comment
        # date of review before current date and after checkout date
        review.append(fake.date_between(reservation[7], CUR_DATE))
        reviews.append(review)
    return reviews

def make_spa_services(hotels, services):
    spas = []
    # Facial, Massage, Pedicure, Manicure, Eyebrow Waxing, Mud Bath, Aromatherapy, Sauna, Steam Room
    # service_id, service_category, name, price, hotel_id
    for hotel in hotels:
        hotel_id = hotel[0]
        spa_service = [service for service in services if service[1] == 'Spa Service' and service[4] == hotel_id]
        if spa_service:
            spa = spa_service[0]

            spas.append([0, spa[0], "Spa Service", "Facial", round(random.uniform(25.0, 500.0), 2), hotel_id])
            spas.append([1, spa[0], "Spa Service", "Massage", round(random.uniform(25.0, 400.0), 2), hotel_id])
            spas.append([2, spa[0], "Spa Service", "Manicure", round(random.uniform(25.0, 200.0), 2), hotel_id])
            spas.append([3, spa[0], "Spa Service", "Eyebrow Waxing", round(random.uniform(15.0, 50.0), 2), hotel_id])
    return spas


hotel_features = ["Pool", "Gym", "Spa", "Restaurant", "Bar", "Room Service",
                  "Free Breakfast", "Free Parking", "Pet Friendly", "Airport Shuttle"]
room_feature = ["Pull Out Couch", "Balcony", "Work Desk", "Mini Fridge", "Microwave", "Coffee Maker", "Iron",
                "Hair Dryer", "Safe", "TV", "Jacuzzi Tub", "Fireplace", "Kitchenette", "Love Seat", "Cable", "Smart TV"]
service = [["Food Service", round(random.uniform(5.0, 200.0), 2)], ["Spa Service", round(random.uniform(50.0, 500.0), 2)], [
    "Laundry Service", round(random.uniform(5.0, 50.0), 2)], ["Valet", round(random.uniform(1.0, 20.0), 2)], ["Wake Up Call", round(random.uniform(1.0, 10.0), 2)]]
types = ["Queen 1 Bed", "Queen 2 Bed",
         "King 1 Bed", "Double Suite", "King Suite"]

guest_categories = [["VIP", .25], ["Military", .15], ["Government", .1], ["Senior", .65], ["Student", .1]]

guests = []
room_types = []
services = []
rooms = []
reservations = []
phones = set()

def main():
    hotels = make_hotels()

    employees = []
    seasons = []
    hotel_phones = []
    admins = []
    housekeeping = []
    cleaning_schedule_id = 1
    cleaning_schedules = []
    hotel_features = []
    room_features = []
    occupants = []
    bills = []
    g_categories = []
    reviews = []
    day_discounts = make_day_discounts()
    spa_services = []

    for hotel in hotels:
        hotel_room_types = make_room_types(hotel)  # 5 room types per hotel
        room_types.extend(hotel_room_types)
        # at least 3 of each room type
        rooms.extend(make_room(hotel, hotel_room_types))
        seasons.extend(make_seasons(hotel))  # at least 3 seasons per hotel
        # hotels have multiple phone numbers
        hotel_phones.extend(make_hotel_phones(hotel))
        # at least 10 employees per hotel
        employees.extend(make_employees(hotel))

        cl_sched, cl_sched_id = make_cleaning_schedule(cleaning_schedule_id)
        # each hotel should have a cleaning schedule for the current day
        cleaning_schedules.extend(cl_sched)
        # increment the schedule id so that each id is different
        cleaning_schedule_id += cl_sched_id

        hotel_features.append(make_hotel_features(hotel))
    guests.extend(make_guests())
    room_features.extend(make_room_features(room_types))
    reservations.extend(make_reservations(hotels[0]))
    bills.extend(make_bills(reservations))
    services.extend(make_services(reservations))
    spa_services.extend(make_spa_services(hotels, services))
    # print(spa_services)
    occupants.extend(make_occupants(reservations))
    g_categories.extend(make_guest_categories(hotels[0]))
    reviews.extend(make_specific_reviews(0, reservations))
    reviews.extend(make_reviews(hotels, guests))

    count = 0
    sched_id = 0  # schedule ids start at 1
    for employee in employees:
        if count < 100:  # bottom half of employee department_id
            admins.extend(make_admin(employee))
        else:
            # house keepers can have multiple schedules
            # each cleaning schedule goes to 10 cleaning employees per hotel
            housekeeping.extend(make_cleaning(
                employee, cleaning_schedules[sched_id]))
            if count % 10 == 0:
                sched_id += 1
        count += 1

    # seasons csv
    with open('seasons.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["season_id", "season_name",
                        "start_date", "end_date", "discount", "hotel_id"])
        for season in seasons:
            writer.writerow(season)

    # day discount csv
    with open('day_discount.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["weekday", "discount", "hotel_id"])
        for day in day_discounts:
            writer.writerow(day)

    # hotels csv
    with open('hotels.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["hotel_id", "name", "addess"])
        for h in hotels:
            writer.writerow(h)

    # hotel_phones csv
    with open('hotel_phones.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["hotel_id", "name", "number"])
        for phone in hotel_phones:
            writer.writerow(phone)

    # hotel features
    with open('hotel_features.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["hotel_id", "name"])
        for feature in hotel_features:
            writer.writerow(feature)

    # room_type csv
    with open('room_type.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["type_id", "price", "capacity", "sq_ft", "hotel_id"])
        for rt in room_types:
            writer.writerow(rt)

    # room_type features
    with open('room_features.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["type_id", "name", "hotel_id"])
        for feature in room_features:
            writer.writerow(feature)

    # room csv
    with open('room.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["room_num", "floor_num", "is_clean",
                        "type_id", "is_occupied", "hotel_id"])
        for room in rooms:
            writer.writerow(room)

    # guest csv
    with open('guest.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["guest_id", "first_name", "last_name",
                        "mobile_phone", "home_phone", "id_type", "id_number"])
        for guest in guests:
            writer.writerow(guest)

    # guest_categories csv
    with open('guest_categories.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["hotel_id", "guest_id", "category", "discount"])
        for category in g_categories:
            writer.writerow(category)

    # reservation csv
    with open('reservations.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["reservation_id", "guest_id", "checkin_date", "checkout_date",
                        "room_num", "type_id", "actual_checkin", "actual_checkout", "hotel_id"])
        for reservation in reservations:
            writer.writerow(reservation)

    # occupant csv
    with open('occupants.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["reservation_id", "name"])
        for occupant in occupants:
            writer.writerow(occupant)

    # bills csv
    with open('bills.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["guest_id", "bill_id", "total", "reservation_id"])
        for bill in bills:
            writer.writerow(bill)

    # services csv
    with open('services.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ["service_id", "name", "price", "guest_id", "hotel_id"])
        for service in services:
            writer.writerow(service)

    # spa_services csv
    with open('spa_services.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ["service_id", "service_cat_id", "service_cat", "name", "price", "hotel_id"])
        for service in spa_services:
            writer.writerow(service)

    # employee csv
    with open('employee.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["employee_id", "first_name", "last_name",
                        "job_title", "department_id", "hotel_id"])
        for employee in employees:
            writer.writerow(employee)

    # admin csv
    with open('admin.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["employee_id", "department_id"])
        for admin in admins:
            writer.writerow(admin)

    # cleaning csv
    with open('cleaning.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["employee_id", "department_id", "schedule_id"])
        for housekeeper in housekeeping:
            writer.writerow(housekeeper)

    # cleaning schedule
    with open('cleaning_schedule.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["employee_id", "department_id", "schedule_id"])
        for schedule in cleaning_schedules:
            writer.writerow(schedule)

    # reviews csv
    with open('reviews.csv', 'w', newline='',
              encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["guest_id", "display_name", "rating",
                         "comment", "date"])
        for review in reviews:
            writer.writerow(review)


if __name__ == "__main__":
    main()
