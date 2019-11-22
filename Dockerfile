#publicly available docker image "python with python 3.6.9" on docker hub will be pulled
FROM python:3.6.9

# creating directory pyuser in home folder in container (linux machine)
RUN mkdir /home/pyuser

# cd into created dir
RUN cd /home/pyuser

# clone repository
CMD git clone https://github.com/rodrigovilar/medieval-bank-python

# cd into repository
RUN cd medieval-bank-python

# running pip to install all requirements
CMD pip install -r requirements.txt

# running python to create database (It must be exec as a module or there will be import errors)
CMD python -m persistence.models

# running the test (Also as a module)
CMD python -m tests.test_service_attendant
