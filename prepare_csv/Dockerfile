FROM python:3

ADD prepare_csv.py /

RUN pip install argparse
RUN pip install google-cloud-storage

ENV key=''
ENV data_bucket=''
ENV dname=''

CMD python3 prepare_csv.py $key $data_bucket $dname
