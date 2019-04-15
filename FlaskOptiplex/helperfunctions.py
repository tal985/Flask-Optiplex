import socket
import struct
import subprocess

from FlaskOptiplex import models

IP_OPTIPLEX = '192.168.1.136'
PORT_NOVAMAGIA = '25565'
PORT_LETITDIE = '25567'

"""Wake on Lan"""
def wol():
    ip = "255.255.255.255"
    port = 9
    mac = "B8CA3AB65DB6"
    packet = create_magic_packet(mac)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.connect((ip, port))
    sock.send(packet)
    sock.close()

"""Create a magic packet to wake a device"""
def create_magic_packet(macaddress):
    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 17:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    else:
        raise ValueError('Incorrect MAC address format')

    data = b'FFFFFFFFFFFF' + (macaddress * 16).encode()
    send_data = b''

    for i in range(0, len(data), 2):
        send_data += struct.pack(b'B', int(data[i: i + 2], 16))
    return send_data

"""Check Optiplex status"""
def checkOptiplex():
    if checkIP(IP_OPTIPLEX, 222):
        return 'static/images/yes.png'
    return 'static/images/no.png'

"""Check if port is open at IP"""
def checkIP(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.05)
    result = sock.connect_ex((ip, port))
    sock.close()
    if result == 0:
        return True
    return False