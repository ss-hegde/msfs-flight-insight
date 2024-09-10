"""
Author: Sharath Hegde
"""

import time
import csv
from SimConnect import SimConnect, AircraftRequests

# Create a connection to MSFS
sm = SimConnect()

# Create an AircraftRequests object to request data from the sim
aq = AircraftRequests(sm)

# Get the current date and time
current_time = time.strftime("%Y%m%d_%H%M%S")

# save the log file
csv_filename = f"logs/msfs_flight_log_{current_time}.csv"


with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write to the header row
    writer.writerow([
        "Timestamp (UTC)", "Latitude", "Longitude", "Alt (ft)", "Phi (deg)", "Theta (deg)", "Psi (deg)", 
        "IAS (knots)", "TAS (knots)", "Temperature (°C)", "Pressure (hPa)"
    ])

    
    try:
        while True:
            # Get simulator time (Zulu/UTC time as decimal hours)
            sim_time = aq.get("ZULU_TIME")

            if sim_time is not None:
                # Convert simulator time to hours, minutes, and seconds
                sim_hours = int(sim_time)
                sim_minutes = int((sim_time - int(sim_time)) * 60)
                sim_seconds = int(((sim_time - int(sim_time)) * 60 - sim_minutes) * 60)

                # Format the simulator UTC time as HH:MM:SS
                sim_utc_time = f"{sim_hours:02}:{sim_minutes:02}:{sim_seconds:02}"
            else:
                sim_utc_time = "N/A"  # Handle case if ZULU_TIME is None


            # Get aircraft states
            aircraft_latitude = aq.get("PLANE_LATITUDE")
            aircraft_longitude = aq.get("PLANE_LONGITUDE")
            aircraft_altitude = aq.get("PLANE_ALTITUDE")
            aircraft_heading = aq.get("PLANE_HEADING_DEGREES_TRUE")
            v_ias = aq.get("AIRSPEED_INDICATED")
            v_tas = aq.get("AIRSPEED_TRUE")
            phi = aq.get("ATTITUDE_INDICATOR_BANK_DEGREES")
            theta = aq.get("ATTITUDE_INDICATOR_PITCH_DEGREES")

            # Get weather data
            ambient_temperature = aq.get("AMBIENT_TEMPERATURE")
            ambient_pressure = aq.get("AMBIENT_PRESSURE")

            # Write the data to the log file
            writer.writerow([
                sim_utc_time, aircraft_latitude, aircraft_longitude, 
                aircraft_altitude,  phi, theta, aircraft_heading, v_ias, v_tas,
                ambient_temperature, ambient_pressure
            ])

            print(f"Data written at simulator time {sim_utc_time}")
            time.sleep(0.1)

    except KeyboardInterrupt:
        # Exit the loop when interrupted
        print("Data collection stopped.")
