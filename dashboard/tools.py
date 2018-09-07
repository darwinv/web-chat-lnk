"""Modulo para herramientas Globales."""
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class Validations(object):
    """Clase para validaciones Generales."""

    def valid_legal_age(date):
        """Se valida la fecha para un menor de 18 años no pueda registrarse."""
        today = datetime.today().date()
        min_date = today - relativedelta(years=18)
        if date > min_date:
            raise ValidationError(_("You must be of legal age"))


class ToolsBackend(object):
    """Esta clase es creada para gestionar de manera global, diferentes procesos
    de forma generica, como el formateo de valores y fechas"""

    def date_format_to_db(self, date):
        formats = ("%d/%m/%Y", "%Y-%m-%d")
        return self.set_date_format(date, formats)

    def date_format_to_view(self, date):
        formats = ("%Y-%m-%d", "%d/%m/%Y")
        return self.set_date_format(date, formats)

    def date_format_full_to_view(self, date):
        """Formatear string para mostrar, no toma en cuenta zona horaria"""
        date_split = date.split(".")
        formats = ("%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M")
        return self.set_date_format(date_split[0], formats)

    def set_date_format(self, date, formats):
        """
        Funcion para cambiar formato de las fechas
        :param date: campo tipo datetime o string
        :param formats: dupla con los valores de los formatos a convertir
        :return:
        """

        if date is None:  # Si no hay fecha para formatear, termina el proceso
            return None
        if type(date) is str:
            date = datetime.strptime(date, formats[0])  # Convertimos string a Datetime

        date_modified = date.strftime(formats[1])  # Convertimos Datetime to String dado

        return date_modified

    def format_to_decimal(self, num):
        """
        Funcion para retornar formato estandar de valores o precios
        :param num: String, Int or Float
        :return: string format "10000.00"
        """
        return "{:.2f}".format(float(num))


def capitalize(line):
    """
        Funcion creada como erramienta para capitalizar el primer caracter de una cadena
        sin modificar el resto de la cadena
    """

    if len(line) <= 0:
        return ''
    return line[0].upper() + line[1:]

