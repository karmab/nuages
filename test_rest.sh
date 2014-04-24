#!/bin/bash

hostname="192.168.8.6"
username="admin"
password="prout"

# LIST ALL PROFILES
#curl --dump-header -  -k -u $username:$password -H "Content-Type: application/json" -X GET http://192.168.8.6/nuages/api/v1/profile
#exit 0 

# LIST ALL VMS
#curl -k -u $username:$password -H "Content-Type: application/json" -X GET http://192.168.8.6/nuages/api/v1/vm/
#exit 0

#USING XML
curl --dump-header -  -k -u $username:$password -H "Accept: application/xml" -X GET http://192.168.8.6/nuages/api/v1/profile

#LIST A GIVEN PROFILE
#curl -k -u $username:$password -H "Content-Type: application/json" -X GET http://192.168.8.6/nuages/api/v1/profile/1/

#CREATE A NEW PROFILE
#curl  --dump-header - -k -u $username:$password -H "Content-Type: application/json" -d  '{"name":"basicprout" }' -X POST http://192.168.8.6/nuages/api/v1/profile
