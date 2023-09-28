# Cara Zablan 001451728

import csv
import datetime

from HashTable import HashTable
from Package import Package

current_time = datetime.datetime.now()
my_hash_table = HashTable()
distances = [] # list that holds distance data from the distance file
addresses = {} # dictionary that holds the address data from the distance file
mileage = [] # list that holds the mileage traveled by each truck

# Creates package objects from the packages file
# Loads the package objects into my_hash_table
def loadPackageData(file_name):
    with open(file_name) as packages:
        packageData = csv.reader(packages, delimiter=',')
        for package in packageData:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZipcode = package[4]
            pDeadline = package[5]
            pWeight = package[6]

            # package object
            p = Package(pID, pAddress, pCity, pState, pZipcode, pDeadline, pWeight)

            # insert into hash table
            my_hash_table.insert(p)

# Creates distance list and addresses dictionary from the distances file
# Removes the first item in every line and adds it to the addresses dictionary
# Adds the rest of the items on the line to the distances list
def loadDistanceData(file_name):
    with open(file_name) as distance:
        distanceData = csv.reader(distance, delimiter=',')
        index = 0
        for line in distanceData:
            addresses[line.pop(0)] = index
            index += 1
            distances.append(line)


loadPackageData('package.csv')
loadDistanceData('distance.csv')

# Truck lists for the three trucks containing package ID in each
truck_1 = [14, 15, 16, 34, 7, 29, 1, 4, 40, 20, 21, 19, 13, 39, 30, 37]
truck_2 = [6, 36, 27, 35, 38, 25, 26, 22, 18, 31, 32, 11, 3, 23, 17]
truck_3 = [24, 12, 2, 33, 9, 10, 5, 8, 28]

# Method for finding the locations associated with each package in the truck list
# Uses the package IDs in the truck list to find the index in the address dictionary
# Also adds the loading time of the truck to each package object
def findLocations(truck, truck_time):
    # stores the address index for each package
    pkg_indexes = []
    for package_ID in truck:
        package = my_hash_table.search(package_ID)
        # adds loading time to package object
        package.loading_time = truck_time.time()
        # adds address index to pkg_indexes list
        pkg_indexes.append(addresses.get(package.address))
    return pkg_indexes


# Method for delivering packages
# Uses the Nearest Neighbor Algorithm, time complexity: O(N^2)
# Calculates the distance traveled by each truck between locations
# Also adds the delivery time for each package
def makeDeliveries(truck, truck_time):
    pkg_indexes = findLocations(truck, truck_time)
    # stores the distances of each package in route
    route_distances = []
    # stores package ID and corresponding distances
    current_location = 0
    route_mileage = 0
    while truck:
        # temporary list of distances for evaluating nearest neighbor
        pkg_distances = []
        # distances for every item in the pkg_indexes list is determined using the distances list
        for item in pkg_indexes:
            if item > current_location:
                distance = float(distances[item][current_location])
            else:
                distance = float(distances[current_location][item])
            # the distance is added to the pkg_distances list
            pkg_distances.append(distance)
        # takes the index with the smallest value from the pkg_distances list
        min_pkg_index = pkg_distances.index(min(pkg_distances))
        # gets the item from pkg_indexes that corresponds with min_pkg_index
        current_location = pkg_indexes[min_pkg_index]
        # adds the minimum distance to the route_distances list
        route_distances.append(min(pkg_distances))
        package = my_hash_table.search(truck[min_pkg_index])
        # removes the item from the pkg_indexes list
        pkg_indexes.pop(min_pkg_index)
        # removes package from truck list
        truck.pop(min_pkg_index)
        # calculates the total distance traveled by the truck
        route_mileage = sum(route_distances)
        # calculates the minutes traveled between each location
        pkg_minutes = min(pkg_distances) * (60 / 18)
        ts = truck_time + datetime.timedelta(minutes=pkg_minutes)
        # converts datetime to time value and adds it to the package object
        package.delivery_time = ts.time()
        # updates the truck time to reflect the truck lists end time
        truck_time = ts
    # adds the truck's mileage to the mileage list
    mileage.append(route_mileage)
    return truck_time

# Calculates the total mileage traveled by all trucks
def totalMileage(m):
    return sum(m)


# makes deliveries for the first truck, start time: 8am
start_time = datetime.datetime(2023, 6, 8, 8, 0)
truck_1_end_time = makeDeliveries(truck_1, start_time)

