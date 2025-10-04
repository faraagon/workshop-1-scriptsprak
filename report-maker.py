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
report += '\nDevices with problem\n\n'
for location in data['locations']:
    #Add hostname, status and location of device with trouble to the report
    for device in location['devices']:
        if device['status'] in ['offline', 'warning']:
            report += (
            f"{device['hostname'].ljust(15)} "
            f"{device['status'].ljust(10)} "
            f"{location['site'] + '\n'}"
            )


report += '\n' + '='*50 + '\n'  


#Creating a counter for different devices
counts = {} 

for location in data['locations']:
    for device in location['devices']:
        #Fetching the type of device
        device_type = device['type']
        #If the device is not already listed in counts start at 0
        if device_type not in counts:
            counts[device_type] = 0
        #increase count by one for this type
        counts[device_type] += 1

#Headline for report
report += '\nTotal number of devices:\n\n'
for dev_type in sorted(counts):
   report += f"{dev_type}: {counts[dev_type]}\n"

report += '\n' + '='*50 + '\n'  

#Creates a set for unique VLANs
vlans = set()
#Loops through JSON
for location in data['locations']:
    for device in location['devices']:
        #Checks if there are VLANs and updates the set with unique VLANs
        if 'vlans' in device:
           vlans.update(device['vlans'])

report += f"\nNumber of unique VLANs: {len(vlans)}"'\n'
#Sorts VLANs to report them in order
sorted_vlans = sorted(vlans)
report += '\nUnique VLANs:\n'
#Counter to count VLANs per row
count = 0 
#Loops through VLANs, sorted
for vlan in sorted_vlans:
    #Adds VLAN-number as string and a comma
    report += str(vlan) + ', '
    #Increase counter by 1
    count += 1
    #When count reaches 8, new line and reset counter
    if count == 8:
        report += '\n'
        count = 0 


report += '\n'
report += '\n' + '='*50 + '\n'      


#Adding devices with less than 30 days uptime to report
report += '\nDevices with less than 30 days uptime\n\n'
for location in data['locations']:
    #Loop through devices
    for device in location['devices']:
      #Look for the key uptime_days and check if value is < 30
      if "uptime_days" in device and device['uptime_days'] < 30:
         #Add device to the report with hostname, uptime and site
         report += (
            f"{device['hostname'].ljust(15)} "
            f"({str(device['uptime_days']).ljust(2)} days) "
            f"- {location['site']}\n"
         )
        
report += '\n' + '='*50 + '\n'

report += '\nSwitch port usage per site:\n'
#Loop through the sites
for location in data['locations']:
    site = location['site']
    #Starts counter for switches, used ports and total ports
    site_switches = 0
    site_used_ports = 0
    site_total_ports = 0
    #Loop through the devices per site
    for device in location['devices']:
        #Checks if device is a switch and adds requested numbers to counters
        if device['type'] == 'switch':
            site_switches += 1
            site_used_ports += device['ports']['used']
            site_total_ports += device['ports']['total']
    #If site has switches, calculate percentage
    if site_switches > 0:
        percent = site_used_ports / site_total_ports * 100 
        #Adds site, number of switches, used ports/total ports and percentage
        report += (
        f"{site.ljust(15)} "
        f"Switches: {site_switches:<3} "
        f"Ports: {site_used_ports}/{site_total_ports} "
        f"({percent:.1f}%)\n"
        )

report += '\n' + '='*50 + '\n'


# write the report to text file
with open('report.txt', 'w', encoding='utf-8') as f:
    f.write(report)