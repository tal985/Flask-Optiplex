import socket
import struct
import subprocess

from FlaskOptiplex import models

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
    nmap = nmapScan('192.168.1.136', '222')
    if nmap == 'open':
        return 'static/images/yes.png'
    return 'static/images/no.png'


"""Wrapper function for using nmap."""
def nmapScan(ip, port):

    #Convert external IP to internal
    if ip == '72.46.198.99':
        if port == '2222':
            ip = '192.168.1.146'
        else:
            ip = '192.168.1.136'

    status = subprocess.run('nmap ' + ip + ' -p ' + port, stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')

    if 'open' in status and 'filtered' not in status:
        status = 'open'
    elif 'closed' in status:
        status = 'closed'
    else:
        status = 'filtered'

    return status

"""Write verification for port and ip code"""
def validIPPort(ip, port):

    try:
        socket.inet_aton(ip)
        if int(port) > 0 and int(port) < 65536:
            return True
        print ("what?")
        return False
    except Exception as e:
        print (e)
        return False