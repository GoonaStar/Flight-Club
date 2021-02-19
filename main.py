from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from pprint import pprint

data_manager = DataManager()
# sheet_data = data_manager.get_destination_data()
sheet_data = [{"city": "Paris", "iataCode": "PAR", "lowestPrice": 150000, "id": 2},
              {"city": "Bali", "iataCode": "BER", "lowestPrice": 69000, "id": 3},
              {"city": "London", "iataCode": "LDN", "lowestPrice": 45000, "id": 4},
              {"city": "Sydney", "iataCode": "SYD", "lowestPrice": 61000, "id": 5},
              {"city": "Istanbul", "iataCode": "IST", "lowestPrice": 52000, "id": 6},
              {"city": "Kuala Lumpur", "iataCode": "KUL", "lowestPrice": 45000, "id": 7},
              {"city": "New York", "iataCode": "NYC", "lowestPrice": 43000, "id": 8},
              {"city": "San Francisco", "iataCode": "SFO", "lowestPrice": 78000, "id": 9},
              {"city": "Cape Town", "iataCode": "CPT", "lowestPrice": 37800, "id": 10},
              {"city": "Bali", "iataCode": "DPS", "lowestPrice": 50100, "id": 11}]
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY_IATA = "HND"

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    if flight is None:
        continue

    if flight.price < destination["lowestPrice"]:
        yen = "¥"
        message = f"Low price alert! Only {yen.encode('utf-8')}{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
        if flight.stop_overs > 0:
            message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."
            print(message)

        notification_manager.send_sms(
            message=message
        )

        users = data_manager.get_customer_email()

        link = f"https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"

        for user in users:
            notification_manager.send_emails(user["emails"], message, link, user["name"])




