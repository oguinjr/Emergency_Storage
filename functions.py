# This file is no longer in use and its use has been replaced by main.py

import csv
import sys
import datetime
from datetime import datetime
from datetime import date
from datetime import timedelta


class Water:
    VOLUMES = {'TALL_CAN_VOL': 0.1238483, 'SHORT_CAN_VOL': 0.09007152, 'BRICK_VOL': 3.5}
    def __init__(self, filename="Emergency_Storage/supply.csv"):
        self.supply_list = []
        self.filename = filename
        with open(filename, 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                self.supply_list.append({"medium": line["medium"], "medium_num": line["medium_num"], "expiration": line["expiration"]})

    def get_supply_list(self):
        return self.supply_list

    def sum_vol(self):
        total = 0
        for entry in self.get_supply_list():
            if entry['medium'] == "tall_can":
                total += float(int(entry["medium_num"]) * self.VOLUMES["TALL_CAN_VOL"])
            elif entry['medium'] == "short_can":
                total += float(int(entry["medium_num"]) * self.VOLUMES["SHORT_CAN_VOL"])
            elif entry['medium'] == "water_brick":
                total += float(int(entry["medium_num"]) * self.VOLUMES["BRICK_VOL"])
        return round(total)

    def remove(self, match, rmv_amt):
        supply_list = self.get_supply_list()
        for line in supply_list:
            if (match['medium'] == line['medium']
                and match['medium_num'] == int(line['medium_num'])
                and int(line['medium_num']) >= rmv_amt
                and match['expiration'] == line['expiration']):

                line['medium_num'] = int(line['medium_num']) - rmv_amt
                self.rewrite_file(supply_list)
                break

    def next_exp(self):
        # create a list of expiration dates from csv file
        exp_list = [x['expiration'] for x in self.get_supply_list()]
        today = (datetime.now()).date()
        delta_list = []
        for date in exp_list:
            date_object = ((datetime.strptime(date, "%Y-%m-%d")).date())
            time_delta_object = (date_object - today).days
            delta_list.append(time_delta_object)

        closest_days = min(delta_list)
        closest_date_object = today + timedelta(closest_days)

        # find the line which the date string comes from
        for line in self.get_supply_list():
            if datetime.strptime(line['expiration'], "%Y-%m-%d").date() == closest_date_object:
                return closest_date_object, line['medium'], line['medium_num'], closest_days

    def rewrite_file(self, new_file_list):
        with open(self.filename, 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["medium", "medium_num", "expiration"])
            writer.writeheader()
            writer.writerows(new_file_list)
