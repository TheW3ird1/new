FROM python:3.10-slim-buster

WORKDIR /app

# Install build dependencies (make, gcc, g++, other essential tools)
RUN apt-get update && \
    apt-get install -y --no-install-recommends make gcc g++

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "main.py"]

#This is the Dockerfile that will be used to build the image. It uses the python:3.10-slim-buster image as the base image. The image is then updated and essential tools are installed. The requirements.txt file is copied to the /app directory and the dependencies are installed. The rest of the files are copied to the /app directory. The container listens on port 8080 and the main.py script is executed when the container is started.