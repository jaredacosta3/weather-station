from gpiozero import Button
import time
import database
import math
import bme280_sensor
import wind_direction_byo
import statistics
import ds18b20_therm
import database

wind_count = 0
radius_cm = 9.0
wind_interval = 5
interval = 5
CM_IN_A_KM = 100000.0
SECS_IN_AN_HOUR = 3600
ADJUSTMENT = 1.18
BUCKET_SIZE = 0.2794
rain_count = 0;
gust = 0
store_speeds = []
store_directions = []

def spin():
	global wind_count
	wind_count = wind_count + 1

def calculate_speed():
	global wind_count
	global gust
	circumference_cm = (2 * math.pi) * radius_cm
	rotations = wind_count / 2.0

	dist_km = (circumference_cm * rotations) / CM_IN_A_KM

	km_per_sec = dist_km / time_sec
	km_per_hour = km_per_sec * SEC_IN_AN_HOUR

	final_speed = km_per_hour * ADJUSTMENT

	return final_speed

def bucket_tipped():
	global rain_count
	rain_count = rain_count + 1

def reset_rainfall():
	global rain_count
	rain_count = 0

def reset_wind():
	global wind_count
	wind_count = 0

def reset_gust():
	global gust
	gust = 0

wind_speed_sensor = Button(5)
wind_speed_sensor.when_activated = spin
temp_probe = ds18b20_therm.DS18B20()

#db = database.weather_database()
while True:
	start_time = time.timer()
	while time.time() - start_timer <= interval:
		wind_start_time = time_time()
		reset_wind()
		while time.time() - wind_start_time <= wind_interval:
			store_directions.append(wind_direction_byo.get_value())
		final_speed = calculate_speed(wind_interval)
		store_speeds.append(final_speed)
	wind_average = wind_direction_byo.get_average(store_directions)
	wind_gust = max(store_speeds)
	wind_speed = statistics.mean(store_speeds)
	rainfall = rain_count* BUCKET_SIZE
	reset_rainfall()
	store_speeds = []
	store_directions = []
	ground_temp = temp_probe.read_temp()
	humidity, pressure, ambient_temp = bme280_sensor.read_all()

	print(wind_average, wind_speed, wind_gust, rainfall, humidity, pressure, ambient_temp, ground_temp)
	#db.insert(ambient_temp, ground_temp, 0, pressure, humidity, wind_average, wind_speed, wind_gust, rainfall)
