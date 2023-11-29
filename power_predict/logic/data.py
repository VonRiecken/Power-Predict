import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

from google.cloud import bigquery
import pandas_gbq
## from colorama import Fore, Style
from pathlib import Path
import os



def clean_production_data(Electricity_Data_Explorer):

    root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    final_path = os.path.join(root_path, "raw_data")

    electricity_data_explorer = pd.read_csv(os.path.join(final_path, f'{Electricity_Data_Explorer}.csv')) ## We create a DF from the file

    ## electricity_data_explorer = pd.read_csv(f'/Users/sylvainvanhuysse/code/VonRiecken/raw_data/{Electricity_Data_Explorer}.csv')

    ## We create a list to be used as a filter on the outputs:
    filter_balance = ['Net Electricity Production']

    ## We create a list to be used as a filter on the different sources of energy:
    filter_products = ['Combustible Renewables', 'Hydro', 'Wind', 'Solar',
                'Total Renewables (Hydro, Geo, Solar, Wind, Other)', 'Other Renewables']

    ## We apply the filters to the initial dataframe:
    electricity_data_explorer = electricity_data_explorer[electricity_data_explorer['Product'].isin(filter_products)]
    electricity_data_explorer = electricity_data_explorer[electricity_data_explorer['Balance'].isin(filter_balance)]

    ## Reordering the columns:
    electricity_data_explorer = electricity_data_explorer[['Time', 'Country', 'Balance','Product','Value']]

    ## Reindexing the dataframe:
    electricity_data_explorer.index = range(len(electricity_data_explorer.index))

    ## Pivoting the table:
    electricity_data_explorer = electricity_data_explorer.pivot_table('Value', ['Time','Country', 'Balance'], 'Product')

    ## Filling up the NaN with zeros:
    electricity_data_explorer = electricity_data_explorer.fillna(0)

    ## We reset the index:
    electricity_data_explorer = electricity_data_explorer.reset_index()

    ## Changing the date format of the column 'Month_year' in electricity_data_explorer
    electricity_data_explorer['Time'] = pd.to_datetime(electricity_data_explorer['Time'], format='%B %Y')
    electricity_data_explorer = electricity_data_explorer.rename(columns={"Time": "Month_year"})

    print("✅ Eletricity Production has been cleaned up!")

    return electricity_data_explorer



