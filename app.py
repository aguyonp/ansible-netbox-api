from flask import Flask, request, Response, render_template, abort

import sys
import json
import pynetbox
import os

app = Flask(__name__)

#Netbox_VARS
netbox_url="https://netbox.ibanfirst.lan"
netbox_token="9712245587739acb26ec34005bc4ead4934e7568"
netbox_cert="certs/cert.pem"
#Netbox_VARS

#Facts_VARS
vm_hostname=""
vm_ram=""
vm_cpu=""
vm_interfaces=[]
vm_ip={}
#Facts_VARS

#Trust SSL
os.environ['REQUESTS_CA_BUNDLE'] = netbox_cert
#Netbox auth
nb = pynetbox.api(url=netbox_url, token=netbox_token)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/api/facts', methods=['POST'])
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

        print("hostname= ",vm_hostname) ; sys.stdout.flush()
        print("Ram= ",vm_ram) ; sys.stdout.flush()
        print("CPU= ",vm_cpu) ; sys.stdout.flush()


        #Add every interfaces in vm_interface array
        for interface in req['interfaces']:
            vm_interfaces.append(interface)
        
        #Assing ip to interface in vm_ip array array
        for interface in vm_interfaces:
            
            #If IPV4 is present, save it in the dic
            try:
                vm_ip[interface] = req[interface]['ipv4']['address']
            except:
                print("Unable to find ip address") ; sys.stdout.flush()
                vm_ip[interface] ="0.0.0.0"

            print(interface) ; sys.stdout.flush()
            print(vm_ip[interface]) ; sys.stdout.flush()

        result = nb.virtualization.virtual_machines.create(
                name=vm_hostname,
                cluster="1",
                vcpus=vm_cpu,
                memory=vm_ram,
                status="active"
        )

        #print(result) ; sys.stdout.flush()
        print(pynetbox.core.endpoint.Endpoint('api')) ; sys.stdout.flush()
        #print(pynetbox.core.endpoint.Endpoint('app')) ; sys.stdout.flush()
        #print(pynetbox.core.endpoint.Endpoint('name')) ; sys.stdout.flush()


        #Return ok state to ansible
        return Response(status=201)

    else:
        abort(400)