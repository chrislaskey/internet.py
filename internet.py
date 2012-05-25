#!/usr/bin/env python

'''
Information
================================================================================

@author Chris Laskey
@contact chrislaskey.com
@contact github.com/chrislaskey
@updated 2012.05.25
@version 1.5.4

About
================================================================================

Internet.py is a script to limit personal web browsing.

It works by modifying the /etc/hosts file. The hosts file associates numeric
based addresses like '127.0.0.1' with named addresses like 'localhost'. Usually
this file is only used to cache local network names, as remote computers
accessible over the internet have numeric addresses that may, and often do,
change.

A web browser utilizes the Domain Name Service (DNS) to keep track of these
dynamically changing numeric addresses. However before asking the remote DNS
service for the numeric address of a domain like 'google.com', the computer
will check the /etc/hosts file just in case the information is already there.

This means a web browser request for 'google.com' can be redirected to a
different numeric address of our choosing, instead of resolving to the actual
address like '173.194.43.5'.

By choosing an unused address, we can create a 'blackhole' where the requested
site can not be reached. By default we use an address in the local 127.0.0.*
range, but you can modify this to whatever you like in the settings below.

_Note_ modern operating systems and web browsers cache DNS entries for a short
time in order to cut down on the number of overall DNS calls. This DNS cache
is checked before the /etc/hosts file. This script attempts to clear all
local DNS caches. However you may need to clear a DNS cache manually, or
simply wait a few minutes for the DNS cache to expire.

_Note_ since this file modifies /etc/hosts, it will effect all users on the
machine.

_Why /etc/hosts?_ I'm not a big fan of cron requirements for scripts, but the
alternative would be to pipe all traffic through a python daemon. I love
Python, but unix based systems already do a good job networking without adding
more cogs.

_Why not /etc/resolve.conf?_ Mac OS X Darwin does not use /etc/resolve.conf
in the same way Linux does. In the interests of this being cross-compatible
I've decided to stick with /etc/hosts modification.

Using the script - groups, domains, and times, oh my!
================================================================================

This script is meant to be flexible, allowing access depending on the time and
day of the week.

Everything is organized into 'groups'. A group contains three pieces of
information: a list of domains; a list of hours to be active during; a list of
days to be active on.

_Remember_ this script modifies the /etc/hosts file, which requires root
privileges. Most command options require using sudo.

Groups
--------------------------------------------------------------------------------
You can define as many groups as you want, or simply use the default group aptly
named 'default.'

Examples:

To add a new group
$ ./internet.py --add --group 'work'

Remove a group
$ ./internet.py --remove --group 'work'
(Warning! This removes all information. See --activate/--deactivate below.)

Active List
--------------------------------------------------------------------------------
A group can be activated or deactivated. This allows you to create a group with
set times and days, but temporarily turn the group off without deleting the
hard work put into setting it up.

The 'default' group is active by default, and new groups are activated by
default as well.

Examples:

List current groups and their status
$ ./internet.py --list

Deactivate a group
$ ./internet.py --deactivate --group 'work'

Activate a group
$ ./internet.py --activate --group 'work'

Domains
--------------------------------------------------------------------------------
The core of this script is the list of domains to block. Domain names should
not include 'http://' at the beginning. The 'http://' in a browser refers to the
method, or protocol, the browser should use to connect to a domain. The domain
name is the part that comes after it, e.g. google.com. This is the named address
of the remote computer, and also the only part we care about.

Also, domains should not include any trailing information. For example write
'google.com', not 'google.com/' or 'google.com/analytics'. Subdomains
(information to the left) are okay, like 'translate.google.com'.

Examples:

Add a domain to the default group
$ ./internet.py --add --domain 'google.com'

Add a domain to a custom group
$ ./internet.py --add --domain 'google.com' --group 'work'

Empty all domains in a group
$ ./internet.py --empty domains --group 'work'

_Notice_ This script only supports single arguments, e.g. one --domain, --hour
or --day args. To add multiple domains, you must call internet.py multiple
times

Days
--------------------------------------------------------------------------------
Days specify when a group's list of domains will be blocked. Days can be given
by their full names (e.g. 'Monday'), or as the wildcard '*'.

The default days range is '*', meaning it is active on all days. This is a
valid range and can be added to any group. _Note_ adding the wildcard will
overwrite current day ranges.

Examples:

Add one day to a group
$ ./internet.py --add --day 'Tuesday'

Empty all days in a group
$ ./internet.py --empty days --group 'work'

Hours
--------------------------------------------------------------------------------
Hours specify when a group's list of domains will be blocked. Hours can be given
in single units (e.g. 8), in a range (9-17), or as the wildcard '*'.

The default hours range is '*', meaning it is active all the time. This is a
valid range and can be added to any group. _Note_ adding the wildcard will
overwrite current hour ranges.

All hours should be given as a __24 hour__ clock. Minutes are not supported and
should not be used, e.g. write '9', not '9:00' or '900'.

Example:

Add one hour to a group
$ ./internet.py --add --hour 8

Add an hour range to a group
$ ./internet.py --add --hour 9-17

Empty all hours in a group
$ ./internet.py --empty hours --group 'work'

Misc
--------------------------------------------------------------------------------
There are more commands and functionality than outlined here. Run the help
command (-h/--help) for a complete list of available flags/options.

Examples:

List current groups and their status
$ ./internet.py --list

View the hosts file before updating it
$ ./internet.py --update --confirm

Print crontab information
$ ./internet.py --print-crontab

_Remember_ this script modifies the /etc/hosts file, which requires root
privileges. Most command options require using sudo.

Recommendations
================================================================================

+ Run the script hourly via a cron job. Use the --print-crontab option for help
on how to set this up.

+ Make sure this script has execute permissions (see $ man chmod; for more
information)

+ Add internet.py to your PATH so it can be called/updated from any location on
the command line.

+ Alias internet.py to internet in your bashrc/zshrc. Alternatively remove the
.py file extension (not recommended!)

+ Don't use this script to limit other people's web browsing activities. It will
do a poor job. The script is designed only to discourage casual browsing habits,
not be a true gatekeeper.

+ Read through the code before using it. It's short and well commented. Don't
trust anyone's script that requires root privileges without looking it over
yourself.

Change log
================================================================================

v1.5.3
------
First release
Added cron job optimizations, args, timestamps, etc.

v1.4.2
------
Working beta

v1.3.3
------
Working version of CRUD functionality
Need remove/empty functionality

v1.2.0
------
Working version with static JSON file

v1.1.4
------
Python version Hello World!

v1.0.0
------
Release of simple bash script version, internet.sh.

Future Plans
================================================================================

+ Support multiple values for fields like --domains
+ Interactive menu mode
+ Move some flags to full args via ArgumentParser.add_subparsers
+ Add full 256 color set to color() function

License
================================================================================

Copyright (C) 2012 Chris Laskey

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

Except as contained in this notice, the name(s) of the above copyright holders
shall not be used in advertising or otherwise to promote the sale, use or other
dealings in this Software without prior written authorization.

The end-user documentation included with the redistribution, if any, must include
the following acknowledgment: "This product includes software developed by
Chris Laskey (http://chrislaskey.com)", in the same place and form as other
third-party acknowledgments. Alternatively, this acknowledgment may appear in
the software itself, in the same form and location as other such third-party
acknowledgments.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Commentary on License Choice
================================================================================

Though I see the appeal of copy-left licensing, I've decided to release all code
under the very permissive MIT license. The upshot is enjoy the code, modify it,
include in proprietary software, relicense it, etc. The only things I ask are:

	- Don't hold me liable for any damages resulting from using my code
	  (e.g. if the code turns you to drinking heavily, don't charge the drinks
	  to my tab).

	- If you do decide to credit people and you use my code, a thank you in the
	  same section as other third-party contributors would be great, but not
	  required!

	- Finally, don't use my name to promote the sale of your product without
	  asking. It's great if you sell a product with my code in it, and I hope
	  you are wildly successful! I just don't want my name associated with a
	  company that acts like a jerk. So ask first. Unless your name is
	  Larry Ellison, there's a 99.9999999%* chance I'll say yes.

	  * That's the fabled nine nines. Quick catch it before it rides away on
	  a unicorn!

Finally, the code may contain third party libaries. I've done my best to adhere
to their licensing rules and make them explicit. But please do your own due
diligence and double check before assuming everything is as permissive as
my own code's license!

For more information on the MIT license check out the Wikipedia page. The
license below is the basic MIT plus the MIT X11 and MIT XFree86 Project clauses:
http://en.wikipedia.org/wiki/MIT_License
'''

