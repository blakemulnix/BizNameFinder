from geopy.geocoders import GoogleV3
import googlemaps
import pprint

# Set up geocoding and Places API clients
geocoder = GoogleV3(api_key='AIzaSyBv5vptmyqJifwC1M0brm8FO5i8gAXqsJQ')
places_client = googlemaps.Client(
    key='AIzaSyBv5vptmyqJifwC1M0brm8FO5i8gAXqsJQ')


def business_lookup(address):
    # Perform geocoding to retrieve the coordinates of the address
    location = geocoder.geocode(address)

    if location is not None:
        # Extract the latitude and longitude from the geocoding result
        lat = location.latitude
        lng = location.longitude

        street_address = location.address.split(',')[0]
        # print('street_address {}'.format(street_address))

        # Perform a place search request based on the coordinates
        places_result = places_client.places_nearby(
            location=(lat, lng),
            radius=50  # Adjust the radius as needed
        )

        # pprint.pprint(places_result)

        if 'results' in places_result and len(places_result['results']) > 0:
            for result in places_result['results']:
                if 'vicinity' in result and street_address in result['vicinity']:
                    name = result['name']
                    return name


address = '3657 Kimball Ave Waterloo Iowa 50702'
print('name {}'.format(business_lookup(address)))
