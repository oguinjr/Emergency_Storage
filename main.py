from functions import Water
import datetime
from datetime import datetime, timedelta
import shutil
import csv

MEDIUMS = ["tall_can", "short_can", "water_brick"]
VOLUMES = {'TALL_CAN_VOL': 0.1238483, 'SHORT_CAN_VOL': 0.09007152, 'BRICK_VOL': 3.5}
columns, rows = shutil.get_terminal_size()
# Define a constant string of dashes to use as a separator line in output
breakline = "\n" + "-"*columns + "\n"
section_break = "\n" + "*"*columns + "\n"

def read_supply_list(filename):
    supply_list = []
    with open(filename, 'r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            supply_list.append({"medium": line["medium"], "medium_num": line["medium_num"], "expiration": line["expiration"]})
    return supply_list

def rewrite_file(filename, new_file_list):
    with open(filename, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["medium", "medium_num", "expiration"])
        writer.writeheader()
        writer.writerows(new_file_list)
        
# TODO: Combine remove() and remove_supply()
def remove(supply_list, match, rmv_amt):
    for line in supply_list:
        if (match['medium'] == line['medium']
            and match['medium_num'] == int(line['medium_num'])
            and int(line['medium_num']) >= rmv_amt
            and match['expiration'] == line['expiration']):
            line['medium_num'] = int(line['medium_num']) - rmv_amt
            rewrite_file(supply_list)

def sum_vol(supply_list):
    total = 0
    for entry in supply_list:
        if entry['medium'] == "tall_can":
            total += float(int(entry["medium_num"]) * VOLUMES["TALL_CAN_VOL"])
        elif entry['medium'] == "short_can":
            total += float(int(entry["medium_num"]) * VOLUMES["SHORT_CAN_VOL"])
        elif entry['medium'] == "water_brick":
            total += float(int(entry["medium_num"]) * VOLUMES["BRICK_VOL"])
    return round(total)
        

def next_exp(supply_list):
    exp_list = [x['expiration'] for x in supply_list]
    today = (datetime.now()).date()
    delta_list = []
    for date in exp_list:
        date_object = ((datetime.strptime(date, "%Y-%m-%d")).date())
        time_delta_object = (date_object - today).days
        delta_list.append(time_delta_object)
    closest_days = min(delta_list)
    closest_date_object = today + timedelta(closest_days)
    for line in supply_list:
        if datetime.strptime(line['expiration'], "%Y-%m-%d").date() == closest_date_object:
            return closest_date_object, line['medium'], line['medium_num'], closest_days

def add_supply():
    while True:
        add_med = input("Medium: ").lower().strip()
        if add_med in MEDIUMS:
            break
        print("Invalid Medium")

    while True:
        try:
            add_amt = int((input("Amount to add: ")).strip())
            break
        except ValueError:
            pass
        print(f"Invalid amount.\nPlease enter a positive integer for{add_med}.")

    while True:
        add_exp = (input("Expiration Date: ")).strip()
        try:
            datetime.strptime(add_exp, '%Y-%M-%d').date()
            break
        except ValueError:
            pass
        print("Enter a date in the format '%Y-%M-%d'")

    add_line = dict(medium=add_med, medium_num=add_amt, expiration=add_exp)
    water = Water()
    supply_list = water.get_supply_list()
    supply_list.append(add_line)
    water.rewrite_file(supply_list)


def remove_supply():
    while True:
        rmv_med = input("Medium To Remove: ").lower().strip()
        if rmv_med in MEDIUMS:
            break
        print("Invalid Medium")

    while True:
        try:
            before_amt = int((input("Amount Before: ")).strip())
            break
        except ValueError:
            pass
        print("Enter the amount before removing as positive integer.")

    while True:
        try:
            rmv_amt = int((input("How Much To Remove: ")).strip())
            break
        except ValueError:
            pass
        print("Please Enter A Positive Integer Amount")

    while True:
        try:
            rmv_exp = input("Removed Expiration Date: ")
            break
        except ValueError:
            pass
        print("Please Enter A Valid Expiration Date in the form '%Y-%M-%d'")
        
    #water = Water()
    remove_line = dict(medium=rmv_med, medium_num=before_amt, expiration=rmv_exp)
    #water.remove(remove_line, rmv_amt)
    remove(remove_line, rmv_amt)


def data_breakdown():
    GOAL_AMOUNT = 3 * 14
    water = Water()
    total_water = int(water.sum_vol())
    # pppd is gallons of water per person per day
    pppd = round(((total_water / 14) / 3), 2)
    supply_delta = GOAL_AMOUNT - total_water
    days_allowed = round(total_water / 3)

    if supply_delta > 0:
        alert = f"!!!!There is a {supply_delta} gallon water deficit currently!!!!"
    else:
        alert = f"Supply goal reached"

    return total_water, pppd, days_allowed, alert

def main():
    header_text = "|E|M|E|R|G|E|N|C|Y|" + "|S|T|O|R|A|G|E|"
    # FIXME: This math is garbage!!
    header_text_length = len(header_text)
    available_space = columns - header_text_length -4
    flank_length = int(available_space / 2)
    header_flank = "+-" * flank_length
    header = f"{header_flank}|{header_text}|{header_flank}"  
    print(f"\n\n{header}\n\n")
    print(input("Press Enter To Continue")) 
    while True:
        print(f"""
        {breakline}
        1 - Display Current Totals{breakline}
        2 - Display Closest Expiration Date{breakline}
        3 - Add Inventory{breakline}
        4 - Remove Inventory{breakline}
        5 - Get Data Breakdown{breakline}
        e - EXIT
        {breakline}
        """)
        
        choice = input("Enter the number corresponding to the desired action --> ")

        if choice == '1':
            print(f"{breakline}There is a total of {sum_vol} gal currently stored{breakline}")

        elif choice == '2':
            closest_date_obj, medium, amount, days = next_exp
            
            if days > 0:
                print(f"{breakline}On {str(closest_date_obj)} there are {amount} of {medium} expiring.\n"
                    f"That is in {days} days!{breakline}")
            elif days == 0:
                print(f"Today there are {amount} of {medium} expiring!{breakline}")
            else:
                days_since = abs(days)
                print(f"{breakline}On {str(closest_date_obj)} there were {amount} of {medium} that expired.\n"
                    f"That was {days_since} days ago!{breakline}")

        elif choice == '3':
            add_supply()
            print(f"{breakline}Now there are {sum_vol()} gallons stored{breakline}")

        elif choice == '4':
            remove_supply()
            print(f"{breakline}Now there is {sum_vol()} total gallons stored.{breakline}")

        elif choice == '5':
            total_water, pppd, days_allowed, alert = data_breakdown()
            print(f"{breakline}Right now there is a total of {total_water} gallons of water in storage\n\n")
            print(f"That will provide {pppd} gal per person for two weeks.\n\n")
            print(f"With the current supply the water will last for {days_allowed} days.\n\n")
            print(f"{alert}\n\n")

        elif choice == 'e':
            print("Goodbye\n")
            break

        else:
            print("Please enter a valid number")

        input("Press Enter to Continue")






if __name__ == "__main__":
    main()
