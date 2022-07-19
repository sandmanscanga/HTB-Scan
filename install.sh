#!/bin/bash

# Project Path Constants
PROJECT_PATH=/opt/HTB-Scan
PROJECT_ENTRY=${PROJECT_PATH}/htb-scan.py

# Current Path Constants
CURRENT_PATH=`pwd -P`
CURRENT_ENTRY=${CURRENT_PATH}/htb-scan.py

# Runner Script Path Constant
RUNNER_PATH=/usr/local/bin/htb-scan

# Checks if user is root when running install
if [ `id -u` != 0 ]; then
    echo "[!] Must be run as root" >&2
    exit 1
fi

# Wipes old project and recreates directory
echo "[*] Wiping old project and recreating directory" &&
rm -rf $PROJECT_PATH &&
mkdir -p $PROJECT_PATH &&

# Copy the HTB-Scan source code to the project path
echo "[*] Copying the HTB-Scan source code to the project path" &&
cp $CURRENT_ENTRY $PROJECT_PATH &&

# Creating the runner script in a local system path
rm -f $RUNNER_PATH &&
echo '#!/bin/bash' > $RUNNER_PATH &&
echo "/usr/bin/python3 $PROJECT_ENTRY \$@" >> $RUNNER_PATH &&

# Lock down the project permissions and ownership
echo "[*] Locking down the project permissions and ownership" &&
chown -R root:root $PROJECT_PATH &&
chmod 700 $PROJECT_PATH &&
chmod 600 $PROJECT_ENTRY &&
chown root:root $RUNNER_PATH &&
chmod 700 $RUNNER_PATH

# Finished
echo "[+] Finished"
