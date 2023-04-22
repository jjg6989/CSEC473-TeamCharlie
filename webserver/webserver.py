from flask import Flask, request, redirect
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

services = {}
scores = {'blue_1_score': 0, 'blue_2_score' : 0}

@app.route("/")
def landing_page():
    return redirect('/display_scores_1')

@app.route("/display_scores_1", methods=['GET'])
def display_services_1():
    content = {'services': services, 'scores' : scores}
    new_services = update_graphics(1)
    new_content = {'services': new_services, 'scores': scores[list(scores.keys())[0]]}
    return new_content
    

@app.route("/display_scores_2", methods=['GET'])
def display_services_2():
    content = {'services': services, 'scores' : scores}
    new_services = update_graphics(2)
    new_content = {'services': new_services, 'scores': scores[list(scores.keys())[1]]}
    return new_content


@app.route("/update_scores", methods=['POST'])
def update_scores():
    try:
        print(f"receives {request} FROM {request.host}\n\n")
        blue_1_score = request.form['blue_1_score']
        blue_2_score = request.form['blue_2_score']
        scores['blue_1_score'] = int(blue_1_score)
        scores['blue_2_score'] = int(blue_2_score)
        for key in services.keys():
            print(services[key])
        print(scores)
        
        return {"Success":True}
    except Exception:
        return {"Success":False}


@app.route("/update_services", methods=['POST'])
def update_services():
    try:
        print(f"Received {request} FROM {request.host}\n\n")

        host = request.form['host']
        service = request.form['service']
        status = request.form['status']
        score = request.form['value']

        if host in services.keys():
            if service in services[host].keys():
                services[host][service] = status
            else:
                services[host][service] = status
        else:
            services[host] = {service : status}
        return {'Success': True}
    except Exception:
        return {'Success' : False}

def update_graphics(team_num):
    global services
    new_services = Vividict()
    for host in services:
        if host.split('.')[2] == str(team_num):
            service = services[host]
            service_name = list(service.keys())[0]
            value = services[host][service_name]
            new_services[host][service_name] = value
        elif str(host.split('.')[3])[0:1] == str(team_num) and host.split('.')[2] == '3':
            service = services[host]
            service_name = list(service.keys())[0]
            value = services[host][service_name]
            new_services[host][service_name] = value
    return new_services
    
class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value
            
