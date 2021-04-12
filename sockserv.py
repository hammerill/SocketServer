import socket
import threading
import os

def sendAll(data: str, exceptClient: socket = None): #отправляем сообщение всем клиентам, кроме exceptClient, но по умолчанию (без аргументов) абсолютно всем
	global clients
	
	for cl in clients:
		if cl != exceptClient:
			cl.sendall(data.encode("utf-8"))

def listenClient(client: socket, client_addr: tuple): #слушаем входящие сообщения от клиента, при получении отправляем всем другим клиентам
	global clients
	
	try:
		data = client.recv(1024)
		client_nick = data.decode("utf-8")
		print(f"Клиент {client_nick} ({client_addr[0]}:{client_addr[1]}) подключился к серверу.")
		sendAll(f"{client_nick} подключился.", client)
	except Exception as e:
		print(f"Клиент {client_addr[0]}:{client_addr[1]} не смог подключиться к серверу из-за ошибки \"{e}\".")
		clients.remove(client)
		client.close()
		return

	while True:
		try:
			data = client.recv(1024)

			if not data:
				print(f"Клиент {client_nick} ({client_addr[0]}:{client_addr[1]}) отключился от сервера.")
				clients.remove(client)
				client.close()
				sendAll(f"{client_nick} отключился.")
				return
				
			try:
				toSend = data.decode("utf-8")
				toSend = f"{client_nick}: {toSend}"
				print(toSend)
				sendAll(toSend, client)
			except UnicodeDecodeError:
				print("\nОшибка расшифровки входящего сообщения (оно пришло не от клиента?).\n")
		except ConnectionResetError:
			print(f"Клиент {client_nick} ({client_addr[0]}:{client_addr[1]}) отключился от сервера.")
			clients.remove(client)
			client.close()
			sendAll(f"{client_nick} отключился.")
			return
		except Exception as e:
			print(f"Произошла неизвестная ошибка: \"{e}\".\nПерезапустите сервер, когда интернет будет в порядке.")
			clients.remove(client)
			client.close()
			return

os.system("cls" if os.name == "nt" else "clear")

clients = []

key = True

while key: #просим данные до тех пор, пока не запустим сервер
	serv_port = input("Укажите порт сервера\n(оставьте пустым для порта по умолчанию): ")
	if not serv_port: serv_port = 7777
	try:
		serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto = 0)
		serv.bind(('', int(serv_port)))
		serv.listen()
		key = False
	except ValueError:
		print("Пожалуйста, введите число.\n")
	except Exception as e:
		print(f"Не удалось запустить сервер на порту {serv_port}, ошибка: \"{e}\".\nВведите данные повторно.\n")


print(f"Сервер инициализирован на порту {serv_port}.")

while True: #слушаем входящие соединения и для каждого нового клиента стартуем поток listenClient
	try:
		client, client_addr = serv.accept()
		clients.append(client)

		print(f"Клиент {client_addr[0]}:{client_addr[1]} подключается к серверу...")
		t = threading.Thread(target = listenClient, args=(client, client_addr))
		t.start()
		
	except ConnectionResetError:
		pass
	except Exception as e:
		print(f"Произошла неизвестная ошибка: \"{e}\".")

serv.close()