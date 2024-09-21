FROM python:latest

WORKDIR /app


# RUN apt-get update && apt-get install libffi-dev \
#                         libjpeg-dev \
#                         zlib1g-dev \
#                         build-essential \
#                         libssl-dev 

# RUN apt-get install \
#     build-essential \
#     libssl-dev \ 
#     libffi-dev  

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8005
USER root

RUN ["chmod", "+x", "/app/entrypoint.sh"]
ENTRYPOINT ["bash", "/app/entrypoint.sh"]