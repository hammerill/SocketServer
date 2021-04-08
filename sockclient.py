import socket
import threading
import os

def listenServer(serv: socket): #слушаем входящие сообщения от сервера, которые приходят от него тогда, когда другой клиент что-то написал
	while True:
		try:
			data = serv.recv(1024)

			if not data:
				print("\nОшибка подключения к серверу.\nПерезапустите клиент, когда интернет и сервер будут в порядке.")
				serv.close()
				return

			try:
				print(data.decode("utf-8"))
			except UnicodeDecodeError:
				print("\nОшибка расшифровки входящего сообщения (оно пришло не от сервера?).\n")

		except ConnectionResetError:
			print("\nСервер отключился.\nПерезапустите клиент, когда сервер будет в порядке.")
			serv.close()
			return
		except Exception as e:
			print(f"\nПроизошла неизвестная ошибка: \"{e}\".\nПерезапустите клиент, когда интернет и сервер будут в порядке.")
			serv.close()
			return

key = True
serv_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_connect.bind(('', 0))

while key: #просим данные до тех пор, пока не подключимся к серверу
	nick = input("Укажите ваш ник: ")

	serv_ip = input("Укажите IP-адрес сервера: ")
	if not serv_ip: serv_ip = "192.168.43.1"
	elif serv_ip == "0": serv_ip = "127.0.0.1"

	serv_port = input("Укажите порт сервера\n(оставьте пустым для порта по умолчанию): ")
	if not serv_port: serv_port = 7777

	print("\nСоединение с сервером...")

	try:
		serv_connect.connect((serv_ip, int(serv_port)))
		serv_connect.sendall(nick.encode("utf-8"))
		key = False
		os.system("cls" if os.name == "nt" else "clear")
		print("Соединение с сервером установлено!\n")

	except Exception as e:
		print(f"Не удалось соединиться с сервером. Ошибка: \"{e}\".\nУбедитесь, что данные введены верно и вы находитесь в одной сети с сервером.\nВведите данные заново.\n\n")

t = threading.Thread(target = listenServer, args=(serv_connect,))
t.start() #отдельным потоком слушаем сообщения от сервера

while True: #а в главном отправляем что-либо
	inp = input()
	data = inp.encode("utf-8")

	try:
		serv_connect.sendall(data)
	except Exception as e:
		print(f"\nОшибка сети...\nНе удаётся отправить сообщение из-за ошибки: \"{e}\".\nУбедитесь, что интернет и сервер в порядке.\n")

serv_connect.close()