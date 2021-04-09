# Netbox-ansible-python

Netbox-ansible-python is an API.
It interprets JSON Post requests containing Ansible Gather Facts and contacts the Netbox Swagger API to add virtual machines with their assigned IP addresses

![Netbox-Diagram](https://i.ibb.co/Sx81wTH/t-l-chargement.png)

# Usage

Follow instructions for using the API

## 1) Build container

### Certificate

 1. Place an PEM (important) certificate in the **certs/** folder
 2. Name it "**cert.pem**"

### Build
Place your terminal on the same floor as the Dockerfile, then:

    > docker build -t REPO/image:tag .

## 2) Run API

 1. Vous pouvez copier le fichier **docker-compose-example/docker-compose.yml**
 2. Edit it and set the desired port, default as **5000**
 3. Replace 'image: **ASSIGNIT**' by the previous image build
 4. Set the environment variables (check the example below)
 5. Compose-it:
 > docker-compose up -d

ENVIRONMENT (**Required**):

 - `NETBOX_URL` (Set the nextbox url -> https://netboxexample.com)
 - `NETBOX_TOKEN` (Your token, you have it set up in the netbox admin panel)
 - `API_USERNAME` (Choose a username for basic auth)
 - `API_PASSWORD` (Choose a password for basic auth)

## 3) Test API

Access the API via HTTP (with the previously configured port). You should see a page indicating that the API is up and running.
Example: **http://myapi:5000**

## 4) Send DATA to API


You can use the example in the **ansible-playbook-example** folder, if you use Ansible.

Otherwise you need to send a Post request to your API container specifying the route **`/api/facts`**.
The body of the request **must be JSON** content and **match an ansible gather_facts**
