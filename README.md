# 📊 salespulse

A Flask-powered sales analytics dashboard for real-time insights into customer orders, product performance, and revenue trends — built as a freelance project and shared for portfolio purposes.

---

## 🎯 Overview

`salespulse` is a lightweight yet feature-rich order management and business intelligence system that enables small businesses to:
- Track clients, products, and orders in a unified interface  
- Analyze top-selling items and high-value customers  
- Visualize sales distribution by category and geography  
- Monitor daily revenue trends with interactive charts  
- Apply dynamic filters for focused data exploration  

All data is processed and visualized in real time using a clean MVC architecture on Flask and SQLite.

---

## ✨ Key Features

### 🗃️ Data Management
- **Client Registry**: Add customers with name, email (unique), phone, and country  
- **Product Catalog**: Define products with price, category, and metadata  
- **Order Processing**: Create orders linked to clients and products; total price auto-calculated (`price × quantity`)

### 📈 Analytics Engine
- **Sales Dashboard**: Real-time metrics — total orders, revenue, unique clients, average ticket  
- **Top Products**: Rank items by purchase frequency (top 5)  
- **Top Clients**: Identify highest-revenue customers (top 5)  
- **Category Breakdown**: Pie chart of sales by product category  
- **Geographic Insights**: Revenue distribution by client country  
- **Time-Series Trends**: Daily revenue line graph

### 🔍 Dynamic Filtering
- Filter clients by country  
- Filter products by category  
- Filter orders by client ID  
- Charts and tables update instantly based on active filters

### 📊 Interactive Visualizations
Powered by **Plotly** and rendered in-browser:
- Bar charts for top entities  
- Pie charts for proportional data  
- Line graphs for temporal trends  
- Responsive design for all screen sizes

---

## 🛠️ Tech Stack

| Layer          | Technology                     |
|----------------|-------------------------------|
| Language       | Python 3.8+                   |
| Web Framework  | Flask 3.1.2                   |
| ORM            | SQLAlchemy 2.0.43             |
| Database       | SQLite                        |
| Forms          | WTForms 3.2.1 + Flask-WTF     |
| Visualization  | Plotly 6.3.0                  |
| Templating     | Jinja2                        |
| Project Layout | MVC-style modular structure   |

### Database Schema
- **`clients`**: `id`, `firstname`, `lastname`, `email` (unique), `phone`, `country`
- **`products`**: `id`, `name`, `price`, `category`
- **`orders`**: `id`, `client_id`, `product_id`, `quantity`, `total_price`, `timestamp`

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- `pip`

### Installation
```bash
git clone https://github.com/tainj/salespulse.git
cd salespulse
pip install -r requirements.txt
python main.py
```

### Launch
Open your browser and navigate to:  
👉 **http://127.0.0.1:5000**

> The SQLite database (`db/store.db`) is auto-created on first run. Tables are generated from SQLAlchemy models at startup.

---

## 📂 Project Structure
```
salespulse/
├── app/
│   ├── db/              # Database session & engine
│   ├── form/            # WTForms definitions
│   ├── models/          # SQLAlchemy models (Client, Product, Order)
│   ├── routes/          # Flask view handlers
│   ├── templates/       # Jinja2 HTML templates
│   └── __init__.py      # Flask app factory
├── db/
│   └── store.db         # Auto-generated SQLite database
├── main.py              # Entry point
└── requirements.txt     # Dependencies
```

---

## 🖥️ Usage Examples

### Add a Client
1. Go to the homepage  
2. Fill the "Add Client" form (firstname, lastname, email, phone, country)  
3. Submit → client is persisted in SQLite

### Create an Order
1. Ensure at least one client and one product exist  
2. Enter client ID, select a product, specify quantity  
3. System auto-computes `total_price = product.price * quantity`  
4. Order timestamp defaults to current time (editable)

### View Analytics
Visit **`/report`** to access:
- Summary KPIs (orders, revenue, avg. ticket)  
- Interactive charts (products, clients, categories, countries, trends)  
- Full order history with relational data

---

## 📝 Portfolio Context

This project demonstrates:
- **Production-grade Flask architecture** (modular, maintainable, scalable)  
- **Robust data modeling** with SQLAlchemy ORM and relational integrity  
- **Form validation and error handling** via WTForms  
- **Business intelligence implementation** without external BI tools  
- **Client-ready UI/UX** with dynamic filtering and real-time updates  
- **Zero external dependencies** beyond Python standard ecosystem

While not deployed by the original client, `salespulse` serves as a reference implementation of a self-contained sales analytics system suitable for SMBs.

---

## 📄 License

Shared for educational and portfolio purposes only.