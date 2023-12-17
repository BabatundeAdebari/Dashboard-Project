from pymongo import MongoClient
from decouple import config
from business.ianalysis import IAnalysis

CONFIG_MONGO_URL = config('MONGO_URL')
CONFIG_DB = config('DB')


class Dbase(IAnalysis):

	def init_data(self):
		return {}

	def get_cities(self):
		return ["Liverpool","Manchester","Portmount"]

	def get_all_year_traffic(self):
		X = []
		Y = []
		T = [] 
		return (X,Y,T)

	def get_traffic_by_location(self):
		X = []
		Y = []
		return (X,Y)

	def get_traffic_by_season(self):
		X = []
		Y = []
		return (X,Y)

	def get_traffic_by_hours_and_days(self):
		x_times= []
		y_days = []
		v_heat_map = []
		return (x_times,y_days,v_heat_map)

	def get_traffic_hourly_by_year(self,year):
		x_hourly =[]
		y_hourly = []
		text_hourly = []
		
		return (x_hourly,y_hourly,text_hourly)