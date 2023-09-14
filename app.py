import xml.etree.ElementTree as ET
import json

# Load the XML data from your file
tree = ET.parse('XmlFeed.xml')
root = tree.getroot()

flight_data = []

for flight in root.findall('.//flight'):
    flight_info = {
        "uniqueID": flight.get("uniqueID"),
        "airline": flight.find('airline').text if flight.find('airline') is not None else "",
        "flight_id": flight.find('flight_id').text if flight.find('flight_id') is not None else "",
        "dom_int": flight.find('dom_int').text if flight.find('dom_int') is not None else "",
        "schedule_time": flight.find('schedule_time').text if flight.find('schedule_time') is not None else "",
        "arr_dep": flight.find('arr_dep').text if flight.find('arr_dep') is not None else "",
        "airport": flight.find('airport').text if flight.find('airport') is not None else "",
        "check_in": flight.find('check_in').text if flight.find('check_in') is not None else ""
    }
    flight_data.append(flight_info)

# Create a dictionary to represent all the flight data
flights_dict = {"flights": flight_data}

# Convert the dictionary to a JSON string
json_data = json.dumps(flights_dict, indent=2)

# Save the JSON data to a file
with open('flights.json', 'w') as json_file:
    json_file.write(json_data)
