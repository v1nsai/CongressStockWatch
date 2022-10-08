# Extract Load Transform (later) Pipeline

## Installation
Only works on Linux and probably Mac

```
# Init and bring up the Airflow Docker services
docker-compose up airflow-init
docker-compose up -d

# Install python packages on containers that need it them
chmod +x install_dependencies
./install_dependencies
```

### Running
The docker-compose file currently sets the webserver to listen on port 8080. If you set it up on the same computer you're currently using, you can just go to [localhost:8080](localhost:8080) in your browser.  Otherwise you'll need to replace `localhost` with the IP address of your server.