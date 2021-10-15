##### CANADA HISTORICAL WEATHER DATA SCRAPER #####
### Author: Kristopher Buote
### This script scrapes weather data from Government of Canada's historical weather data. See https://climate.weather.gc.ca/historical_data/search_historic_data_e.html
### User can specify the start and end date to search and the weather station they wish to search.
### The data is saved to a CSV file

import requests
import pandas as pd

######### USER CHANGE SEARCH PARAMETERS BELOW ###########
# Warning: Program not smart and easy to break, follow the format
# See a sample URL below
# https://climate.weather.gc.ca/climate_data/hourly_data_e.html?hlyRange=2005-01-18%7C2021-10-13&dlyRange=2005-06-13%7C2021-10-13&mlyRange=2005-11-01%7C2007-02-01&StationID=43500&Prov=BC&urlExtension=_e.html&searchType=stnName&optLimit=yearRange&StartYear=1840&EndYear=2021&selRowPerPage=25&Line=0&searchMethod=contains&Month=7&Day=19&txtStationName=CALLAGHAN+VALLEY&timeframe=1&Year=2021

### Data scrape range  
# Start date as numbers
# e.g. January 7, 2021 -> 1-7-2021
startMonth = 1
startDay = 1
startYear = 2021

# End date for data scrape
endMonth = 10
endDay = 13
endYear = 2021

### Enter your weather station code here. e.g. CALLAGHAN+VALLEY
weatherStationURLparam = 'CALLAGHAN+VALLEY'

################ END OF PARAMETERS #################

# number of days in each month. use this for the for loop iteration
daysInMonths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# create a list to add all the daily dataframes to
dfMasterList = []

### iterate over years, months, days
# add one to adjust for python's zero indexing
for yearCount in range(endYear - startYear + 1):
	yearURLparam = str(startYear + yearCount)

	for monthCount in range(endMonth - startMonth + 1):
		monthURLparam = str(startMonth + monthCount)

		# If we're on the last month to search, set the end date as the specified end date
		if monthCount + startMonth == endMonth:
			monthStartDay = startDay
			monthEndDay = endDay

		# otherwise, set the the start/end dates as the 1st day and number of days in the month (i.e. scrape the whole month)
		else:
			monthStartDay = 1
			monthEndDay = daysInMonths[startMonth - 1 + monthCount]

		for dayCount in range(monthEndDay - monthStartDay + 1):
			dayURLparam = str(monthStartDay + dayCount) 

			# Read HTML from URL, get the data table, store in df
			URL = "https://climate.weather.gc.ca/climate_data/hourly_data_e.html?hlyRange=2005-01-18%7C2021-10-13&dlyRange=2005-06-13%7C2021-10-13&mlyRange=2005-11-01%7C2007-02-01&StationID=43500&Prov=BC&urlExtension=_e.html&searchType=stnName&optLimit=yearRange&StartYear=1840&EndYear=2021&selRowPerPage=25&Line=0&searchMethod=contains&Month=" + monthURLparam + "&Day=" + dayURLparam + "&txtStationName=" + weatherStationURLparam + "&timeframe=1&Year=" + yearURLparam
			html_tables = pd.read_html(URL)
			df = html_tables[0]

			# add date to the dataframe, format to YYYY-MM-DD
			yearDate = yearURLparam
			monthDate = ('0' + monthURLparam) if len(monthURLparam) == 1 else monthURLparam
			dayDate = ('0' + dayURLparam) if len(dayURLparam) == 1 else dayURLparam

			dateString = yearDate + '-' + monthDate + '-' + dayDate
			df.insert(loc=0, column='Date', value=dateString)

			# Append daily dataframe to master list
			dfMasterList.append(df)

# concatenate all daily dataframes to one master dataframe
data = pd.concat(dfMasterList)

# Create a function to produce neat date strings for exporting to csv
def neatDatePath(year, month, day):
	# Takes integers, specified at start of program by user, converts to nice string 
	yearDate = str(year)
	monthDate = ('0' + str(month)) if month < 10 else str(month)
	dayDate = ('0' + str(day)) if day < 10 else str(day)

	return yearDate + '-' + monthDate + '-' + dayDate

dataPath = weatherStationURLparam + '-Historical-Weather-Data-' + neatDatePath(startYear, startMonth, startDay) + '-to-' + neatDatePath(endYear, endMonth, endDay) + '.csv'

data.to_csv(dataPath, index=False)