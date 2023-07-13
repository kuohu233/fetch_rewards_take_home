# Fetch Rewards Take-Home
This is the Data Engineer take home task for Fetch Rewards on 07/12/2023. 

This application is going to fetch JSON data from AWS SQS Queue with Docker to run them locally, transform parts of the data, and then load to a Postgres database. 


## Setup
Tools include: 
* Docker (and also docker compose) 
* Python 3.8 (include packages: boto3, pycryptodome, psycopg2)

Build up docker compose container in the same folder of the application with command line `docker-compose up -d`. After this step, you should be able to connect both the source data and the target database. 

#### Note:
If you already have a Python package `Crypto`, try:

```
pip uninstall crypto
pip uninstall pycryptodome
```

and then 

```
pip install pycryptodome
```

The `Crypto` package was no longer maintained since 2013.

## How to use
Pull this repository, and try this command in command line:

`python <folder of repo>/sqs_fetcher.py <16 character key>`

## Credentials and Encryption
This task will not require any AWS accounts and we only use dummy credentials. 

AES (ECB mode) encryption is used to mask PII. The key for decryption can be customized. If you need to recover the masked PII, please remember your key which would be used in the `decrypt` function.


## Possible Improvements
Currently this repo is a sample application. If we want to make it a formal production, we can think about:
* A configuration management, instead of taking everything in one file. 
* Error handling. This will let debugging process easier.
* Logging system will allow people to track what happened to this application.

Also, in order to deploy this application, I would suggest to get:
* Well tested and well prepared.
* CI/CD.
* Prepare for possible scaling. The unused messages can be offload from the database in the future. Upgrading the server (or use multiple nodes with parallel distributed system) can also be a solution.
