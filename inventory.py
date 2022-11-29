# we import the tabulate function
from tabulate import tabulate, SEPARATING_LINE

#========The beginning of the class==========
class Shoe:
    # we initialise our class with 5 attributes: country, code, product, cost, quantity
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    # we create a function which returns the cost of the object
    def get_cost(self):
        return self.cost

    # we create a function which returns the quantity of the object
    def get_quantity(self):
        return self.quantity

    # we create a function which returns a string interpretation of the object
    def __str__(self):
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"

#==========Functions outside the class==============
def read_shoes_data():
    # we use the open method to read the data from 'inventory.txt'. We then split this data to create a list. For each entry we create a Shoes object which we then add to our shoe_list. We also add the shoes sku to a separate list
    try:
        with open('inventory.txt', 'r', encoding='utf-8') as file_information:
            data = file_information.read()
        data = data.split("\n")
        for shoes in data:
            shoes = shoes.split(",")
            pair_of_shoes = Shoe(shoes[0], shoes[1], shoes[2], shoes[3], shoes[4])
            shoe_list.append(pair_of_shoes)
            sku_list.append(shoes[1].lower())
        # if the file loaded correctly we return True so that the main menu can load
        return True
    except FileNotFoundError:
        print("Sorry, inventory.txt is missing - unable to load")

# we create a function which appends new information onto 'inventory.txt'
def write_shoes_data(data):
    with open('inventory.txt', 'a+', encoding='utf-8') as file_information:
        file_information.write(f"\n{data}")

# we create a function which takes edited data as an argument. We open 'inventory.txt' with the 'w+' method, this deletes the data which is already there. 
# We then loop through our shoe_list, sending each set of data to our write_shoes_data function to be appended. Once we find the data we need to replace, matching on the shoes 'code' attribute, we edit that entry
def replace_shoes_data(edited_data):
    with open('inventory.txt', 'w+', encoding='utf-8') as file_information:
        # we first write entry 0 in our list as this contains the file headers
        file_information.write(shoe_list[0].__str__())
        for shoes in shoe_list:
            if shoes.code == edited_data.code:
                shoes = edited_data
                write_shoes_data(shoes.__str__())
            else:
                write_shoes_data(shoes.__str__())

# we create a function called 'capture_shoes()' which asks the user to enter information in regards to a new pair of shoes. We have validation to make sure that the data we collect is valid
def capture_shoes():
    print("\n------- New Shoes -------")
    country = input("Please enter the country of origin: ")
    while True:
        sku = input("Please enter the SKU of the shoes: ")
        # we check that a pair of shoes with this SKU does not already exist
        if sku.lower() in sku_list:
            print("Sorry, that SKU already exists. Please enter the correct SKU.\n")
        else:
            break
    name = input("Please enter the name of the shoes: ")
    while True:
        try:
            price = float(input("Please enter the price of the shoes: "))
            break
        except ValueError:
            print("Sorry, that cost was not valid.\n")
    while True:
        try:
            quantity = int(input("Please enter the quantity of stock: "))
            break
        except ValueError:
            print("Sorry, that quantity was not valid.\n")
    # once we have collected our data we create a new Shoe object. We append it to our shoe_list and the new shoes SKU to our sku_list. 
    # We also pass the new Shoe object to our write_shoes_data function to be added to 'inventory.txt'
    new_shoes = Shoe(country, sku, name, price, quantity)
    shoe_list.append(new_shoes)
    sku_list.append(new_shoes.code.lower())
    write_shoes_data(f"{country},{sku},{name},{price},{quantity}")
    print("----- Shoes Added! -----")

# we create a function called view_all which loops through our shoe_list. For each entry we use the __str__ function to append a string representation of that object to a new list.
# once our loop has finished we print out our new list using the tabulate function
def view_all():
    list_of_shoes = []
    print(f"{'-' * 30} View All {'-' * 30}\n")
    # we use shoe_list[1:] so we do not add the line with the file headers
    for shoes in shoe_list[1:]:
        list_of_shoes.append(shoes.__str__().split(","))
    print(tabulate(list_of_shoes, headers=["Country","Code","Product","Cost","Quantity"], tablefmt="rounded_grid"))

