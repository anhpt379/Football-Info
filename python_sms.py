import cookielib
import getpass
import urllib2
import getopt
import string
import sys

__author__ = "Ramanathan Vishnampet"
__copyright__ = "None"
__credits__ = ["Ramanathan Vishnampet"]
__license__ = "Free"
__email__ = "ramanathanvishnampet@gmail.com"

def usage():
    print """Usage: sms [-hq] [-u username] [-p password] [-n number]
 
Mandatory arguments to long options are mandatory for short \
options too. If the options -u, -p or -n are not specified, \
the user is prompted to enter these details.
 
-h, --help                 display this help and exit
-q, --quiet                suppress all output (except error messages)
-u, --username=username    specify the Way2SMS username (mobile number)
-p, --password=password    specify the password
-n, --number=number        specify the mobile number of the intended recipient\
"""

quiet = False;
username = "";
password = "";
number = "";

try:
    opts, args = getopt.getopt(sys.argv[1:], "hqu:p:n:",
["help", "quiet", "username=", "password=", "number="])
except getopt.GetoptError:
    usage()
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-h", "--help"):
        usage()
        sys.exit()
    elif opt in ("-q", "--quiet"):
        quiet = True;
    elif opt in ("-u", "--username"):
        username = arg
    elif opt in ("-p", "--password"):
        password = arg
    elif opt in ("-n", "--number"):
        number = arg

url = 'http://wwwk.way2sms.com//auth.cl'

if not username:
    if not quiet:
        username = raw_input("Enter your Way2SMS username\
 (mobile number): ");
    else:
        username = raw_input();
if not password:
    if not quiet:
        password = getpass.getpass("Enter your password: ");
    else:
        password = getpass.getpass();

data = 'username=' + username + '&password=' + password + '&Submit=Sign+in'
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('Referer', 'http://wwwk.way2sms.com//entry.jsp'),
('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) \
Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3')]
