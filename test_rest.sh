#!/bin/bash

hostname="192.168.8.6"
username="karim"
password="karim"

# LIST ALL PROFILES
#curl --dump-header -  -k -u $username:$password -H "Content-Type: application/json" -X GET http://192.168.8.6/nuages/api/v1/profile
#exit 0 
#curl --dump-header -  -k -u $username:$password -H "Content-Type: application/json" -X GET http://192.168.8.6/nuages/api/v1/profile

# LIST ALL VMS
#curl  --dump-header - -k -u $username:$password -H "Content-Type: application/json" -X GET http://192.168.8.6/nuages/api/v1/vm
#exit 0

# LIST ONE VM
#curl -k -u $username:$password -H "Content-Type: application/json" -X GET http://192.168.8.6/nuages/api/v1/vm/satellite6
#exit 0

#START A VM 
curl --dump-header - -k -u $username:$password -H "Content-Type: application/json" -X GET  http://192.168.8.6/nuages/api/v1/vm/satellite6/start
exit 0 

#USING XML
#curl --dump-header -  -k -u $username:$password -H "Accept: application/xml" -X GET http://192.168.8.6/nuages/api/v1/profile

#LIST A GIVEN PROFILE
#curl -k -u $username:$password -H "Content-Type: application/json" -X GET http://192.168.8.6/nuages/api/v1/profile/basic6
curl -k -u $username:$password -H "Content-Type: application/json" -X GET http://192.168.8.6/nuages/api/v1/stack

#CREATE A NEW PROFILE
#curl  --dump-header - -k -u $username:$password -H "Content-Type: application/json" -d  '{"name":"basicprout" }' -X POST http://192.168.8.6/nuages/api/v1/profile
