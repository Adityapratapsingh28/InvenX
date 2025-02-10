from flask import Flask, request, jsonify, render_template
import requests
import pickle
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List
from scipy.optimize import linear_sum_assignment
import re
import os
from dotenv import load_dotenv
from groq import Groq
import mysql.connector
from mysql.connector import Error
load_dotenv()


app = Flask(__name__)

# Load the models
models = {
    'Warehouse1': pickle.load(open('model1.pkl', 'rb')),
    'Warehouse2': pickle.load(open('model2.pkl', 'rb')),
    'Warehouse3': pickle.load(open('model3.pkl', 'rb')),
    'Warehouse4': pickle.load(open('model4.pkl', 'rb'))
}
# Define products and warehouses
products = ['Product_0349', 'Product_2167', 'Product_0191', 'Product_1342', 'Product_1432']
warehouses = ['Warehouse1', 'Warehouse2', 'Warehouse3', 'Warehouse4']

DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'database': os.getenv('MYSQL_DATABASE', 'warehouse_management')
}

# Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)

def initialize_sequence(features):
    """Initialize sequence with random normal values scaled to reasonable range"""
    base = np.random.normal(50, 10, features)  # Generate base demands around 50 units
    sequence = np.tile(base, (1, 30, 1))  # Repeat for all timesteps
    return sequence

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def get_current_stock_levels():
    """Fetch current stock levels from database"""
    connection = get_db_connection()
    if not connection:
        return {}

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT warehouse_id, product_id, quantity 
            FROM stock_levels
        """)
        results = cursor.fetchall()

        # Format the results into the required structure
        current_stocks = {}
        for row in results:
            warehouse = row['warehouse_id']
            if warehouse not in current_stocks:
                current_stocks[warehouse] = {}
            current_stocks[warehouse][row['product_id']] = row['quantity']

        return current_stocks

    except Error as e:
        print(f"Error fetching stock levels: {e}")
        return {}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def update_stock_level(warehouse_id, product_id, quantity):
    """Update stock level for a specific product in a warehouse"""
    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE stock_levels 
            SET quantity = %s 
            WHERE warehouse_id = %s AND product_id = %s
        """, (quantity, warehouse_id, product_id))
        
        connection.commit()
        return True

    except Error as e:
        print(f"Error updating stock level: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def forecast_next_days(model, days, features):
    predictions = []
    
    # Initialize with realistic values instead of zeros
    sequence = initialize_sequence(features)
    
    for _ in range(days):
        try:
            # Make prediction using the current sequence
            prediction = model.predict(sequence, verbose=0)
            
            # Apply activation to ensure non-negative values
            prediction = np.maximum(prediction, 0)  # ReLU-like activation
            
            # Add some randomness to avoid static predictions
            noise = np.random.normal(0, 2, prediction.shape)
            prediction = prediction + noise
            
            predictions.append(prediction[0])
            
            # Update sequence by shifting the time window
            sequence = np.roll(sequence, -1, axis=1)
            sequence[0, -1, :] = prediction[0]
            
        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            print(f"Input shape: {sequence.shape}")
            raise e
    
    return np.array(predictions)

def generate_recommendations(transfer_details):
    """Generate recommendations using Groq Gemma model."""
    messages = [
        {
            "role": "system",
            "content": "You are a warehouse distribution expert."
        },
        {
            "role": "user",
            "content": f"""Based on the following transfer details, suggest the optimal way to move items between warehouses:

Transfer Details:
{transfer_details}

Provide clear and actionable recommendations in simple language."""
        }
    ]

    try:
        # Use the Groq Gemma model
        response = groq_client.chat.completions.create(
            model="gemma2-9b-it",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        # Correctly access the response content
        if response and response.choices and len(response.choices) > 0:
            recommendation = response.choices[0].message.content
            return recommendation.strip()
        else:
            return "No recommendation generated"
            
    except Exception as e:
        return f"Error generating recommendations: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/forecast', methods=['POST'])
def get_forecast():
    try:
        data = request.json
        warehouse_type = data['warehouse']
        days = int(data['days'])
        
        if warehouse_type not in models:
            return jsonify({'error': 'Invalid warehouse type'}), 400
        
        if days not in [10, 20, 30, 40]:
            return jsonify({'error': 'Invalid number of days'}), 400
        
        model = models[warehouse_type]
        
        # Map warehouses to their feature dimensions
        feature_dims = {
            'Warehouse1': 24,
            'Warehouse2': 18,
            'Warehouse3': 83,
            'Warehouse4': 265
        }
        
        # Get forecast using the unified function
        forecast_data = forecast_next_days(model, days, feature_dims[warehouse_type])
        
        # Create dates for the forecast period
        dates = [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days)]
        
        # Create response data
        products = ['Product_0349', 'Product_2167', 'Product_0191', 'Product_1342', 'Product_1432']
        
        # Ensure we only return data for available products
        n_products = min(len(products), forecast_data.shape[1])
        products = products[:n_products]
        
        # Apply post-processing to make predictions more realistic
        forecast_data = np.maximum(forecast_data, 0)  # Ensure non-negative values
        forecast_data = np.round(forecast_data)  # Round to whole numbers
        
        response_data = {
            'dates': dates,
            'predictions': {
                products[i]: forecast_data[:, i].tolist() for i in range(n_products)
            }
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Add these new routes to your Flask application

@app.route('/optimize-distribution', methods=['POST'])
def optimize_distribution():
    try:
        data = request.json
        forecasts = data.get('forecasts', {})

        # Get current stocks from database instead of request
        current_stocks = get_current_stock_levels()

        # Validate data
        if not current_stocks or not forecasts:
            return jsonify({'error': 'Missing stock data or forecasts'}), 400

        distribution = calculate_optimal_distribution(current_stocks, forecasts)
        return jsonify(distribution)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def calculate_optimal_distribution(current_stocks, forecasts):
    """
    Calculate the optimal distribution of stock across warehouses
    """
    distribution = {
        'requiredStock': {},
        'surplus': {},
        'orderNeeded': {},
        'transfers': {}
    }

    # Calculate total demand for each product in each warehouse
    for product in products:
        distribution['requiredStock'][product] = {}
        distribution['surplus'][product] = {}
        distribution['orderNeeded'][product] = 0

        totalRequired = 0
        totalCurrentStock = 0

        for warehouse in warehouses:
            # Ensure the product exists in the forecasts
            if product not in forecasts[warehouse]['predictions']:
                continue

            demands = forecasts[warehouse]['predictions'][product]
            required = sum(demands)
            current = current_stocks.get(warehouse, {}).get(product, 0)

            distribution['requiredStock'][product][warehouse] = required
            distribution['surplus'][product][warehouse] = current - required

            totalRequired += required
            totalCurrentStock += current

        distribution['orderNeeded'][product] = max(0, totalRequired - totalCurrentStock)

    # Calculate transfer recommendations
    distribution['transfers'] = recommend_stock_transfers(distribution)

    return distribution

import numpy as np

# Assume constant distances for simplicity (km)
DISTANCE_MATRIX = {
    'Warehouse1': {
        'Warehouse1': 0, 
        'Warehouse2': 100, 
        'Warehouse3': 200, 
        'Warehouse4': 300
    },
    'Warehouse2': {
        'Warehouse1': 100, 
        'Warehouse2': 0, 
        'Warehouse3': 150, 
        'Warehouse4': 250
    },
    'Warehouse3': {
        'Warehouse1': 200, 
        'Warehouse2': 150, 
        'Warehouse3': 0, 
        'Warehouse4': 100
    },
    'Warehouse4': {
        'Warehouse1': 300, 
        'Warehouse2': 250, 
        'Warehouse3': 100, 
        'Warehouse4': 0
    }
}

# Estimated transportation cost per km ($/km)
TRANSPORT_COST_PER_KM = 0.5

def calculate_transfer_cost(source, destination, quantity):
    """
    Calculate transportation cost between warehouses
    
    Args:
        source (str): Source warehouse
        destination (str): Destination warehouse
        quantity (float): Quantity of goods to transfer
    
    Returns:
        float: Total transportation cost
    """
    distance = DISTANCE_MATRIX[source][destination]
    cost = distance * TRANSPORT_COST_PER_KM * quantity
    return cost

def recommend_stock_transfers(distribution):
    transfers = {}

    for product in products:
        transfers[product] = []

        # Find warehouses with surplus and deficit
        surplus_warehouses = [w for w in warehouses if distribution['surplus'][product][w] > 0]
        deficit_warehouses = [w for w in warehouses if distribution['surplus'][product][w] < 0]

        for deficit_wh in deficit_warehouses:
            deficit_amount = abs(distribution['surplus'][product][deficit_wh])

            # Find best source warehouse with minimum transfer cost
            best_source = min(
                surplus_warehouses,
                key=lambda source: calculate_transfer_cost(source, deficit_wh, deficit_amount)
            )

            transfer_cost = calculate_transfer_cost(best_source, deficit_wh, deficit_amount)

            transfers[product].append({
                'from': best_source,
                'to': deficit_wh,
                'quantity': deficit_amount,
                'cost': transfer_cost
            })

    return transfers

@app.route('/ai-recommendations', methods=['POST'])
def ai_recommendations():
    """Get AI-generated recommendations for transfers."""
    try:
        data = request.json
        transfer_details = data.get('transfer_details', {})

        if not transfer_details:
            return jsonify({"error": "No transfer details provided"}), 400

        # Generate recommendations using Groq Gemma model
        recommendations = generate_recommendations(transfer_details)

        return jsonify({"recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/update-stock', methods=['POST'])
def update_stock():
    try:
        data = request.json
        warehouse_id = data.get('warehouse')
        product_id = data.get('product')
        quantity = data.get('quantity')

        if not all([warehouse_id, product_id, quantity]):
            return jsonify({'error': 'Missing required fields'}), 400

        success = update_stock_level(warehouse_id, product_id, quantity)
        if success:
            return jsonify({'message': 'Stock level updated successfully'})
        else:
            return jsonify({'error': 'Failed to update stock level'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)