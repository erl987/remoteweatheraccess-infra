"""Read in data from a TE923-compatible weather station via USB and store the data in a CSV-file compatible to PC-Wetterstation."""
import sys

import te923ToCSVreader

data_folder = '/opt/weatherstation/data/'
station_data_file_name = 'stationData.dat'

input_list = sys.argv
script_name = input_list.pop(0)

# Read new weather data from the TE923-station and save it in a CSV-file compatible to PC-Wetterstation
te923ToCSVreader.te923ToCSVreader( data_folder, station_data_file_name, script_name )