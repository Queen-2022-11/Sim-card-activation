from flask import Flask, render_template, request, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your MySQL user
    password="",  # Replace with your MySQL password
    database="sim_activation"
)

# Function to check if SIM exists
def check_sim_exists(sim_number):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM sim_cards WHERE sim_number = %s", (sim_number,))
    sim = cursor.fetchone()
    cursor.close()
    return sim
# Function to add a new SIM card
def add_sim(sim_number, phone_number):
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO sim_cards (sim_number, phone_number, status) 
        VALUES (%s, %s, 'inactive')
    """, (sim_number, phone_number))
    db.commit()
    cursor.close()

# Route to serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')

# Route to add SIM details
@app.route('/add-sim', methods=['POST'])
def add_sim_card():
    data = request.json
    sim_number = data.get('sim_number')
    phone_number = data.get('phone_number')

    # Check if SIM already exists
    if check_sim_exists(sim_number):
        return jsonify({"error": "SIM card already exists"}), 400
    
    # Add SIM to the database
    add_sim(sim_number, phone_number)
    return jsonify({"message": "SIM card added successfully"}), 201


# 1. Activate SIM Card
@app.route('/activate', methods=['POST'])
def activate_sim():
    data = request.json
    sim_number = data.get('sim_number')
    
    sim = check_sim_exists(sim_number)
    if not sim:
        return jsonify({"error": "SIM card does not exist"}), 404
    
    if sim['status'] == 'active':
        return jsonify({"error": "SIM card is already active"}), 400
    
    cursor = db.cursor()
    activation_date = datetime.now()
    cursor.execute("""
        UPDATE sim_cards SET status = 'active', activation_date = %s 
        WHERE sim_number = %s
    """, (activation_date, sim_number))
    db.commit()
    cursor.close()
    
    return jsonify({"message": "SIM card activated successfully"}), 200

# 2. Deactivate SIM Card
@app.route('/deactivate', methods=['POST'])
def deactivate_sim():
    data = request.json
    sim_number = data.get('sim_number')
    
    sim = check_sim_exists(sim_number)
    if not sim:
        return jsonify({"error": "SIM card does not exist"}), 404
    
    if sim['status'] == 'inactive':
        return jsonify({"error": "SIM card is already inactive"}), 400
    
    cursor = db.cursor()
    cursor.execute("""
        UPDATE sim_cards SET status = 'inactive', activation_date = NULL 
        WHERE sim_number = %s
    """, (sim_number,))
    db.commit()
    cursor.close()
    
    return jsonify({"message": "SIM card deactivated successfully"}), 200

# 3. Get SIM Details
@app.route('/sim-details/<sim_number>', methods=['GET'])
def get_sim_details(sim_number):
    sim = check_sim_exists(sim_number)
    if not sim:
        return jsonify({"error": "SIM card does not exist"}), 404
    
    return jsonify(sim), 200

# Error handling for missing/invalid input
@app.errorhandler(400)
def bad_request(error=None):
    message = {
        'status': 400,
        'message': 'Bad Request: ' + request.url,
    }
    return jsonify(message), 400

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
