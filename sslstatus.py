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

import socket
import ssl
import datetime
from prettytable import PrettyTable

def check_ssl_certificate(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                current_time = datetime.datetime.now()
                if not_after > current_time:
                    estado_certificado = "Al día"
                else:
                    estado_certificado = "Vencido"
                
                return [domain, cert['subjectAltName'][0][1], not_after.strftime('%Y-%m-%d'), estado_certificado]
    except (socket.gaierror, ssl.SSLError, ConnectionRefusedError) as e:
        return [domain, "Error", "", "No se pudo conectar"]

if __name__ == "__main__":
    domains_to_check = ["youtube.com",
                        "github.com",
                        "netflix.com"
                        ]
    
    table = PrettyTable()
    table.field_names = ["Sitio Consultado", "Código de Respuesta", "Fecha de Vencimiento", "Estado del Certificado"]

    for domain in domains_to_check:
        result = check_ssl_certificate(domain)
        table.add_row(result)

    print(table)
