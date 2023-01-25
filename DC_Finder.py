import os
import re
import argparse
from termcolor import colored
import subprocess

#required arguments
parser = argparse.ArgumentParser()
parser.add_argument('-n', default='none', dest='network', help='provide the CIDR network to scan (eg 10.0.0.1/24)', type=str)
parser.add_argument('-l', default='none', dest='network_list', help='provide a list of CIDR networks to scan', type=str)
args = parser.parse_args()

#check required args completed
if args.network == 'none' and args.network_list == 'none':
        print(colored('\n[!] Network range or list not provided with \'-n\' or \'-l\'.\n\nQuitting.','red'))
        quit()

#check if too many args completed:
if args.network != 'none' and args.network_list != 'none':
        print(colored('\n[!] List and network provided! Dont be greedy, only use one...\n\nQuitting.','red'))
        quit()

#check if sudo was used
if not 'SUDO_UID' in os.environ.keys():
        print('\nThis script requires super user privs (sudo), please come back when the grown-ups say it\'s ok...')
        quit()

#define freq used functions
def printbanner():
        print(colored('\n***************************************************','green'))
def cmdline(command):
        terminal_output = subprocess.getoutput(command)
        return(terminal_output)

networks = []
if args.network != 'none':
        networks.append(args.network)
if args.network_list != 'none':
        with open(args.network_list,'r') as network_list:
                for line in network_list:
                        networks.append(line)
domain_controllers = []
printbanner()
for line in networks:
        if args.network_list != 'none':
                print('\nScanning',colored(line[:-1],'blue'),'for the Domain Controllers')
                printbanner()
        elif args.network != 'none':
                print('\nScanning',colored(line),'blue'),'for the Domain Controllers')
                printbanner()

        #set the nmap command
        scan_cmd = 'nmap -sS -p 53,88,139,389 --open '+line

        #run the scan
        initial_scan = cmdline(scan_cmd)

        #split the scan into individual IPs
        individual_ips = initial_scan.split('MAC Address')

        #check if all required ports are open and add to list of DCs:
        for ip in individual_ips:
                if '53' in ip:
                        if '88' in ip:
                                if '139' in ip:
                                        if '389' in ip:
                                                dc_name = ip.split('Nmap scan report for ')[1]
                                                dc_name = dc_name.split('Host is up')[0]
                                                print(colored('\nThis is likely a DC:\n\n','blue'),dc_name)
                                                printbanner()
                                                domain_controllers.append(dc_name)

if len(domain_controllers) < 1:
        print('\nWe didn\'t find shit. Probably your fault...')
else:
        print('\nAll done! Would you like to save the results to a text file?')
        createtext = ''
        while createtext != 'y' and createtext != 'n':
                createtext = input('Please choose (y/n): ')
        if createtext == 'n':
                print('\nHappy hacking!')
        elif createtext == 'y':
                with open('domain_controllers.txt','a') as outfile:
                        pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
                        for line in domain_controllers:
                                dcip = (pattern.search(line)[0])
                                outfile.write(dcip + '\n')
                        print('\nOutput saved as domain_controllers.txt.\nHappy Hacking!')
