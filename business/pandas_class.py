import pandas as pd
from business.ianalysis import IAnalysis
import random
import pathlib
import os


FOLDER_PATH    = str(pathlib.Path(__file__).parent.resolve())
APP_PATH_SPEC  =  os.path.join(FOLDER_PATH,'..',os.path.join("data","spc_data.csv"))
#APP_PATH_CYCLE =  os.path.join(FOLDER_PATH,'..',os.path.join("data","cycle.csv"))
APP_PATH_TRAFFIC =  os.path.join(FOLDER_PATH,'..',os.path.join("data","accidents_2012_to_2014.csv"))

df = pd.read_csv(APP_PATH_SPEC)
#df2 = pd.read_csv(APP_PATH_CYCLE)
df3 = pd.read_csv(APP_PATH_TRAFFIC)

class Pandas(IAnalysis):

	def init_data(self):
		data = {}

		for col in list(df[1:]):
			d = df[col]
			stats = d.describe()

			std = stats["std"].tolist()
			ucl = (stats["mean"] + 3 * stats["std"]).tolist()
			lcl = (stats["mean"] - 3 * stats["std"]).tolist()
			usl = (stats["mean"] + stats["std"]).tolist()
			lsl = (stats["mean"] - stats["std"]).tolist()

			data.update({
        		col: {
                    "count": stats["count"].tolist(),
                    "data": d,
                    "mean": stats["mean"].tolist(),
                    "std": std,
                    "ucl": round(ucl, 3),
                    "lcl": round(lcl, 3),
                    "usl": round(usl, 3),
                    "lsl": round(lsl, 3),
                    "min": stats["min"].tolist(),
                    "max": stats["max"].tolist(),
                    "ooc": self.populate_ooc(d, ucl, lcl),
                }
        	})

		return data


	def populate_ooc(self,data, ucl, lcl):
	    ooc_count = 0
	    ret = []

	    for i in range(len(data)):
	        if data[i] >= ucl or data[i] <= lcl:
	            ooc_count += 1
	            ret.append(ooc_count / (i + 1))
	        else:
	            ret.append(ooc_count / (i + 1))
	    return ret

	def get_cities(self):
		return ["Liverpool"]

	# def get_all_year_traffic(self):
	# 	counts = df3["Year"].value_counts(sort=False)
	# 	df_count = pd.DataFrame(counts)
	# 	df_value_counts_reset = df_count.reset_index()
	# 	df_value_counts_reset.columns =["year","value"]

	# 	years = list(map(lambda x:str(x),df_value_counts_reset["year"].values))
	# 	Y = years
	# 	X = df_value_counts_reset["value"].values
	# 	T = []

	# 	for k in X:
	# 		m = str(round(k/1000,1))+'K'
	# 		T.append(m)

	# 	Y.reverse()

	# 	self.YEARS = Y
	# 	self.CURRENT_YEAR = Y[0]
	# 	return X,Y,T

	def get_all_year_traffic(self):
		X = []
		Y = []
		T = []
		s = 2015

		for i in range(9):
		    k = random.randint(1,5000)
		    X.append(k)
		    Y.append(s)
		    m = str(round(k/1000,1))+'M'
		    T.append(m)
		    s += 1

		Y.reverse()

		self.YEARS = Y
		self.CURRENT_YEAR = Y[0]
		return X,Y,T

	def get_traffic_by_location(self):
		
		X = ["Urban","Rural"]
		Y = df3["Urban_or_Rural_Area"].value_counts().values
		# for i in range(2):
		#     Y.append(random.randint(100000,500000))

		return (X,Y)

	def get_traffic_by_season(self):
		# X = ["Dry","Wet","Snow"]
		# Y = []

		# for i in range(3):
		#     Y.append(random.randint(100000,500000))

		# return (X,Y)
		names = df3["Road_Surface_Conditions"].unique()
		values = df3["Road_Surface_Conditions"].value_counts().values
		
		return (names,values)

	def get_traffic_by_hours_and_days(self):
		v_heat_map = []
		a = []
		b = []
		c = []
		d = []
		e = []
		f = []
		g = []

		x_times = []
		y_days = ["Sunday",'Tuesday','Wednesday','Thursday',"Friday","Saturday"]

		for i in range(24):
			x_times.append(str(i)+'AM')

			a.append(random.randint(0,100))
			b.append(random.randint(0,100))
			c.append(random.randint(0,100))
			d.append(random.randint(0,100))
			e.append(random.randint(0,100))
			f.append(random.randint(0,100))
			g.append(random.randint(0,100))

			v_heat_map.extend([a,b,c,d,e,f,g])

		return (x_times,y_days,v_heat_map)

	def get_traffic_hourly_by_year(self,year):
		
		x_hourly =[]
		y_hourly = []
		text_hourly = []

		for i in range(24):
			x_hourly.append(str(i)+":00")
			k = random.randint(100,500000)
			y_hourly.append(k)
			text_hourly.append(str(round(k/1000,1))+"M")

		
		return (x_hourly,y_hourly,text_hourly)

	def get_traffic_cities(self):

		df3["Date/Time"] = df3["Date"] +' '+ df3["Time"]
		df3["Date/Time"] = pd.to_datetime(df3["Date/Time"])
		df3.index = df3["Date/Time"]
		# print(df3["Date/Time"].head())
		# df.drop("Date/Time", 1, inplace=True)
		totalList = []
		for month in df3.groupby(df3.index.month):
		    dailyList = []
		    for day in  month [1].groupby(month[1].index.day):
		        dailyList.append(day[1])
		    totalList.append(dailyList)

		return totalList