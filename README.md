## REST-API WITH FLASK

So here it is. A Python Flask API with real endpoints. And some JWT authentication security.

```
flask run
```

### TO RUN LOCALLY RUN DOCKER-FILE:
```
docker run -dp 5005:5000 -w /app -v "$(pwd):/app" IMAGE_NAME sh -c "flask run --host 0.0.0.0"
```

Replace the IMAGE_NAME with the DockerImage file-name.

**Don't forget to create the .env file and add your DATABASEURL**

When it is running, you can open the local swagger file with this link to see all the endpoints:
[Swagger Stuf](localhost:5005/swagger-ui)