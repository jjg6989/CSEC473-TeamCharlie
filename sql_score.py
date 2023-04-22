import mysql.connector
from time import sleep

DDATABASE='sqli'

def score_SQL(queue, alive, lock, server, port, value, team_num, database=DDATABASE):
    while alive():
        try:
            config = {
                    'user':'root',
                    'password':'password',
                    'host':server,
                    'database':'sqli',
                    'connect_timeout':20
                    }
            connection = mysql.connector.connect(**config)
            # SQL Server connects sucessfully 
            lock.acquire()
            queue.put({'service': 'sql', 'status': 'UP', 'host':server, 'value':value, 'team_num': team_num})
            lock.release()

        # SQL Server failed to respond
        except Exception as e:
            lock.acquire()
            queue.put({'service': 'sql', 'status': 'DOWN', 'host':server, 'value':value, 'team_num': team_num, 'error':e})
            lock.release()
        sleep(60)
