import csv
import sys
import datetime
from datetime import datetime
from datetime import date
from datetime import timedelta

D = "/workspaces/22947782/project/type_data.csv"
coeffs = {'TALL_CAN_VOL': 0.1238483, 'SHORT_CAN_VOL': 0.09007152, 'BRICK_VOL': 3.5}


class Water:
    def __init__(self):
        self.dic_list = []
        with open("/workspaces/22947782/project/supply.csv", 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                self.dic_list.append({"type": line["type"], "medium": line["medium"], "medium_num": line["medium_num"], "expiration": line["expiration"]})



    # Getter
    def get_dic_list(self):
        return self.dic_list

    def sum_vol(self):
        total = 0
        for entry in self.get_dic_list():
            if entry['medium'] == "tall_can":
                total += float(int(entry["medium_num"]) * coeffs["TALL_CAN_VOL"])
            elif entry['medium'] == "short_can":
                total += float(int(entry["medium_num"]) * coeffs["SHORT_CAN_VOL"])
            elif entry['medium'] == "water_brick":
                total += float(int(entry["medium_num"]) * coeffs["BRICK_VOL"])
        return round(total)



    def remove(self, match, rmv):
        dic_list = self.get_dic_list()
        for line in dic_list:
            if match['medium'] == line['medium']:
                if match['medium_num'] == int(line['medium_num']):
                    if match['expiration'] == line['expiration']:
                        if int(line["medium_num"]) >= rmv:
                            line["medium_num"] = int(line["medium_num"]) - rmv
                            self.rewrite_file(dic_list)
                            break
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
            else:
                continue

    ################### THIS DOES NOT ALLOW FOR MULTIPLE DATES THAT ARE THE SAME ######################
    def next_exp(self):
        # create a list of expiration dates from csv file
        exp_list = list(map((lambda x: x['expiration']), self.get_dic_list()))
        today = (datetime.now()).date()
        delta_list = []

        for date in exp_list:
            date_object = ((datetime.strptime(date, "%Y-%m-%d")).date())
            time_delta = (date_object - today).days
            delta_list.append(time_delta)

        closest_days = min(delta_list)
        closest_date_obj = today + timedelta(closest_days)

        # find the line which the date string comes from
        for line in self.get_dic_list():
            if datetime.strptime(line['expiration'], "%Y-%m-%d").date() == closest_date_obj:
                return closest_date_obj, line['medium'], line['medium_num'], closest_days

    def rewrite_file(self, new_file):
        with open("/workspaces/22947782/project/supply.csv", 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["type", "medium", "medium_num", "expiration"])
            writer.writeheader()
            writer.writerows(new_file)
