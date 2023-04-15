import ldap
from time import sleep

def score_AD(queue, alive, lock, servername, team_num, port, value=1):
    while alive():
        try:
            l = ldap.initialize(f'ldap://10.0.{team_num}.1')
            l.simple_bind_s()

            l.search('(&(objectCategory=person)(objectClass=user))', ldap.SCOPE_SUBTREE)
            lock.acquire()
            queue.put({'service': 'Active Directory', 'status': 'UP', 'host' : servername, 'value': value, 'team_num': team_num})
            lock.release()

        except Exception:
            lock.acquire()
            queue.put({'service': 'Active Directory', 'status': 'DOWN', 'host' : servername, 'value': value, 'team_num': team_num})
            lock.release()
        sleep(60)
