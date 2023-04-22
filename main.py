from queue import Queue
import sys
from http_score import score_HTTP
from ssh_score import score_SSH
from ftp_score import score_FTP
from sql_score import score_SQL
from dns_score import score_DNS
from smb_score import score_SMB
from ad_score import score_AD
from http_score_node import score_NODE
from http_score_nginx import score_NGINX
from irc_score import score_IRC
import requests
import threading

shared_queue = Queue()
flaskServAddr = 'http://127.0.0.1:5000'
SCORE_FILE = 'scores.txt'
lock = threading.Lock()
value = 1


def spawn_threads(alive, team_num):

    df = open('host_list', 'r')
    threads = []
    for line in df:
        split_line = line.split(' ')
        if team_num == 1:
            protocol = split_line[0]
            host = split_line[1]
            port = split_line[2]
        else:
            protocol = split_line[0]
            host = split_line[3]
            port = split_line[4]
        # because python hates me and added match statements in 3.10
        if protocol == 'APACHE':
            target = score_HTTP
        elif protocol == 'DNS':
            target = score_DNS
        elif protocol == 'SSH':
            target = score_SSH
            port = '22'
        elif protocol == 'SQL':
            target = score_SQL
        elif protocol == 'FTP':
            target = score_FTP
        elif protocol == 'SMB':
            target = score_SMB
        elif protocol == 'AD':
            target = score_AD
        elif protocol == 'NGINX':
            target = score_NGINX
        elif protocol == 'NODE':
            target = score_NODE
        elif protocol == 'IRC':
            target = score_IRC
        else:
            print("Undefined protocol in input")
            exit(-1)

        t = threading.Thread(target=target, args=(shared_queue, alive, lock, host, port, value, team_num))
        threads.append(t)
    return threads

def main():
    alive_bool = True
    alive = lambda : alive_bool
    threads_blue1 = spawn_threads(alive, 1)
    threads_blue2 = spawn_threads(alive, 2)
    # spawn the threads
    for thread in threads_blue1:
        thread.start()
    for thread in threads_blue2:
        thread.start()

    # main loop
    try:
        blue1_score = 0
        blue2_score = 0
        try: 
            f = open(SCORE_FILE, 'r')
            line = f.readline()
            scores = line.split(',')
            print(f"Reading scores from file: blue 1: {scores[0]}, blue 2: {scores[1]}")
            # If we got this far, the score file exists and is populated.
            blue1_score = int(scores[0])
            blue2_score = int(scores[1])
        except FileNotFoundError:
            blue1_score = 0
            blue2_score = 0

        while(True):
            content = shared_queue.get()
            print(content)

            if content['status'] == 'UP' and content['team_num'] == 1:
                blue1_score += int(content['value'])
            elif content['status'] == 'UP' and content['team_num'] == 2:
                blue2_score += int(content['value'])
            
            print(f"Blue 1 score: {blue1_score}\n Blue 2 Score: {blue2_score}\n\n")


            try:
                print(f"Posting {content} to {flaskServAddr}\n")
                res = requests.post(flaskServAddr + '/update_services', content)
                print(f"Received response: {res} from {flaskServAddr}\n\n")
                print(f"Posting current scores to {flaskServAddr}\n")
                res = requests.post(flaskServAddr + '/update_scores', {'blue_1_score' : blue1_score, 'blue_2_score' : blue2_score})
                print(f"Received response: {res} from {flaskServAddr}\n\n")
            except requests.exceptions.ConnectionError:
                print("Error while connecting to the webserver!", file=sys.stderr)

    except KeyboardInterrupt:
        print('\n\nAttempting to exit gracefully....')
        alive_bool = False


        for thread in threads_blue1:
            thread.join()
        for thread in threads_blue2:
            thread.join()

        print("All threads shutdown successfully!")
        print("Writing score state: ")
        with open(SCORE_FILE, 'w') as f:
            f.write(f"{blue1_score}, {blue2_score}")
    


if __name__ == '__main__':
    main()

