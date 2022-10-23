# dataplane-python-package
The data engineering library to build robust, reliable and on time data pipelines in Python.

### To use with Dataplane Data Platform
Install Python Package on Dataplane: https://learn.dataplane.app/installing-python-packages
Recipes to use Dataplane Python Package: https://recipes.dataplane.app/office-365/sharepoint-api

### Run tests in repo root
```shell
pytest -s
```

### For a specific test
```shell
pytest -s src/dataplane/data_storage/test_sharepoint_upload.py
pytest -s -k test_sharepoint_upload.py
```

### S3 / Minio for testing in VS code devcontainers
* Go to http://localhost:9011
* Login with: username: admin and password: hello123
* bucket: dataplanebucket
