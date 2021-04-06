import csv
import json
from os import name
from helpers import datetime_to_str


def write_to_csv(results, filename):

    fieldnames = ('datetime_utc',
                  'distance_au',
                  'velocity_km_s',
                  'designation',
                  'name',
                  'diameter_km',
                  'potentially_hazardous')

    with open(filename, 'w') as fd:
        writer = csv.DictWriter(fd, fieldnames=fieldnames)
        writer.writeheader()

        for ca in results:
            writer.writerow({
                'datetime_utc': datetime_to_str(ca.time),
                'distance_au': ca.distance,
                'velocity_km_s': ca.velocity,
                'designation': ca.designation,
                'name': ca.neo.name,
                'diameter_km': ca.neo.diameter,
                'potentially_hazardous': str(ca.neo.hazardous)})


def write_to_json(results, filename):
    s = list()

    for ca in results:
        dict_obj = {
            'datetime_utc': datetime_to_str(ca.time),
            'distance_au': ca.distance,
            'velocity_km_s': ca.velocity,
            'neo': {
                'designation': ca.designation,
                'name': ca.neo.name,
                'diameter_km': ca.neo.diameter,
                'potentially_hazardous': ca.neo.hazardous
            }
        }
        s.append(dict_obj)

    with open(filename, 'w') as fd:
        fd.write(json.dumps(s, indent=2))
