#!/bin/bash

# Update
# ==============================================================================
# See internet.py for a more advanced and user friendly interface!

# Simple script to swap hosts files. I use host files to block internet sites
# to boost productivity and force single-tasking.
#
# @author: Chris Laskey
# @source: http://chrislaskey.com
# @version: 1.0.2
# Last updated 2011-05-20
#
# Since modifying the hosts file requires root privileges, the options are
# to call this script with $ sudo; or set the sticky bit for 
# privileged execution.
#
# Three arguments are available on|off|default. Each loads the respective
# hosts.<argument> file if it exists.

# Functions
help_message () { 
	echo "Error, invalid argument."
	echo "Valid arguments for ${0} are on|off|default"
} 

# Validate argument
if [[ ! "$1" =~ (on|off|default) ]]; then
	help_message
	exit 1
fi

# Set variables
HOSTS_PATH=/etc/
HOSTS_FILE="${HOSTS_PATH}hosts"
HOSTS_NEW_FILE="${HOSTS_FILE}.${1}"
UNAME=`uname`

# Verify new file exists
if [[ ! -f "$HOSTS_NEW_FILE" ]]; then
	echo "Error, new file not found: ${HOSTS_NEW_FILE}"
	exit 1
fi

# Remove hosts file
if [[ ! -z "$(rm ${HOSTS_FILE})" ]]; then
	echo "Error, could not remove hosts file: ${HOSTS_FILE}"
	exit 1
fi

# Replace with new file
if [[ ! -z "$(cp -p ${HOSTS_NEW_FILE} ${HOSTS_FILE})" ]]; then
	echo "*** CRITICAL WARNING ***"
	echo "Could not move new hosts file after removing current hosts file."
	echo "You must restore the original ${HOSTS_FILE}."
	echo "*** CRITICAL WARNING ***"
	exit 1
fi

# Flush old DNS entries
if [[ "$UNAME" == Darwin ]]; then
	dscacheutil -flushcache
elif [[ "$UNAME" == Linux && -f /etc/init.d/nscd ]]; then
	/etc/init.d/nscd restart
else
	echo "Warning, could not flush DNS cache entries. You may need to flush these manually."
fi

# Return successfully
exit 0
