# db_api
This is a sample django rest api project. This app provides only one api and it only accepts POST method.
Travis CI has been used to manage the CI/CD pipeline and the whole project is deployed to heroku cloud server.

## Run the project locally
1. Go inside the project's root directory
2. Run the app with the following command:
```
docker-compose up --
```
To test the api, use postman.
The API is http://localhost:8000/analyze. Use post method and in body, give the payload like this:
```
{"text": "hello 2 times  "}
```

The response for this payload will be:
```
{
    "textLength": {
        "withSpaces": 15,
        "withoutSpaces": 11
    },
    "wordCount": 3,
    "characterCount": [
        {
            "e": 2
        },
        {
            "h": 1
        },
        {
            "i": 1
        },
        {
            "l": 2
        },
        {
            "m": 1
        },
        {
            "o": 1
        },
        {
            "s": 1
        },
        {
            "t": 1
        }
    ]
}
```
## Test case
To run the test cases in docker container, just run the following command in terminal (inside project root directory)
```
docker-compose run app sh -c "python manage.py test && flake8"
```

N.B. No database has been used in this project. To check code syntax and provide instructions on how to clean it, flake8
linting tool has been used.

## CI/CD
The following steps are applied to build the CI/CD pipeline.
1. Commit to the project repo.
2. Travis ci will run the test first.
3. After successful test run, Travis CI build image and deploy the image to docker hub account and registry.heroku.com.
4. Finally the project is deployed into heroku cloud.

The build image can be found in docker hub account (https://hub.docker.com/r/rupak08012/analyze_string/tags).
The API in heroku is available in this link: https://dream-broker-api.herokuapp.com/analyze