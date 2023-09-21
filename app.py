import requests
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime

# Mapping of airline abbreviations to full names
airline_mapping = {
    "ENT": "Enter Air",
    "BT": "Air Baltic",
    "DY": "Norwegian Air Shuttle",
    "SK": "SAS Scandinavian Airlines",
    "AY": "Finnair",
    "FI": "Icelandair",
    "LX": "Swiss International Air Lines",
    "DX": "DAT Danish Air Transport",
    "KL": "KLM Royal Dutch Airlines",
    "EK": "Emirates",
    "PC": "Pegasus Airlines",
    "TK": "Turkish Airlines",
    "WF": "Widerøe",
    "OS": "Austrian Airlines",
    "FR": "Ryanair",
    "N0": "Nordica",
    "AF": "Air France",
    "QR": "Qatar Airways",
    "D8": "Norwegian Air International",
    "LH": "Lufthansa",
    "BA": "British Airways",
    "DK": "Thomas Cook Airlines Scandinavia",
    "SN": "Brussels Airlines",
    "W6": "Wizz Air",
    "RK": "Royal Jordanian",
    "TP": "TAP Air Portugal",
    "LO": "LOT Polish Airlines",
    "ET": "Ethiopian Airlines",
    "RC": "Atlantic Airways",
    "LM": "Loganair",
    "A3": "Aegean Airlines",
    "LG": "Luxair",
    "IB": "Iberia Airlines",
    "EW": "Eurowings",
    "JU": "Jat Airways",
    "VY": "Vueling Airlines",
}

# Mapping of city abbreviations to full names
airports_mapping = {
    "JFK": "John F. Kennedy International Airport",
    "LAX": "Los Angeles International Airport",
    "ORD": "O'Hare International Airport",
    "DFW": "Dallas/Fort Worth International Airport",
    "ATL": "Hartsfield-Jackson Atlanta International Airport",
    "OLB": "Olbia Costa Smeralda Airport",
    "OSL": "Oslo Airport Gardermoen",
    "AES": "Ålesund Airport",
    "BOO": "Bodø Airport",
    "MME": "Durham Tees Valley Airport",
    "LGW": "London Gatwick Airport",
    "HEL": "Helsinki-Vantaa Airport",
    "SVG": "Stavanger Airport Sola",
    "LHR": "London Heathrow Airport",
    "BGO": "Bergen Airport Flesland",
    "TRD": "Trondheim Airport Værnes",
    "EVE": "Harstad/Narvik Airport Evenes",
    "KSU": "Kristiansund Airport Kvernberget",
    "CPH": "Copenhagen Airport",
    "KEF": "Keflavík International Airport",
    "HAU": "Haugesund Airport",
    "ARN": "Stockholm Arlanda Airport",
    "ZRH": "Zurich Airport",
    "FRO": "Florø Airport",
    "AMS": "Amsterdam Airport Schiphol",
    "KRS": "Kristiansand Airport Kjevik",
    "FAO": "Faro Airport",
    "DXB": "Dubai International Airport",
    "BLL": "Billund Airport",
    "SAW": "Sabiha Gökçen International Airport",
    "IST": "Istanbul Airport",
    "HOV": "Ørsta-Volda Airport Hovden",
    "BDU": "Bardufoss Airport",
    "FDE": "Ørland Airport",
    "GOT": "Gothenburg Landvetter Airport",
    "TOS": "Tromsø Airport",
    "VIE": "Vienna International Airport",
    "VNO": "Vilnius Airport",
    "AGP": "Malaga Airport",
    "LAX": "Los Angeles International Airport",
    "CDG": "Charles de Gaulle Airport",
    "DOH": "Hamad International Airport",
    "CTA": "Catania–Fontanarossa Airport",
    "PMI": "Palma de Mallorca Airport",
    "MOL": "Molde Airport",
    "DBV": "Dubrovnik Airport",
    "BRU": "Brussels Airport",
    "FRA": "Frankfurt Airport",
    "FCO": "Leonardo da Vinci–Fiumicino Airport",
    "DUS": "Düsseldorf Airport",
    "PSA": "Pisa International Airport",
    "NCE": "Nice Côte d'Azur Airport",
    "AAL": "Aalborg Airport",
    "RRS": "Røros Airport",
    "KKN": "Kirkenes Airport, Høybuktmoen",
    "GDN": "Gdańsk Lech Wałęsa Airport",
    "BER": "Berlin Brandenburg Airport",
    "BUD": "Budapest Ferenc Liszt International Airport",
    "STN": "London Stansted Airport",
    "ALF": "Alta Airport",
    "LIS": "Lisbon Airport",
    "MUC": "Munich Airport",
    "KTW": "Katowice Airport",
    "BCN": "Barcelona–El Prat Airport",
    "ALC": "Alicante–Elche Airport",
    "WAW": "Warsaw Chopin Airport",
    "ADD": "Addis Ababa Bole International Airport",
    "JFK": "John F. Kennedy International Airport",
    "AAR": "Aarhus Airport",
    "SZZ": "Szczecin-Goleniów Solidarność Airport",
    "PLQ": "Palanga International Airport",
    "RIX": "Riga International Airport",
    "OLA": "Ørland Airport",
    "SDN": "Sandane Airport, Anda",
    "TLL": "Tallinn Airport",
    "LPA": "Las Palmas de Gran Canaria Airport",
    "LYR": "Svalbard Airport",
    "KRK": "Krakow Airport",
    "MXP": "Milan Malpensa Airport",
    "EDI": "Edinburgh Airport",
    "PRG": "Prague Airport",
    "DUB": "Dublin Airport",
    "EWR": "Newark Liberty International Airport",
    "FAE": "Vágar Floghavn",
    "MAN": "Manchester Airport",
    "NCL": "Newcastle International Airport",
    "ATH": "Athens International Airport",
    "BEG": "Belgrade Nikola Tesla Airport",
    "LUX": "Luxembourg Airport",
    "HAM": "Hamburg Airport",
    "MAD": "Adolfo Suárez Madrid–Barajas Airport",
    "KGS": "Kos International Airport",
    "BLQ": "Bologna Airport",
    "CHQ": "Chania Airport",
    "SPU": "Split Airport",
    "FLR": "Florence Airport",
    "GVA": "Geneva Airport",
    "TRF": "Sandefjord Airport",
    "ABZ": "Aberdeen International Airport"
}

