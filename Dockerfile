FROM python:3.7-alpine
WORKDIR /opt/checker
ADD requirements.txt /opt/checker/requirements.txt
RUN pip install -r requirements.txt

ADD checker.py /opt/checker/checker.py
CMD python -u checker.py