# makes deliveries for the second truck, start time: 9:06am
start_time = datetime.datetime(2023, 6, 8, 9, 6)
truck_2_end_time = makeDeliveries(truck_2, start_time)

# makes deliveries for the third truck, start time: 10:21am
start_time = datetime.datetime(2023, 6, 8, 10, 21)
truck_3_end_time = makeDeliveries(truck_3, start_time)

# prints the status for all packages at a given time: input_time
# time complexity O(N)
def lookUpAll(input_time):
    for _ in range(len(my_hash_table.table) + 30):
        package = (my_hash_table.search(_ + 1))
        delivered_time = package.delivery_time
        load_time = package.loading_time
        # updates package status at a given time: input_time
        if delivered_time < input_time:
            package.status = "Delivered"
        elif (delivered_time > input_time) and (load_time < input_time):
            package.status = "En Route"
        else:
            package.status = "At HUB"
    # prints data for all packages
    print("\nPackages Status:")
    for _ in range(len(my_hash_table.table) + 30):
        print((my_hash_table.search(_ + 1)))

# prints the status of a single package at a given time: input_time
# time complexity: O(1)
def lookUpOne(input_time, package_id):
    package = (my_hash_table.search(package_id))
    delivered_time = package.delivery_time
    load_time = package.loading_time
    # updates package status at a given time: input_time
    if delivered_time < input_time:
        package.status = "Delivered"
    elif (delivered_time > input_time) and (load_time < input_time):
        package.status = "En Route"
    else:
        package.status = "At HUB"
    # prints data for one package
    print("\nPackage Status:")
    print((my_hash_table.search(package_id)))


# takes input from the user and returns user_time
# time complexity: O(1)
def userTime():
    while True:
        try:
            # asks user for the hour
            input_HH = int(input("Enter hour (1-12): "))
            if input_HH < 1 or input_HH > 12:
                raise ValueError
            break
        except ValueError:
            print("\nHour must be in the range of 1-12.")
    while True:
        try:
            # asks user for the minutes
            input_MM = int(input("Enter minute (0-59): "))
            if input_MM > 59:
                raise ValueError
            break
        except ValueError:
            print("\nMinute must be in the range of 0-59.")
    while True:
        try:
            # asks user for am or pm
            am_pm = input("AM/PM? ")
            if am_pm == 'AM' or am_pm == 'am':
                # if am and HH=12, HH is changed to 0
                if input_HH == 12:
                    input_HH = 0
                else:
                    input_HH = input_HH
            elif am_pm == 'PM' or am_pm == 'pm':
                # if pm add 24 to HH
                input_HH = input_HH + 12
                # if pm and HH=24, HH is changed to 12
                if input_HH == 24:
                    input_HH = 12
                else:
                    input_HH = input_HH
            else:
                raise ValueError
            break
        except ValueError:
            print("\nType 'AM' or 'PM'.")
    # adds user input values into user_time
    user_time = datetime.time(input_HH, input_MM)
    # user_time is converted to 12HR format
    user_tf = user_time.strftime("%I:%M %p")
    print("Time Entered:", user_tf)
    return user_time

# header for program
print("\nWelcome to WGUPS")
# prints total mileage travelled by all trucks: totalMileage function is called with mileage list as parameter
print("Total mileage traveled by all trucks:", totalMileage(mileage), "miles")

# main menu for program
pkg_option = None
# program loops until user types Q or q
while pkg_option != 'Q':
    # 1. user can see the status for all packages at a specified time
    # 2. user can see the status of a particular package at a specified time
    # Q. user can quit program
    pkg_option = input("\nMenu choices:"
                       "\n1. Status on all packages."
                       "\n2. Status on one package."
                       "\nType 'Q' to quit. \n")
    while True:
        try:
            # exits program
            if pkg_option == 'Q' or pkg_option == 'q':
                exit()
            # prints all packages
            elif pkg_option == '1':
                lookUpAll(userTime())
            # prints a single package
            elif pkg_option == '2':
                while True:
                    try:
                        # finds the package using the package ID
                        pkg_id = input("\nEnter package ID number (1-40): ")
                        if (int(pkg_id) >= 1) and (int(pkg_id) <= 40):
                            lookUpOne(userTime(), (int(pkg_id)))
                        else:
                            raise ValueError
                        break
                    except ValueError:
                        print("Enter a number in the range of 1-40")
            else:
                raise ValueError
            break
        except ValueError:
            print("\nInvalid entry, try again.")
        break
