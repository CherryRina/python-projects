from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

money_machine = MoneyMachine()
coffee_maker = CoffeeMaker()
menu = Menu()

in_loop = True

# report
coffee_maker.report()
money_machine.report()

while in_loop:
    options = menu.get_items()
    answear = input(f"what would you like to drink {options}? ")

    # turn off
    if answear =="off":
        in_loop = False

    #report
    elif answear == "report":
        coffee_maker.report()
        money_machine.report()

    # order drink
    else:
        # Check resources
        drink = menu.find_drink(answear)
        if coffee_maker.is_resource_sufficient(drink):
            if money_machine.make_payment(drink.cost):
                coffee_maker.make_coffee(drink)

