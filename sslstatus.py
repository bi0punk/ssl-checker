import http.client
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
                
                # Obtener el código de respuesta HTTP
                conn = http.client.HTTPSConnection(domain)
                conn.request("HEAD", "/")
                response = conn.getresponse()
                codigo_respuesta = response.status
                
                return [domain, str(codigo_respuesta), not_after, estado_certificado]
    except (socket.gaierror, ssl.SSLError, ConnectionRefusedError, http.client.HTTPException) as e:
        return [domain, "Error", "", "No se pudo conectar"]

def format_date(date):
    if date:
        return date.strftime('%d, %B, %Y')
    else:
        return ""

if __name__ == "__main__":
    domains_to_check = [
                        ]
    
    table = PrettyTable()
    table.field_names = ["Sitio Consultado", "Código de Respuesta", "Fecha de Vencimiento", "Estado del Certificado"]

    for domain in domains_to_check:
        result = check_ssl_certificate(domain)
        result[2] = format_date(result[2])  # Formatear la fecha
        table.add_row(result)

    # Imprimir la tabla en la consola
    print(table)
    
    # Guardar la tabla en un archivo .txt
    with open("ssl_status.txt", "w") as file:
        file.write(str(table))
