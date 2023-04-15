import requests
from time import sleep

DPORT = 80


def score_NGINX(queue, alive, lock, target, port, value, team_num):
    while alive():
        try:
            res = requests.get('http://' + target, timeout=5)

            # We got a 200 response code
            if res.ok:
                lock.acquire()
                queue.put({'service': 'HTTP', 'status': 'UP', 'host': target, 'value': value, 'team_num': team_num})
                lock.release()
            # We got a non-200 response code
            else:
                lock.acquire()
                queue.put({'service': 'HTTP', 'status': 'DOWN', 'host': target, 'value': value, 'team_num': team_num})
                lock.release()

        # HTTP Server failed to respond
        except requests.exceptions.ConnectionError:
            lock.acquire()
            queue.put({'service': 'HTTP', 'status': 'DOWN', 'host': target, 'value': value, 'team_num': team_num})
            lock.release()
        except:
            lock.acquire()
            queue.put({'service': 'HTTP', 'status': 'DOWN', 'host': target, 'value': value, 'team_num': team_num})
            lock.release()

        sleep(60)



