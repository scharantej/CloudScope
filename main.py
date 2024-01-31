
from flask import Flask, render_template, request
import subprocess
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vms')
def vms():
    vms = subprocess.check_output(['gcloud', 'compute', 'instances', 'list']).decode('utf-8')
    return render_template('vms.html', vms=vms)

@app.route('/gke_workloads')
def gke_workloads():
    workloads = subprocess.check_output(['gcloud', 'container', 'workloads', 'list']).decode('utf-8')
    return render_template('gke_workloads.html', workloads=workloads)

@app.route('/cloudsql_instances')
def cloudsql_instances():
    instances = subprocess.check_output(['gcloud', 'sql', 'instances', 'list']).decode('utf-8')
    return render_template('cloudsql_instances.html', instances=instances)

@app.route('/create_dashboard', methods=['POST'])
def create_dashboard():
    data = request.get_json()
    dashboard_name = data['dashboard_name']
    dashboard_description = data['dashboard_description']
    dashboard_resources = data['dashboard_resources']

    # Create a new dashboard
    dashboard_id = subprocess.check_output(['gcloud', 'monitoring', 'dashboards', 'create', dashboard_name, '--description', dashboard_description]).decode('utf-8')

    # Add resources to the dashboard
    for resource in dashboard_resources:
        subprocess.check_output(['gcloud', 'monitoring', 'dashboards', 'add-resource', dashboard_id, resource])

    return json.dumps({'dashboard_id': dashboard_id})

if __name__ == '__main__':
    app.run()


This code includes the necessary routes and functionality to create a Flask application that serves as a monitoring dashboard for a multi-layered app deployed in GCP. It can display metrics related to VMs, GKE Workloads, and CloudSQL instances. Additionally, it provides a route to create custom dashboards using the Google Cloud Monitoring API.