#api_key = 'AIzaSyBToJhU5VDk0V8UA9Gf_tQB_2acbud3W2k'
import googlemaps
import re

api_key ='AIzaSyBToJhU5VDk0V8UA9Gf_tQB_2acbud3W2k'

# Start and end locations
origin = '1175 Boylston St, Boston, MA 02215, United States'
destination = '820 Commonwealth Ave, Brookline, MA 02446, United States'

# User's choice of mode (walking, driving, or restroom)
mode = input("Choose a mode (walking or driving): ").lower()

if mode not in ['walking', 'driving', 'restroom']:
    print("Invalid mode. Please choose 'walking', 'driving', or 'restroom'.")
else:
    # Initialize Google Maps client
    gmaps = googlemaps.Client(key=api_key)

    # Define a function to remove HTML tags
    def clean_html_tags(text):
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    if mode == 'walking':
        # Find the directions from the origin to the destination
        directions = gmaps.directions(origin, destination, mode="walking")

        if not directions:
            print("No directions found.")
        else:
            restroom_directions = None
            restroom_location = None

            for i, step in enumerate(directions[0]['legs'][0]['steps']):
                instructions = step['html_instructions']  # Step-by-step instructions
                distance = step['distance']['text']  # Distance for the step

                # Remove HTML tags from instructions
                instructions = clean_html_tags(instructions)

                if restroom_location:
                    print(f"Step {i + 1}: {instructions} ({distance})")
                else:
                    print(f"Step {i + 1}: {instructions} ({distance})")

                # Check if there's a public restroom nearby
                keyword = "public restroom"
                lat = step['end_location']['lat']
                lng = step['end_location']['lng']

                places_result = gmaps.places_nearby(location=(lat, lng), radius=1000, keyword=keyword)

                if places_result['results']:
                    restroom_name = places_result['results'][0]['name']
                    restroom_location = places_result['results'][0]['vicinity']
                    print(f"   - There's a public restroom nearby: {restroom_name}")

                    restroom_choice = input("Do you want to go to the restroom (yes/no)? ").lower()

                    if restroom_choice == 'yes':
                        print("Redirecting to the restroom...")
                        restroom_directions = gmaps.directions(origin, restroom_location, mode="walking")
                        for j, restroom_step in enumerate(restroom_directions[0]['legs'][0]['steps']):
                            if j == 0:
                                continue  # Skip the first step (e.g., "Head northeast (213 ft)")
                            restroom_instructions = restroom_step['html_instructions']
                            distance = restroom_step['distance']['text']
                            restroom_instructions = clean_html_tags(restroom_instructions)
                            print(f"   - Restroom Step {j}: {restroom_instructions} ({distance})")

                        i += len(restroom_directions[0]['legs'][0]['steps'])

            if restroom_directions:
                print("Restroom reached.")

                for k, step in enumerate(directions[0]['legs'][0]['steps'][i:]):
                    instructions = step['html_instructions']
                    distance = step['distance']['text']
                    instructions = clean_html_tags(instructions)

                    # Skip the message about a nearby restroom for the rest of the route
                    if "There's a public restroom nearby:" not in instructions:
                        print(f"Step {i + k + 1}: {instructions} ({distance})")

            print("Destination reached.")

    if mode == 'driving':
        # Find the directions from the origin to the destination
        directions = gmaps.directions(origin, destination, mode="driving")

        if not directions:
            print("No directions found.")
        else:
            for i, step in enumerate(directions[0]['legs'][0]['steps']):
                instructions = step['html_instructions']  # Step-by-step instructions
                distance = step['distance']['text']  # Distance for the step

                # Remove HTML tags from instructions
                instructions = clean_html_tags(instructions)

                print(f"Step {i + 1}: {instructions} ({distance})")

                if i == len(directions[0]['legs'][0]['steps']) - 1:
                    # If it's the last step, search for parking spaces near the destination
                    destination_location = directions[0]['legs'][0]['end_location']
                    parking_spaces = gmaps.places_nearby(location=destination_location, radius=500, keyword="parking")

                    if parking_spaces['results']:
                        nearest_parking = parking_spaces['results'][0]
                        print(f"Nearest parking space: {nearest_parking['name']} ({nearest_parking['vicinity']})")

            print("Destination reached.")
