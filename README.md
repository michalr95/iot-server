## iot-proj
Includes:
- Flask server for processing sensor readings, smart lights discovery and management, REST API, and handling
custom Alexa skill requests
- Mongo database, used by the Flask server
- INO scripts for reading sensor values and sending data to the Flask server
- Scripts for environment setup

### Docker
Create a docker network for components to communicate with  
`docker network create iot_net`  
Build the Flask application image using  
`docker build -t iotproj:<TAG> .`  
Run container with  
`docker run -d --name iot-app --net iot-net -p <HOST_PORT>:<CONTAINER_PORT> iotproj:<TAG>
`  
Override environment variables with `-e` e.g. `-e APP_PORT=5001`  

Similarly, build mongo database with  
`docker build -t iot-db:<TAG> .`  
And run container with  
`docker run -d --name iot-db --net iot-net iot-db:<TAG>`  
Override defaults if needed  

**Or** do it all in one step with  
`docker-compose up --build`  
Note that compose is configured to mount volume to a directory on host's filesystem such that app logs are available from the host.
Make sure that directory may be shared with Linux containers - https://docs.docker.com/docker-for-mac/#file-sharing

Common issues:
- Flask server docker build fails at `pip install -r requirements.txt` step due to timeout - add http_proxy and https_proxy in Dockerfile ENV entries and set appropriately
