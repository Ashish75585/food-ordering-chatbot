# food-ordering-chatbot
Food Ordering Chatbot using Dialogflow and Flask A chatbot built using Dialogflow and Flask that allows users to order food, track their orders, and interact seamlessly with the backend. This project integrates NLP to handle order management and provides a simple user interface for food ordering.
# 🍔 Food Ordering Chatbot using Dialogflow and Flask

## 📚 **Overview**
A chatbot built using **Dialogflow** and **Flask** that allows users to order food, track their orders, and interact seamlessly.

## 🚀 **Features**
- Add and remove food items from the order.  
- Track order status.  
- Real-time communication with the backend server.

## 🛠️ **Tech Stack**
- **Dialogflow**  
- **Flask**  
- **MySQL**
- **ngrok**

## 💻 **Setup Instructions**

### Prerequisites:
- Python 3.x  
- Flask  
- MySQL  

### Installation:
1. Clone the repository:  
   ```bash
   git clone https://github.com/Ashish75585/food-ordering-chatbot.git
   cd food-ordering-chatbot
2. Install Dependencies:
   ```bash
   pip install -r requirements.txt

3. Set Up the Database
   - Open MySQL Workbench and create a new database.
   - Run the SQL script located at scripts/setup_database.sql (or wherever you have your database setup scripts). This will create the    necessary tables in the database.

4. Configure Database Connection
   Edit the db.py (or equivalent) file to match your MySQL database credentials:
   ```python
   DB_CONFIG = {
    "host": "localhost",
    "user": "your-username",
    "password": "your-password",
    "database": "food_order"  # Change this to your actual database name
}
5. Run the Application
```bash
python app.py

The app should now be running at `http://127.0.0.1:5000`.
   
