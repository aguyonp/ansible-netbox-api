from flask import Flask, request, Response, render_template, abort

import sys
import json
import pynetbox
import os

app = Flask(__name__)

#Netbox_VARS
netbox_url=""
netbox_token=""
netbox_cert="certs/cert.pem"
#Netbox_VARS

#Facts_VARS
vm_hostname=""
vm_ram=""
vm_cpu=""
vm_interfaces=[]
vm_ip={}
vm_id=0
vm_interface_id=0
#Facts_VARS

#Trust SSL
os.environ['REQUESTS_CA_BUNDLE'] = netbox_cert
#Netbox auth
nb = pynetbox.api(url=netbox_url, token=netbox_token)

#APIFunctions
def add_vm(vm_hostname, vm_cpu, vm_ram):
    result = nb.virtualization.virtual_machines.create({
        "name": vm_hostname,
        "cluster": "1",
        "vcpus": vm_cpu,
        "memory": vm_ram,
        "status": "active"
    })
    global vm_id
    vm_id = result["id"]

def modify_vm(vm_hostname, vm_cpu, vm_ram):
    result = nb.virtualization.virtual_machines.get(name=vm_hostname)
    global vm_id
    vm_id = result["id"]
    result.update({
        "vcpus": vm_cpu,
        "memory": vm_ram,
        "status": "active"
    })

def addinterface_ip_vm(vm_id, vm_ip):
    #print(vm_id) ; sys.stdout.flush()
    for interface in vm_ip:
        try:
            result = nb.virtualization.interfaces.create({
                "virtual_machine": vm_id,
                "name": interface
            })

            vm_interface_id = result["id"]

            result = nb.ipam.ip_addresses.create({
                "address": vm_ip[interface]+"/24",
                "assigned_object_type": "virtualization.vminterface",
                "assigned_object_id": vm_interface_id,
                "nat_outside": "null"
            })

        except Exception:
            pass

#APIFunctions

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

        #Add every interfaces in vm_interface array
        for interface in req['interfaces']:
            vm_interfaces.append(interface)
        
        #Assing ip to interface in vm_ip array array
        for interface in vm_interfaces:
            
            #If IPV4 is present, save it in the dic
            try:
                vm_ip[interface] = req[interface]['ipv4']['address']
            except:
                vm_ip[interface] ="0.0.0.0"

        try:
            print("Add the VM to Netbox if it does not exist") ; sys.stdout.flush()
            #If VM dont exist
            add_vm(vm_hostname, vm_cpu, vm_ram)

        except pynetbox.RequestError as e:
            print("Failed to add VM, it already exist in netbox") ; sys.stdout.flush()
            print("Updating VM") ; sys.stdout.flush()

            #If VM exist
            modify_vm(vm_hostname, vm_cpu, vm_ram)
            #print("Could not create the VM, error: {}".format(str(e))) ; sys.stdout.flush()

        print("Add interfaces to vm", vm_hostname) ; sys.stdout.flush()
        
        #Add interfaces
        addinterface_ip_vm(vm_id, vm_ip)
        
        #Return ok state to ansible
        return Response(status=201)

    else:
        abort(400)