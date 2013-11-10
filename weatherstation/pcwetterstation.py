"""Provides functions for managing weather data compatible to the software PC-Wetterstation.

Functions:
write:                          Writes a weather data CSV-file compatible to PC-Wetterstation for arbitrary data.
writesinglemonth:               writes a weather data CSV-file compatible to PC-Wetterstation for a single month.
read:                           Reads a CSV-file with the weather data compatible to PC-Wetterstation.
merge:                          Merges two CSV-files compatible to PC-Wetterstation.
convertTo:                      Converts weather data into units and format compatible to PC-Wetterstation.
finddatafiles:                  Finds all PC-Wetterstation files in a given folder.
deletedatafiles:                Deletes all given files from a given folder.
"""
import csv
import os
import datetime
from datetime import datetime as dt
from collections import OrderedDict

import constants
import utilities


data_file_tag = 'EXP'       # indicating a PC-Wetterstation data file


def write( data_folder, rain_calib_factor, station_name, station_height, station_type, export_data, sensor_list ):
    """Writes a CSV-file with the weather data compatible to PC-Wetterstation for arbitrary data.
    
    Args:
    data_folder:                Folder where the CSV-file for PC-Wetterstation will be stored. It must be given relative to the current path.
                                The file names will be automatically "EXP_MM_YY.CSV" with MM and YY being the months and the years of the datasets.
    rain_calib_factor:          Calibration factor of the rain sensor (1.000 if the rain sensor has the original area).
    station_name:               ID of the station (typically three letters, for example ERL).
    station_height:             Altitude of the station (in meters).
    station_type:               Information string on the detailed type of the weather station (producer, ...).
    export_data:                Data to be written on file. It is not required to be sorted regarding time.
                                The required format is a list of ordered dicts with the key being registered in sensor_list. It must contain at least 
                                the following information in this order:
                                    - date of the data in the format dd.mm.yyyy
                                    - time of the data (local time) in the format mm:hh
                                    - all measured data according to PC-Wetterstation specification with:
                                            * wind speeds in km/h
                                            * rain in mm since last recording
                                            * temperatures in degree Celsius
                                            * pressure in hPa
                                            * humidities in percent
                                
    sensor_list:                Ordered dict containing the mapping of all sensors to the index of the sensor in the weatherstation and the software PC-Wetterstation,
                                the name and the units of the sensors. The keys must be identical to that used in the 'export_data'.

    Returns:
    file_list:                  List containing the names of all written files
    num_new_datasets:           Number of the new datasets merged into the existing data
    first_time:                 Timepoint of the first merged new dataset (datetime-object)
    last_time:                  Timepoint of the last merged new dataset (datetime-object)

    Raises:
    IOError:                    An error occurred accessing the file.
    """
    getmonth = lambda x: dt.strptime( x['date'], '%d.%m.%Y' )
    getdate = lambda k: dt.strptime( k['date'] + ' ' + k['time'], '%d.%m.%Y %H:%M')
    
    # determine the months existing in the data
    export_data = sorted( export_data, key = getdate )
    months_set = { ( getmonth(x).month, getmonth(x).year ) for x in export_data }
    
    # write the data separately for each month into a file
    file_list = []
    for curr_month in months_set:
        monthly_export_data = [ x for x in export_data if ( getmonth(x).month == curr_month[0] and getmonth(x).year == curr_month[1] ) ]
        file_list.append( writesinglemonth( data_folder, rain_calib_factor, station_name, station_height, station_type, monthly_export_data, sensor_list ) )

    if len( export_data ) > 0:
        first_time = getdate( export_data[0] )
        last_time = getdate( export_data[-1] )
    else:
        first_time = dt( datetime.MINYEAR, 1, 1, 0, 0, 0, 0 )
        last_time = dt( datetime.MINYEAR, 1, 1, 0, 0, 0, 0 )

    return file_list, len( export_data ), first_time, last_time


