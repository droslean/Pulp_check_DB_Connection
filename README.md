# Pulp Check DB Connection
Pulp checking connection to mongoDB, created for Jenkins job.
The script takes the hostname,port,username and password of the pulp server 
from environment variables. This was done this way in order to be suitable to be used in 
Jenkins job. 

The script is restarting the following services:

qpidd
pulp_celerybeat
pulp_resource_manager
httpd

then it uses the pulp API to check the connection to the database.
