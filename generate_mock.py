#!/usr/bin/env python3
import json
from datetime import datetime, timezone, timedelta

BASE_TIME = datetime(2024, 5, 26, 13, 0, 0, tzinfo=timezone.utc)

def ts(offset_seconds=0):
    t = BASE_TIME + timedelta(seconds=offset_seconds)
    return t.strftime("%Y-%m-%dT%H:%M:%S.000Z")

DRIVERS = [
    # nr, short, first, last, broadcast, team, color, country, pos, gap, laptime
    ("16", "LEC", "Charles",   "Leclerc",    "C LECLERC",    "Ferrari",          "E8002D", "MON",  1,  "",          "1:13.166"),
    ("55", "SAI", "Carlos",    "Sainz",      "C SAINZ",      "Ferrari",          "E8002D", "ESP",  2,  "+7.152",    "1:13.490"),
    ("81", "PIA", "Oscar",     "Piastri",    "O PIASTRI",    "McLaren",          "FF8000", "AUS",  3,  "+15.621",   "1:13.601"),
    ("4",  "NOR", "Lando",     "Norris",     "L NORRIS",     "McLaren",          "FF8000", "GBR",  4,  "+20.357",   "1:13.210"),
    ("20", "MAG", "Kevin",     "Magnussen",  "K MAGNUSSEN",  "Haas F1 Team",     "B6BABD", "DNK",  5,  "+55.022",   "1:14.100"),
    ("63", "RUS", "George",    "Russell",    "G RUSSELL",    "Mercedes",         "27F4D2", "GBR",  6,  "+56.014",   "1:13.890"),
    ("44", "HAM", "Lewis",     "Hamilton",   "L HAMILTON",   "Mercedes",         "27F4D2", "GBR",  7,  "+59.527",   "1:13.950"),
    ("22", "TSU", "Yuki",      "Tsunoda",    "Y TSUNODA",    "RB",               "6692FF", "JPN",  8,  "+60.873",   "1:14.200"),
    ("14", "ALO", "Fernando",  "Alonso",     "F ALONSO",     "Aston Martin",     "358C75", "ESP",  9,  "+73.125",   "1:14.050"),
    ("18", "STR", "Lance",     "Stroll",     "L STROLL",     "Aston Martin",     "358C75", "CAN", 10,  "+73.908",   "1:14.500"),
    ("10", "GAS", "Pierre",    "Gasly",      "P GASLY",      "Alpine",           "0093CC", "FRA", 11,  "+1 LAP",    "1:14.800"),
    ("23", "ALB", "Alexander", "Albon",      "A ALBON",      "Williams",         "64C4FF", "THA", 12,  "+1 LAP",    "1:15.000"),
    ("27", "HUL", "Nico",      "Hulkenberg", "N HULKENBERG", "Haas F1 Team",     "B6BABD", "DEU", 13,  "+1 LAP",    "1:14.900"),
    ("1",  "VER", "Max",       "Verstappen", "M VERSTAPPEN", "Red Bull Racing",  "3671C6", "NLD", 14,  "+1 LAP",    "1:13.800"),
    ("3",  "RIC", "Daniel",    "Ricciardo",  "D RICCIARDO",  "RB",               "6692FF", "AUS", 15,  "+2 LAPS",   "1:15.200"),
    ("11", "PER", "Sergio",    "Perez",      "S PEREZ",      "Red Bull Racing",  "3671C6", "MEX", 16,  "+2 LAPS",   "1:14.700"),
    ("31", "OCO", "Esteban",   "Ocon",       "E OCON",       "Alpine",           "0093CC", "FRA", 17,  "+2 LAPS",   "1:15.100"),
    ("77", "BOT", "Valtteri",  "Bottas",     "V BOTTAS",     "Kick Sauber",      "52E252", "FIN", 18,  "+3 LAPS",   "1:15.500"),
    ("24", "ZHO", "Zhou",      "Guanyu",     "GUANYU ZHOU",  "Kick Sauber",      "52E252", "CHN", 19,  "+3 LAPS",   "1:15.600"),
    ("2",  "SAR", "Logan",     "Sargeant",   "L SARGEANT",   "Williams",         "64C4FF", "USA", 20,  "+3 LAPS",   "1:15.800"),
]

