import os


from cleaning_data import cleaning_weather_data


print(os.path.dirname(os.path.dirname(__file__)))

root_path = os.path.dirname(os.path.dirname(__file__))
print(os.path.join(root_path, "raw_data"))


cleaning_weather_data()

##print(Cleaning.clean_production_data('Electricity_Data_Explorer'))
##print(Cleaning.storing_weather_data)

## print(cleaning_weather_data())
## print(Cleaning.cleaning_weather_data)
