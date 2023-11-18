# Setup project on local
```bash
mkdir var

# NOTE: create virtual environemnt
python3.11 -m venv var/env

# NOTE: install requirements
pip install -r src/requirements.txt
```

# Run the application
## VSCode launch.json
Easier for the user would be to create `.vscode/launch.json` launch configuration files in the project's root directory which would take care to run the backend & worker w/ VSCode debugger.

### Windows
- ***User must replace <REDIS_CS> & <MONGODB_CS> values w/ real connection strings***
- ***For windows it is required for python RQ to use worker class `worker.workers.BasicWindowsWorker`, which is done using `-w` flag in the RQ worker command***

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "FastAPI Server",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "cwd": "${workspaceFolder}/src",
            "args": [
                "main:app",
                "--reload"
            ],
            "env": {
                "MONGODB_CS": "<MONGODB_CS>",
                "REDIS_CS": "<REDIS_CS>"
            },
            "jinja": true,
            "justMyCode": true
        },
        {
            "name": "RQ Worker",
            "type": "python",
            "request": "launch",
            "module": "rq.cli",
            "cwd": "${workspaceFolder}/src",
            "args": [
                "worker",
                "-w",
                "worker.workers.BasicWindowsWorker",
                "--url",
                "<REDIS_CS>"
            ],
            "env": {
                "MONGODB_CS": "<MONGODB_CS>",
                "REDIS_CS": "<REDIS_CS>"
            },
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```

# Setup services
## MongoDB
### MongoDB Atlas
Easier for the user would be to setup the [Atlas](https://account.mongodb.com/account/login?nds=true) database & use it.

### Docker
To run the database using docker use the command below or Docker Desktop (for windows)

```bash
# TODO: go to the project root & make sure you have directory named "var"

# NOTE: pull the image
docker pull mongo:latest

# NOTE: run the image
docker run -ti -p 27017:27017 -v ./var/mongodb:/data/db mongo:latest

# NOTE: MONGO_CS=mongodb://localhost:27017
```

## Redis
### Redis Cloud
Easier for the user would be to setup the [Redis labs](https://app.redislabs.com/#/) database & use it.

### Docker
To trun the redis using docker use the command below or Docker Desktop (for windows)

```bash
# NOTE: pull the image
docker pull redis:alpine

# NOTE: run the image
docker run -ti redis:alpine

# NOTE: REDIS_CS=redis://localhost:6379
```
