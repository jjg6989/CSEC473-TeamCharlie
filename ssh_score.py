import paramiko
from time import sleep
import traceback

DPORT = '22'
DUSERNAME = 'charlie'
DPASSWORD = 'letsgocharlie'

def score_SSH(queue, alive, lock, target, port, value, team_num, username=DUSERNAME, password=DPASSWORD):
    while alive():
        test = 0
        print(str(team_num) + target)
        try:
            s = paramiko.SSHClient()
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            s.connect(target, int(port), username, password, timeout=5)
            
            # SSH Server connects sucessfully 
            lock.acquire()
            queue.put({'service': 'SSH', 'status': 'UP', 'host':target, 'value': value, 'team_num': team_num, 'test':test, 'port':int(port), 'user': username, 'password': password, 'error': 'none'})
            lock.release()

        # SSH Server failed to login
        except paramiko.ssh_exception.AuthenticationException:
            lock.acquire()
            queue.put({'service': 'SSH', 'status': 'UP', 'host':target, 'value': value, 'team_num': team_num, 'test': test, 'port':int(port), 'user': username, 'password': password, 'error': 'auth'})
            lock.release()

        # SSH Server failed to respond
        except:
            lock.acquire()
            queue.put({'service': 'SSH', 'status': 'DOWN', 'host':target, 'value':value, 'team_num': team_num, 'test':test, 'port':int(port), 'user': username, 'password': password, 'error': 'failed to respond'})
            lock.release()
            
        sleep(60)

