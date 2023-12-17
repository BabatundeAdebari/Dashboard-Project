import abc

class IAnalysis(abc.ABC):

	@abc.abstractmethod
	def get_cities(self) -> list:
		pass

	@abc.abstractmethod
	def get_all_year_traffic(self):
		pass

	@abc.abstractmethod
	def get_traffic_by_location(self):
		pass

	@abc.abstractmethod
	def get_traffic_by_season(self):
		pass

	@abc.abstractmethod
	def get_traffic_by_hours_and_days():
		pass

	@abc.abstractmethod
	def init_data(self):
		pass

	@abc.abstractmethod
	def get_traffic_hourly_by_year(self,year:int):
		pass

	@abc.abstractmethod
	def get_traffic_cities(self):
		pass