def writesinglemonth( data_folder, rain_calib_factor, station_name, station_height, station_type, export_data, sensor_list ):
    """Writes a CSV-file with the weather data compatible to PC-Wetterstation for a certain single month.
    
    Args:
    data_folder:                Folder where the CSV-file for PC-Wetterstation will be stored. It must be given relative to the current path.
                                The file name will be automatically "EXP_MM_YY.CSV" with MM and YY being the month and the year of the datasets.
    rain_calib_factor:          Calibration factor of the rain sensor (1.000 if the rain sensor has the original area).
    station_name:               ID of the station (typically three letters, for example ERL).
    station_height:             Altitude of the station (in meters).
    station_type:               Information string on the detailed type of the weather station (producer, ...).
    export_data:                Data to be written on file. It must be only from one single month. It is not required to be sorted regarding time.
                                The required format is a list of ordered dicts with the key being registered in sensor_list. It must contain at least 
                                the following information in this order:
                                    - date of the data in the format dd.mm.yyyy
                                    - time of the data (local time) in the format mm:hh
                                    - all measured data according to PC-Wetterstation specification with:
                                            * wind speeds in km/h
                                            * rain in mm since last recording
                                            * temperatures in degree Celsius
                                            * pressure in hPa
                                            * humidities in percent
                                
    sensor_list:                Ordered dict containing the mapping of all sensors to the index of the sensor in the weatherstation and the software PC-Wetterstation,
                                the name and the units of the sensors. The keys must be identical to that used in the 'export_data'.

    Returns:
    file_name:                  Name of the written file

    Raises:
    IOError:                    An error occurred accessing the file.
    AssertionError:             The data in 'export_data' is from more than one month.
    """
    # Sort data
    export_data = sorted( export_data, key = lambda k: dt.strptime( k['date'] + ' ' + k['time'], '%d.%m.%Y %H:%M') )

    # Check if data is really only from one month
    getmonth = lambda x: dt.strptime( x['date'], '%d.%m.%Y' )
    months_set = { ( getmonth(x).month, getmonth(x).year ) for x in export_data }
    if len( months_set ) > 1:
        raise AssertionError( 'The data is from more than one month.' )

    # Generate file name assuming that all datasets are from one month
    firstDate = dt.strptime( export_data[0]['date'], '%d.%m.%Y')
    file_name = data_file_tag + firstDate.strftime('%m_%y') + '.csv'
    data_file_name = data_folder + '/' + file_name

    # Generate settings line for the CSV-file
    settings_line = '#Calibrate=' + str( '%1.3f' % rain_calib_factor ) + ' #Regen0=0mm #Location=' + str( station_name ) + '/' + str( int( station_height ) ) + 'm #Station=' + station_type

    # Write header lines in a PC-Wetterstation compatible CSV-file
    with open( data_file_name, 'w', newline = '\r\n', encoding='latin-1' ) as f:
        for index, key in enumerate( export_data[0] ):
            if index > 0:
                f.write(',')
            f.write( sensor_list[key][constants.name] )
        f.write( '\n' )
        for index, key in enumerate( export_data[0] ):
            if index > 0:
                f.write( ',' )
            f.write( sensor_list[key][constants.unit] )
        f.write( '\n' )
        f.write( settings_line + '\n' )

    # Store all valid data in a PC-Wetterstation compatible CSV-file
    with open( data_file_name, 'a', newline='', encoding='latin-1' ) as f:
        writer = csv.writer( f, lineterminator="\r\n" )    

        # Write sensor indices line
        sensor_index_list = [ sensor_list[key][constants.export_index] for key in export_data[0] ]
        writer.writerows( [ sensor_index_list ] );

        # Write data
        for line in export_data:
            data_output_line = [ line[key] for key in line ]
            writer.writerows( [ data_output_line ] )

    return file_name