# we create a function called re_stock which loops through our shoe_list and checks for the shoes with the lowest stock value. 
def re_stock():
    print("------- Re-stock Shoes -------\n")
    # we start with entry 1 in our list as our initial checking value
    lowest_stock = shoe_list[1]
    # we use shoe_list[2:] so we do not check the line with the file headers and because we already have shoe_list[1] as our initial lowest_stock value
    for shoes in shoe_list[2:]:
        if int(shoes.quantity) < int(lowest_stock.quantity):
            lowest_stock = shoes
    # once the loop has finished and we have found the entry with the lowest value we print the result to the user using the tabulate function and ask how many shoes they would like to order and add this onto our lowest_stock object
    while True:
        try:
            print(f'''The lowest stock is currently: 
{tabulate([[lowest_stock.country, lowest_stock.code, lowest_stock.product, lowest_stock.cost, lowest_stock.quantity]], headers=["Country","Code","Product","Cost","Quantity"], tablefmt="rounded_grid")}''')
            new_stock = int(input("How many would you like to order? If none enter -1 : "))
            if new_stock == -1:
                break
            elif new_stock >= 1:
                lowest_stock.quantity = int(lowest_stock.quantity) + new_stock
                print("\n----- Shoe List Updated -----")
                break
            else:
                print("Sorry, that was an invalid amount")
        except ValueError:
            print("\nSorry, that value was not valid.\n")
    # we pass our edited object to out replace_shoes_data function so that 'inventory.txt' can be re-written with the updated data
    replace_shoes_data(lowest_stock)

# we create a function called search_shoe which searches loops through our shoes_list and attempts to match of the code attribute. Once we have found the correct shoes we print out the data using the tabulate function
def search_shoe():
    shoe_sku = input("\nPlease enter the SKU code you are looking for: ")
    # we check if it exists in our sku list. If it doesn't there is no point in looping and we can just print an error
    if shoe_sku.lower() in sku_list:
        # we use shoe_list[1:] so we do not search the line with the file headers
        for shoes in shoe_list[1:]:
            if shoes.code.lower() == shoe_sku.lower():
                data = [[shoes.country, shoes.code, shoes.product, shoes.cost, shoes.quantity]]
                print(tabulate(data, headers=["Country","Code","Product","Cost","Quantity"], tablefmt="rounded_grid"))
                break
    else:
        print("\nSorry, that SKU does not exist\n")

# we create a function called value_per_item which loops through our shoe_list and multiplies each items cost by its quantity to get its value. Once the loop has finished we print the data using the tabulate function
def value_per_item():
    price_table = []
    # we use shoe_list[1:] so we do not calculate the line with the file headers
    for shoes in shoe_list[1:]:
        value = float(shoes.cost) * int(shoes.quantity)
        price_table.append([f"{shoes.code}", f"£{value:.2f}"])
    print("\n------- Total Value -------")
    print(tabulate(price_table, headers=["Code", "Value"], tablefmt="rounded_grid"))

# we create a function called highest_qty which loops through our shoe_list and finds the pair with the highest quantity. We then print this result to the user using the tabulate function
def highest_qty():
    highest_stock = shoe_list[1]
    # we use shoe_list[1:] so we do not search the line with the file headers
    for shoes in shoe_list[1:]:
        if int(shoes.quantity) > int(highest_stock.quantity):
            highest_stock = shoes
    print(f'''{'-' * 30} Highest Stock {'-' * 30}\n
{tabulate([[highest_stock.country, highest_stock.code, highest_stock.product, highest_stock.cost, highest_stock.quantity]], 
headers=["Country","Code","Product","Cost","Quantity"], tablefmt="rounded_grid")}\n
We do not need to order more of this product!''')

#=============Lists===========

# The list will be used to store a list of objects of shoes.
shoe_list = []
# this list will contain every products sku
sku_list = []
# this list contains our menu choices
menu_choices = [
    ["1", "Add New Shoes"], 
    ["2", "View All Shoes"], 
    ["3", "Re-stock Shoes"], 
    ["4", "Search For Shoes"], 
    ["5", "Highest Quantity"], 
    ["6", "Total Value"],
    ["7", "Exit"]
]

#==========Main Menu=============
# we invoke the read_shoes_data function on launch to read 'inventory.txt' and populate our lists with data. If 'inventory.txt' is missing the main menu won't load and the user will receive an error
file_exists = read_shoes_data()
while file_exists:
    # we print out our main menu and ask the user to select an option. We have validation to make sure that the data they enter is valid
    print("\n--------- Main Menu ---------")
    print(tabulate(menu_choices, headers=["Option", "Function"], tablefmt="rounded_grid"))
    while True:
        try:
            selection = int(input("Please select an option: "))
            if selection > 0 and selection <= len(menu_choices):
                break
            else:
                print("Sorry, that selection is not valid")
        except ValueError:
            print("That selection was not valid. Please try again.")
    # once the user has entered a valid selection we launch the associated function
    if selection == 1:
        capture_shoes()
    elif selection == 2:
        view_all()
    elif selection == 3:
        re_stock()
    elif selection == 4:
        search_shoe()
    elif selection == 5:
        highest_qty()
    elif selection == 6:
        value_per_item()
    elif selection == 7:
        print("Goodbye!")
        exit()