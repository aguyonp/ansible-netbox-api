from flask import Flask, request, Response, render_template, abort

import sys
import json

app = Flask(__name__)

#Facts_VARS
vm_hostname=""
vm_ram=""
vm_cpu=""
vm_interfaces=[]
vm_ip=[]
#Facts_VARS

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/facts', methods=['POST'])
def post_respond():

    json_req = json.dumps(request.json)
    print("Retrive DATA From POST Request"); sys.stdout.flush()
    
    if request.method == 'POST':

        #Parse JSON
        req = json.loads(json_req)

        #Catch Datas from json req
        vm_hostname = req['hostname']
        vm_ram = req['memory_mb']['real']['total']
        vm_cpu = req['processor_vcpus']

        print('Hostname=', vm_hostname) ; sys.stdout.flush()
        print(vm_ram ,'Mb') ; sys.stdout.flush()
        print('CPU:', vm_cpu) ; sys.stdout.flush()

        #Add every interfaces in vm_interface array
        for interface in req['interfaces']:
            vm_interfaces.append(interface)
        
        #Assing ip to interface in vm_ip array array
        # for interface in vm_interfaces:
        #     print(interface) ; sys.stdout.flush()
        #     interface = slice(interface)
        #     vm_ip[interface] ="LOL"
            # print(vm_ip[interface]) ; sys.stdout.flush()

        #Return ok state to ansible
        return Response(status=201)

    else:
        abort(400)