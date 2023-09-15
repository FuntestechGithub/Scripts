from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.authorization import AuthorizationManagementClient

from multiprocessing.pool import ThreadPool

from collections import deque
from functools import partial

import json
import time


'''
This script is both CPU-bound and I/O bound, so parallel will be done through ThreadPool
'''
def getSPNList(cachedResource, subscriptionId:str, rbacMap:dict) -> None:
    resourceId = cachedResource[0]
    resourceType = cachedResource[1]

    # if resource group, get all resources in the resource group and put them to 'cache'
    if resourceType == "Microsoft.Resources/resourceGroups":
        resourceList = resource_client.resources.list_by_resource_group(resource_group_name=f"{cachedResource[2]}")
        for resource in list(resourceList):
            cache.append([resource.id,resource.type,resource.name])

    # for logging purpose
    print(f"Checking RBAC assignment on {resourceId}")

    # there will be cases that resouce is deleted after they got detected, use try/except to handle the unexpected exit
    try:
        auth_client = AuthorizationManagementClient(credential, subscriptionId)

        rbacList = auth_client.role_assignments.list_for_scope(
            scope=resourceId
        )
        
        for rbacAssignment in rbacList:
            if rbacAssignment.principal_type == "ServicePrincipal":
                if not rbacMap.get(resourceId):
                    rbacMap[resourceId] = {}
                    rbacMap[resourceId]['type'] = resourceType
                    rbacMap[resourceId]['spns'] = []
                rbacMap[resourceId]['spns'].append({
                    'principal_id': rbacAssignment.principal_id,
                    'role_definition_id': rbacAssignment.role_definition_id
                })

    except Exception as error:
        print(error)
    
    # remove the resource from cache
    cache.remove(cachedResource)
        


    
# writea file to JSON
def write2File(data):
    with open(f'./{subscriptionId}.json', 'w') as file:
        jsonObject = json.dumps(data)
        file.write(jsonObject)

# subscription based
def rbacDiscovery(subscriptionId:str):
    resource_client = ResourceManagementClient(credential, subscriptionId)
    
    # create a RBAC map
    rbacMap = {}

    # put resource groups to cache
    rgList = resource_client.resource_groups.list()
    for resourceGroup in rgList:
        cache.append([resourceGroup.id,resourceGroup.type,resourceGroup.name])

    # process on all resources
    while cache:
        with ThreadPool(20) as pool:
            pool.map(partial(getSPNList, subscriptionId=subscriptionId, rbacMap=rbacMap),cache, chunksize=1)

    # write JSON data to file
    write2File(rbacMap)




if __name__ == '__main__':
    global credential, cache, subscriptionId
    
    # credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
    subscriptionId = input('Enter the subscription ID:')
    credential = InteractiveBrowserCredential()

    
    # processCount = input('Enter the number of workers for the script execution (Suggested value: 20):  ')
    resource_client = ResourceManagementClient(credential, subscriptionId)
    cache = deque([])
    start_time = time.time()
    rbacDiscovery(subscriptionId)

    print("---Finished in %s seconds ---" % (time.time() - start_time))
     