"""Database queries and functions."""

import psycopg
import socket
from faker import Faker
import datetime
import getpass


fake = Faker()

# Determine whether running on/off campus
# Note: PGUSER and PGPASSWORD must be set


def get_database_credentials():
    username = input("Enter your database username: ")
    password = getpass.getpass("Enter your database password: ")
    return username, password


# user, password = get_database_credentials()
try:
    socket.gethostbyname("data.cs.jmu.edu")
    # DSN = f"host=localhost dbname=jblv user={user} password={password}"
    DSN = "host=data.cs.jmu.edu dbname=jblv"
except:
    # DSN = f"host=localhost dbname=jblv user={user} password={password}"
    DSN = "host=localhost dbname=jblv"



def flight_search(airport, beg_date, end_date):
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM flight_search(%s, %s, %s)",
                        (airport, beg_date, end_date))
            return cur.fetchall()


def q1_reservations(hotel_id, checkin, checkout):
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM q1_reservations(%s, %s, %s)",
                        (hotel_id, checkin, checkout))
            return cur.fetchall()

def make_reservation(hotel_id, checkin, checkout, room, first_name,
                last_name, mobile_phone, home_phone, id_type, id_number):
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            guest_id = None

            # Check if guest already exists in database
            sql = """SELECT * FROM guest
                    WHERE first_name = %s AND last_name = %s"""
            cur.execute(sql, (first_name, last_name))
            check = cur.fetchone()

            if check == None:
                # Generate guest_id if guest doesn't currently exist
                cur.execute("SELECT MAX(guest_id) FROM guest")
                guest_id = cur.fetchone()[0] + 1

                # Add guest to the database
                sql = """INSERT INTO guest (guest_id, first_name, last_name, mobile_phone, home_phone, id_type, id_number)
                        VALUES(%s, %s, %s, %s, %s, %s, %s)"""
                args = (guest_id, first_name, last_name, mobile_phone, home_phone, id_type, id_number)
                cur.execute(sql, args)
            else:
                # Get guest_id
                guest_id = check[0]

            # Generate reseration_id
            cur.execute("SELECT MAX(reservation_id) FROM reservation")
            reservation_id = cur.fetchone()[0] + 1

            # Create reservation
            room_num = None
            type_id = room
            sql = """INSERT INTO reservation (reservation_id, guest_id, checkin_date,
                                                checkout_date, room_num, type_id, hotel_id)
                VALUES(%s, %s, %s, %s, %s, %s, %s)"""
            args = (reservation_id, guest_id, checkin, checkout, room_num, type_id, hotel_id)
            cur.execute(sql, args)

            return reservation_id


def q2(checkin, hotelid):
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_available_double_rooms(%s::DATE, %s)", (checkin,hotelid))
            return cur.fetchall()

def reserve_room_num(checkin, roomnum):
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            sql = """SELECT guest.guest_id, res.reservation_id, guest.first_name, guest.last_name
                    FROM reservation res
                    LEFT JOIN guest
                        ON res.guest_id = guest.guest_id
                    WHERE res.actual_checkin IS NULL
                        AND %s BETWEEN res.checkin_date AND res.checkout_date;"""
            cur.execute(sql, (checkin, ))
            return cur.fetchall()

def final_check_in(guestid, resid, roomnum, checkin):
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            # Create the booking
            sql = "UPDATE reservation SET actual_checkin = %s, room_num = %s WHERE guest_id = %s AND reservation_id = %s"
            args = (checkin, roomnum, guestid, resid)
            cur.execute(sql, args)  # will wait if table is locked
            print("update")

            # Fill rooms with occupants
            # Get Room Capacity
            sql = """SELECT rt.capacity
                    FROM room r JOIN room_type rt
                    ON r.type_id = rt.type_id
                    WHERE r.room_num = %s
                    AND r.hotel_id = rt.hotel_id"""
            cur.execute(sql, (roomnum, ))
            capacity = cur.fetchone()[0]
            # print("Capacity:", capacity)
            print("select")

            # Fill Occupants
            for _ in range(capacity):
                sql = "INSERT INTO occupant VALUES (%s, %s)"
                args = (resid, fake.name())
                cur.execute(sql, args)  # will wait if table is locked
            print("insert")

            # Information to be displayed
            return guestid

