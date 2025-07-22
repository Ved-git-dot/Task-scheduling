from skyfield.api import load, wgs84, EarthSatellite, utc
from datetime import datetime, timedelta, timezone
import pytz


IST = pytz.timezone('Asia/Kolkata')
LAT, LON, ELEV = 8.6265, 77.0338, 160
CHECK_NEXT_HOURS = 24
TLE_FILE = "../tle.txt"
SAT_NAME = "INSPIRESAT 1"

#convert time from utc to localtime
def convert_timezone(dt_utc):
    return dt_utc.replace(tzinfo=timezone.utc).astimezone(IST)

def schedule_the_pass():
    def find_tle(name):
        with open(TLE_FILE) as f:
            lines = f.readlines()
            for i in range(len(lines) - 2):
                if name in lines[i]:
                    return lines[i].strip(), lines[i+1].strip(), lines[i+2].strip()
        raise ValueError("Satellite not found")

    def to_ist(utc_dt):
        return utc_dt.replace(tzinfo=timezone.utc).astimezone(IST)

    tle_name, line1, line2 = find_tle(SAT_NAME)

    ts = load.timescale()
    sat = EarthSatellite(line1, line2, tle_name, ts)
    observer = wgs84.latlon(LAT, LON, elevation_m=ELEV)

    t0 = ts.now()
    t1 = ts.utc(datetime.now(utc) + timedelta(hours=CHECK_NEXT_HOURS))

    times, events = sat.find_events(observer, t0, t1, altitude_degrees=1.0)

    if len(events) < 3:
        print("No full pass in next 24 hrs.")
        exit()

        # Get the next pass
    for i in range(0,len(times)-2):
        aos_time_utc = times[i].utc_datetime()
        max_time_utc = times[i + 1].utc_datetime()
        los_time_utc = times[i + 2].utc_datetime()

        aos_ist = convert_timezone(aos_time_utc)
        max_ist = convert_timezone(max_time_utc)
        los_ist = convert_timezone(los_time_utc)
        # If pass has alredy started change the next pass to
        if (max_ist - aos_ist < timedelta(minutes=25)) and (los_ist - max_ist < timedelta(minutes=25)):
            return aos_ist, los_ist
        else:
            continue



print(schedule_the_pass())