def convertTo(read_data, last_old_rain_counter, sensor_list):
    """Converts weather data to units and format compatible to PC-Wetterstation.
    
    Args:
    read_data:                  List containing the new read data to be processed. For each time a list containing the data with the 
                                indices specified in 'sensor_list' must be present. It is not required to be sorted. 
                                The units of the data must be as follows:
                                    * time of measurement as standard c-time in seconds since epoch (CET considering daylight saving)
                                    * wind speeds in m/s
                                    * rain as absolute rain counter since the last reset at the measurement time (in tipping bucket counts)
                                    * temperatures in degree Celsius
                                    * pressure in hPa
                                    * humidities in percent
                                Invalid data is specified as 'i'.
    last_old_rain_counter:      Last rain counter setting before the first dataset of the new read data (in tipping bucket counts).
    sensor_list:                Ordered dict containing the mapping of all sensors to the index of the sensor in 'read_data'.
                                The keys must be identical to that used in the 'export_data'.
    
    Returns:
    export_data:                List containing the weather data compatible to PC-Wetterstation. The format is a list of ordered dicts 
                                with the key being registered in sensor_list. It contains at least the following information as strings in this order 
                                and is sorted according to date and time:
                                    - date of the data in the format dd.mm.yyyy
                                    - time of the data (CET time considering daylight saving) in the format mm:hh
                                    - all measured data according to PC-Wetterstation specification with:
                                            * wind speeds in km/h
                                            * rain in mm since last recording
                                            * temperatures in degree Celsius
                                            * pressure in hPa
                                            * humidities in percent
                                Not measured data is given as zero.
    last_dataset_time:          Time of the last measurement in the dataset (with an accuracy of minutes).
    last_dataset_rain_counter:  Rain counter setting of the last read dataset (in tipping bucket counts).

    Raises:
    None
    """
     # Generate export data collection
    export_data = []
    for imported_line in read_data:
        new_line = []
        for key in sensor_list:
            if ( sensor_list[ key ][ constants.import_index ] != 'none' ):
                new_line.append( ( key, imported_line[ sensor_list[ key ][ constants.import_index ] ] ) )
            else:
                new_line.append( ( key, '0' ) )
        export_data.append( OrderedDict( new_line ) )

    # Replace non-valid values by zeros
    for line_index, line in enumerate( export_data[:] ):
        processed_line = OrderedDict( ( index, val ) if utilities.isFloat(val) else ( index, '0' ) for index, val in line.items() )
        export_data[ line_index ] = processed_line

    # Delete all sensor data that should not be exported to the CSV-file
    delete_keys = [ key for key in sensor_list if sensor_list[ key ][ constants.export_index ] == 'none' ]
    export_data = [ OrderedDict( ( key, line[key] ) for key in line if key not in delete_keys ) for line in export_data ]

    # Convert date stamps (date zone and DST according to system settings)
    for line in export_data[:]:
        curr_time = dt.fromtimestamp( int( line['date'] ) );            # import ctime seconds since epoch
        line['date'] = curr_time.strftime( '%d.%m.%Y' )
        line['time'] = curr_time.strftime( '%H:%M' )

    # Sort data
    export_data = sorted( export_data, key = lambda k: dt.strptime( k['date'] + ' ' + k['time'], '%d.%m.%Y %H:%M') )

    # Perform required unit convertions
    for line in export_data[:]:
        line['windGusts'] = str( float( line['windGusts'] ) * 3.6 );    # convert from m/s to km/h
        line['windSpeed'] = str( float( line['windSpeed'] ) * 3.6 );    # convert from m/s to km/h
        line['windDir'] = str( float( line['windDir'] ) * 22.5 );       # convert to degree

    # Calculate rain amount differences
    rain_counters = [ float( line['rainCounter'] ) for line in export_data ]
    rain_counters.insert( 0, last_old_rain_counter )
    rain_amounts = [ 0.68685 * ( x - rain_counters[i-1] ) for i, x in enumerate( rain_counters ) ][1:]            # convert from tipping bucket counts to mm
    for export_line, amount in zip( export_data[:], rain_amounts ):
        export_line['rainCounter'] = str( amount );                      # set to rain amount differences since the last dataset before the current (in mm)

    last_dataset_time = dt.strptime( export_data[-1]['date'] + ' ' + export_data[-1]['time'], '%d.%m.%Y %H:%M') # the accuracy is minutes
    last_dataset_rain_counter = rain_counters[-1]
    return export_data, last_dataset_time, last_dataset_rain_counter


