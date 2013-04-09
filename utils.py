import csv
from datetime import date, datetime, timedelta


def is_rangers_at_home(today=date.today()):
    with open('fixtures.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if row[0][:7].lower() == "rangers":
                day, month, year = [int(x) for x in row[2].strip().split("-")]
                
                fixture_day = date(year, month, day)

                if fixture_day == today:
                    hour, minute = [int(x) for x in row[3].strip().split(":")]
                    kickoff = datetime(year, month, day, hour, minute)

                    keep_away_period = timedelta(hours=2)
                    match_duration = timedelta(hours=2)

                    return {
                        "start": kickoff - keep_away_period, 
                        "end": kickoff + keep_away_period + match_duration, 
                        "kickoff": kickoff
                    }

    return False