def q3(first_name, last_name, date):
    print("First Name:", first_name)  # Add console log
    print("Last Name:", last_name)  # Add console log
    print("Date:", date)  # Add console log
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_billing_statement(%s, %s, %s)",
                        (first_name, last_name, date))
            data = cur.fetchall()
            print("Data from Database:", data)  # Add console log
            return data


def final_check_out(firstname, lastname, date):
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            sql = """
                DO $$
                    DECLARE
                        guest_id_val INT;
                        f_reservation_id INT;
                        f_checkout_date DATE;
                        total_due NUMERIC;
                    BEGIN
                        -- Get guest_id
                        SELECT guest_id INTO guest_id_val FROM guest WHERE first_name = %s::TEXT AND last_name = %s::TEXT;

                        -- Update reservations with actual checkout date
                        SELECT reservation_id, actual_checkout INTO f_reservation_id, f_checkout_date FROM reservation WHERE guest_id = guest_id_val AND actual_checkout IS NULL LIMIT 1;
                        UPDATE reservation SET actual_checkout = %s::DATE WHERE reservation_id = f_reservation_id;

                        -- Delete occupant from occupants
                        DELETE FROM occupant WHERE reservation_id = f_reservation_id;

                        -- Update room status; set is_clean and is_occupied to False
                        UPDATE room SET is_clean = FALSE, is_occupied = FALSE WHERE room_num = (SELECT room_num FROM reservation WHERE reservation_id = f_reservation_id);

                        -- Get the total amount due from the billing statement
                        SELECT COALESCE(total_amount_due, 0) INTO total_due FROM get_billing_statement(%s::TEXT, %s::TEXT, %s::DATE);

                        -- Insert into the bill table
                        INSERT INTO bill (guest_id, bill_id, total, reservation_id) VALUES (guest_id_val, gen_random_uuid(), total_due, f_reservation_id);

                        -- Mark the room as clean
                        UPDATE room SET is_clean = TRUE WHERE room_num IN (SELECT room_num FROM reservation WHERE reservation_id = f_reservation_id);

                    END $$;
            """
            print("firstname:", firstname)
            # args = (firstname, lastname, date, firstname, lastname, date)
            # cur.execute(sql, args)
            cur.execute("SELECT * FROM checkout_and_generate_bill(%s, %s, %s)", (firstname, lastname, date))
            result = cur.fetchall()
            print("Final Check Out:", result)
            return result


def q4(maxprice):
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_spa_service(%s)", (maxprice,))
            return cur.fetchall()


def order_service(service, reservation_id):
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:

            # Get destination
            # Get a bill based on guest_id and reservation_id, make sure the spa service is for the current hotel
            sql = """SELECT g.guest_id, b.bill_id, b.total + ss.price
                    FROM guest g
                    JOIN bill b ON b.guest_id = g.guest_id
                    JOIN reservation r ON r.reservation_id = b.reservation_id
                    JOIN spa_service ss ON ss.hotel_id = r.hotel_id
                        WHERE r.reservation_id = %s
                        AND ss.name = %s"""
            cur.execute(sql, (reservation_id, service,))
            guest_id, bill_id, new_total = cur.fetchone()

            # Create the booking
            sql = "UPDATE bill SET total = %s WHERE guest_id = %s AND bill_id = %s AND reservation_id = %s"
            args = (new_total, guest_id, bill_id, reservation_id)
            cur.execute(sql, args)  # will wait if table is locked

            # Information to be displayed
            return new_total


if __name__ == "__main__":
    # print(flight_search("IAD", "2023-10-29", "2023-10-30"))
    # print(q2("2024-04-15"))
    pass