def finddatafiles(data_folder):
    """Finds all PC-Wetterstation files in a given folder.
    
    Args:
    data_folder:                Folder in which the data files are searched. It can be a relative path to the current working directory. 
                                
    Returns:
    returns file_names:         A list containing all found PC-Wetterstation file names relative to 'data_folder' 
                               
    Raises:
    FileNotFoundError:          Risen if the data folder is not existing.
    """
    file_names = [ x for x in os.listdir( data_folder ) if x.find( data_file_tag ) != -1 ]

    return file_names


def deletedatafiles(data_folder, data_file_list):
    """Deletes all given files from a given folder.
    
    Args:
    data_folder:                Folder in which the data files are deleted. It can be a relative path to the current working directory. 
    data_file_list:             All files to be deleted in the folder 'data_folder'
                                
    Returns:
    None
                               
    Raises:
    FileNotFoundError:          Risen if the data folder is not existing.
    """
    for data_file in data_file_list:
        os.remove( data_folder + '/' + data_file )


def read( data_folder, file_name, sensor_list ):
    """Reads a CSV-file with the weather data compatible to PC-Wetterstation.
    
    Args:
    data_folder:                Folder where the CSV-file for PC-Wetterstation is be stored. It must be given relative to the current path.
    file_name:                  Name of the CSV-file, there are no requirements regarding the name.
    sensor_list:                Ordered dict containing the mapping of all sensors to the index of the sensor in the weatherstation and the software PC-Wetterstation,
                                the name and the units of the sensors. The keys must be identical to that used in the 'export_data'.  
    
    Returns:                             
    data_data:                  All data from the file. The format is a list of ordered dicts with the key being registered in sensor_list. It contains at least 
                                the following information as strings in this order:
                                    - date of the data in the format dd.mm.yyyy
                                    - time of the data (local time) in the format mm:hh
                                    - all measured data according to PC-Wetterstation specification with:
                                            * wind speeds in km/h
                                            * rain in mm since last recording
                                            * temperatures in degree Celsius
                                            * pressure in hPa
                                            * humidities in percent
    rain_calib_factor:          Calibration factor of the rain sensor (1.000 if the rain sensor has the original area).
    rain_counter_base:          Reference value of the rain counter before the start of the present data (in mm).
    station_name:               ID of the station (typically three letters, for example ERL).
    station_height:             Altitude of the station (in meters).
    station_type:               Information string on the detailed type of the weather station (producer, ...).
    sensor_descriptions_dict:   OrderedDict containing the read descriptions of all sensors in the file. The keys are those from the sensor_list.
    sensor_units_dict:          OrderedDict containing the read units of all sensors in the file. The keys are those from the sensor_list. 

    Raises:
    IOError:                    The file could not be opened.
    ImportError:                The file is not compatible to PC-Wetterstation
    """
    # Determine the sensors present in the file    
    file_name = data_folder + '/' + file_name
    with open( file_name, 'r', newline='', encoding='latin-1' ) as f:
        file_reader = csv.reader( f )

        # Read the three header lines
        sensor_descriptions = next( file_reader )
        sensor_units = next( file_reader )
        metadata = ','.join( next( file_reader ) )

        # Read first data line containing the sensor indices
        indices_list = next( file_reader )

    key_list = []
    for index in indices_list:
        curr_key = ''
        for key, sensor in sensor_list.items():
            if utilities.isFloat( index ):
                if sensor[constants.export_index] == int( index ):
                    curr_key = key
                    break
            else:
                break
        key_list.append( curr_key )

    # parse header lines # TODO: not all metadata entries must be present according to the specification!!!
    splitted_line = str.split( metadata, '#' )
    for line in splitted_line:
        line_pair = str.split( line, '=' )
        if line_pair[0] == 'Calibrate':
            rain_calib_factor = float( line_pair[1] )
        elif line_pair[0] == 'Regen0':
            line_pair[1].index( 'mm' )      # will raise an exception if the format is wrong
            rain_counter_base = float( line_pair[1].replace( 'mm', '' ) )
        elif line_pair[0] == 'Location':
            location_pair = str.split( line_pair[1], '/' )
            station_name = location_pair[0]
            location_pair[1].index( 'm' )   # will raise an exception if the format is wrong
            station_height = int( location_pair[1].replace( 'm', '' ) )
        elif line_pair[0] == 'Station':
            station_type = line_pair[1]

    # Handle the entries for date and time (by specification the first two entries)
    empty_entries = [ i for i, x in enumerate( key_list ) if x == '' ]
    if ( len( empty_entries ) != 2 ) or ( 0 not in empty_entries ) or ( 1 not in empty_entries ):
        raise ImportError( 'The file is no PC-Wetterstation compatible file' )
    key_list[0] = list( sensor_list.keys() )[0]
    key_list[1] = list( sensor_list.keys() )[1]
              
    # Read all weather data from the file
    with open( file_name, 'r', newline='', encoding='latin-1' ) as f:
        file_reader = csv.DictReader( f, key_list )

        # Skip all header lines
        next( file_reader )
        next( file_reader )
        next( file_reader )
        next( file_reader )

        # Read data
        data = []
        for row in file_reader:
            data.append( OrderedDict( ( f, row[f] ) for f in file_reader.fieldnames ) )

    # Export sensor informations
    sensor_descriptions_dict = OrderedDict( [ ( key, sensor_descriptions[index] ) for index, key in enumerate( key_list ) ] )
    sensor_units_dict = OrderedDict( [ ( key, sensor_units[index] ) for index, key in enumerate( key_list ) ] )

    return data, rain_calib_factor, rain_counter_base, station_name, station_height, station_type, sensor_descriptions_dict, sensor_units_dict


