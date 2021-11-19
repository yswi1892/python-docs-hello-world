from flask import Flask
from azure.identity import DefaultAzureCredential
from azure.mgmt.web import WebSiteManagementClient
import datetime
import time
import psutil 

app = Flask(__name__)

@app.route('/')
def hello():
    SUBSCRIPTION_ID = 'd7b6f37e-f1a4-4f7e-80ee-d38d12e83e2c'
    GROUP_NAME = 'rg-zuerst-prod-001'
    APP_SERVICE_PLAN = 'ASP-rgazuremlpoc001-8052'
    
    web_client = WebSiteManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # Get app service plan
    app_service_plan = web_client.app_service_plans.get(
        GROUP_NAME,
        APP_SERVICE_PLAN
    )
    print("Get app service plan:\n{}".format(app_service_plan.sku))
    
    #Create app service plan
    app_service_plan = web_client.app_service_plans.begin_create_or_update(
        GROUP_NAME,
        APP_SERVICE_PLAN,
        {
            "location": "japaneast",
            "sku": {
                "name": "P3v2",
                "tier": "PremiumV2",
                "size": "P3v2",
                "family": "Pv2",
                "capacity": "1"
            }
        }
    ).result()
    print("Create app service plan:\n{}".format(app_service_plan.sku))
    
    ###########

    print("Machine Learning")

    for i in range(6):
        print({
            'cpu_count':psutil.cpu_count(),
            'cpu_count_logical':psutil.cpu_count(logical=False),
            'cpu_percent':psutil.cpu_percent(interval=1, percpu=True)
        })
        
        #sleep 10s
        time.sleep(10)
    
    # Create app service plan
    app_service_plan = web_client.app_service_plans.begin_create_or_update(
        GROUP_NAME,
        APP_SERVICE_PLAN,
        {
            "location": "japaneast",
            "sku": {
                "name": "P1v2",
                "tier": "PremiumV2",
                "size": "P1v2",
                "family": "Pv2",
                "capacity": "2"
            }
        }
    ).result()
    print("Create app service plan:\n{}".format(app_service_plan.sku))
    
    ##################
    
    dt_now = datetime.datetime.now()
    print('time from app:', dt_now)

    return "current sku: {}".format(app_service_plan.sku)
    
if __name__ == "__main__":
    app.debug = True
    app.run()