def storing_weather_data():

    root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    final_path = os.path.join(root_path, "raw_data")

    list_dir = os.listdir(final_path)

    file_names = []

    ## Here we select all the csv files except Electricity_Data_Explorer that has been cleaned with another function
    for index, value in enumerate(list_dir):
        if value.endswith(".csv") and 'Electricity_Data_Explorer' not in value:
            file_names.append(value)

    ## We create a dictionary that will contain the dataframes created from each file
    dataframes = {}

    for file in file_names:

        name_df = file.split('.csv')[0] ## This line takes the name of the file without the extension .csv
        ## DataFrame = pd.DataFrame() ## We create a DF
        DataFrame = pd.read_csv(os.path.join(final_path, file)) ## We create a DF from the file

        ## Converting the date columns into rows
        DataFrame=pd.melt(DataFrame, id_vars=['Country','parameter'],value_vars=['Jan-10',
        'Feb-10','Mar-10','Apr-10','May-10','Jun-10','Jul-10', 'Aug-10','Sep-10','Oct-10', 'Nov-10', 'Dec-10','Jan-11', 'Feb-11',
        'Mar-11', 'Apr-11', 'May-11', 'Jun-11', 'Jul-11', 'Aug-11', 'Sep-11', 'Oct-11', 'Nov-11', 'Dec-11', 'Jan-12', 'Feb-12', 'Mar-12', 'Apr-12',
        'May-12','Jun-12','Jul-12','Aug-12', 'Sep-12','Oct-12','Nov-12', 'Dec-12','Jan-13',
        'Feb-13','Mar-13','Apr-13', 'May-13', 'Jun-13', 'Jul-13', 'Aug-13', 'Sep-13', 'Oct-13', 'Nov-13', 'Dec-13', 'Jan-14', 'Feb-14', 'Mar-14',
        'Apr-14', 'May-14', 'Jun-14', 'Jul-14', 'Aug-14', 'Sep-14', 'Oct-14', 'Nov-14', 'Dec-14', 'Jan-15', 'Feb-15', 'Mar-15', 'Apr-15', 'May-15', 'Jun-15',
        'Jul-15','Aug-15','Sep-15', 'Oct-15', 'Nov-15', 'Dec-15', 'Jan-16', 'Feb-16', 'Mar-16','Apr-16', 'May-16', 'Jun-16', 'Jul-16', 'Aug-16', 'Sep-16',
        'Oct-16','Nov-16','Dec-16','Jan-17','Feb-17','Mar-17','Apr-17','May-17','Jun-17','Jul-17','Aug-17','Sep-17','Oct-17','Nov-17','Dec-17','Jan-18','Feb-18','Mar-18', 'Apr-18',
        'May-18','Jun-18', 'Jul-18', 'Aug-18','Sep-18', 'Oct-18', 'Nov-18', 'Dec-18', 'Jan-19', 'Feb-19', 'Mar-19', 'Apr-19', 'May-19', 'Jun-19', 'Jul-19', 'Aug-19', 'Sep-19',
        'Oct-19', 'Nov-19', 'Dec-19', 'Jan-20', 'Feb-20','Mar-20', 'Apr-20', 'May-20', 'Jun-20', 'Jul-20', 'Aug-20', 'Sep-20', 'Oct-20', 'Nov-20', 'Dec-20',
        'Jan-21', 'Feb-21', 'Mar-21', 'Apr-21', 'May-21', 'Jun-21', 'Jul-21','Aug-21', 'Sep-21', 'Oct-21', 'Nov-21', 'Dec-21', 'Jan-22', 'Feb-22', 'Mar-22',
        'Apr-22','May-22', 'Jun-22', 'Jul-22', 'Aug-22', 'Sep-22', 'Oct-22', 'Nov-22', 'Dec-22', 'Jan-23', 'Feb-23', 'Mar-23', 'Apr-23',
        'May-23', 'Jun-23', 'Jul-23', 'Aug-23','Sep-23'],var_name='Month_year',value_name=f'value_{name_df}')

        dataframes[name_df] = DataFrame

    print("✅ Dictionary with weather data has been prepared!")

    return dataframes


