from hashlib import md5
from os import remove, path
import sqlite3
from flask import Flask, request, render_template, session

app = Flask(__name__)

if path.exists('products.db'):
	remove('products.db')

with sqlite3.connect('products.db', check_same_thread=False) as conn:
	cursor = conn.cursor()

	cursor.executescript('''
		CREATE TABLE IF NOT EXISTS products (id integer PRIMARY KEY, name text, price real, quantity integer);
		CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, username text, hash text, user_type text)
	''')

	conn.commit()

def populate_db():
	products = [
		("Apples", 1.99, 20),
		("Bananas", 0.99, 15),
		("Broccoli", 2.49, 12),
		("Carrots", 1.29, 18),
		("Cereal", 3.99, 10),
		("Cheese", 4.99, 8),
		("Chicken", 5.99, 6),
		("Eggs", 2.29, 24),
		("Milk", 1.99, 20),
		("Onions", 0.79, 15),
		("Pasta", 1.49, 20),
		("Potatoes", 2.99, 18),
		("Rice", 3.49, 12),
		("Tomatoes", 1.49, 18),
		("Yogurt", 2.99, 8)
	]
	users = [
		("Joe Mama", md5("password123".encode()).hexdigest(), "Administrator"),
		("Mark Zuckerberg", md5("goggleshmoggleperdoggle".encode()).hexdigest(), "Moderator"),
		("Sam Altman", md5("agiSeCrEtPa$$".encode()).hexdigest(), "Customer"),
		("Nasral Perdanul", md5("BBZNOT9893".encode()).hexdigest(), "Customer"),
		("Manula Perdanula", md5("darthvader111".encode()).hexdigest(), "Customer"),
		("Cuckfield_Resident", md5("B23june2021".encode()).hexdigest(), "Moderator"),
		("Berglomba Perdomba", md5("abruhalol92".encode()).hexdigest(), "Customer"),
		("Don Bewds", md5("I_died_of_death".encode()).hexdigest(), "Customer")
	]

	with sqlite3.connect('products.db', check_same_thread=False) as conn:
		cursor = conn.cursor()
		for product in products:
			cursor.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", product)

		for user in users:
			cursor.execute("INSERT INTO users (username, hash, user_type) VALUES (?, ?, ?)", user)

		conn.commit()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
	product_name = request.form['product_name']  # Vulnerable to SQLi

	with sqlite3.connect('products.db', check_same_thread=False) as conn:
		cursor = conn.cursor()
		cursor.execute(f"SELECT * FROM products WHERE LOWER(name) LIKE '%{product_name}%';")
		result = cursor.fetchall()
		return render_template('results.html', search_result=result)

if __name__ == '__main__':
	app.secret_key = 'random-secret'
	populate_db()

app.debug = True
app.run(host="0.0.0.0")

