from datetime import datetime

class ToolsBackend(object):
	"""Esta clase es creada para gestionar de manera global, diferentes procesos
	de forma generica, como el formateo de valores y fechas"""
	
	
	def set_date_format(self,date):
		"""
		Funcion para cambiar formato de las fechas
		de a yyyy-mm-dd
		data: campo tipo datetime
		"""

		if date is None:  # Si no hay fecha para formatear, termina el proceso
			return None


		date_modified = date.strftime('%Y-%m-%d')

		return date_modified


