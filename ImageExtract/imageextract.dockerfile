FROM python:3.9.7-bullseye

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

RUN pip3 install \
    numpy \
    python-bioformats \
    typer

WORKDIR /usr/local/src/
COPY . /usr/local/src/

ENTRYPOINT ["python", "imageextract.py"]