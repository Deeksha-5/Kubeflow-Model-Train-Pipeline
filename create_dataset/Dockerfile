FROM python:3

ADD create_dataset.py /

RUN pip install argparse
RUN pip install google-cloud-automl
RUN pip install google-cloud-storage
RUN pip install google-auth

ENV pid='' 
ENV dname=''
ENV key='' 

CMD python3 create_dataset.py $key $pid $dname