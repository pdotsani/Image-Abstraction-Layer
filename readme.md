# FCC Image Abstraction Layer  
  
## Summary  
A python based application that allows users to perform an image search with a return of JSON. History of past searches can also be retrieved as well.  
  
Two endpoints are available:
- `/imagesearch/<query>`: perform image search based on query  
- `/history`: query the history of searches  
  
## Setup  
Configuration was done using virtualenv. Dependencies are in `requirements.txt` Running on localserver requires a config file called `CONFIG_FILE.py` with the following enviornmental variables:
  
- GOOGLE_AUTH: "google auth key for custom search"
- GOOGLE_SEARCH_ENGINE: "engine key with image search enabled"  
  
For deployment, you must create an instance of [mlab](mlab.com). Also, the following enviornmental variables must be declared:  
  
- MONGODB_NAME
- MONGODB_HOST
- MONGODB_PORT
- MONGODB_USER
- MONGODB_PASS
- GOOGLE_AUTH
- GOOGLE_SEARCH_ENGINE  
  
## Demo  
To view the demo, visit https://fcc-img-abstraction-layer.herokuapp.com