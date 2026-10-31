#Use the offical Python runtime image as your baseline kitchen
FROM python:3.11-slim 

#Establish an active working directory inside the container
WORKDIR /app

#Copy our local auditor.py script into the container workspace
COPY persistent_auditor.py .  

#Define the execution command to run when the container 
CMD ["python", "persistent_auditor.py"]