import nmap
from time import sleep
def score_IRC(queue, alive, lock, target, port, value, team_num):
    try:    
        nmScan = nmap.PortScanner()
        nmScan.scan(target, '6697')
        status = nmScan[target]['tcp'][6697]['state']
        if status == 'open':
            print(1)
            lock.acquire()
            queue.put({'service': 'irc', 'status': 'UP', 'host': target, 'value': value, 'team_num': team_num})
            lock.release()
        #Port is anything except open
        else:
            lock.acquire()
            queue.put({'service': 'irc', 'status': 'DOWN', 'host': target, 'value': value, 'team_num': team_num})
            lock.release() 
        
    #IRC failed to connect
    except Exception as e:
        lock.acquire()
        queue.put({'service': 'irc', 'status': 'DOWN', 'host': target, 'value': value, 'team_num': team_num})
        lock.release()
    sleep(60)
