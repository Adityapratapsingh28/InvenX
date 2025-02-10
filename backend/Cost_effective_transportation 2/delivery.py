import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants for Indian market
FUEL_PRICES = {
    "petrol": 100.80,  # INR per liter
    "diesel": 92.39,   # INR per liter
    "cng": 90.50      # INR per kg
}

# Fuel consumption rates (per km)
FUEL_CONSUMPTION = {
    "truck": {
        "diesel": 0.35,    # 3.5 km/L
        "cng": 0.40       # 4.0 km/kg
    },
    "van": {
        "diesel": 0.20,    # 5 km/L
        "petrol": 0.25,    # 4 km/L
        "cng": 0.25       # 4 km/kg
    },
    "car": {
        "petrol": 0.10,    # 10 km/L
        "diesel": 0.08,    # 12.5 km/L
        "cng": 0.12       # 8.3 km/kg
    }
}

# Per km maintenance cost in INR
MAINTENANCE_COST = {
    "truck": 5.0,  # INR per km
    "van": 3.0,    # INR per km
    "car": 2.0     # INR per km
}

def validate_api_keys():
    """Validate that required API keys are present"""
    tomtom_key = os.getenv("TOMTOM_API_KEY")
    weather_key = os.getenv("WEATHER_API_KEY")
    
    if not tomtom_key:
        raise ValueError("TOMTOM_API_KEY not found in environment variables")
    if not weather_key:
        raise ValueError("WEATHER_API_KEY not found in environment variables")
    
    return tomtom_key, weather_key

def validate_vehicle_fuel_combination(vehicle, fuel):
    """Validate if the chosen fuel type is available for the vehicle"""
    if fuel not in FUEL_CONSUMPTION[vehicle]:
        available_fuels = ", ".join(FUEL_CONSUMPTION[vehicle].keys())
        raise ValueError(f"Invalid fuel type for {vehicle}. Available options: {available_fuels}")

def get_user_input():
    # Get vehicle type
    while True:
        vehicle = input("\nEnter vehicle type (truck/van/car): ").lower()
        if vehicle in FUEL_CONSUMPTION:
            break
        print("❌ Invalid vehicle type. Please choose truck, van, or car.")
    
    # Get fuel type
    while True:
        print(f"\nAvailable fuel types for {vehicle}: {', '.join(FUEL_CONSUMPTION[vehicle].keys())}")
        fuel = input("Enter fuel type: ").lower()
        try:
            validate_vehicle_fuel_combination(vehicle, fuel)
            break
        except ValueError as e:
            print(f"❌ {str(e)}")
    
    # Get coordinates
    while True:
        try:
            start = input("\nEnter start coordinates (format: lat,lon): ")
            if len(start.split(",")) != 2:
                raise ValueError
            float(start.split(",")[0]), float(start.split(",")[1])
            break
        except ValueError:
            print("❌ Invalid coordinates. Please use format: latitude,longitude (e.g., 28.6139,77.2090)")
    
    while True:
        try:
            end = input("Enter end coordinates (format: lat,lon): ")
            if len(end.split(",")) != 2:
                raise ValueError
            float(end.split(",")[0]), float(end.split(",")[1])
            break
        except ValueError:
            print("❌ Invalid coordinates. Please use format: latitude,longitude (e.g., 19.0760,72.8777)")
    
    return vehicle, fuel, start, end

def calculate_costs(vehicle, fuel, distance_km):
    """Calculate all costs per kilometer and total"""
    
    # Fuel cost calculation
    fuel_consumption_per_km = FUEL_CONSUMPTION[vehicle][fuel]
    fuel_price_per_unit = FUEL_PRICES[fuel]
    fuel_cost_per_km = fuel_consumption_per_km * fuel_price_per_unit
    
    # Maintenance cost per km
    maintenance_cost_per_km = MAINTENANCE_COST[vehicle]
    
    # Total costs
    total_fuel_cost = fuel_cost_per_km * distance_km
    total_maintenance_cost = maintenance_cost_per_km * distance_km
    
    return {
        "per_km": {
            "fuel": fuel_cost_per_km,
            "maintenance": maintenance_cost_per_km,
            "total": fuel_cost_per_km + maintenance_cost_per_km
        },
        "total": {
            "fuel": total_fuel_cost,
            "maintenance": total_maintenance_cost,
            "total": total_fuel_cost + total_maintenance_cost
        }
    }

def main():
    print("\n🚚 Indian Delivery Cost Calculator 🚚")
    print("-" * 50)
    
    try:
        # Get user input
        vehicle, fuel, start, end = get_user_input()
        
        # For demonstration, using a fixed distance (you can replace with actual API call)
        # Example: Delhi to Mumbai is approximately 1,400 km
        distance_km = 1400  # You can replace this with actual API distance
        
        # Calculate costs
        costs = calculate_costs(vehicle, fuel, distance_km)
        
        # Display results
        print("\n" + "="*50)
        print(f"{'Delivery Cost Report':^50}")
        print("="*50)
        print(f"{'Vehicle Type:':<25} {vehicle.capitalize()}")
        print(f"{'Fuel Type:':<25} {fuel.capitalize()}")
        print(f"{'Fuel Price:':<25} ₹{FUEL_PRICES[fuel]:.2f} per {'kg' if fuel == 'cng' else 'liter'}")
        print(f"{'Distance:':<25} {distance_km:.1f} km")
        print("\nPer Kilometer Costs:")
        print("-"*50)
        print(f"{'Fuel Cost/km:':<25} ₹{costs['per_km']['fuel']:.2f}")
        print(f"{'Maintenance Cost/km:':<25} ₹{costs['per_km']['maintenance']:.2f}")
        print(f"{'Total Cost/km:':<25} ₹{costs['per_km']['total']:.2f}")
        print("\nTotal Journey Costs:")
        print("-"*50)
        print(f"{'Total Fuel Cost:':<25} ₹{costs['total']['fuel']:.2f}")
        print(f"{'Total Maintenance:':<25} ₹{costs['total']['maintenance']:.2f}")
        print("-"*50)
        print(f"{'TOTAL JOURNEY COST:':<25} ₹{costs['total']['total']:.2f}")
        print("="*50)
        
    except ValueError as e:
        print(f"\n❌ Error: {str(e)}")
    except Exception as e:
        print(f"\n❌ Unexpected Error: {str(e)}")
        print("Please try again or contact support if the problem persists")

if __name__ == "__main__":
    main()