STINTS = {
    "16": [{"Compound": "HARD",         "TotalLaps": 40, "New": "TRUE"}],
    "55": [{"Compound": "HARD",         "TotalLaps": 40, "New": "TRUE"}],
    "81": [{"Compound": "MEDIUM",       "TotalLaps": 25, "New": "FALSE"}, {"Compound": "HARD",   "TotalLaps": 15, "New": "TRUE"}],
    "4":  [{"Compound": "MEDIUM",       "TotalLaps": 25, "New": "FALSE"}, {"Compound": "HARD",   "TotalLaps": 15, "New": "TRUE"}],
    "20": [{"Compound": "HARD",         "TotalLaps": 40, "New": "FALSE"}],
    "63": [{"Compound": "MEDIUM",       "TotalLaps": 30, "New": "FALSE"}, {"Compound": "HARD",   "TotalLaps": 10, "New": "TRUE"}],
    "44": [{"Compound": "SOFT",         "TotalLaps": 15, "New": "TRUE"},  {"Compound": "HARD",   "TotalLaps": 25, "New": "FALSE"}],
    "22": [{"Compound": "HARD",         "TotalLaps": 40, "New": "FALSE"}],
    "14": [{"Compound": "HARD",         "TotalLaps": 40, "New": "FALSE"}],
    "18": [{"Compound": "MEDIUM",       "TotalLaps": 40, "New": "FALSE"}],
    "10": [{"Compound": "SOFT",         "TotalLaps": 20, "New": "TRUE"},  {"Compound": "MEDIUM", "TotalLaps": 20, "New": "FALSE"}],
    "23": [{"Compound": "MEDIUM",       "TotalLaps": 40, "New": "FALSE"}],
    "27": [{"Compound": "HARD",         "TotalLaps": 40, "New": "FALSE"}],
    "1":  [{"Compound": "SOFT",         "TotalLaps": 5,  "New": "TRUE"},  {"Compound": "HARD",   "TotalLaps": 35, "New": "FALSE"}],
    "3":  [{"Compound": "SOFT",         "TotalLaps": 20, "New": "FALSE"}, {"Compound": "HARD",   "TotalLaps": 20, "New": "FALSE"}],
    "11": [{"Compound": "HARD",         "TotalLaps": 40, "New": "FALSE"}],
    "31": [{"Compound": "MEDIUM",       "TotalLaps": 40, "New": "FALSE"}],
    "77": [{"Compound": "HARD",         "TotalLaps": 40, "New": "FALSE"}],
    "24": [{"Compound": "MEDIUM",       "TotalLaps": 40, "New": "FALSE"}],
    "2":  [{"Compound": "SOFT",         "TotalLaps": 20, "New": "FALSE"}, {"Compound": "HARD",   "TotalLaps": 20, "New": "FALSE"}],
}

def sector(value, personal_best=False, overall_fastest=False):
    return {
        "Stopped": False,
        "Value": value,
        "Status": 2051 if overall_fastest else (2049 if personal_best else 2048),
        "OverallFastest": overall_fastest,
        "PersonalFastest": personal_best,
        "Segments": [{"Status": 2048}] * 3,
    }

def speed(value):
    return {"Value": value, "Status": 2048, "OverallFastest": False, "PersonalFastest": False}

def build_driver_list():
    dl = {}
    for nr, short, first, last, broadcast, team, color, country, pos, gap, laptime in DRIVERS:
        dl[nr] = {
            "RacingNumber": nr,
            "BroadcastName": broadcast,
            "FullName": f"{first.upper()} {last.upper()}",
            "Tla": short,
            "Line": pos,
            "TeamName": team,
            "TeamColour": color,
            "FirstName": first,
            "LastName": last,
            "Reference": f"{first.upper()}_{last.upper()}",
            "HeadshotUrl": "",
            "CountryCode": country,
        }
    return dl

