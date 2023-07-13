# Fetch Rewards Take-Home
This is the Data Engineer take home task for Fetch Rewards on 07/12/2023. 

This application is going to fetch JSON data from AWS SQS Queue with Docker to run them locally, transform (or encrypt) parts of the data, and then load to a Postgres database. 


## Setup
Tools include: 
* Docker (and also docker compose) 
* Python 3.8 (include packages: boto3, pycryptodome, psycopg2)
`pip install <packages>` for the needs.

### Note:
If you already have a Python package `Crypto`, try:
`pip uninstall crypto`
`pip uninstall pycryptodome`
and then 
`pip install pycryptodome`

Build up docker compose container in the same folder of the application with command line `docker-compose up -d'. After this step, you should be able to connect the data source and the target database. 

## Credentials and Encryption
This task will not require any AWS accounts and we only use dummy credentials. 
AES encryption is used to mask parts of the data. The KEY and other variables (nounce and tag) for decryption are also accessable. 
