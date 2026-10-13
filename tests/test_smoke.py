import datetime

from sslstatus import check_ssl_certificate, format_date


def test_format_date():
    fecha = datetime.datetime(2027, 8, 8, 12, 0, 0)
    assert format_date(fecha) == "08, August, 2027"


def test_format_date_vacio():
    assert format_date(None) == ""


def test_check_ssl_certificate_error_no_hace_red():
    resultado = check_ssl_certificate("this-domain-does-not-exist-12345.invalid")
    assert resultado[0] == "this-domain-does-not-exist-12345.invalid"
    assert resultado[3] == "No se pudo conectar"