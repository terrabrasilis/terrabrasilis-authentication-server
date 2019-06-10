# Authentication with JWT

Implements one Authentication API based in PyJWT and Flask (version specifically for docker swarm).

Inspired by: https://github.com/realpython/flask-jwt-auth

# Docker file to deploy

This docker is prepared to run a Flesk server used in this project. No has PostgreSQL database service. You need your our SGDB service.

### Prerequisites

Your environment to run this docker is the Docker Engine and a PostgreSQL service.

- [Docker](https://docs.docker.com/install/)
- [PostgreSQL](https://www.postgresql.org/)

### Installing

#### Database

Prepare your database using the db.sql script from api/storage_module/config/db.sql

#### Build your image

You may change the image version before building using the tag_version appended in image name. \
The command line template is: *docker build -t <image_name>:<tag_version> .*

Run these commands to build your image:

```sh
git clone https://github.com/andre-carvalho/AuthenticationServer.git

docker build -t auth-api-server:v1 -f deploy/Dockerfile .
```

#### Run the container
[Only works for docker swarm]
Just run the image and your service is starting. Note that command use the set env parameters to send the database connection information for API service.

* --env HOST=&lt;your ip or hostname&gt;
* --env PORT=&lt;port&gt;
* --env DBUSER=&lt;username&gt;
* --env DBPASS=&lt;secret&gt;
* --env DBNAME=&lt;database name&gt;


```sh
docker run -p 5000:5000 --env HOST=IP --env PORT=5432 \
--env DBNAME=auth_api --env DBUSER=postgres \
--env DBPASS=postgres -d auth-api-server:v1
```

You may run with less parameters, like this:

```sh
docker run -p 5000:5000 --env HOST=IP --env DBNAME=dbname --env DBPASS=postgres -d auth-api-server:v1
```

Or run docker accessing the terminal and set your connection informations.

To procced that, you may run the docker:

```sh
docker run -it auth-api-server:v1 sh
```
And just run these commands to create the storage_module/config/db.cfg file setting your values:
```sh
echo "[database]" >> storage_module/config/db.cfg
echo "host=localhost" >> storage_module/config/db.cfg
echo "port=5432" >> storage_module/config/db.cfg
echo "database=auth_api" >> storage_module/config/db.cfg
echo "user=postgres" >> storage_module/config/db.cfg
echo "password=postgres" >> storage_module/config/db.cfg
```

You may use the docker compose to that task:

The compose file is in deploy/ directory.
*deploy/docker-compose.yml*


Note: see this link to read about docker-compose: https://docs.docker.com/compose/overview/

```sh
# to run compose
docker-compose -f deploy/docker-compose.yml up -d

# to stop compose
docker-compose -f deploy/docker-compose.yml down
```

### Test

After run the server, use the command line to test:
```
curl http://127.0.0.1:5000/register -d '{"email": "afacarvalho@yahoo.com.br","password": "secret_word"}' -v -H "Content-Type: application/json"
```
or use [Postman](https://www.getpostman.com/downloads/).