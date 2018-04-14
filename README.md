## A very simple script to brute force ssh

This script will use the first username and password combination to test all IPs,then the the second one.

<pre>
Usage: main.py [options]

Options:
  --version    show program's version number and exit
  -h, --help   show this help message and exit
  -I IPLIST    IP list
  -U USERLIST  Username list
  -P PASSLIST  Password list
  -i IP        Single ip to attack
  -u USERNAME  Single username to attack
  -p PASSWORD  Single password to attack
  -t THREAD    Number of threads  default:5
  -v           Verbose
  -o OUT       Output file
</pre>

## Example
Single IP with single username and password list
<pre>
python main.py -i 127.0.0.1 -u root -P password.txt
</pre>

IP list with single username list and password list
<pre>
python main.py -I ip.txt -u root -P password.txt
</pre>
