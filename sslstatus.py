import datetime
import http.client
import socket
import ssl

from prettytable import PrettyTable


def check_ssl_certificate(domain: str):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            sock.settimeout(10)  # Establece un tiempo de espera de 10 segundos
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                not_before_after = cert.get("notAfter") if cert else None
                if not not_before_after:
                    return [domain, "", "", "Sin certificado"]
                not_after = datetime.datetime.strptime(str(not_before_after), "%b %d %H:%M:%S %Y %Z")
                current_time = datetime.datetime.now()
                estado_certificado = "Al día" if not_after > current_time else "Vencido"

                # Obtener el código de respuesta HTTP
                conn = http.client.HTTPSConnection(domain, timeout=10)
                conn.request("HEAD", "/")
                response = conn.getresponse()
                codigo_respuesta = response.status

                return [domain, str(codigo_respuesta), not_after, estado_certificado]
    except (TimeoutError, socket.gaierror, ssl.SSLError, ConnectionRefusedError, http.client.HTTPException):
        return [domain, "Error", "", "No se pudo conectar"]


def format_date(date) -> str:
    if date:
        return date.strftime('%d, %B, %Y')
    return ""


if __name__ == "__main__":
    # Leer los enlaces desde el archivo de texto
    domains_to_check = []
    with open("enlaces.txt") as file:
        for line in file:
            domain = line.strip()  # Eliminar espacios en blanco y saltos de línea
            domains_to_check.append(domain)

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