def merge( out_data_folder, in_data_folder_1, input_file_name_1, in_data_folder_2, input_file_name_2, sensor_list ):
    """Merges two CSV-files compatible to PC-Wetterstation.
    
    Args:
    out_data_folder:            Folder where the merged CSV-file for PC-Wetterstation is be stored. It must be given relative to the current path.
    in_data_folder_1:           Folder of the first input CSV-file to be merged.
    input_file_name_1:          Name of the first input CSV-file to be merged, there are no requirements regarding the name.
    in_data_folder_2:           Folder of the second input CSV-file to be merged.
    input_file_name_2:          Name of the second input CSV-file to be merged, there are no requirements regarding the name.
    sensor_list:                Ordered dict containing the mapping of all sensors to the index of the sensor in the weatherstation and the software PC-Wetterstation,
                                the name and the units of the sensors. The keys must be identical to that used in the 'export_data'.  
    
    Returns:                             
    output_data_file_list:      List containing all output files written. They are automatically named following the specification: 'EXP_MM_YY.csv'.
                                For each month an own file is written according to the specification. 
                                
    Raises:
    IOError:                    A file could not be opened.
    ImportError:                A file is not compatible to PC-Wetterstation or the files are inconsistent regarding sensor types or units.
    """
    # Import data files
    data_1, rain_calib_factor_1, rain_counter_base_1, station_name_1, station_height_1, station_type_1, sensor_descriptions_dict_1, sensor_units_dict_1 = read( in_data_folder_1, input_file_name_1, sensor_list )
    data_2, rain_calib_factor_2, rain_counter_base_2, station_name_2, station_height_2, station_type_2, sensor_descriptions_dict_2, sensor_units_dict_2 = read( in_data_folder_2, input_file_name_2, sensor_list )

    # Check if the files are from the identical station (the rain counter base does not need to be identical)
    if rain_calib_factor_1 != rain_calib_factor_2 or station_name_1 != station_name_2 or station_height_1 != station_height_2 or station_type_1 != station_type_2 or sensor_descriptions_dict_1 != sensor_descriptions_dict_2 or sensor_units_dict_1 != sensor_units_dict_2:
        raise ImportError( 'The stations are not identical.' )

    # Merge data to a unique list
    merged_data = data_1 + data_2

    unique_merged_data = []
    seen_times = []
    for line in merged_data: # TODO: is this an efficient solution???
        if ( ( line['date'] + ' ' + line['time'] ) not in seen_times ): # TODO: This will delete data during shift of daylight saving!!!
            unique_merged_data.append( line )
            seen_times.append( line['date'] + ' ' + line['time'] )

    # Write merged data in data files (one for each month)
    output_data_file_list = write( out_data_folder, rain_calib_factor_1, station_name_1, station_height_1, station_type_1, unique_merged_data, sensor_list )

    return output_data_file_list
