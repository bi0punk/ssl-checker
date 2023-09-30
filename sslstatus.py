#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sslstatus.py
#  
#  Copyright 2023 sysbot <sysbot@kali-server>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

import ssl
import socket
import datetime

def check_ssl_certificate(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                current_time = datetime.datetime.now()
                if not_after > current_time:
                    print(f"El certificado SSL de {domain} es válido hasta {not_after}.")
                else:
                    print(f"El certificado SSL de {domain} ha caducado el {not_after}.")
    except (socket.gaierror, ssl.SSLError, ConnectionRefusedError) as e:
        print(f"No se pudo conectar a {domain}. Error: {e}")

if __name__ == "__main__":
    domains_to_check = ["youtube.com",
                        "github.com",
                        "netflix.com"
                        
                        ]
    for domain in domains_to_check:
        check_ssl_certificate(domain)

