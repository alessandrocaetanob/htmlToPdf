# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:4-python3.11-appservice
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

ARG DEBIAN_FRONTEND=noninteractive 

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

RUN apt-get update -qq && apt-get install -y wkhtmltopdf \
    && apt-get clean \ 
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p -m 0700 /run/root/wkhtmltopdf

ENV XDG_RUNTIME_DIR=/run/root/wkhtmltopdf

COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY . /home/site/wwwroot

EXPOSE 80
