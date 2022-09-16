FROM python:3

ADD deploy_model.py /

RUN pip install argparse
RUN pip install google-cloud-automl
RUN pip install google-cloud-storage
RUN pip install google-auth

ENV key=''
ENV pid=''
ENV mid=''

CMD python3 deploy_model.py $key $pid $mid
