# DC_finder
Python script for finding domain controllers on a given network range.

sudo python3 DC_Finder.py -n 10.0.0.0/24

Utilises nmap to scan the network for only the Domain Controllers, and outputs the results to both the terminal and (optionally) saves the DC IP addresses to a text file.

Updates coming to allow it to accept a list of network ranges rather than just the one network, will also add a flag to specify your own naming convention for the output file.
