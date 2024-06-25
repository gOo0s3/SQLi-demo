import socket
import json
import sqlite3
import threading

def handle_client(client_socket):
	with sqlite3.connect('products.db') as conn:
		cur = conn.cursor()
		product_name = client_socket.recv(1024).strip().decode()
		if not product_name:
			print("Client disconnected")
			return
		
		print("Message from client: ", product_name)
		
		try:
			query = f"SELECT * FROM products WHERE LOWER(name) LIKE '%{product_name}%'"
			print(f"Executing: {query}")
			cur.execute(query)
			products = cur.fetchall()
			product_details = []

			response = json.dumps(products)
			client_socket.sendall(response.encode())
			print("Product details sent to client")
			
		except socket.error as e:
			print("Client disconnected")

		except Exception as e:
			client_socket.sendall(str(e).encode())
			print("Error occurred: ", str(e))


def start_server():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind(('localhost', 12345))
		s.listen(5)
		print("Server started on localhost:12345")

		while True:
			client_socket, addr = s.accept()
			threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == '__main__':
    start_server()

