from geopy.geocoders import GoogleV3
import googlemaps
from itertools import islice

# Geocoding and Places API clients
geocoder = GoogleV3(api_key='AIzaSyBv5vptmyqJifwC1M0brm8FO5i8gAXqsJQ')
places_client = googlemaps.Client(
    key='AIzaSyBv5vptmyqJifwC1M0brm8FO5i8gAXqsJQ')
types_to_filter = ['point_of_interest', 'establishment']

# Function to lookup business name and type of establishment at a given address


def business_lookup(address):
    location = geocoder.geocode(address)

    if location is not None:
        lat = location.latitude
        lng = location.longitude

        street_address = location.address.split(',')[0]
        address_number = address.split(' ')[0]

        places_result = places_client.places_nearby(
            location=(lat, lng),
            radius=50
        )

        # Find the place that has the matching street address and grab the name and types
        if 'results' in places_result and len(places_result['results']) > 0:
            for result in places_result['results']:
                if 'vicinity' in result and address_number in result['vicinity']:
                    name = result['name']
                    types = ', '.join(result['types'])

                    types = list(
                        filter(lambda x: x not in types_to_filter, result['types']))
                    return name, types

# Function to massage types into a more human readable form


def stringify_types(types):
    for type in types:
        type.replace('_', ' ')
    types = list(map(lambda x: x.replace('_', ' '), types))

    return ', '.join(types)


# Process list of address
# Print out business data in format for import to spreadsheet:
# address   business name   business type
input_path = "addresses.txt"
with open(input_path, "r") as file:
    addresses = file.readlines()

output_lines = []
for address in addresses[0: 5]:
    address = address.replace('\t', ' ').replace('\n', '')
    result = business_lookup(address)

    if result:
        name, types = result
        output_lines.append('{}\t{}\t{}'.format(
            address, name, stringify_types(types)))
        print('{}\t{}\t{}'.format(address, name, stringify_types(types)))
    else:
        output_lines.append('{}\t\t'.format(address))

output_path = 'output.txt'
with open(output_path, "w") as file:
    for line in output_lines:
        file.write(line + "\n")

print('Complete!')
