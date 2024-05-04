from flask import Flask, flash, redirect, request, render_template, url_for
from psycopg import DatabaseError
import db
import datetime
import getpass

app = Flask(__name__)
app.secret_key = "dev"
CURR_DATE = '2024-04-15'


@app.route("/")
def index():
    links = ["Reservation", "Check-In", "Check-Out", "Spa"]
    return render_template("index.html", links=links)


@app.route("/Reservation")
def q1():
    # Get form inputs with default values
    hotelid = request.args.get("hotelid", 0)
    checkin = request.args.get("checkin", CURR_DATE)
    checkout = request.args.get("checkout", CURR_DATE)
    if request.args:
        data = db.q1_reservations(hotelid, checkin, checkout)
    else:
        data = None
    return render_template("q1_reservations.html", hotelid=hotelid, checkin=checkin, checkout=checkout, data=data)


@app.route("/made_reservation")
def reserve():
    # Information already available
    hotelid = request.args.get("hotelid", 0)
    checkin = request.args.get("checkin", CURR_DATE)
    checkout = request.args.get("checkout", CURR_DATE)

    # Select room type
    room = request.args.get("room_id", "")

    # New information input
    first_name = request.args.get("first_name", "")
    last_name = request.args.get("last_name", "")
    mobile_phone = request.args.get("mobile_phone", '000-000-0000')
    home_phone = request.args.get("home_phone", '000-000-0000')
    id_type = request.args.get("id_type", "Passport")
    id_number = request.args.get("id_number", '123456789')

    if not all ([hotelid, checkin, checkout, room, first_name, last_name, mobile_phone, home_phone, id_type, id_number]):
        print(hotelid, checkin, checkout, room, first_name, last_name,
              mobile_phone, home_phone, id_type, id_number)
        return f"ERROR NOT ALL INFO {hotelid} {checkin} {checkout}"

    try:
        id = db.make_reservation(hotelid, checkin, checkout, room, first_name,
                                 last_name, mobile_phone, home_phone, id_type, id_number)
        flash(f"Reservation made for {first_name} {last_name}, id: {id}")
    except Exception as e:
        flash(e)

    return render_template("made_reservation.html")

checkin = None
roomnum = None
@app.route("/Check-In")
def q2():
    global checkin
    checkin = request.args.get("checkin", CURR_DATE)
    hotelid = request.args.get("hotelid", 0)
    if request.args:
        data = db.q2(checkin, hotelid)
    else:
        data = None
    return render_template("q2_checking_in.html", data=data, checkin=checkin, hotelid=hotelid)


@app.route("/reserve_room_num")
def checkin_hotel_reservation():
    global checkin
    global roomnum
    roomnum = request.args.get("room_num", -1)
    if roomnum == -1:
        return redirect("/Check-In")

    # print(checkin, roomnum)
    # if firstname and lastname:
    if roomnum:
        try:
            data = db.reserve_room_num(checkin, roomnum)
            if not data:
                flash("There are no reservations who need to be checked in at this date.")

        except DatabaseError as error:
            data = None
    return render_template("reserve_room_num.html", checkin=checkin, roomnum=roomnum, data=data)


@app.route("/final_check_in")
def final_check_in():
    global checkin
    global roomnum
    guestid = request.args.get("guestid", -1)
    resid = request.args.get("resid", -1)

    if guestid == -1:
        return redirect("/reserve_room_num")

    try:
        data = db.final_check_in(guestid, resid, roomnum, checkin)
        flash(f"Successfully checked in to {roomnum}")
    except DatabaseError as error:
        flash(error)
    return render_template("final_check_in.html", guestid=guestid, resid=resid, data=data)


@app.route("/Check-Out")
def q3():
    firstname = request.args.get("firstname", "")
    lastname = request.args.get("lastname", "")
    date = request.args.get("date", datetime.date.today())

    if request.args:
        data = db.q3(firstname, lastname, date)
    else:
        data = None
    return render_template("q3_checking_out.html", firstname=firstname, lastname=lastname, date=date, data=data)

@app.route("/final_check_out", methods=["POST"])
def final_check_out():
    firstname = request.form.get("firstname", "")
    lastname = request.form.get("lastname", "")
    date = request.form.get("date")

    if not all ([firstname, lastname, date]):
        print(firstname, lastname, date)
        return "ERROR NOT ALL INFO"

    try:
        result = db.final_check_out(firstname, lastname, date)
        print("Result", result)
        flash(f"Successfully checked out {firstname} {lastname}")
        return render_template("checkout_success.html")
    except Exception as e:
        flash(f"{firstname} {lastname} has already been checked out on {date}.")
        # flash("Error from sql as follows:")
        # flash(e)
        return render_template("checkout_success.html")

    return redirect(url_for("q3", firstname=firstname, lastname=lastname, date=date))

@app.route("/Spa")
def q4():
    # Get form inputs with default values
    maxprice = request.args.get("maxprice", 100.00)
    # If the user submitted the form
    if request.args:
        data = db.q4(maxprice)
    else:
        data = None
    return render_template("q4_special_feature.html", maxprice=maxprice, data=data)


@app.route("/order_service")
def order_service():
    # Make sure a flight was selected
    service_name = request.args.get("service_name", "")
    if not service_name:
        print("No service name provided")
        return redirect("/Spa")
    # Get inputs from this page's form
    reservation_id = request.args.get("reservation_id", 0)

    if reservation_id:
        try:
            total = db.order_service(service_name, reservation_id)
            flash(
                f"Successfully ordered {service_name} to reservation {reservation_id}; New bill total: {total}")
        except DatabaseError as error:
            flash(error)
    return render_template("order_service.html", service_name=service_name, reservation_id=reservation_id)

if __name__ == '__main__':
    app.run(debug=True, port=5432)