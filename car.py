import pandas as pd
import os

CSV_PATH = "car_showroom.csv"
BILL_PATH = "bills.csv"

CSV_HEADER = [
    {"key": "car_model", "title": "Car Model"},
    {"key": "manufacturer", "title": "Manufacturer"},
    {"key": "year", "title": "Year"},
    {"key": "price", "title": "Price"},
    {"key": "quantity", "title": "Quantity"}
]

BILL_HEADER = [
    {"key": "buyer_name", "title": "Buyer Name"},
    {"key": "buyer_number", "title": "Buyer Number"},
    {"key": "job_certification", "title": "Job Certification"},
    {"key": "car_model", "title": "Car Model"},
    {"key": "quantity", "title": "Quantity"},
    {"key": "total_price", "title": "Total Price"}
]

def initialize_csv():
    if not os.path.exists(CSV_PATH):
        df = pd.DataFrame(columns=[header['key'] for header in CSV_HEADER])
        df.to_csv(CSV_PATH, index=False)
    if not os.path.exists(BILL_PATH):
        df = pd.DataFrame(columns=[header['key'] for header in BILL_HEADER])
        df.to_csv(BILL_PATH, index=False)

def add_car_record(car_dict):
    try:
        df = pd.read_csv(CSV_PATH)
        new_record = pd.DataFrame([car_dict])
        df = pd.concat([df, new_record], ignore_index=True)
        df.to_csv(CSV_PATH, index=False)
        print("-" * 60)
        print("Success: Car record added successfully!")
        print("-" * 60)
    except Exception as e:
        print("-" * 60)
        print(f"Error: An error occurred: {str(e)}")
        print("-" * 60)

def view_all_cars():
    try:
        if os.path.exists(CSV_PATH):
            df = pd.read_csv(CSV_PATH)
            print("-" * 60)
            print("All Car Records:")
            print(df)
            print("-" * 60)
        else:
            print("-" * 60)
            print("No car records found.")
            print("-" * 60)
    except Exception as e:
        print("-" * 60)
        print(f"Error: An error occurred: {str(e)}")
        print("-" * 60)

def search_car_by_model(model):
    try:
        if os.path.exists(CSV_PATH):
            df = pd.read_csv(CSV_PATH)
            result = df[df['car_model'] == model]
            if not result.empty:
                print("-" * 60)
                print("Car Record Found:")
                print(result)
                print("-" * 60)
            else:
                print("-" * 60)
                print("No car record found for the given model.")
                print("-" * 60)
        else:
            print("-" * 60)
            print("No car records found.")
            print("-" * 60)
    except Exception as e:
        print("-" * 60)
        print(f"Error: An error occurred: {str(e)}")
        print("-" * 60)

def sell_car():
    try:
        if os.path.exists(CSV_PATH):
            df = pd.read_csv(CSV_PATH)
            buyer_name = input("Enter buyer's name: ")
            buyer_number = input("Enter buyer's number: ")
            job_certification = input("Enter buyer's job certification: ")
            car_model = input("Enter car model to sell: ")
            quantity = int(input("Enter quantity to sell: "))

            car_record = df[df['car_model'] == car_model]
            if not car_record.empty:
                available_quantity = int(car_record['quantity'].values[0])
                price_per_unit = float(car_record['price'].values[0])
                if quantity <= available_quantity:
                    total_price = quantity * price_per_unit
                    new_quantity = available_quantity - quantity
                    df.loc[df['car_model'] == car_model, 'quantity'] = new_quantity
                    df.to_csv(CSV_PATH, index=False)

                    bill_dict = {
                        "buyer_name": buyer_name,
                        "buyer_number": buyer_number,
                        "job_certification": job_certification,
                        "car_model": car_model,
                        "quantity": quantity,
                        "total_price": total_price
                    }
                    bill_df = pd.read_csv(BILL_PATH)
                    new_bill = pd.DataFrame([bill_dict])
                    bill_df = pd.concat([bill_df, new_bill], ignore_index=True)
                    bill_df.to_csv(BILL_PATH, index=False)

                    print("-" * 60)
                    print("Bill Generated:")
                    print(new_bill)
                    print("-" * 60)
                else:
                    print("-" * 60)
                    print("Error: Not enough quantity available.")
                    print("-" * 60)
            else:
                print("-" * 60)
                print("Error: Car model not found.")
                print("-" * 60)
        else:
            print("-" * 60)
            print("No car records found.")
            print("-" * 60)
    except Exception as e:
        print("-" * 60)
        print(f"Error: An error occurred: {str(e)}")
        print("-" * 60)

def main():
    initialize_csv()
    while True:
        print("\n" + "-" * 60)
        print("Car Showroom Management")
        print("-" * 60)
        print("1. Add a new car record")
        print("2. View all car records")
        print("3. Search for a car by model")
        print("4. Sell a car")
        print("5. Exit")
        print("-" * 60)
        choice = input("Enter your choice: ")

        if choice == '1':
            car_model = input("Enter car model: ")
            manufacturer = input("Enter manufacturer: ")
            year = input("Enter year: ")
            price = input("Enter price: ")
            quantity = input("Enter quantity: ")
            car_dict = {
                "car_model": car_model,
                "manufacturer": manufacturer,
                "year": year,
                "price": price,
                "quantity": quantity
            }
            add_car_record(car_dict)
        elif choice == '2':
            view_all_cars()
        elif choice == '3':
            model = input("Enter car model to search: ")
            search_car_by_model(model)
        elif choice == '4':
            sell_car()
        elif choice == '5':
            break
        else:
            print("-" * 60)
            print("Invalid choice. Please try again.")
            print("-" * 60)

if __name__ == "__main__":
    main()