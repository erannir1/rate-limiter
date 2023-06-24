# chuck-norris-jokes
Chuck Norris Jokes server

### Endpoints
**GET /joke**</br>
Get a Chuck Norris joke 

**Headers**
|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `Authorization` | required | string  | Your account authorization.                                                                     |
**Response**
```
{
    "id": "F6v0fEXeREek9FnF6_9k4A",
    "categories": ["some category"],
    "createdAt": "2020-01-05 13:42:25.352697",
    "joke": "Chuck Norris' first car was Optimus Prime."
}
```

In order to run a requst run one of the following servers(NodeJs\ Python) and you can use this request
```bash
curl --location --request GET 'http://localhost:8000/joke' \
--header 'Authorization: 1111-2222-3333'
```
*******

# Rate Limiter

The goal of the service is to create a rate limiter for the client's requests per second and per day.

## Run it

The repo contains Dockerfile and docker-compose setup for multiplatform local run.

```bash
cd path/to/project
docker-compose build --no-cache
docker-compose up -d
```
In order to list all the running containers
```bash
docker ps
```
Show the log of the service
```bash
docker logs -f rate-limiter
```


## Settings and ENVs

| ENV            | Description                  | Default                          |
|----------------|------------------------------|----------------------------------|
| DB_CONN_STR    | connection string to MongoDB | mongodb://localhost:27017/       |
| REDIS_HOST     | redis host string            | redis                            |
| REDIS_PORT     | redis port int               | 6379                             |
| REDIS_PASSWORD | password to the redis        | eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81 |


## How it works

The Rate Limiter Service works by allowing you to set and enforce rate limits for clients based on different plans.
It utilizes a combination of MongoDB and Redis to store and manage the necessary data.
When a request is made, the service checks the client's plan and retrieves the corresponding rate limits.
It then counts the number of requests made by the client per second and per day using Redis as a fast and efficient counter.
If the request count exceeds the defined limits, the service enforces the rate limit and blocks further requests from the client until the limit resets.
This ensures that clients adhere to the specified rate limits, preventing excessive usage and promoting fair resource allocation.

## Unit tests and linter
1. Run tests locally by running:
    ```bash
    python -m unittest discover -s rate_limiter.tools.tests -p "*_tests.py"
   ```

2. Linter:
    black
    flake8