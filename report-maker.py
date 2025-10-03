# Import the json library so that we can handle json
import json

# Read json from products.json to the variable data
data = json.load(open('network_devices.json','r',encoding = 'utf-8'))

# Create a variable that holds our whole text report
report = ''
#Header with company name and last update
report += '='*50 + '\n'
report += 'Company: ' + data['company'] + '\n' 
report += 'Last updated: ' + data['last_updated']+'\n'
report += '='*50 + '\n'


# loop through the location list and list offline/warning devices
report += '\n'+'Devices with problems'+'\n'
for location in data['locations']:
    #Add hostname, status and location of device with trouble to the report
    for device in location['devices']:
      if device['status'] in ['offline', 'warning']:
        report += ('  ' + device['hostname'].ljust(15) 
                + ' ' + device['status'].ljust(10) + location['site'] + '\n')


report += '\n' + '='*50 + '\n'  


#Creating a counter for different devices
counts = {} 

for location in data['locations']:
    for device in location['devices']:
       #Fetching the type of device
       device_type = device['type']

report += '\n' + '='*50 + '\n'  

#Creates a set for unique VLANs
vlans = set()
for location in data['locations']:
    for device in location['devices']:
        #Checks if there are VLANs and updates the set with unique VLANs
        if 'vlans' in device:
           vlans.update(device['vlans'])
report += f"\nUnique vlans:{sorted(vlans)}\n"


report += '\n' + '='*50 + '\n'      


#Adding devices with less than 30 days uptime to report
report += "\nDevices with less than 30 days uptime\n"
for location in data['locations']:
    #Loop through devices
    for device in location['devices']:
      #Look for the key uptime_days and check if value is < 30
      if "uptime_days" in device and device['uptime_days'] < 30:
         #Add device to the report with hostname, uptime and site
         report += f"{device['hostname'].ljust(15)}\
 - ({str(device['uptime_days']).ljust(2)} days) - {location['site']}\n"
        

        




# write the report to text file
with open('report.txt', 'w', encoding='utf-8') as f:
    f.write(report)