def cleaning_weather_data():

    ## We call the dataframe containing the production data
    electricity_data_explorer = clean_production_data('Electricity_Data_Explorer')

    ## We call the dictionary containing the dataframes for the weather data
    dataframes = storing_weather_data()

    ## Merging CDD_18 and CDD_21
    concat1 = dataframes['CDD_18'].merge(dataframes['CDD_21'][['Country','Month_year', 'value_CDD_21']])
    concat1 = concat1.drop(['parameter'], axis=1)

    ## Merging concat1 and Global_Horizontal_Irrandiance
    concat2 = concat1.merge(dataframes['Global_Horizontal_Irrandiance'][['Country','Month_year', 'value_Global_Horizontal_Irrandiance']])

    ## Merging concat2 and HDD_16
    concat3 = concat2.merge(dataframes['HDD_16'][['Country','Month_year', 'value_HDD_16']])

    ## Merging concat3 and HDD_18
    concat4 = concat3.merge(dataframes['HDD_18'][['Country','Month_year', 'value_HDD_18']])

    ## Merging concat4 and Heat_index
    concat5 = concat4.merge(dataframes['Heat_index'][['Country','Month_year', 'value_Heat_index']])

    ## Merging concat5 and Relative_Humidty
    concat6 = concat5.merge(dataframes['Relative_Humidty'][['Country','Month_year', 'value_Relative_Humidty']])

    ## Merging concat6 and Temperature
    concat7 = concat6.merge(dataframes['Temperature'][['Country','Month_year', 'value_Temperature']])

    ## Merging concat7 and Total_Precipitation
    concat8 = concat7.merge(dataframes['Total_Precipitation'][['Country','Month_year', 'value_Total_Precipitation']])

    ## Changing the date format of the column 'Month_year' in concat8
    concat8['Month_year'] = pd.to_datetime(concat8['Month_year'], format='%b-%y')

    ## Merging concat8 (containing the weather data) and the electricity_data_explorer (containing the elec prod)
    final = electricity_data_explorer.merge(concat8[['Country','Month_year','value_CDD_18',
                                                                            'value_CDD_21',
                                                                            'value_Global_Horizontal_Irrandiance',
                                                                            'value_HDD_16',
                                                                            'value_HDD_18',
                                                                            'value_Heat_index',
                                                                            'value_Relative_Humidty',
                                                                            'value_Temperature',
                                                                            'value_Total_Precipitation']])

    ## We add a column for the total production of wind, solar, hydro (GWh)
    final['total_sol_wind_hyd'] = final['Wind'] + final['Solar'] + final['Hydro']

    # replace white spaces by underscores
    final.columns = [c.replace(' ', '_') for c in final]
    # replace "," by underscores
    final.columns = [c.replace(',', '_') for c in final]
    # replace "(" by underscores
    final.columns = [c.replace('(', '_') for c in final]
    # replace ")" by underscores
    final.columns = [c.replace(')', '_') for c in final]

    ## Specifying the data type 'datetime' of the Month_year column (needed to upload to BigQuery)
    final['Month_year'] = pd.to_datetime(final['Month_year'])

    ##os.makedirs(final_path, exist_ok=True) ## We check if the folder power_predict/data exists, if not, we create it

    root_path = root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ## We call the path of the current folder
    final_path = os.path.join(root_path, "power_predict/data") ## We place ourlseves in the folder power_predict/data

    final.to_csv(f'{final_path}/merged_dataset{datetime.now()}.csv') ## We export the dataframe as csv and store it in power_predict/data and we put the timestamp at the end of the file's name

    print(f"✅ The merged_dataset{datetime.now()}.csv has been exported!")

    return final


def upload_data_bq():

    # We call the cleaned dataframe
    cleaned_weather_data = cleaning_weather_data()

    # Replace these with your own values
    project_id = 'peppy-aileron-401514'
    dataset_id = 'Power_Predict'
    table_id = 'cleaned_data'
    json_credentials_path = '/Users/sylvainvanhuysse/code/bonawa/gcp/peppy-aileron-401514-167fede484a0.json'  # Replace with the path to your service account JSON key file

    # Set up BigQuery client
    client = bigquery.Client.from_service_account_json(json_credentials_path, project=project_id)
    ##print('BQ Client is set up')

    # Set up table reference
    table_ref = client.dataset(dataset_id).table(table_id)
    ##print('BQ table reference is set up')

    # Create the schema based on DataFrame columns for the BQ table
    schema = [bigquery.SchemaField(column, cleaned_weather_data[column].dtype.name.lower()) for column in cleaned_weather_data.columns]

    # Specifying the type of the column Month_year (necessary for BigQuery)
    schema = [bigquery.SchemaField('Month_year', 'TIMESTAMP')]

    # Check if the table exists
    table_exists = False

    try:
        existing_table = client.get_table(table_ref)
        ##print(f'Table {table_ref} already exists.')
        table_exists = True
    except Exception as e:
        print('No table was found.')

    # If the table exists, delete it
    if table_exists:
        client.delete_table(table_ref)
        print(f'✅ Table {table_ref} deleted.')

    # Create the BigQuery table with the dynamically generated schema
    table = bigquery.Table(table_ref, schema=schema)
    table = client.create_table(table)
    print(f'✅ Table {table_ref} created.')

    # Set up the destination table
    destination_table = f"{project_id}.{dataset_id}.{table_id}"

    # Upload DataFrame to BigQuery
    pandas_gbq.to_gbq(cleaned_weather_data, destination_table, project_id=project_id, if_exists='replace')

    print(f"✅ DataFrame uploaded to BigQuery table: {destination_table}")
