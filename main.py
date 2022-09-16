from functions import Water
import datetime
from datetime import datetime

breakline = "\n-----------------------------------------------------------------\n"
section_break = f"{breakline}{breakline}"
MEDIUMS = ["tall_can", "short_can", "water_brick"]

def main():
    while True:
        print(section_break)
        print(f"""1 - Display Current Totals{breakline}2 - Display Closest Expiration Date{breakline}\
3 - Add Inventory{breakline}4 - Remove Inventory{breakline}5 - Get Data Breakdown{breakline}\
e - EXIT{breakline}
                """)
        choice = input("Enter the number coresponding to the desired action --> ")
        if choice == '1':
            print(f"{breakline}There is a total of {get_total()} gal currently stored{breakline}")
        # if choice 2 : Return the closest expiration data, medium, amount and days until
        elif choice == '2':
            closest_date_obj, medium, amount, days = next_expiration()
            print(breakline)
            print(f"On {str(closest_date_obj)} there are {amount} of {medium}  expiring.\nThat is in {days} days!{breakline}")
        # if choice 3 : add supply to csv and print new total
        elif choice == '3':
            print()
            add_supply()
            print(breakline)
            print(f"Now there are {get_total()} gallons stored{breakline}")
        # if choice 4: remove supply
        elif choice == '4':
            print()
            remove_supply()
            print(breakline)
            print()
            print(f"Now there is {get_total()} total gallons stored.{breakline}")
        # if choice 5: data breakdown
        elif choice == '5':
            print()
            print(breakline)
            total_water, pppd, days_allowed, alert = data_breakdown()
            print(f"Right now there is a total of {total_water} gallons of water in storage\n\n")
            print(f"That will provide {pppd} gal per person for two weeks.\n\n")
            print(f"With the current supply the water will last for {days_allowed} days.\n\n")
            print(f"{alert}\n\n")
        # if choice e : exit program
        elif choice == 'e':
            print("Goodbye\n")
            break
        else:
            print("Please Enter a valid number")
        {breakline}
        input("Press Enter to Continue")

def get_total():
    water = Water()
    return water.sum_vol()


def next_expiration():
    water = Water()
    return water.next_exp()

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
        
    water = Water()
    remove_line = dict(medium=rmv_med, medium_num=before_amt, expiration=rmv_exp)
    water.remove(remove_line, rmv_amt)


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




if __name__ == "__main__":
    main()
