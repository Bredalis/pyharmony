#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python port of JavaScript Harmony discovery here:
# https://github.com/swissmanu/harmonyhubjs-discover

import socket
import time
import threading
import logging

# Constants for UDP broadcast
UDP_IP = '0.0.0.0'
PORT_TO_ANNOUNCE = 61991

# Set up logging
logger = logging.getLogger(__name__)

class Discovery:
    # Method to listen for responses from Harmony hubs
    def listen(self, hubs, listen_socket):
        while True:
            try:
                client_connection, client_address = listen_socket.accept()
            except (OSError) as err:
                logger.debug("Listen socket closed {0}".format(err))
                return
            request = client_connection.recv(1024)
            if request:
                hub = self.deserialize_response(request.decode('UTF-8'))

                if hub:
                    uuid = hub['uuid']
                    if uuid not in hubs:
                        logger.debug('Found new hub %s', uuid)
                        hubs[hub['uuid']] = hub
                    else:
                        logger.debug('Found existing hub %s', uuid)
            client_connection.close()

    # Method to parse response into key-value pairs
    def deserialize_response(self, response):
        pairs = {}
        if not response.strip():
            return False

        for data_point in response.split(';'):
            key_value = data_point.split(':')
            pairs[key_value[0]] = key_value[1]
        return pairs

    # Main method for discovering Harmony hubs
    def discover(self, scan_attempts, scan_interval):
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind((UDP_IP, PORT_TO_ANNOUNCE,))
        listen_socket.listen(1)

        hubs = {}

        listen_thread = threading.Thread(
            target=self.listen,
            args=(hubs, listen_socket,),
            daemon=True)
        listen_thread.start()

        ping_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ping_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        MESSAGE = '_logitech-reverse-bonjour._tcp.local.\n{}'.format(
                        PORT_TO_ANNOUNCE).encode('utf-8')

        for scan in range(0, scan_attempts):
            try:
                ping_sock.sendto(MESSAGE, ('255.255.255.255', 5224))
            except Exception as e:
                logger.error('Error pinging network: %s', e)

            time.sleep(scan_interval)
        
        # Close sockets after scanning
        ping_sock.close()
        listen_socket.shutdown(socket.SHUT_RDWR)
        listen_socket.close()
        
        logger.info('Completed scan, %s hub(s) found.', len(hubs))
        return [hubs[h] for h in hubs]

# Entry function for external use
def discover(scan_attempts=10, scan_interval=1):
    return Discovery().discover(scan_attempts, scan_interval)
