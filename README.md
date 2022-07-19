
# HTB-Admin

A tool used for automatically scanning HackTheBox machine instances with Nmap.

---

## OS & Python Version Info

```bash
lsb_release -a
# Distributor ID: Kali
# Description:    Kali GNU/Linux Rolling
# Release:        2022.2
# Codename:       kali-rolling
```

*Tested using Python 3.10.5*

---

## Installation

```bash

git clone https://github.com/sandmanscanga/HTB-Scan.git
cd HTB-Scan

# To run installed on the system
sudo bash install.sh

```

---

## Dependency

There is a dependency that the `htb-scan` has which is that it relies on [htb-admin](https://github.com/sandmanscanga/HTB-Admin) to be installed on the system.  For additional information on how to install the dependency, please see [this](https://github.com/sandmanscanga/HTB-Admin/blob/main/README.md) document...

---

## Example Usage

```bash

: '

By default, the application will lookup the currently active machine instance IP address using the "htb-admin" utility.  

The application will then execute a SYN stealth scan on all ports, then executes a version scan against any found open ports, and then a full OS scan with scripts against any found open ports.

The output of the default scan will save a file for each scan in a folder called "nmap/".

'

# Portable Install
python htb-scan.py                                # default behavior
python htb-scan.py -t '<ip_address or hostname>'  # specify a custom target host
python htb-scan.py -o '<output_directory_path>'   # specify a custom output directory location
python htb-scan.py -e                             # specify enum scan (verbose comprehensive scan)
python htb-scan.py -u '<number_of_ports>'         # specify udp scan (defaults to top 100 ports)

#### OR ####

# Full Install
htb-scan                                # default behavior
htb-scan -t '<ip_address or hostname>'  # specify a custom target host
htb-scan -o '<output_directory_path>'   # specify a custom output directory location
htb-scan -e                             # specify enum scan (verbose comprehensive scan)
htb-scan -u '<number_of_ports>'         # specify udp scan (defaults to top 100 ports)

```

**This application was designed for educational purposes ONLY. I am not responsible for any misuse of the application or legal issues that arise due to you're own decisions.**