import argparse
import json
import os
import pprint
import re
import shutil
import sys

from datetime import datetime
from subprocess import call

class Internet:

	def __init__(self):

		# Set variables
		self.settings = {
			'hosts_file': '/etc/hosts',
			'hosts_file_original': '/etc/hosts.original',
			'hosts_file_template': '/etc/hosts.template',
			'hosts_file_blackhole': '127.0.0.250',
			'timestamp': '[' + str(datetime.now()) + ']'
		}
		self.options = self._parse_arguments()
		self.pp = pprint.PrettyPrinter(indent=4)

		# Make setup function calls
		self.data = self._load_json()

		# Parse arguments via passed flags (above) or interactively (below)
		if hasattr(self.options, 'interactive') and self.options.interactive != False:

			# Delete args list as these will be redefined in interactive mode
			# and we don't want a mix of passed and unpassed values.
			del self.options

			# Default python objects() do not allow dynamic attribute
			# assignment. We create a simple class we can extend to mimic
			# the argparse object.
			class MyObject(object): pass
			self.options = MyObject()

			# Launch interactive menu
			self.interactive()

		# Optimize cron job options
		if self.options.cron:
			self.options.no_color = True
			self.options.confirm = False
			self.options.update = True

		# The following can conflict with eachother.
		# Allow only one to be executed per command.
		if self.options.remove != False:
			self.remove()

		elif self.options.empty != False:
			self.empty()

		elif self.options.add != False:
			self.add()

		elif self.options.activate != False:
			self.activate()

		elif self.options.deactivate != False:
			self.deactivate()

		# Second conflict group
		if self.options.list != False:
			self.list()

		# The following can be run without conflicts
		if self.options.print_crontab != False:
			self.print_crontab()

		# Update if no arguments are passed
		if self.options.update != False or len(sys.argv) == 1:
			self.update_hosts()

	def _parse_arguments(self):

		# Create argparse instance
		parser = argparse.ArgumentParser(description='A script to prevent connecting to domains according to custom time-based rules.', epilog='For time-based rules to work, this script needs to be executed via a cron job every hour. Basic functionality will work without cron job.')

		# Setup arguments
		setup = parser.add_argument_group('Setup options')
		setup.add_argument('-f', '--file', default='{0}'.format(os.path.abspath(__file__ + '/../internet.json')), dest='json_file', metavar='<path>', help='Use specified json storage file.')
		setup.add_argument('--log-file', default='{0}'.format(os.path.abspath(__file__ + '/../internet.log')), metavar='<path>', help='Use specified file as the cron job log file.')

		# General actions
		general_actions = parser.add_argument_group('General actions')
		general_actions.add_argument('-l', '--list', '--status', action='store_const', const=True, default=False, help='Display current groups, group fields and status.')
		general_actions.add_argument('-u', '--update', action='store_const', default=False, const=True, help='Update hosts file.')
		general_actions.add_argument('--confirm', action='store_const', default=False, const=True, help='Confirm hosts file before updating. Use with --update.')

		# Group actions
		group_actions = parser.add_argument_group('Actions on groups')
		group_actions.add_argument('-A', '--activate', action='store_const', default=False, const=True, help='Activate a group.')
		group_actions.add_argument('-D', '--deactivate', action='store_const', default=False, const=True, help='Deactivate a group.')
		group_actions.add_argument('-r', '--remove', action='store_const', default=False, const=True, help='Remove a group. Warning: this permenantly removes all group information.')

		# Group arguments
		groups = parser.add_argument_group('Group objects')
		groups.add_argument('-g', '--group', default=None, metavar='<group>', help='Specify a group. Can be use in conjunction with actions like --add, --delete, etc.')

		# Group field actions
		field_actions = parser.add_argument_group('Actions on group fields. Specify a group with -g/--group')
		field_actions.add_argument('-a', '--add', action='store_const', default=False, const=True, help='Add a group or group field object')
		field_actions.add_argument('-e', '--empty', choices=['hours','domains','days'], default=False, help='Empty a specific group field.')

		# Group field object arguments
		group_fields = parser.add_argument_group('Group field objects')
		group_fields.add_argument('-d', '--domain', '--domains', default=None, metavar='<domain>', help='Specify a domain. Can be use in conjunction with group field actions like --add, --delete, etc. If no group (-g/--group) is specified, action will be on "default" group.')
		group_fields.add_argument('-H', '--hour', '--hours', default=None, metavar='<hour-range>', help='Specify a group. Can be use in conjunction with group field actions like --add, --delete, etc. If no group (-g/--group) is specified, action will be on "default" group.')
		group_fields.add_argument('-y', '--day', '--days', default=None, metavar='<full-day-name>', help='Specify an hour (e.g. 8) or hour range (e.g. 9-17). Times should be based on a 24 hour clock. Can be use in conjunction with actions like --add, --delete, etc. If no group (-g/--group) is specified, action will be on "default" group.')

		# Other options
		others = parser.add_argument_group('Other options')
		# others.add_argument('-i', '--interactive', action='store_const', default=False, const=True, help='Use interactive mode')
		others.add_argument('--no-color', action='store_const', default=False, const=True, help='Do not display ascii colors in terminal.')
		others.add_argument('--print-crontab', action='store_const', default=False, const=True, help='Display line to add to the crontab.')
		others.add_argument('--cron', action='store_const', default=False, const=True, help='Opitmizes options for running script as a cron job.')

		return parser.parse_args()

	def _load_json(self):

		# Return JSON file contents, return a skeleton if file is empty or does not exist
		if os.path.exists(self.options.json_file) and os.path.isfile(self.options.json_file):
			f = open(self.options.json_file, 'r')
			file_contents = f.read()
			f.close()
		else:
			try:
				# Verify file is writeable
				f = open(self.options.json_file, 'w+')

				# Create base data for new file
				file_contents = '''
					{
						"active": [
							"default"
						],
						"groups": {
							"default": {
								"hours": [ "*" ],
								"domains": [],
								"days": [ "*" ]
							}
						}
					}
					'''

				# Save new file contents
				f.write(file_contents)

			except IOError:
				print(self.settings.get('timestamp', '') + ' Could not write to JSON data file location: {0}. Do you have proper permissions?'.format(self.options.json_file))
				sys.exit(1)

		# Convert to JSON
		# Set default value to return if keyname does not exist
		# e.g.: file_json.get('keyname') will return {} now instead of None
		# This lets us not do explicit checks before loops, etc
		try:
			file_json = json.loads(file_contents)
			file_json.setdefault('groups', {})
			file_json.setdefault('active', {})
		except ValueError:
			print(self.settings.get('timestamp', '') + ' Could not parse JSON data in file {0}. The data may be malformed.'.format(self.options.json_file))
			sys.exit(1)

		return file_json

	def _save_json(self, raw_data):
		try:
			# Turn on pretty printing of JSON
			encoder = json.JSONEncoder(False, True, True, True, False, 4)
			data = encoder.encode(raw_data)
			f = open(self.options.json_file, 'w')
			f.write(data)
			f.close()
		except IOError:
			print(self.settings.get('timestamp', '') + self.color(' Error', 'red') + ' Could not save JSON file: {0}'.format(self.settings.get('hosts_file')))
			sys.exit(1)

	def _init_hosts(self):

		# Verify hosts file exists
		if not os.path.exists(self.settings.get('hosts_file')):
			print(self.settings.get('timestamp', '') + self.color(' Error', 'red') + ' Could not find hosts file: {0}'.format(self.settings.get('hosts_file')))
			sys.exit(1)

		# Create hosts.original file
		if not os.path.exists(self.settings.get('hosts_file_original')):
			try:
				shutil.copy2(self.settings.get('hosts_file'), self.settings.get('hosts_file_original'))
			except IOError:
				print(self.settings.get('timestamp', '') + self.color(' Error', 'red') + ' Could not backup hosts file from: {0}'.format(self.settings.get('hosts_file')) + ' to: {0}'.format(self.settings.get('hosts_file_original')))
				sys.exit(1)

		# Create hosts.template file
		if not os.path.exists(self.settings.get('hosts_file_template')):
			try:
				shutil.copy2(self.settings.get('hosts_file_original'), self.settings.get('hosts_file_template'))
			except IOError:
				print(self.settings.get('timestamp', '') + self.color(' Error', 'red') + ' Could not create template hosts file from: {0}'.format(self.settings.get('hosts_file')) + ' to: {0}'.format(self.settings.get('hosts_file_template')))
				sys.exit(1)

	def _is_live(self, groupname):

		# Verify group exists
		if not self.data.get('groups').get(groupname):
			return False
		else:
			group = self.data.get('groups').get(groupname)

		# Set variables
		now = datetime.now()
		hour = now.hour
		day = {
			0 : 'Monday',
			1 : 'Tuesday',
			2 : 'Wednesday',
			3 : 'Thursday',
			4 : 'Friday',
			5 : 'Saturday',
			6 : 'Sunday'
		}.get(now.weekday(), '*')

		# Verify current day falls in days list
		in_day = False
		if '*' in group.get('days'):
			in_day = True
		elif day in group.get('days', []):
			in_day = True

		# Verify current time falls in hours range
		in_hours = False
		if '*' in group.get('hours'):
			in_hours = True
		else:
			for str in group.get('hours', []):
				if re.search('\-', str):
					(hour_start, _, hour_end) = str.partition('-')
					if hour >= int(hour_start) and hour < int(hour_end):
						in_hours = True
				else:
					if hour == str:
						in_hours = True

		return in_hours and in_day

	# Actions

	def interactive(self):

		print('Interactive mode is not supported yet. Please use -h/--help to learn what flags to pass.')
		sys.exit(0)

	def list(self):

		# Determine if listing all or just one group
		groups = self.data.get('groups')
		if self.options.group != None:
			if groups.get(self.options.group):
				groups = {self.options.group: groups.get(self.options.group)}
			else:
				print(self.color('Error', 'red') + ' Could not list group, no group found with the name: {0}'.format(self.options.group))
				return False

		# Parse data
		active = self.data.get('active')
		for name, group in groups.iteritems():
			print('\nGroup: {0}\n'.format(name))

			if active and name in active:
				print('In Active List: ' + self.color('Yes', 'green'))
				is_active = True
			else:
				print('In Active List: ' + self.color('No', 'red'))
				is_active = False

			if self._is_live(name) and is_active:
				print('Current Status: ' + self.color('Running', 'green') + '\n')
			else:
				print('Current Status: ' + self.color('Not Running', 'red') + '\n')

			# Use join on list instead of using a for loop to print each value
			print('Hours:\n\t' + '\n\t'.join(group.get('hours', {})) + '\n')
			print('Days:\n\t' + '\n\t'.join(group.get('days', {})) + '\n')
			print('Domains:\n\t' + '\n\t'.join(group.get('domains', {})) + '\n')

	def add(self):

		# Determine group. Create group if needed.
		if not self.options.group:
			groupname = 'default'
		else:
			groupname = self.options.group.lower()
			if not self.data.get('groups').get(groupname):
				self.data.get('groups')[groupname] = json.loads('''
					{
						"hours": ["*"],
						"domains": [],
						"days": ["*"]
					}
					''')

		# Add hours to group if needed
		if self.options.hour and re.search('[0-9-\*]', self.options.hour):

			# Cache hours list for readability
			hours = self.data.get('groups').get(groupname).get('hours')

			# Determine how to add hours
			if self.options.hour == '*':
				hours = ['*']
			elif '*' in self.data.get('groups').get(groupname).get('hours'):
				hours = [self.options.hour]
			else:
				hours.append(self.options.hour)

			# Filter uniques and sort before saving
			hours = list(set(hours))
			hours.sort()
			self.data.get('groups').get(groupname)['hours'] = hours

		# Add days to group if needed
		days_map = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', '*']
		if self.options.day and self.options.day in days_map:

			# Cache days list for readability
			days = self.data.get('groups').get(groupname).get('days')

			# Determine how to add days
			if self.options.day == '*':
				days = ['*']
			elif '*' in self.data.get('groups').get(groupname).get('days'):
				days = [self.options.day]
			else:
				days.append(self.options.day)

			# Filter uniques and sort before saving
			days = list(set(days))
			days.sort()
			self.data.get('groups').get(groupname)['days'] = days

		# Add group domains if needed
		if self.options.domain:
			domain = self.options.domain.lower();
			if re.match('http://', domain):
				domain = domain[len('http://'):]
			self.data.get('groups').get(groupname).get('domains').append(domain)

		# Activate group by default
		self.data.get('active').append(groupname)

		# Save and reload new information
		self._save_json(self.data)
		self._load_json()
		self.options.update = True

	def remove(self):

		# Verify group flag is set
		if not self.options.group:
			print( self.color('Error', 'red') + ' Could not remove, no group specified. Please include --group value, even if it is "--group default". See --help for command more information.')
			return False

		# Verify group exists
		if not self.data.get('groups').get(self.options.group.lower()):
			print( self.color('Error', 'red') + ' Could not remove group, group does not exist: {0}'.format(self.options.group))
			return False

		# Remove group if no domain/day/hour field is specified
		if not (self.options.day or self.options.domain or self.options.hour):

			# Prompt for confirmation
			command = raw_input('Are you sure you want to delete the group {0}? (y/n/quit): '.format(self.options.group)).lower()

			# Verify input
			if not re.match('(y|n|quit)', command):
				print('Input not recongized. Please try again')
				self.remove()

			# Take appropriate action
			if command == 'quit':
				sys.exit(0)
			elif command == 'n':
				return False

			# Remove group and update JSON
			del self.data.get('groups')[self.options.group.lower()]

		else:

			# Cache group object
			group = self.data.get('groups').get(self.options.group.lower())

			# Remove day
			if self.options.day != None and self.options.day in group.get('days'):
				group['days'].remove(self.options.day)

			# Remove domains
			if self.options.domain != None and self.options.domain in group.get('domains'):
				group['domains'].remove(self.options.domain)

			# Remove hours
			if self.options.hour != None and self.options.hour in group.get('hours'):
				group['hours'].remove(self.options.hour)

			# Save modified cache object
			self.data.get('groups')[self.options.group.lower()] = group

		# Save and update hosts file
		self._save_json(self.data)
		self._load_json()
		self.options.update = True

	def empty(self):

		# Verify group flag is set
		if not self.options.group:
			print( self.color('Error', 'red') + ' Could not empty field, no group specified. Specify a group name with -g/--group. See --help for command information.')
			return False

		# Verify group exists
		if self.data.get('groups').get(self.options.group.lower()):
			group = self.data.get('groups').get(self.options.group.lower())
		else:
			print( self.color('Error', 'red') + ' Could not empty group, group does not exist: {0}'.format(self.options.group))
			return False

		# Check if other flags are set
		if self.options.empty == 'days':
			group['days'] = []

		elif self.options.empty == 'domains':
			group['domains'] = []

		elif self.options.empty == 'hours':
			group['hours'] = []

		# Save changes
		self._save_json(self.data)
		self._load_json()
		self.options.update = True

	def activate(self):

		# Add to active group
		if (self.options.group != None and
			self.options.group not in self.data.get('active') and
			self.options.group in self.data.get('groups')):

			data = self.data.get('active', [])
			data.append(self.options.group)
			self.data['active'] = data

		# Save and reload new information
		self._save_json(self.data)
		self._load_json()

	def deactivate(self):

		# Remove from active group
		if (self.options.group != None and
			self.options.group in self.data.get('active') and
			self.options.group in self.data.get('groups')):

			data = self.data.get('active', [])
			data.remove(self.options.group)
			self.data['active'] = data

		# Save and reload new information
		self._save_json(self.data)
		self._load_json()

	def update_hosts(self):

		# Setup files if script hasn't run before
		self._init_hosts()

		# Grab template file
		try:
			hosts_template = open(self.settings.get('hosts_file_template'), 'r')
			template = hosts_template.read()
		except IOError:
			print(self.settings.get('timestamp', '') + self.color(' Error', 'red') + ' Could not open hosts template file: {0}'.format(self.settings.get('hosts_file_template')))
			sys.exit(1)

		# Create new content
		disclaimer = '''
##
# WARNING
#
# This file has been dynamically created by the internet.py script. Any changes
# made will be erased next time the file is generated. Add changes to the
# /etc/hosts.template file.
#
# The original hosts file can be found at /etc/hosts.original. Be sure to
# disable the internet.py script first!
##
'''

		# Use a set to collect a unique domain list from active groups
		domains = set()
		active = self.data.get('active')
		groups = self.data.get('groups')

		# Check active groups, verify each exists and is live
		# if so, add to domains list.
		for name in active:
			if groups.get(name) and self._is_live(name):
				for domain in groups.get(name).get('domains', {}):
					domains.add(domain)

		# Turn back into a list, sort it, then create file lines
		# Since we are using join, need to add an extra blackhole value at the
		# beginning
		body = ''
		if len(domains) > 0:
			domains = list(domains)
			domains.sort()
			body += '\n{0}\t'.format(self.settings.get('hosts_file_blackhole'))
			body += '\n{0}\t'.format(self.settings.get('hosts_file_blackhole')).join(domains)

		# Confirm file if requested
		def confirm(hosts_content):
			print(hosts_content)

			# Query user for confirmation
			command = raw_input('\nWrite the above content to the hosts file: {0}? (y/n/quit): '.format(os.path.abspath(self.settings.get('hosts_file'))))
			if not re.match('(y|n|quit)', command):
				print('Input not recongized. Please try again')
				confirm('')

			# Take appropriate action
			if command == 'quit' or command == 'n':
				sys.exit(0)

		hosts_content = template + disclaimer + body
		if self.options.confirm:
			confirm(hosts_content)

		# Write to hosts file
		try:
			hosts_file = open(self.settings.get('hosts_file'), 'w')
			hosts_file.write(hosts_content)
			if os.path.exists('/etc/init.d/nscd'):
				call(['/etc/init.d/nscd', 'restart'])
			elif os.path.exists('/usr/bin/dscacheutil'):
				call(['/usr/bin/dscacheutil', '-flushcache'])
			if self.options.cron:
				print(self.settings.get('timestamp', '') + ' Successfully wrote to the hosts file: {0}'.format(self.settings.get('hosts_file')))
			sys.exit(0)
		except IOError:
			print(self.settings.get('timestamp', '') + self.color(' Error', 'red') + ' Could not write to hosts file: {0}'.format(self.settings.get('hosts_file')))
			sys.exit(1)

	def print_crontab(self):
		filepath = os.path.abspath(__file__)
		logpath = os.path.abspath(self.options.log_file)
		print('Add the following to the root crontab (e.g. $ sudo crontab -e):')
		print('0 * * * * {0} --cron >> {1} 2>&1'.format(filepath, logpath))

	# Utilities

	def color(self, str, color):

		# Determine and cache whether terminal supports colors
		try:
			self.options.color_terminal
		except AttributeError:
			term = os.getenv('TERM')
			if re.search('256', term, flags=re.IGNORECASE):
				self.options.color_terminal = 256
			elif re.search('color', term, flags=re.IGNORECASE):
				self.options.color_terminal = 8
			else:
				self.options.color_terminal = False
			return self.color(str, color)

		# If terminal supports color return ascii code
		# For more advanced color handling check out python clint:
		# http://www.nicosphere.net/clint-command-line-library-for-python/
		# Todo: finish 256 colors
		color_map = {
			'8_red': '\x1b[31m',
			'8_green': '\x1b[32m',
			'8_yellow': '\x1b[33m',
			'8_blue': '\x1b[34m',
			'8_pink': '\x1b[35m',
			'8_cyan': '\x1b[36m',
			'8_white': '\x1b[37m',
			'256_red': '\x1b[38;5;196m',
			'256_green': '\x1b[38;5;190m',
			'256_yellow': '\x1b[38;5;3m',
			'256_blue': '\x1b[38;5;4m',
			'256_pink': '\x1b[38;5;5m',
			'256_cyan': '\x1b[38;5;6m',
			'256_white': '\x1b[38;5;7m',
			'clear': '\x1b[0m'
		}
		color_map.setdefault('clear')

		# See: http://ascii-table.com/ansi-escape-sequences.php
		# http://www.mudpedia.org/wiki/Xterm_256_colors
		if self.options.color_terminal != False and self.options.no_color != True:
			color_prefix = self.options.color_terminal.__str__()
			return color_map.get(color_prefix + '_' + color) + '{0}'.format(str) + color_map.get('clear')
		else:
			return str

if __name__ == "__main__":
	try:
		Internet()
	except EOFError:
		print('')
		sys.exit(1)
	except KeyboardInterrupt:
		print('')
		sys.exit(1)
else:
	print('Error: Command line support only')
	sys.exit(1)
