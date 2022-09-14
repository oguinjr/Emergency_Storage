from functions import Water, Sanity

breakline = "\n-----------------------------------------------------------------\n"
section_break = f"{breakline}{breakline}"

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
            print(f"{breakline}On {str(closest_date_obj)} there are {amount} of {medium}  expiring.\nThat is in {days} days!{breakline}")
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
            print()
            print(f"Now there is {get_total()} total gallons stored.{breakline}")
        # if choice 5: data breakdown
        elif choice == '5':
            print()
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


def add_supply_check(add_med, add_amt, add_exp):
    try:
        sanity = Sanity()
        if not sanity.medium_check(add_med):
            print("Added Medium is invalid")
            raise Exception()
        if not sanity.amount_check(add_amt):
            print("Added Medium Amount Invalid.\nPlease Enter Integer Amount.")
            raise Exception()
        if not sanity.date_check(add_exp):
            print("Expiration date for added medium should be in the form '%Y-%M-%d'")
            raise Exception()
        return True
    except:
        return False

def remove_supply_check(rmv_med, bfr_amt, rmv_amt, rmv_exp):
    try:
        sanity = Sanity()
        if not sanity.medium_check(rmv_med):
            print("Removed Medium is Invalid")
            raise Exception()
        if not sanity.amount_check(bfr_amt):
            print("Before Amount Not A Valid Integer")
            raise Exception()
        if not sanity.amount_check(rmv_amt):
            print("Removed Amount Not A Valid Integer")
            raise Exception()
        if not sanity.date_check(rmv_exp):
            print("Expiration date for removed medium should be in the form '%Y-%M-%d'")
            raise Exception()
        if not sanity.size_check(bfr_amt, rmv_amt):
            print("Removed Amount Larger Than Before Amount")
            raise Exception()
        return True
    except:
        return False

def add_supply():
    while True:
        add_med = ((input("Medium: ")).lower()).strip()
        add_amt = int(((input("Amount to add: "))).strip())
        add_exp = (input("Expiration: ")).strip()

        if add_supply_check(add_med, add_amt, add_exp):
            add_line = dict(medium=add_med, medium_num=add_amt, expiration=add_exp)
            water = Water()
            supply_list = water.get_supply_list()
            supply_list.append(add_line)
            water.rewrite_file(supply_list)
            break
        else:
            print("Something went wrong while adding")
            continue


def remove_supply():
    while True:
        rmv_med = input("Medium: ")
        before_amt = int(input("Amount Before: "))
        rmv_amt = int(input("Removed: "))
        rmv_exp = input("Expiration: ")

        if remove_supply_check(rmv_med, before_amt, rmv_amt, rmv_exp):
            water = Water()
            remove_line = dict(medium=rmv_med, medium_num=before_amt, expiration=rmv_exp)
            water.remove(remove_line, rmv_amt)
            break
        else:
            print("Something went wrong with the subtracting.")
            continue

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
