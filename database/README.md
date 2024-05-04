#  Database
## Description of each script file
* create.sql -- Drops and creates all tables for the database.
* alter.sql -- Adds all primary and foreign keys to the tables from create.sql
* eer_model.png -- EER diagram from [draw.io](https://www.drawio.com/) that depicts the conceptual model.
* rel_model.pgerd -- relational ERD (pgAdmin)

## Commands to run in terminal to build database
Define environment variables:
``` sh
export PGHOST=data.cs.jmu.edu
export PGDATABASE=jblv
export PGUSER=eid
export PGPASSWORD=student_number
```

Run the following commands to create the tables and relationships in the database:
``` sh
psql < create.sql
psql < alter.sql
```

## Changes made to conceptual model
* Clarified weak tables (Reservation, Cleaning Schedule, Review, Bill, Service)
* Changed attribute locations
* Modified relationships to be correct format
* Changed relationship cardinalities to better align with the project goals

## Relational Model Notes
## Added attributes to tables
* Added primary keys and foreign keys to tables
* Split name attribute in employee into first_name and last_name attributes
* Split name attribute in guest into first_name and last_name attributes

### Assumptions/Design Decisions
* Each guest category has a different discount value
* Can check if a Room is occupied by seeing if the Room’s GuestId is null (GuestId is null if the room is empty)
* The room is deemed ‘occupied’ on the check out date, so the cleaning service comes on that day
* You can make a reservation on someone else’s checkout day (checkout done in the morning and checkin done in the afternoon, giving a buffer for cleaning time)
* A room must have a cleaning schedule, even if it’s marked ‘do not clean’. A cleaning schedule keeps a list of reservations that require cleaning
* Available services provided by the hotel or room are derived from the room type and hotel.
* A reviewer is able to make only one review per account
* A reservation eventually gets a room number (null until checked in)
* A guest has to make multiple reservations for each room type to get a reservation with multiple rooms
* The spa is the added service and is not attached to the employees
