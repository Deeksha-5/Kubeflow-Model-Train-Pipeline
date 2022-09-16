FROM python:3

ADD train_model.py /

RUN pip install argparse
RUN pip install google-cloud-automl
RUN pip install google-cloud-storage
RUN pip install google-auth

ENV key=''
ENV pid=''
ENV did=''
ENV mname=''
ENV nodehrs=''

CMD python3 train_model.py $key $pid $did $mname $nodehrs
