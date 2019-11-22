#publicly available docker image "python with python 3.6.9" on docker hub will be pulled
FROM python:3.6.9

# creating necessary folders in container (linux machine)
RUN mkdir /home/pyuser/

RUN mkdir /home/pyuser/medieval-bank-python

# clone repository
RUN git clone https://github.com/rodrigovilar/medieval-bank-python /home/pyuser/medieval-bank-python/

# running pip to install all requirements
RUN pip install -r /home/pyuser/medieval-bank-python/requirements.txt

