from random import randint
from ipaddress import IPv4Address
from socket import socket, AF_INET, SOCK_STREAM, setdefaulttimeout, getfqdn
from os import path
from optparse import OptionParser
from selenium import webdriver
from ipwhois import IPWhois
from dns import resolver, reversename
from sqlite3 import connect
from sys import exit


def isOpenPort(host, port, timeout):
    
    setdefaulttimeout(timeout)
    template = "{0:16}{1:3}{2:40}"
	
    #Intentamos establecer una conexión a un puerto, en caso positivo realizamos las funciones pertinentes
    try:
        # Definimos conexión
        #   AF_INET: Representa conjunto (host, port)
        #   SOCK_STREAM: Establece protocolo de la conexión TCP
        connection = socket(AF_INET, SOCK_STREAM)

        # Establecemos par de dirección IP y puerto
        connection.connect((host, port))
		
        # Obtenemos el banner y lo parseamos
        connection.send(b'HEAD / HTTP/1.0\r\n\r\n')
        banner = connection.recv(1024)
		
        # Imprimimos mensaje Puerto abierto junto a la dirección IPv4
        print(template.format(host, '->', 'Open Port'))
		
        # Adaptamos salto de línea a HTML
        aux = str(banner).replace('\\r\\n','<br/>')
		
        # Obtenemos banner eliminando carácteres especiales del principio y del final
        banner = aux[2:len(aux)-3]
		
        # Cerramos la conexión
        connection.close()
        
        #Intenamos realizar la captura de la página web, si se realiza con éxito generamos el fichero de información.
        #screenshot = takeScreenshot(host, str(port))

        #if generateInformationDB( host, port, banner, screenshot ) :
        #    return True
        with open("ips.txt", "a") as archivo:
            archivo.write(f"http://{host}/ ~  ~ \n")

    except Exception as e:
        print(template.format(host, '->', 'Closed Port: ('+str(e)+')'))
        connection.close()
        return False
        
with open("ips.txt", "a") as archivo:
    archivo.write("----------------------Nueva Serie----------------------\n")
    
for ip in range(255):
    host = f"172.16.14.{ip}"
    isOpenPort(host, 80, 5)
    
    
    
    
    
    
