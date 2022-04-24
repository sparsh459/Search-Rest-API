This repository is for a searchAPI written in django framework of python

## Description
This is a Django REST API service

### Prerequisites
This project requires Docker and docker-compose

See the [Docker website](http://www.docker.io/gettingstarted/#h_installation) for installation instructions.

To install docker-compose do ```pip install docker-compose``` 

#### To run development server
1. Build the docker images 
    ```docker-compose build```
2. Run the containers in background ```docker-compose up -d```
3. Access the application at [http://0.0.0.0:8000/
](http://0.0.0.0:8000)
4. To stop the containers do ```docker-compose down```

