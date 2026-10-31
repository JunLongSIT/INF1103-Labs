#Use the offical Python runtime image as your baseline kitchen
FROM python:3.11-slim 

#Establish an active working directory inside the container
WORKDIR /app

#Copy our local inventory_manager.py script into the container workspace
COPY inventory_manager.py .  

#Define the execution command to run when the container 
CMD ["python", "inventory_manager.py"]