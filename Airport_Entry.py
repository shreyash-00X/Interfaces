import time
import pandas as pd
import string as stg
import random as ran
from datetime import datetime

# Constant charges
fuel_charges = 600
passenger_charges = 150
convenience_charge = 250
security_fees = 50
constant_charges = fuel_charges + passenger_charges + convenience_charge + security_fees

# Loading animation
def loading():
    a = '='
    for i in range(5):
        a += '='
        print(f'\r{a}', end='')
        time.sleep(1)
    print('\r Done ')

# Plane list
plane = {
    'Airbus A320': "A320",
    'Airbus A321': "A321",
    'Airbus A330': "A330",
    'Air India': "AI",
    'IndiGo': '6E',
    'Delta Air Lines': 'DL',
    'Emirates': 'EK'
}

plane_code = list(plane.values())
plane_name = list(plane.keys())

# Passenger details
def details():
    print("\n========== General Details ==========\n")
    while True:
        name = input("Passenger's first name: ").strip()
        if name:
            break
        print("First name cannot be empty!")

    sr_name = input("Enter last name: ")
    full_name = name + ' ' + sr_name

    while True:
        phone = input("Enter number: ")
        if len(phone) == 10 and phone.isdigit():
            phone = int(phone)
            break
        print("Invalid number, try again.")

    sex = input("Enter Sex (male/female): ").lower()
    if sex not in ['male', 'female']:
        sex = 'Not mentioned'

    return {"Name": full_name.title(), "Phone": phone, "Sex": sex.title()}

# Journey details
def location_details():
    print("\n========== Location Details ==========\n")
    while True:
        place_from = input("Ticket From: ")
        place_to = input("Ticket To: ")
        if place_from and place_to:
            break
        print("Required data missing!")

    flight = ran.choice(plane_name)
    return {"From": place_from.title(), "To": place_to.title(), "Flight Name": flight.title()}

# Seat generator
def seat():
    s = ran.choice(stg.ascii_uppercase)
    s += ran.choice(stg.digits)
    s += ran.choice(stg.digits)
    return {"Seat Number": s}

# Class & pricing
def typeclass():
    env = {
        "1": "Economy",
        "2": "Premium Economy",
        "3": "Business",
        "4": "First"
    }

    price_margin = {
        "Economy": 1600,
        "Premium Economy": 2000,
        "Business": 3000,
        "First": 4000
    }

    tax_per = {
        "Economy": 5,
        "Premium Economy": 8,
        "Business": 12,
        "First": 16
    }

    while True:
        print("\n---------- Available Classes ----------")
        print("1) Economy\n2) Premium Economy\n3) Business\n4) First")
        user = input("Enter class number: ")
        if user in env:
            tclass = env[user]
            class_amount = price_margin[tclass]
            gst = (class_amount * tax_per[tclass]) / 100
            return {"Class": tclass, "Class Amount": class_amount, "GST": gst}
        print("Invalid input, try again.")

# Generate PNR
def gen_id():
    value = ran.choice(plane_code) + "_"
    for _ in range(10):
        value += ran.choice(stg.digits)
    return {"PNR": value}

# Luggage calculation
def luggage_count(class_amount, gst, constant_charges):
    amt_per_luggage = 200
    special_bag_cost = 150

    while True:
        try:
            lug = int(input("Luggage Count: "))
            break
        except:
            print("Invalid input!")

    while True:
        try:
            spe = int(input("Special Bag Count: "))
            break
        except:
            print("Invalid input!")

    luggage_cost = lug * amt_per_luggage
    special_cost = spe * special_bag_cost

    total_cost = luggage_cost + special_cost
    final_amount = class_amount + gst + constant_charges + total_cost

    return {
        "Luggages": lug,
        "Special Bags": spe,
        "Cost on Luggage": luggage_cost,
        "Cost on Special Luggage": special_cost,
        "Total Charges": total_cost,
        "Total Amount": final_amount
    }

# Date & Time
def dandt():
    now = datetime.now()
    return {"Date": now.strftime("%d-%m-%y"), "Time": now.strftime("%H:%M")}

# Ticket display
def generate_ticket(data):
    ticket = f"""
==================================================
                    FLIGHT TICKET                   
==================================================

PNR:               {data['PNR']}
Date:              {data['Date']}
Time:              {data['Time']}

Name:              {data['Name']}
Sex:               {data['Sex']}

From:              {data['From']}
To:                {data['To']}

Flight Name:       {data['Flight Name']}
Seat Number:       {data['Seat Number']}

Class:             {data['Class']}
Class Amount:      {data['Class Amount'] + data['GST']} INR

Luggages:          {data['Luggages']}
Special Bags:      {data['Special Bags']}

Luggage Charges:       {data['Cost on Luggage']} INR
Special Bag Charges:   {data['Cost on Special Luggage']} INR

Total Charges:     {data['Total Charges']} INR
TOTAL AMOUNT:      {data['Total Amount']} INR

==================================================
"""
    print(ticket)

# Book Flight
def book_flight():
    user_details = details()
    loc = location_details()
    seat_no = seat()
    ticket = typeclass()
    pnr = gen_id()
    luggage = luggage_count(ticket["Class Amount"], ticket["GST"], constant_charges)
    dt = dandt()

    data = [user_details, loc, seat_no, ticket, pnr, luggage, dt]

    keys = []
    values = []
    for block in data:
        for k in block:
            keys.append(k)
            values.append(block[k])

    booking = dict(zip(keys, values))

    df = pd.DataFrame([booking])
    df.to_csv("Passenger_Entry.csv", index=False,
              mode='a', header=not pd.io.common.file_exists("Passenger_Entry.csv"))

    print("\nRecord Updated Successfully!\n")
    generate_ticket(booking)

    return booking

# View bookings
def view_bookings(datax):
    if datax is None:
        print("No previous booking.")
        return

    print("\n1. Previous Data")
    print("2. Saved Data\n")
    choice = input("Choose option: ")

    if choice == '1':
        generate_ticket(datax)

    elif choice == '2':
        print("Loading...")
        loading()
        print(pd.read_csv("Passenger_Entry.csv"))

    else:
        print("Invalid input")

# Record Book
def record_book():
    print("Loading...")
    loading()
    print(pd.read_csv("Passenger_Entry.csv"))

# Main menu
def main_menu():
    datax = None
    while True:
        print("\n================= Flight Booking System =================")
        print("1. Book a Flight")
        print("2. View My Bookings")
        print("3. Show Record Book")
        print("4. Exit\n")

        choice = input("Select option: ")

        if choice == '1':
            datax = book_flight()
        elif choice == '2':
            view_bookings(datax)
        elif choice == '3':
            record_book()
        elif choice == '4':
            print("Thank you for using the system!")
            loading()
            break
        else:
            print("Invalid choice!")

# Run program
if __name__ == "__main__":
    main_menu()
