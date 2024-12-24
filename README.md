### Welcome

To run activate the virtual env

source env/bin/activate

### Frontend Setup

pip install reflex  
reflex init  
reflex run  

### Backend configuration 

Create a .env file in the root of project 

add the following keys: 

mongo_uri = ***** 

  - to get the mongoURI click connect on the cluster and set the password to your user password in your approved user

Create an open AI key reference in your system: 
  - nano ~/.zshrc
  - paste in export OPENAI_API_KEY="your_api_key_here"
  - Control + X to exit → Y (for yes) → hit enter

To run a file on the backend from the root: python3 -m backend.prebuiltparsing.FILENAME 
