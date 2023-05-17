ARG BASEIMG=python:3.8.16-buster
FROM ${BASEIMG}

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y python3-pip
	
# Java
# Install OpenJDK-8
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get install -y ant && \
    apt-get clean;

# Fix certificate issues
RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;

# Setup JAVA_HOME -- useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME
# End Java

RUN pip3 install numpy==1.20.2

# copy project
COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install libgl1-mesa-glx -y    

# copy project
COPY . /usr/src/app/

EXPOSE 8000

RUN chmod +x ./start.sh
RUN chmod -R +x bioformats 

CMD ["./start.sh"]