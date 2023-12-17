from business.pandas_class import Pandas
from business.db_class import Dbase


def get_analysis(value:str):
	if value.upper() == "PANDAS":
		return Pandas()
	elif value.upper() == "DB":
		return Dbase()
	else:
		raise Exception("Invalid operation was passed, set value to either pandas or db")
