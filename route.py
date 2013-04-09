from datetime import date, datetime, timedelta
from stations import stations
from utils import rangers_is_at_home
from math import floor
import random
from colorama import Fore, Back, Style
from colorama import init as colorama_init

colorama_init()

def random_pub_name():
    starts = ["Nag's", "Queen's", "Vicar's", "King's", "Barmaid's", "Jester's", "Bird's", "Lion's"]
    ends = ["Arms", "Legs", "Head", "Tail", "Knackers", "Knees"]

    return "The {whos} {what}".format(whos=random.choice(starts), what=random.choice(ends))

def route():
    warnings = []
    # we want to go inner
    stations.reverse()

    for s in stations:
        s["correct_type"] = True if random.randint(1,10) > 5 else False
        if not s["correct_type"]:
            warnings.append({
                "color": Fore.MAGENTA,
                "msg": "Could not find a {venue_type} in {station}. Defaulted to {default}".format(
                    venue_type = random.choice(["Strip Club", "Bistro", "Gastro", "Gay Bar", "Cocktail Bar"]),
                    station = s["name"],
                    default = random.choice(["Pub", "Dive Bar"])
                )
            })

    # timings for stops
    time_per_stop = timedelta(minutes=42)
    travel_time = timedelta(minutes=10)
    today = date.today()
    crawl_start = datetime(today.year, today.month, today.day, 12, 00)
    current_crawl_time = crawl_start

    # Get Ibrox tae fuck if Rangers is playing
    at_home = rangers_is_at_home()
    if at_home:
        warnings.append({
            "color": Fore.RED,
            "msg": "# Rangers is playing at home at {kickoff}. Make sure you leave Ibrox by {start}".format(
            kickoff=at_home["kickoff"].time(),
            start=at_home["start"].time()
        )})
        planned_route = stations[4:] + stations[:4]
    else:
        planned_route = stations[1:] + stations[:1]

    if len(warnings) > 0:
        print(Back.GREEN + Fore.WHITE + "-- Notices:" + Fore.RESET + Back.RESET)
        for warning in warnings:
            print(warning["color"] + warning["msg"] + Fore.RESET)

    print(Back.GREEN + Fore.WHITE + "-- Route:" + Fore.RESET + Back.RESET)
    index = 1
    for s in planned_route:

        rating = random.randint(1,5)

        print "#{i} - {station} - {pub} {rating}".format(
            i=index,
            station=s["name"],
            pub=random_pub_name(),
            rating="*" * rating
        )

        spaces = " " * int(floor(index / 10) + 1)
        start_time = current_crawl_time
        end_time = current_crawl_time + time_per_stop - travel_time

        print " {spacing}   be there for {start} and leave by {end}".format(
            spacing=spaces,
            start=Style.BRIGHT + str(start_time.time()) + Style.RESET_ALL,
            end=Style.BRIGHT + str(end_time.time()) + Style.RESET_ALL
        )

        current_crawl_time = current_crawl_time + time_per_stop
        index += 1

route()