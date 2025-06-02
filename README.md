
# Overview

Inventory Maintainer is a smart warehouse management system that optimizes demand forecasting, inventory placement, and transportation logistics using machine learning and AI-driven recommendations.

![image](https://github.com/user-attachments/assets/5b8b92d1-a18c-4064-b622-17f5811383d5)

# Problem Statement

Traditional warehouse management faces several challenges:

Inaccurate Demand Forecasting: Manual forecasting leads to overstocking or understocking, causing financial losses and inventory waste.
Inefficient Storage Utilization: Poor warehouse layouts reduce space efficiency, increasing costs and retrieval time.
High Transportation Costs: Suboptimal stock distribution results in unnecessary transfers, leading to increased logistics costs and delays.

# Architecture Diagram
<img width="357" alt="image" src="https://github.com/user-attachments/assets/7004100f-83d7-48a6-92b6-24afd61cf2ef" />

# 🛠️ Solution

✅ Optimal Warehouse Assortment Selection
Machine Learning Models: Uses Random Forest, XGBoost, and Neural Networks to predict regional demand based on historical sales and external factors.
Generative AI for Inventory Placement: Recommends optimized warehouse assortment to minimize waste and maximize efficiency.
![image](https://github.com/user-attachments/assets/af0ffd8f-f719-4b35-9cd0-5d964bcbd44e)

🚚 Cost-Effective Parcel & Transportation Delivery
Route Optimization: Uses TomTom API and weather conditions to suggest the most cost-efficient delivery routes.

![image](https://github.com/user-attachments/assets/5e0cd65e-967d-4770-8183-9fcaf573def1)
![image](https://github.com/user-attachments/assets/461c3320-c57a-4a71-b4c6-6671e07babf7)
![image](https://github.com/user-attachments/assets/1a416970-88d9-44cd-ab2f-3c44bac34dfa)


🔄 Inventory Movement Recommendations
ML-Based Transfer Recommendations: Algorithms like XGBoost and Random Forest analyze inventory levels, demand forecasts, and transportation costs to recommend optimal stock transfers between warehouses.

![image](https://github.com/user-attachments/assets/f84fc635-de22-4baa-af23-db99904ef906)

# 🏗️ Tech Stack

📌 Frontend

Framework: Next.js 

UI: Tailwind CSS

Charts & Visualization: Chart.js


📌 Backend

Machine Learning: Scikit-learn, XGBoost, LSTM

AI Models: GROQ, Phi-data

Cloud API Integration: GROQ Cloud

📌 Database :
MySQL

📌 API Integrations : TomTom API (Route Optimization)
OpenWeather API (Weather-based Logistics Planning)
GROQ Cloud Platform API

## Authors

- [@kantinilesh](https://www.github.com/kantinilesh)
- [@Srijansarkar17](https://github.com/Srijansarkar17)
- [@Adityapratapsingh28](https://github.com/Adityapratapsingh28)

