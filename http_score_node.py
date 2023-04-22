import requests
from time import sleep

DPORT = 80


def score_NODE(queue, alive, lock, target, port, value, team_num):
    while alive():
        try:
            res = requests.get('http://' + target + ":" + str(port) + '/api/v1/products', timeout=5)

            # We got a 200 response code
            if res.ok:
                lock.acquire()
                queue.put({'service': 'NODE', 'status': 'UP', 'host': target, 'value': value, 'team_num': team_num, 'port': port})
                lock.release()
            # We got a non-200 response code
            else:
                lock.acquire()
                queue.put({'service': 'NODE', 'status': 'DOWN', 'host': target, 'value': value, 'team_num': team_num, 'port': port})
                lock.release()

        # HTTP Server failed to respond
        except requests.exceptions.ConnectionError:
            lock.acquire()
            queue.put({'service': 'NODE', 'status': 'DOWN', 'host': target, 'value': value, 'team_num': team_num, 'port': port})
            lock.release()
        except:
            lock.acquire()
            queue.put({'service': 'NODE', 'status': 'DOWN', 'host': target, 'value': value, 'team_num': team_num, 'port': port})
            lock.release()

        sleep(60)



