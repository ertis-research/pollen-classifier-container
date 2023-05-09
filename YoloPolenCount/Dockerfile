ARG BASEIMG=python:3.8.16-buster
FROM ${BASEIMG}

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install libgl1-mesa-glx -y

# copy project
COPY . /usr/src/app/

EXPOSE 8530

RUN chmod +x ./start.sh
CMD ["./start.sh"]