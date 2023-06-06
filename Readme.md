# AuthService
AuthService is a RESTful web service built with FastAPI that offers account creation and verification functionality.

## Running the service locally
- Install python 3.9
- Install peotry module using pip command: pip install poetry
- Run "poetry install --no-root"
- Execute uvicorn src.app.main:app --host 0.0.0.0 --port 8087
- OpenapiUrl: http://localhost:8087/docs

## Running the service from docker hub image
 - Make sure docker desktop is installed
 - In root directory, execute below command:
      docker-compose -f dockerhub-compose.yml up --build

## Running the service locally using docker contianer
 - Make sure docker desktop is installed
 - In root directory, execute below command:
      docker-compose up --build

## API's supported
- HEALTH API:
  - GET /health : To get service health
- User API's:
  - POST user/create : To create user account
  - POST user/verify  : To verify user account


## Linter command
pylama -o setup.cfg src

## Unit test command
pytest

## API document:
 - Start the service by any of the method mentioned above
 - From the browser open: http://localhost:8087/docs
 - The page will display all the supported API's and format to use them
 
 # API document without running the service
  - For offline doc reffer to openapi.yml file
  - For documentation with UI, go swagger editor, https://editor.swagger.io/
    Click on "File"
    Select "Import file"
    Select the file "openapi.yml"
    
    ![image](https://github.com/gotcha1/AuthService/assets/51114133/beeee3ae-6832-41a3-9d69-c91fd9888f07)

 
