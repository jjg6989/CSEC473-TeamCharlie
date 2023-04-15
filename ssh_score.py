import paramiko
from time import sleep

DPORT = '22'
DUSERNAME = 'root'
DPASSWORD = 'password'

def score_SSH(queue, alive, lock, target, team_num, port=DPORT, value=1, username=DUSERNAME, password=DPASSWORD):
    while alive():
        try:
            s = paramiko.SSHClient()
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            s.connect(target, int(port), username, password)
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            s.connect(target, int(port), username, password)
            
            # SSH Server connects sucessfully 
            lock.aquire()
            queue.put({'service': 'SSH', 'status': 'UP', 'host':target, 'value': value, 'team_num': team_num})
            lock.release()

        # SSH Server failed to login
        except paramiko.ssh_exception.AuthenticationException:
            queue.put({'service': 'SSH', 'status': 'UP', 'host':target, 'value': value, 'team_num': team_num})

        # SSH Server failed to respond
        except:
            lock.acquire()
            queue.put({'service': 'SSH', 'status': 'DOWN', 'host':target, 'value':value, 'team_num': team_num})
            lock.release()
            
        sleep(60)

