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

#Creating lists for future use
high_port_usage = []
offline_devices = []
low_uptime_devices = []

# loop through the location list and list offline/warning devices
report += '\nDevices with problems\n\n'
for location in data['locations']:
    for device in location['devices']:
        if device['status'] in ['offline', 'warning']:
            #Adds device information to offline devices list for future use
            offline_devices.append((device['hostname'], location['site'], device['status']))

            #Add hostname, status and location of device with trouble to the report
            report += (
            f"{device['hostname'].ljust(15)} "
            f"{device['ip_address'].ljust(15)} "
            f"{device['status'].ljust(8)} "
            f"{location['site'] + '\n'}"
            
            )


report += '\n' + '='*50 + '\n'  


#Creating a counter for different devices
device_counts = {} 

for location in data['locations']:
    for device in location['devices']:
        #Fetching the type of device
        device_type = device['type']
        #If the device is not already listed in counts start at 0
        if device_type not in device_counts:
            device_counts[device_type] = 0
        #increase count by one for this type
        device_counts[device_type] += 1

#Headline for report
report += '\nTotal number of devices:\n\n'
for dev_type in sorted(device_counts):
   report += f"{dev_type}: {device_counts[dev_type]}\n"

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
vlan_count = 0 
#Loops through VLANs, sorted
for vlan in sorted_vlans:
    #Adds VLAN-number as string and a comma
    report += str(vlan) + ', '
    #Increase counter by 1
    vlan_count += 1
    #When count reaches 8, new line and reset counter
    if vlan_count == 8:
        report += '\n'
        vlan_count = 0 


report += '\n'
report += '\n' + '='*50 + '\n'      


#Adding devices with less than 30 days uptime to report
report += '\nDevices with less than 30 days uptime\n\n'
for location in data['locations']:
    #Loop through devices
    for device in location['devices']:
      #Look for the key uptime_days and check if value is < 30
      if "uptime_days" in device and device['uptime_days'] < 30:
         #Add it to low uptime list for future use
         low_uptime_devices.append((device['hostname'], location['site'], device['uptime_days']))

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
        #Checks if device is a switch and adds number to counter
        if device['type'] == 'switch':
            site_switches += 1
            #Saves values per switch for summary further below
            used = device['ports']['used']
            total = device['ports']['total']

            #Adds switch used ports and total ports to total sum per site
            site_used_ports += device['ports']['used']
            site_total_ports += device['ports']['total']
            
            
            #If used ports are above 80%, add them to list for future use
            if site_total_ports > 0 and (site_used_ports / site_total_ports * 100) > 80:
                high_port_usage.append((device['hostname'], site, used, total))

    #If site has switches, calculate percentage
    if site_switches > 0:
        percent = site_used_ports / site_total_ports * 100 
        #Adds site, number of switches, used ports/total ports and percentage
        report += (
        f"{site.ljust(15)} "
        f"Switches: {site_switches} "
        f"Ports: {site_used_ports}/{site_total_ports} "
        f"({percent:.1f}%)\n"
        )

report += '\n' + '='*50 + '\n'

report += 'Device status per site\n'
#Loop through locations
for location in data['locations']:
    #Create variable for site and counters for online/offline
    site = location['site']
    online_counts = 0
    offline_counts = 0
    #Loop through devices
    for device in location['devices']:
        #Add devices with status online to online counter
        if device['status'] == 'online':
            online_counts += 1
        #Else the rest of the devices to offline counter
        else: offline_counts += 1
    #Add site with both counters to report
    report += (
        f"{site}:"
        f"\nOnline devices: {online_counts}    "
        f"Offline/warning devices: {offline_counts}"'\n----\n'
        )

report += '\n' + '='*50 + '\n'

#Summary of issues section
report += '\nSUMMARY OF ISSUES\n\n'
#Writes out our saved list in case offline/warning devices are detected
if offline_devices:
    report += f"Offline/Warning devices: {len(offline_devices)}\n\n"
    for hostname, site, status in offline_devices:
        report += f"{hostname.ljust(12)} - {status.ljust(8)} - {site}\n"
#If no errors found, run else
else:
    report +=  'No warning/online device found'
#Write out high port usage devices using saved list
if high_port_usage:
    report += f"\nDevices with high port usage: {len(high_port_usage)}\n\n"
    for hostname, site, used, total in high_port_usage:
        percent = used / total * 100
        report += f"{hostname.ljust(15)} - {site.ljust(12)}: {used}/{total} ({percent:.1f}%)\n"
#If no high usage found, run else
else:
    report += 'No port usage above 80 percent found'

#Write out low uptime devices using saved list
if low_uptime_devices:
    report += f"\nDevices with uptime less than 30 days: {len(low_uptime_devices)}\n\n"
    for hostname, site, days in low_uptime_devices:
        report += f"{hostname.ljust(13)} - {days} days - {site}\n"
#If no device found, run else
else:
    report += 'No low uptime devce found'

report += '\n' + '='*50 + '\n'


# write the report to text file
with open('report.txt', 'w', encoding='utf-8') as f:
    f.write(report)