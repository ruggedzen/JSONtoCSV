#limitation: Only works for VMs with agents. Cannot find containers.

#You will need to download the JSON permalink file from Datadog infrastructure list. 
#Script will output a file called *Client Code* devices.csv

import csv
from json import load
from re import findall

#Get client code from user
client_code = input("Please enter client's 4 letter Code: ").upper()

#Checks if CC is correct length
while len(client_code) != 4:
    print("\nClient Code should be 4 letters.")
    client_code = input("Please enter client's 4 letter Code: ").upper()

#Get the full file path from user. If the filepath is invalid, ask again.
while True:
    try:
        jsonfile = input("\nEnter path to JSON file: ")

        #Opens JSON file and creates dict
        with open(jsonfile, 'r') as j:
            data = load(j)
            device_data = data["rows"]

    except FileNotFoundError:
        print("\nEnter valid file path\n")
        continue

    else:
        break

#Creates csv file and writes device names and IP addresses
with open(client_code + " devices.csv", "w") as d:
    column_names = ["Device Name", "IP Address", "Agent Version", "Platform"]
    writer = csv.DictWriter(d, fieldnames=column_names)
    writer.writeheader()
    
    for device in device_data:

        #checks if the fields exist in device, if not, skip.
        #devices without agents will not have the gohai, agent ver, and plaform fields
        if "gohai" in device["meta"] and "agent_version" in device["meta"] and "platform" in device["meta"]:
            gohai = device["meta"]["gohai"] 
            agent_ver = device["meta"]["agent_version"]
            platform = device["meta"]["platform"]                   
        else:
            continue
        
        #finds all IP addresses in gohai field. First IP is the device IP, second is the Gateway
        ipv4 = findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", gohai)
        device_name = device["host_name"]        
         
        #Checks to see if the ipv4 list isn't empty.
        if len(ipv4) != 0:
            writer.writerow({"Device Name": device_name, "IP Address": ipv4[0], "Agent Version": agent_ver,"Platform": platform})

print('\nCreated file "{} devices.csv" in current folder.\n'.format(client_code))

        

       
            
        
      