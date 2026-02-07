import pandas as pd
import os
import io


def parse_trackpoint(line):
    # Extract components from the line
    time_utc = line[1:7]  # HHMMSS
    latitude_raw = line[7:15]  # DDMMmmmN
    longitude_raw = line[15:24]  # DDDMMmmmE
    gps_altitude = int(line[25:30])  # GGGG
    pressure_altitude = int(line[30:35])  # LLLL

    # Convert UTC time
    hours = int(time_utc[:2])
    minutes = int(time_utc[2:4])
    seconds = int(time_utc[4:6])

    # Convert latitude to decimal degrees
    latitude_deg = int(latitude_raw[:2])
    latitude_min = float(latitude_raw[2:7]) / 1000
    latitude = latitude_deg + latitude_min / 60
    if latitude_raw[7] == "S":
        latitude *= -1

    # Convert longitude to decimal degrees
    longitude_deg = int(longitude_raw[:3])
    longitude_min = float(longitude_raw[3:8]) / 1000
    longitude = longitude_deg + longitude_min / 60
    if longitude_raw[8] == "W":
        longitude *= -1

    return {
        "time": f"{hours:02}:{minutes:02}:{seconds:02}",
        "latitude": latitude,
        "longitude": longitude,
        "gps_altitude_m": gps_altitude,
        "pressure_altitude_m": pressure_altitude,
    }


def getdata(file_data, loginterval=1):
    lines = file_data.splitlines()
    flight_data = [line for line in lines if line.startswith("B")]
    flight_date = [line for line in lines if line.startswith("HFDTE")][0].strip()
    for x in range(len(flight_date)):
        if flight_date[x].isdigit():
            flight_date = flight_date[x : x + 6]
            break
    pilot_name = [line for line in lines if "PILOT" in line][0]
    pilot_name = pilot_name.split(":")[1].strip()
    df = pd.DataFrame([parse_trackpoint(line) for line in flight_data])
    df["datetime"] = pd.to_datetime(
        flight_date + " " + df["time"], format="%d%m%y %H:%M:%S"
    )
    df["pilot"] = pilot_name
    df = df[
        [
            "pilot",
            "datetime",
            "latitude",
            "longitude",
            "gps_altitude_m",
            "pressure_altitude_m",
        ]
    ]
    df = df.drop_duplicates(subset=["datetime"])
    if loginterval > 1:
        df = df.iloc[::loginterval, :]
    return df


def convert_igc_to_excel(file_data):
    df = getdata(file_data)
    output = io.BytesIO()
    df.to_excel(output, index=False, engine="openpyxl")
    return output.getvalue()


def fligth_data_to_json(flight_data):
    df = getdata(flight_data)
    df = df[
        [
            "longitude", #longitude should be first for Cesium
            "latitude",
            "pressure_altitude_m",
        ]
    ]

    return df.to_json(orient="values")


if __name__ == "__main__":
    file_path = "D:/wolf/Documents/Projelerim/Paragliding_Portal/tmp/250519102215.igc"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"Generated Excel size: {len(convert_igc_to_excel(content))} bytes")
