#RAGProject
by: Abdallah Ahmed & Dhruv Oza  My Github ID (AbdallahAhmed8102): #167634173 Partners  Github ID (Dhruv-Oza): #181366697

RAG Model Steps:

Pre-Step. Set up Docker and used docker compose file.

Step 1. MongoDB (For Storing Documentation & Information)

- Storing information grabbed from Gituhub of:
    ros2 robotics middleware subdomain.
    nav2 navigation subdomain.
    movit2 motion planning subdomain.
    gazebo simulation subdomain
Step 2. Generated Embeddings & Vectorized data using Qdrant

- Used a HuggingFace Model all-MiniLM-L6-v2 to help create working responses.
- Generated Embeddings to help format the data within MongoDB in a way that would help Qdrat vectorize the data
- Transfered Embeddings from MongoDB by setting up its specific UUID and sent it over to Qdrant
Step 3. Used ClearML and created a file to integrate it into the program

- Used ClearML to help understand process and debug code
Step 4. Querying the code

- Used a special distro of GPT-2 to help create responses which is called distilgpt2 which lets us access a working english language model without authentication.
Files that were created:

Github_Data.py
Generate_Embeddings.py
Transfer_Embeddings.py
Querying_Qdrant.py
Integrating_Language_Gen_Model.py
clearml_Integration.py


