from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import re
import requests
from datetime import datetime

app = Flask(__name__)

# Load environment variables
load_dotenv()



# Constants
FUEL_PRICES = {
    "petrol": 100.80,
    "diesel": 92.39,
    "cng": 90.50
}

FUEL_CONSUMPTION = {
    "truck": {"diesel": 0.35, "cng": 0.40,"petrol":0.30},
    "van": {"diesel": 0.20, "petrol": 0.25, "cng": 0.25},
    "car": {"petrol": 0.10, "diesel": 0.08, "cng": 0.12}
}

MAINTENANCE_COST = {
    "truck": 5.0,
    "van": 3.0,
    "car": 2.0
}

def validate_vehicle_fuel_combination(vehicle, fuel):
    if fuel not in FUEL_CONSUMPTION[vehicle]:
        available_fuels = ", ".join(FUEL_CONSUMPTION[vehicle].keys())
        raise ValueError(f"Invalid fuel for {vehicle}. Choose: {available_fuels}")

def calculate_costs(vehicle, fuel, distance):
    fuel_consumption = FUEL_CONSUMPTION[vehicle][fuel]
    fuel_price = FUEL_PRICES[fuel]
    
    fuel_cost_km = fuel_consumption * fuel_price
    maintenance_km = MAINTENANCE_COST[vehicle]
    
    return {
        "per_km": {
            "fuel": round(fuel_cost_km, 2),
            "maintenance": maintenance_km,
            "total": round(fuel_cost_km + maintenance_km, 2)
        },
        "total": {
            "fuel": round(fuel_cost_km * distance, 2),
            "maintenance": round(maintenance_km * distance, 2),
            "total": round((fuel_cost_km + maintenance_km) * distance, 2)
        }
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    form_data = request.form.to_dict() if request.method == 'POST' else {}
    return render_template('index.html', form_data=form_data)

def get_tomtom_distance(start_coords, end_coords, api_key):
    """Get route distance using TomTom API with proper coordinate formatting"""
    formatted_coords = f"{start_coords.replace(' ', '')}:{end_coords.replace(' ', '')}"
    url = f"https://api.tomtom.com/routing/1/calculateRoute/{formatted_coords}/json"
    params = {
        'key': api_key,
        'traffic': 'true',
        'routeType': 'fastest',
        'travelMode': 'truck',
        'avoid': 'unpavedRoads'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if not data.get('routes'):
            raise ValueError("No routes found between these coordinates")
        route = data['routes'][0]
        return route['summary']['lengthInMeters'] / 1000  # Convert to km
    except requests.exceptions.HTTPError as e:
        error_msg = f"TomTom API Error: {e.response.status_code} - {e.response.text}"
        raise Exception(error_msg)
    except KeyError:
        raise Exception("Unexpected API response format")

def get_tomtom_routes(start_coords, end_coords, api_key):
    """Get multiple routes (fastest and eco) from TomTom API"""
    formatted_coords = f"{start_coords.replace(' ', '')}:{end_coords.replace(' ', '')}"
    base_url = f"https://api.tomtom.com/routing/1/calculateRoute/{formatted_coords}/json"
    
    route_types = [
        {"type": "fastest", "color": "red", "params": {"routeType": "fastest", "travelMode": "truck"}},
        {"type": "eco", "color": "green", "params": {"routeType": "eco", "travelMode": "truck"}},
    ]
    
    routes = []
    for route_type in route_types:
        params = {
            'key': api_key,
            'traffic': 'true',
            'avoid': 'unpavedRoads',
            **route_type['params']
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('routes'):
                raise ValueError(f"No {route_type['type']} route found between these coordinates")
            
            route = data['routes'][0]
            route['color'] = route_type['color']  # Add color to the route
            routes.append(route)
        except requests.exceptions.HTTPError as e:
            error_msg = f"TomTom API Error ({route_type['type']} route): {e.response.status_code} - {e.response.text}"
            raise Exception(error_msg)
        except KeyError:
            raise Exception(f"Unexpected API response format for {route_type['type']} route")
    
    return routes

def get_weather_data(lat, lon, api_key):
    """Fetch weather data using OpenWeatherMap API"""
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        error_msg = f"Weather API Error: {e.response.status_code} - {e.response.text}"
        raise Exception(error_msg)

def get_nearby_places(coords, category, api_key, radius=5000):
    """Fetch nearby places (hotels, restaurants, fuel stations) using TomTom Places API"""
    url = f"https://api.tomtom.com/search/2/nearbySearch/.json"
    params = {
        'key': api_key,
        'lat': coords[0],
        'lon': coords[1],
        'radius': radius,
        'categorySet': category,
        'limit': 10  # Limit the number of results
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])
    except requests.exceptions.HTTPError as e:
        error_msg = f"TomTom Places API Error: {e.response.status_code} - {e.response.text}"
        raise Exception(error_msg)

def get_pois(lat, lon, category, api_key, radius=5000):
    """Get points of interest using TomTom Search API"""
    url = "https://api.tomtom.com/search/2/nearbySearch/.json"
    params = {
        'key': api_key,
        'lat': lat,
        'lon': lon,
        'radius': radius,
        'categorySet': category,
        'limit': 5
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])
    except Exception as e:
        print(f"POI API Error: {str(e)}")
        return []

def get_route_pois(route_coords, api_key):
    """Get POIs along a route with sampling"""
    pois = {'hotel': [], 'restaurant': [], 'fuel': []}
    
    # Sample every 10th coordinate to reduce API calls
    for i, coord in enumerate(route_coords[::10]):
        lat, lon = coord
        
        # Get hotels
        hotels = get_pois(lat, lon, '7314', api_key)
        for hotel in hotels:
            pois['hotel'].append({
                'name': hotel['poi'].get('name'),
                'lat': hotel['position']['lat'],
                'lon': hotel['position']['lon']
            })
            
        # Get restaurants
        restaurants = get_pois(lat, lon, '7315', api_key)
        for rest in restaurants:
            pois['restaurant'].append({
                'name': rest['poi'].get('name'),
                'lat': rest['position']['lat'],
                'lon': rest['position']['lon']
            })
            
        # Get fuel stations
        fuel_stations = get_pois(lat, lon, '7311', api_key)
        for fuel in fuel_stations:
            pois['fuel'].append({
                'name': fuel['poi'].get('name'),
                'lat': fuel['position']['lat'],
                'lon': fuel['position']['lon']
            })
    
    return pois

def get_pois_along_route(route, category, api_key, radius=5000, max_pois=15):
    """
    Fetch POIs along the route using TomTom Places API with distributed sampling:
    33% at start, 33% at middle, and 34% at end of route
    """
    pois = []
    waypoints = route['legs'][0]['points']
    total_points = len(waypoints)
    
    # Calculate points per section
    points_per_section = max_pois // 3
    remaining_points = max_pois % 3  # Add remaining to end section
    
    # Define sections
    start_section = waypoints[:total_points // 3]
    mid_section = waypoints[total_points // 3:2 * total_points // 3]
    end_section = waypoints[2 * total_points // 3:]
    
    # Function to sample points from a section
    def sample_section(section, num_points):
        if not section:
            return []
        
        step = max(1, len(section) // num_points)
        section_pois = []
        
        for i in range(0, len(section), step):
            if len(section_pois) >= num_points:
                break
                
            point = section[i]
            coords = [point['latitude'], point['longitude']]
            nearby_pois = get_nearby_places(coords, category, api_key, radius)
            section_pois.extend(nearby_pois[:num_points])
        
        return section_pois[:num_points]
    
    # Sample POIs from each section
    start_pois = sample_section(start_section, points_per_section)
    mid_pois = sample_section(mid_section, points_per_section)
    end_pois = sample_section(end_section, points_per_section + remaining_points)
    
    # Combine all POIs
    pois.extend(start_pois)
    pois.extend(mid_pois)
    pois.extend(end_pois)
    
    return pois[:max_pois]

def geocode_location(location_name, api_key):
    """Convert a location name (e.g., 'Delhi') to latitude and longitude using TomTom Geocoding API."""
    url = f"https://api.tomtom.com/search/2/geocode/{location_name}.json"
    params = {
        'key': api_key,
        'limit': 1  # Only return the top result
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if not data.get('results'):
            raise ValueError(f"No results found for location: {location_name}")
        result = data['results'][0]
        lat = result['position']['lat']
        lon = result['position']['lon']
        return f"{lat},{lon}"
    except requests.exceptions.HTTPError as e:
        error_msg = f"Geocoding API Error: {e.response.status_code} - {e.response.text}"
        raise Exception(error_msg)
    

def format_time(seconds):
    minutes = seconds // 60
    hours = minutes // 60
    minutes = minutes % 60
    return {'hours': hours, 'minutes': minutes}

@app.route('/calculate', methods=['POST'])
def calculate():
    form_data = request.form.to_dict()
    try:
        tomtom_key = os.getenv("TOMTOM_API_KEY")
        weather_key = os.getenv("WEATHER_API_KEY")
        if not tomtom_key or not weather_key:
            raise ValueError("API keys not configured")

        # Get start and end locations
        start_input = form_data['start'].strip()
        end_input = form_data['end'].strip()

        # Geocode start and end locations if they are not coordinates
        if not re.match(r'^-?\d+\.?\d*,-?\d+\.?\d*$', start_input):
            start = geocode_location(start_input, tomtom_key)
        else:
            start = start_input

        if not re.match(r'^-?\d+\.?\d*,-?\d+\.?\d*$', end_input):
            end = geocode_location(end_input, tomtom_key)
        else:
            end = end_input

        # Calculate routes and get times
        routes = get_tomtom_routes(start, end, tomtom_key)
        fastest_time = routes[0]['summary']['travelTimeInSeconds']
        eco_time = routes[1]['summary']['travelTimeInSeconds']
        
        # Calculate distance from the fastest route
        distance_km = routes[0]['summary']['lengthInMeters'] / 1000
        if distance_km <= 0:
            raise ValueError("Could not calculate valid route distance")

        # Get weather data
        weather_start = get_weather_data(*start.split(','), weather_key)
        weather_end = get_weather_data(*end.split(','), weather_key)

        # Fetch POIs along the route
        pois = {
            'hotels': get_pois_along_route(routes[0], '7314', tomtom_key, max_pois=15),
            'restaurants': get_pois_along_route(routes[0], '7315', tomtom_key, max_pois=15),
            'fuel': get_pois_along_route(routes[0], '7311', tomtom_key, max_pois=15),
        }

        vehicle = form_data['vehicle'].lower()
        fuel = form_data['fuel'].lower()

        validate_vehicle_fuel_combination(vehicle, fuel)
        costs = calculate_costs(vehicle, fuel, distance_km)

        # Calculate route differences
        time_diff = eco_time - fastest_time
        time_diff_minutes = time_diff // 60
        distance_diff = (routes[1]['summary']['lengthInMeters'] - routes[0]['summary']['lengthInMeters']) / 1000

        report = {
            'vehicle': vehicle.capitalize(),
            'fuel': fuel.capitalize(),
            'fuel_price': FUEL_PRICES[fuel],
            'fuel_unit': 'kg' if fuel == 'cng' else 'liter',
            'distance': round(distance_km, 2),
            'per_km': costs['per_km'],
            'total': costs['total'],
            'routes': routes,
            'route_comparison': {
                'time_diff_minutes': int(time_diff_minutes),
                'distance_diff': round(distance_diff, 2)
            },
            'weather_start': weather_start,
            'weather_end': weather_end,
            'pois': pois,
            'start': start_input,
            'end': end_input,
            'time': {
                    'fastest': format_time(fastest_time),
                    'eco': format_time(eco_time)
                },
        }

        return render_template('index.html', report=report, form_data=form_data)

    except Exception as e:
        return render_template('index.html', error=str(e), form_data=form_data)
if __name__ == '__main__':
    app.run(debug=True)