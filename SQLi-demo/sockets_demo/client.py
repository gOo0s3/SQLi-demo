import socket

def send_product_request(product_name):
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.connect(('localhost', 12345))
			s.sendall(product_name.encode())

			response = s.recv(1024).decode()
			print(response)
	except ConnectionRefusedError:
		print("server is down at the moment")
if __name__ == '__main__':
    product_name = input("Enter the product name to request details: ")
    send_product_request(product_name)