def build_timing_data(current_lap):
    lines = {}
    for nr, short, first, last, broadcast, team, color, country, pos, gap, laptime in DRIVERS:
        is_leader = pos == 1
        laps_done = max(1, current_lap - (pos - 1) // 10)
        lines[nr] = {
            "GapToLeader": gap,
            "IntervalToPositionAhead": {"Value": "+0.000", "Catching": False} if not is_leader else {},
            "Line": pos,
            "Position": str(pos),
            "ShowPosition": True,
            "RacingNumber": nr,
            "Retired": False,
            "InPit": False,
            "PitOut": False,
            "Stopped": False,
            "Status": 0,
            "Sectors": [
                sector("26.123", overall_fastest=is_leader, personal_best=is_leader),
                sector("40.456"),
                sector("6.587"),
            ],
            "Speeds": {
                "I1": speed("261"),
                "I2": speed("201"),
                "Fl": speed("180"),
                "St": speed("289"),
            },
            "BestLapTime": {"Value": laptime, "Position": pos},
            "LastLapTime": {
                "Value": laptime,
                "Status": 2051 if is_leader else 2048,
                "OverallFastest": is_leader,
                "PersonalFastest": is_leader,
            },
            "NumberOfLaps": laps_done,
        }
    return {"Lines": lines, "Withheld": False}

def build_timing_app_data():
    lines = {}
    for nr, short, first, last, broadcast, team, color, country, pos, gap, laptime in DRIVERS:
        lines[nr] = {
            "RacingNumber": nr,
            "Stints": STINTS[nr],
            "Line": pos,
            "GridPos": str(pos),
        }
    return {"Lines": lines}

def build_timing_stats():
    lines = {}
    for nr, short, first, last, broadcast, team, color, country, pos, gap, laptime in DRIVERS:
        lines[nr] = {
            "Line": pos,
            "RacingNumber": nr,
            "PersonalBestLapTime": {"Value": laptime, "Position": pos},
            "BestSectors": [
                {"Value": "26.123", "Position": 1},
                {"Value": "40.456", "Position": 2},
                {"Value": "6.587",  "Position": 3},
            ],
            "BestSpeeds": {
                "I1": {"Value": "261", "Position": 1},
                "I2": {"Value": "201", "Position": 2},
                "Fl": {"Value": "180", "Position": 3},
                "St": {"Value": "289", "Position": 4},
            },
        }
    return {"Lines": lines, "SessionType": "Race", "Withheld": False, "_kf": False}

def update_msg(topic, data, offset):
    return json.dumps({"M": [{"H": "Streaming", "M": "feed", "A": [topic, data, ts(offset)]}]})

def main():
    current_lap = 40
    total_laps  = 78
    offset = 0

    initial = {
        "Heartbeat": {"Utc": ts(0)},
        "ExtrapolatedClock": {"Utc": ts(0), "Remaining": "00:58:00", "Extrapolating": True},
        "SessionInfo": {
            "Meeting": {
                "Key": 1229,
                "Name": "Monaco Grand Prix",
                "OfficialName": "FORMULA 1 GRAND PRIX DE MONACO 2024",
                "Location": "Monte Carlo",
                "Country": {"Key": 68, "Code": "MCO", "Name": "Monaco"},
                "Circuit":  {"Key": 9, "ShortName": "Monaco"},
            },
            "ArchiveStatus": {"Status": "Generating"},
            "Key": 9587,
            "Type": "Race",
            "Name": "Race",
            "StartDate": "2024-05-26T13:00:00",
            "EndDate":   "2024-05-26T15:00:00",
            "GmtOffset": "02:00:00",
            "Path": "2024/2024-05-26_Monaco_Grand_Prix/2024-05-26_Race/",
            "Number": 1,
        },
        "SessionStatus":  {"Status": "Started"},
        "LapCount":       {"CurrentLap": current_lap, "TotalLaps": total_laps},
        "TrackStatus":    {"Status": "1", "Message": "AllClear"},
        "WeatherData": {
            "AirTemp": "24.8", "Humidity": "60", "Pressure": "1017.3",
            "Rainfall": "0", "TrackTemp": "43.2", "WindDirection": "225", "WindSpeed": "1.9",
        },
        "DriverList":     build_driver_list(),
        "TimingData":     build_timing_data(current_lap),
        "TimingAppData":  build_timing_app_data(),
        "TimingStats":    build_timing_stats(),
        "SessionData": {
            "Series": [{"Utc": ts(0), "Lap": 1}],
            "StatusSeries": [
                {"Utc": ts(0),  "TrackStatus": "1"},
                {"Utc": ts(5),  "SesionStatus": "Started"},
            ],
        },
        "RaceControlMessages": {
            "Messages": [
                {"Utc": ts(0),    "Lap": 1,  "Message": "RACE STARTED",                                          "Category": "Other"},
                {"Utc": ts(900),  "Lap": 15, "Message": "VIRTUAL SAFETY CAR DEPLOYED",                           "Category": "SafetyCar", "Flag": "YELLOW"},
                {"Utc": ts(1020), "Lap": 16, "Message": "VIRTUAL SAFETY CAR ENDING",                             "Category": "SafetyCar"},
                {"Utc": ts(1200), "Lap": 20, "Message": "CAR 1 (VER) 5 SECOND TIME PENALTY - CAUSING A COLLISION","Category": "Other",     "Flag": "BLACK AND WHITE"},
            ]
        },
    }

    print(json.dumps({"I": "1", "R": initial}))

    # Simulate ~35 more laps, one lap ≈ 75 seconds at Monaco
    for lap in range(current_lap + 1, total_laps + 1):
        offset += 75

        # Heartbeat every lap
        print(update_msg("Heartbeat", {"Utc": ts(offset)}, offset))

        # LapCount
        print(update_msg("LapCount", {"CurrentLap": lap, "TotalLaps": total_laps}, offset))

        # Weather every 5 laps
        if lap % 5 == 0:
            temp_var = (lap % 3) * 0.2
            print(update_msg("WeatherData", {
                "AirTemp":      str(round(24.8 + temp_var, 1)),
                "Humidity":     "60",
                "Pressure":     "1017.3",
                "Rainfall":     "0",
                "TrackTemp":    str(round(43.2 + temp_var * 0.5, 1)),
                "WindDirection":"225",
                "WindSpeed":    "1.9",
            }, offset))

        # Timing updates — slight gap variation
        timing_update = {}
        for nr, short, first, last, broadcast, team, color, country, pos, gap, laptime in DRIVERS:
            laps_done = max(1, lap - (pos - 1) // 10)
            is_leader = pos == 1
            timing_update[nr] = {
                "LastLapTime": {
                    "Value": laptime,
                    "Status": 2051 if is_leader else 2048,
                    "OverallFastest": is_leader,
                    "PersonalFastest": is_leader,
                },
                "NumberOfLaps": laps_done,
            }
        print(update_msg("TimingData", {"Lines": timing_update}, offset))

        # Safety car on lap 55
        if lap == 55:
            print(update_msg("TrackStatus", {"Status": "4", "Message": "SafetyCar"}, offset))
            print(update_msg("RaceControlMessages", {"Messages": [
                {"Utc": ts(offset), "Lap": lap, "Message": "SAFETY CAR DEPLOYED", "Category": "SafetyCar", "Flag": "YELLOW"}
            ]}, offset))

        if lap == 58:
            print(update_msg("TrackStatus", {"Status": "1", "Message": "AllClear"}, offset))
            print(update_msg("RaceControlMessages", {"Messages": [
                {"Utc": ts(offset), "Lap": lap, "Message": "SAFETY CAR IN THIS LAP", "Category": "SafetyCar", "Flag": "GREEN"}
            ]}, offset))

        # Final lap
        if lap == total_laps:
            print(update_msg("SessionStatus", {"Status": "Finished"}, offset))
            print(update_msg("TrackStatus",   {"Status": "1", "Message": "AllClear"}, offset))
            print(update_msg("RaceControlMessages", {"Messages": [
                {"Utc": ts(offset), "Lap": lap, "Message": "CHEQUERED FLAG", "Category": "Flag", "Flag": "CHEQUERED"}
            ]}, offset))

    # Loop back: sleep and restart (simulator loops by replaying the file on reconnect)

if __name__ == "__main__":
    main()
