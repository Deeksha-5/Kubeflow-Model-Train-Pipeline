FROM python:3

ADD import_items.py /

RUN pip install argparse
RUN pip install google-cloud-automl
RUN pip install google-cloud-storage
RUN pip install google-auth

ENV key=''
ENV did=''
ENV csv=''

CMD python3 import_items.py $key $did $csv