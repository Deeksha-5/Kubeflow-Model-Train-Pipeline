import argparse
from google.cloud import storage
import csv

parser = argparse.ArgumentParser()
parser.add_argument("key", type=str, help="GCS path of key file")
parser.add_argument("data_bucket", type=str, help="GCS path")
parser.add_argument("dname", type=str, help="CSV Dataset Name")
args = parser.parse_args()

if len(vars(args)) == 3:
    if '=' in args.key:
        key = args.key.split('=')[-1]
    else:
        key = args.key
    if '=' in args.data_bucket:
        data_bucket = args.data_bucket.split('=')[-1]
    else:
        data_bucket = args.data_bucket
    if '=' in args.dname:
        dname = args.dname.split('=')[-1]
    else:
        dname = args.dname
    url = data_bucket
    if url[-1] != '/':
        url = url+'/'
    sclient = storage.Client()
    bucket_name = url.split('/')[2]
    bucket = sclient.get_bucket(bucket_name)
    blobs = sclient.list_blobs(bucket)
    dname = dname+'.csv'
    with open(dname, 'w', newline='') as wfile:
        for blob in blobs:
            if blob.name[-1] != '/':
                uri = url + blob.name
                label = blob.name.split('/')[0]
                writer = csv.writer(wfile)
                writer.writerow([uri, label])
    with open(dname, 'r', newline='') as rfile:
        key_bucket_name = key.split('/')[2]
        key_bucket = sclient.get_bucket(key_bucket_name)
        key_blob = storage.Blob(dname, key_bucket)
        key_blob.upload_from_file(rfile)
        setname = 'gs://' + key_bucket_name + '/' + key_blob.name
    with open('/tmp/path.txt', 'w') as pfile:
        pfile.write(setname)
