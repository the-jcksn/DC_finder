# DC_finder
Python script for finding domain controllers on a given network range.

sudo python3 DC_Finder.py -n 10.0.0.0/24
sudo python3 DC_Finder.py -l list_of_network_ranges.txt

Utilises nmap to scan the network/list of networks for only the Domain Controllers, and outputs the results to both the terminal and (optionally) saves the DC IPs found to a text file. 

Upcoming update - Will add a flag to specify your own naming convention for the output file.
