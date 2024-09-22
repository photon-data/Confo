


<p align="center"><img src="https://raw.githubusercontent.com/photon-data/Confo/refs/heads/main/assets/logo.png" width="300">
<img src="https://raw.githubusercontent.com/photon-data/Confo/refs/heads/main/assets/logophoton.png" width="100">
</p>
<p align="center"></p>

<p align="center"><h3 style="color: #193967; text-align: center">Multi backend configuration manager for python</h3></p>

<p align="center">

[//]: # (<a href="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml"><img src="https://github.com/sambe-consulting/confo/actions/workflows/pytest-workflow.yml/badge.svg"></a>)
<a href="https://houndci.com"><img src="https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg"></a>
<a href="https://github.com/apache/zookeeper/blob/master/LICENSE.txt"><img src="https://img.shields.io/github/license/apache/zookeeper"></a>


</p>

## About Confo
Confo is a flexible multi backend configuration manager for python. Built to provide a unified configuration management
interface in different environments.Confo supports both local configuration with json files and distributed configurations,
best suited for micro-service and distributed systems development.
## Getting started
1.Installation
```
pip install confo2

```

2.Setup Backends 

Confo currently supports two backends, a `filesystem` backend and a `ZooKeeper` backend.

2.1 Filesystem backend

The filesystem backend simply works by reading json files from the filesystem. An example configuration can be setup like below. Imagine you have a 
sales database with credentials you want to expose to your application, and you want to use a sales forecasting model which is exposed via REST api.
Confo uses namespaces to separate logical groups of configurations. For example everything concerned with systems from the `sales` department can be stored in the
`sales` namespace and every configuration concerned with systems from the `anlytics team` can be store in a namespace called `analytics`.

```
mkdir Configurations
mkdir Configurations/sales
mkdir Configurations/analytics
echo '{"host":"127.0.0.1", "port":5432,"username":"kabelo","password":"confoRocks"}' > Configurations/sales/database.json
echo '{"host":"127.0.0.1", "port":5432,"token":"2df228d6-890b-11eb-8dcd-0242ac130003","secret":"d51a8a7a-3286-4deb-8805-85f4528920ae 
dcfb49c0-a251-4657-87df-44996ea308ee"}' > Configurations/analytics/api_one.json
```
In the setup above both namespaces only have one configuration,but each namespace can have infinite configurations. `Confo` uses a json files to store each configuration.
```
backend 
   |______namespace
             |_______configuration
                          |__________fields
                          
e.g

filesystem 
  |________sales
             |___________database 
                             |_________host : 127.0.0.1 
                             |_________port : 5432
                             |_________user : kabelo 
                             |_________password :confoRocks 
```

```python
from confo.Confo import Confo
import confo.Backends as BE

#create the singleton configuration manager object 
config = Confo()


```

The `Confo` object is a singleton, meaning you can instantiate it multiple time through the code base, but you will always have
up to date configurations loaded. 

```python
# Instantiate a FILE_BACKEND backend 
cred = {"config_path":"Configurations/"}
config.load_backend(credentials=cred,name="example_backend",backend_type=BE.FILE_BACKEND)


```
The `Confo.load_backend(credentials,name,backend_type)` method is used to create a backend management object.The credentials differ by backend type 
The filesystem backend accepts a dictionary of credentials which contains the `config_path` key, this is 
the path where the configurations are stored.
#### backed operations 

To list all backends loaded 
```python
config.get_backends()
#RESULTS:

{'all_backends': ['example_backend'], 'active_backend': None}

```
This return a dictionary with two keys: `all_backends` holds  list of all backends registered in this application; and `active_backend` holds the 
name of the currently active backend.Note that activate_backend is None meaning the manager cannot access any configuration.If any of the configuration 
level methods are invoked a `BackendsActivationException` error is raised.Now to make sure a backend is active,

```python
#activate the example_backend
config.activate_backend("example_backend")
# List backends again to see if we have an active backend
print(config.get_backends())
#RESULTS
{'all_backends': ['example_backend'], 'active_backend': 'example_backend'}

```

Note that the `activate_backend` field has the backend we activated with `Confo.activate_backend`.

#### Namespace operations

As mentioned above namespaces create a logical partition between groups of configuration, this becomes more 
useful when dealing with distributed configurations, where multiple microservices are accessing and sharing configuration and data through Confo.

```python
#The method below is the namespace level analog to get_backends()
print(config.get_namespaces())
#RESULTS:
{'all_namespaces': ['sales', 'analytics'], 'current_namespace': '*'}

```

Please note we need to choose a namespace to use before we can access any configuration. If no namespace is chosen 
a `NamespaceNotLoadedException` error will be raised.

```python 

#choose namespace 
config.use_namespace("sales")
#check if a namespace is chosen
print(config.get_namespaces())

#RESULTS:
{'all_namespaces': ['sales', 'analytics'], 'current_namespace': 'sales'}

```

#### configuration level operations

lets get all configurations in the current namespace

```python
print(config.get_all())

#RESULTS: 
{'database': {'host': '127.0.0.1',
              'port': 5432,
              'username': 'kabelo',
              'password': 'confoRocks'}}
```

The sales department is exposing daily sales reports through a REST API, the report is read a json data 
which will be used by our application to build visualization. Lets create a new configuration programmatically, 
and store the credentials to this API. 

```python

config.set("sale_report","host","10.222.194.146")
config.set("sale_report","port","2389")
config.set("sale_report","token","01e947b6-8914-11eb-8dcd-0242ac130003")
config.set("sale_report","host","78f45902-c9b8-4151-b924734+18080f28-8914-11eb-8dcd-0242ac133")

#OR 

sales_report_data = {
    "host":"10.222.194.146",
    "port":"2389",
    "token":"01e947b6-8914-11eb-8dcd-0242ac130003",
    "secret":"78f45902-c9b8-4151-b924734+18080f28-8914-11eb-8dcd-0242ac133"
}
config.set("sale_report",sales_report_data,None)

```

The `Confo.set(config,field,value)` method creates a new configuration in the current namespace. This method 
can be used this way `Confo.set(config,field,value)`  or `Confo.set(config,dictionary,None)`, by replacing the value of `field` with a dictionary or list and replacing the last argument with None we can overload the default behaviour 
and set the configuration values directly. 

Now lets check all available configuration in the namespace:
```python
print(config.get_all())
#RESULTS: 
{'database': {'host': '127.0.0.1',
              'port': 5432,
              'username': 'kabelo',
              'password': 'confoRocks'},
 'sale_report': {'host': '10.222.194.146',
                 'port': '2389',
                 'token': '01e947b6-8914-11eb-8dcd-0242ac130003',
                 'secret': '78f45902-c9b8-4151-b924734+18080f28-8914-11eb-8dcd-0242ac133'}}
```

Perfect we can now consume configuration and metadata in a clean and decoupled way.Imagine if you have a 100 configurations and metadata
in a given namespace,the output dictionary from `Confo.get_all()` can be overwhelming to traverse. Lets find a more efficient way

```python
#Get the database host 
print(config.get("database","host"))

#RESULT
127.0.0.1

#get the database password 
print(config.get("database","confoRocks"))

#RESULTS:
confoRocks

#get the entire sale_report configuration
print(config.get("sale_report"))

#RESULT
{'host': '10.222.194.146',
 'port': '2389',
 'token': '01e947b6-8914-11eb-8dcd-0242ac130003',
 'secret': '78f45902-c9b8-4151-b924734+18080f28-8914-11eb-8dcd-0242ac133'}

#By ommiting the `field` argument `Confo.get()` returns the whole  configuration 

```
Lets assume we were able to programmatically retrieve a new secret and token for the sales report API. 
`Confo` allows us to update the configuration, by using `Confo.set()` to overwrite the old values. 

```python
new_token = "e9f2b59d-130d-4b61-b20c-94c73496655f"
new_secret = "cd58cb1d-22fc-4420-b5ab-6b67a565671d7d34f5e4-8916-11eb-8dcd"
config.set("sale_report","token",new_token)
config.set("sale_report","secret",new_secret)
print(config.get("sale_report"))

#RESULTS:
{'host': '10.222.194.146',
 'port': '2389',
 'token': 'e9f2b59d-130d-4b61-b20c-94c73496655f',
 'secret': 'cd58cb1d-22fc-4420-b5ab-6b67a565671d7d34f5e4-8916-11eb-8dcd'}

```
#### swapping namespaces
What if we now want to access the analytics's sales forecasting REST API. 

```python

#You can start by checking available namespaces 
print(config.get_namespaces())
#RESULTS: 
{'all_namespaces': ['sales', 'analytics'], 'current_namespace': 'sales'}

#Lets swap from sales to analytics.
config.use_namespaces("analytics")
print(config.get_namespaces())

#RESULTS: 

{'all_namespaces': ['sales', 'analytics'], 'current_namespace': 'analytics'}
```

After swapping namespaces check which configurations exist in analytics namespace

```python
config.get_all()

#RESULTS
{'api_one': {'host': '127.0.0.1',
             'port': 5782,
             'token': '2df228d6-890b-11eb-8dcd-0242ac130003',
             'secret': 'd51a8a7a-3286-4deb-8805-85f4528920aecfb49c0-a251-4657-87df-44996ea308ee'}}

config.get("api_one")

#RESULTS
{'host': '127.0.0.1',
 'port': 5782,
 'token': '2df228d6-890b-11eb-8dcd-0242ac130003',
 'secret': 'd51a8a7a-3286-4deb-8805-85f4528920aecfb49c0-a251-4657-87df-44996ea308ee'}

#Only `api_one` exists in the `analytics` namespace as expected
```
We have retrieved the `api_one` values lets go back to the sales namespace

```python
config.use_namespace("sales")
print(config.get_all())

#RESULTS 
{'database': {'host': '127.0.0.1',
              'port': 5432,
              'username': 'kabelo',
              'password': 'confoRocks'},
 'sale_report': {'host': '10.222.194.146',
                 'port': '2389',
                 'token': 'e9f2b59d-130d-4b61-b20c-94c73496655f',
                 'secret': 'cd58cb1d-22fc-4420-b5ab-6b67a565671d7d34f5e4-8916-11eb-8dcd'}}
```

Now if we were to open the `Configurations/` directory this is what I would find in the `sale` directory:

```
Configurations
        |___________analytics 
        |                |_________api_one.json 
        |____________sales
                       |___________database.json          
```
There is no file `Configurations/sales/sale_report.json` . The `sale_report` configuration only exists in memory. The
This allows the developer to explicitly decide when they want to persist the updated or new configuration as a 
result this helps the developer to handle cases where he creates session specific configurations, these should remain in
in memory and not be persisted.

#### persistence

`Confo` handles persistance at three levels :
```
backend level : This option persist the current state of all configuration in the current backend.
    |
    |namespace level: This option persist the current state of all configuration in the current namespace
         |
         | Configuration level: This option persists a specific configuration

```
##### backend level

```python
config.persist()
```
The code above will persist every configuration from all namespaces. 

##### namespace level

```python
config.persist(namespace="sales")
```

The above code will persist every configuration in the `sales` namespace

##### configuration level 

```python
config.persist(namespace="sales",config="sale_report")
```
The above code will persist the `sale_report` configuration only.If the configuration file already exists i will be updated.

2.2 ZooKeeper backend 

Lets assume our application is operating a very distributed environments. One of the main problems in distributed systems
is finding one source of truth for application state and configuration.ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services.
All of these kinds of services are used in some form or another by distributed applications.We use zookeeper as a backend
for `Confo` essentially abstracting away the complex zookeeper API. The advantage of using confo in this environment is that you get the same API 
when testing locally and when deploying on production.

Lets load a zookeeper backend 

```python
# Instantiate a ZOOKEEPER_BACKEND backend 
cred = {"zookeeper_host":"127.0.0.1","zookeeper_port":"2181",
        #if your zookeeper instance has password authentication we can also send 

        "zookeeper_user":"kabelo",
        "zookeeper_passwd":"confoRocks"
        }
config.load_backend(credentials=cred,name="zookeeper_backend",backend_type=BE.ZOOKEEPER_BACKEND )

print(config.get_backend())

#RESULTS:
{'all_backends': ['example_backend', 'zookeeper_backend'],
 'active_backend': 'example_backend'}

```

Lets activate the zookeeper backend.

```python
config.activate_backend("zookeeper_backend")
config.get_backends()

#RESULTS:

{'all_backends': ['zookeeper_backend', 'example_backend'],
 'active_backend': 'zookeeper_backend'}
```

##### Zookeeper quick overview
ZooKeeper allows distributed processes to coordinate with each other through a shared hierarchical 
name space of data registers (we call these registers znodes), much like a file system.
Unlike normal file systems ZooKeeper provides its clients with high throughput, low latency,
highly available, strictly ordered access to the znodes.
The performance aspects of ZooKeeper allow it to be used in large distributed systems.
The reliability aspects prevent it from becoming the single point of failure in big systems. 
Its strict ordering allows sophisticated synchronization primitives to be implemented at the client.

Znodes are analogous to files and directory at the same time. Because a Znode can have children Znodes like a directory can have subdirectories and files.
Also every znode can store data just like a file. `Confo` depends on a znode call `confo` which it will create automatically if it does not exist.
Then every znode which is a child of `confo` is a namespace so they will not be queried for any data.Then every child of a namespace znode is considered a
configuration znode and are expected to have json object stored within. Now imagine we have znodes `systemA` and `systemB` under the `confo` znode:

``` 
"/"                                                                          ->zookeeper root 
  |________"confo"                                                           -> confo root ("/confo")
            |_________"systemA"                                              -> namespace called "systemA" ("/confo/systemA")
            |             |__________"database"                              -> a configuration called "database" ("/confo/systemA/database")
            |                           |______________host: 127.0.0.1       -> a configuration field called "host"
            |                           |______________port: 3306 
            |                           |______________user: root 
            |                           |______________password: newpassword
            |                           |______________vendor: postgres 
            |
            |_____________"systemB"                                          -> namespace called "systemB" ("/confo/systemB")  
                            |__________"email"                               -> a configuration called "email" ("/confo/systemB/email")
                                           |___________ "port":587           -> a configuration field called "port"
                                           |___________ "smtp_server": "smtp.gmail.com"
                                           |___________ "sender_email":"confo@sambe.co.za"
                                           |___________ "password" :"ThisIsAStrongPasswordTrustMeItIs"            
                                        

```

Now lets build a python app that sends an email verification link to newly registered users.We decoupled configuration from actual code by using confo:

```python
from confo.Confo import Confo
import confo.Backends as BE
import smtplib, ssl
from sqlalchemy import create_engine

config = Confo()
cred = {"zookeeper_host":"127.0.0.1","zookeeper_port":"2181",

        }

config.load_backend(credentials=cred,name="zookeeper_backend",backend_type=BE.ZOOKEEPER_BACKEND )
config.active_backend("zookeeper_backend")
config.use_namespace("systemA")
def send_email(smtp_server,sender_email,receiver_email,password,port=587):
    # Create a secure SSL context
    context = ssl.create_default_context()
    # Try to log in to server and send email
    try:
        message= "Please click <a href=\"http://verification-link.com\">here</a> to verify your email"
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    except Exception as e:
            # Print any error messages to stdout
            print(e)
    finally:
        server.quit()
def build_data_url(database):
    url = database['vendor'] + '://' + database['user'] + ':' + database['password']
    url = url +'@' +database['host'] + ':' + database['port'] + '/' + database['db_name'] + '?driver=' + database['driver']
    return url
def build_engine(config):
    database_config = config.get('database')
    url = build_data_url(database_config)
    engine = create_engine(url)
    return engine
def mail_recipients(engine,config):
    smtp_server = config["smtp_server"]
    port= config["port"]
    sender_email = config["sender_email"]
    password= config["password"]
    with engine.connect() as connection:
        result = connection.execute("select email from users where verified=0")
    for row in result:
        sender_email(smtp_server=smtp_server,sender_email=sender_email,receiver_email=row['email'],password=password,port=port) 
        
engine = build_engine(config)
config.active_backend("systemB")
email_config = config.get("email")
mail_recipients(engine,email_config)

    

```

The script above shows a simple use case for a robust configuration manager.

