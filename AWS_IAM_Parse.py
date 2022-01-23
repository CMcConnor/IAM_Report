# AWS IAM Parser
# @Version 1.0

import boto3
import csv
import json
from urllib.parse import quote

# API call to the AWS Account
client = boto3.client('iam')
response = client.get_account_authorization_details()

# Convert URL Encoded JSON object
r = json.dumps(response, indent=4, sort_keys=True, default=str)

# write JSON object to text file
f = open("response.json", "a")
f.write(r)
f.close()

# initialize variables
RoleDetails = response["RoleDetailList"]
GroupDetails = response["GroupDetailList"]
UserDetails = response["UserDetailList"]
PolicyDetails = response["Policies"]
extraPolicies = []

# create output file
csv_file = open('output.csv', 'w')
writer = csv.writer(csv_file)

#Users
writer.writerow(('----------Users----------',))
writer.writerow(("UserName", "Group", "Policy"))

for user in UserDetails:
    for group in user["GroupList"]:
        writer.writerow((user["UserName"], group))
    for pol in user["AttachedManagedPolicies"]:
        extraPolicies.append(pol)
        writer.writerow((user["UserName"],"", pol["PolicyName"]))

#Groups
writer.writerow(('----------Groups----------',))
writer.writerow(("GroupName", "AWS Managed Policies", "Custom Policies"))

for group in GroupDetails:
    #print(group["GroupName"])
    if isinstance(group["AttachedManagedPolicies"], (list, tuple)):
        if(len(group["AttachedManagedPolicies"]) == 0):
            for custPol in group["GroupPolicyList"]:
                extraPolicies.append(custPol)
                writer.writerow((group["GroupName"],"",custPol["PolicyName"]))
        else:
            for x in group["AttachedManagedPolicies"]:
                writer.writerow((group["GroupName"], x["PolicyName"],))
    else:
        writer.writerow((group["GroupName"], group["AttachedManagedPolicies"]["PolicyName"]))

#Roles
writer.writerow(('----------Roles----------',))
writer.writerow(("Role Name", "AWS Managed Policies", "Managed Policies"))
for role in RoleDetails:
    for pol in role["AttachedManagedPolicies"]:
        writer.writerow((role["RoleName"], pol["PolicyName"], ""))

csv_file.close()
