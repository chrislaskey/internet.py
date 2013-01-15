About
================================================================================

Internet.py is a script to limit personal web browsing.

It works by modifying the ```/etc/hosts file```. The hosts file associates
numeric based addresses like ```127.0.0.1``` with named addresses like
```localhost```. Usually this file is only used to cache local network names,
as remote computers accessible over the internet have numeric addresses that may,
and often do, change.

A web browser utilizes the Domain Name Service (DNS) to keep track of these
dynamically changing numeric addresses. However before asking the remote DNS
service for the numeric address of a domain like ```google.com```, the computer
will check the /etc/hosts file just in case the information is already there.

This means a web browser request for ```google.com``` can be redirected to a
different numeric address of our choosing, instead of resolving to the actual
address like ```173.194.43.5```.

By choosing an unused address, we can create a 'blackhole' where the requested
site can not be reached. By default we use an address in the local
```127.0.0.*``` range, but you can modify this to whatever you like in the
settings below.

__Note__ modern operating systems and web browsers cache DNS entries for a short
time in order to cut down on the number of overall DNS calls. This DNS cache
is checked before the /etc/hosts file. This script attempts to clear all
local DNS caches. However you may need to clear a DNS cache manually, or
simply wait a few minutes for the DNS cache to expire.

__Note__ since this file modifies ```/etc/hosts```, it will effect all users
on the machine.

__Why ```/etc/hosts```?__ I'm not a big fan of cron requirements for scripts,
but the alternative would be to pipe all traffic through a python daemon. I
love Python, but unix based systems already do a good job networking without
adding more cogs.

__Why not ```/etc/resolve.conf```?__ Mac OS X Darwin does not use
```/etc/resolve.conf``` in the same way Linux does. In the interests of this
being cross-compatible I've decided to stick with ```/etc/hosts``` modification.

Usage - groups, domains, and times, oh my!
================================================================================

This script is meant to be flexible, allowing access depending on the time and
day of the week.

Everything is organized into 'groups'. A group contains three pieces of
information: a list of domains; a list of hours to be active during; a list of
days to be active on.

__Remember__ this script modifies the ```/etc/hosts``` file, which requires root
privileges. Most command options require using sudo.

Groups
--------------------------------------------------------------------------------
You can define as many groups as you want, or simply use the default group aptly
named 'default.'

#### Examples

To add a new group:
```$ ./internet.py --add --group 'work'```

Remove a group:
```$ ./internet.py --remove --group 'work'```

__Warning!__ This removes all information. See ```--activate/--deactivate```
below.

Active List
--------------------------------------------------------------------------------
A group can be activated or deactivated. This allows you to create a group with
set times and days, but temporarily turn the group off without deleting the
hard work put into setting it up.

The 'default' group is active by default, and new groups are activated by
default as well.

#### Examples

List current groups and their status
```$ ./internet.py --list```

Deactivate a group:
```$ ./internet.py --deactivate --group 'work'```

Activate a group:
```$ ./internet.py --activate --group 'work'```

Domains
--------------------------------------------------------------------------------
The core of this script is the list of domains to block. Domain names should
not include 'http://' at the beginning. The 'http://' in a browser refers to the
method, or protocol, the browser should use to connect to a domain. The domain
name is the part that comes after it, e.g. ```google.com```. This is the named
address of the remote computer, and also the only part we care about.

Also, domains should not include any trailing information. For example write
```google.com```, not ```google.com/``` or ```google.com/analytics```.
Subdomains (information to the left) are okay, like ```translate.google.com```.

#### Examples

Add a domain to the default group:
```$ ./internet.py --add --domain 'google.com'```

Add a domain to a custom group:
```$ ./internet.py --add --domain 'google.com' --group 'work'```

Empty all domains in a group:
```$ ./internet.py --empty domains --group 'work'```

__Notice__ This script only supports single arguments, e.g. one ```--domain```,
```--hour``` or ```--day``` args. To add multiple domains, you must call
internet.py multiple times.

Days
--------------------------------------------------------------------------------
Days specify when a group's list of domains will be blocked. Days can be given
by their full names (e.g. ```Monday```), or as the wildcard '*'.

The default days range is '*', meaning it is active on all days. This is a
valid range and can be added to any group.

__Note__ adding the wildcard will overwrite current day ranges.

#### Examples

Add one day to a group:
```$ ./internet.py --add --day 'Tuesday'```

Empty all days in a group:
```$ ./internet.py --empty days --group 'work'```

Hours
--------------------------------------------------------------------------------
Hours specify when a group's list of domains will be blocked. Hours can be given
in single units (e.g. ```8```), in a range (e.g. ```9-17```), or as the wildcard
'*'.

The default hours range is '*', meaning it is active all the time. This is a
valid range and can be added to any group. __Note__ adding the wildcard will
overwrite current hour ranges.

All hours should be given as a __24 hour__ clock. Minutes are not supported and
should not be used, e.g. write ```9```, not ```9:00``` or ```900```.

#### Examples

Add one hour to a group:
```$ ./internet.py --add --hour 8```

Add an hour range to a group:
```$ ./internet.py --add --hour 9-17```

Empty all hours in a group:
```$ ./internet.py --empty hours --group 'work'```

Misc
--------------------------------------------------------------------------------
There are more commands and functionality than outlined here. Run the help
command (```-h/--help```) for a complete list of available flags/options.

#### Examples

List current groups and their status:
```$ ./internet.py --list``

View the hosts file before updating it:
```$ ./internet.py --update --confirm``

Print crontab information:
```$ ./internet.py --print-crontab``

__Remember__ this script modifies the ```/etc/hosts``` file, which requires root
privileges. Most command options require using sudo.

Recommendations
================================================================================

+ Run the script hourly via a cron job. Use the ```--print-crontab``` option
  for help on how to set this up.

+ Make sure this script has execute permissions (see ```$ man chmod``` for more
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

+ Support multiple values for fields like ```--domains```
+ Interactive menu mode
+ Move some flags to full args via ArgumentParser.add_subparsers
+ Add full 256 color set to color() function

License
================================================================================

All code is released under MIT license. See the attached LICENSE.txt file for
more information, including commentary on license choice.