url = "https://flydata.avinor.no/XmlFeed.asp?TimeFrom=1&TimeTo=7&airport=BGO&direction=D&lastUpdate=2009-03-10T15:03:00Z"
xml_filename = "data.xml"
json_filename = "flights.json"

try:
    # Download XML data
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Save the content to the XML file
        with open(xml_filename, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {xml_filename} successfully.")
        
        # Load the XML data from the file
        tree = ET.parse(xml_filename)
        root = tree.getroot()
        
        flight_data = []
        current_date = datetime.now().date()
        
        for flight in root.findall('.//flight'):
            airline_abbreviation = flight.find('airline').text if flight.find('airline') is not None else ""
            airline_name = airline_mapping.get(airline_abbreviation, "")
            
            city_abbreviation = flight.find('airport').text if flight.find('airport') is not None else ""
            city_name = airports_mapping.get(city_abbreviation, "")
            
            schedule_time_str = flight.find('schedule_time').text if flight.find('schedule_time') is not None else ""
            
            # Parse the schedule_time as a datetime object
            
            schedule_time = datetime.strptime(schedule_time_str, "%Y-%m-%dT%H:%M:%SZ").date()
            # # Check if the flight is scheduled for the current date
            
            
            if schedule_time == current_date:
                flight_info = {
                    "uniqueID": flight.get("uniqueID"),
                    "airline": airline_name,
                    "flight_id": flight.find('flight_id').text if flight.find('flight_id') is not None else "",
                    "dom_int": flight.find('dom_int').text if flight.find('dom_int') is not None else "",
                    "schedule_time": schedule_time_str,
                    "arr_dep": flight.find('arr_dep').text if flight.find('arr_dep') is not None else "",
                    "airport": city_name,
                    "check_in": flight.find('check_in').text if flight.find('check_in') is not None else ""
                }
                flight_data.append(flight_info)
        
        # Create a dictionary to represent all the flight data
        flights_dict = {"flights": flight_data}
        
        # Convert the dictionary to a JSON string
        json_data = json.dumps(flights_dict, indent=2)
        
        # Save the JSON data to a file
        with open(json_filename, 'w') as json_file:
            json_file.write(json_data)
        
        print(f"Converted XML to {json_filename} successfully.")
        
        # Delete the XML file
        os.remove(xml_filename)
        print(f"Deleted {xml_filename}.")
        
    else:
        print(f"Failed to download content. Status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
