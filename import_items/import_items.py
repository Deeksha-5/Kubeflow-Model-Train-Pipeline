import argparse
from google.cloud import automl
from google.cloud import storage
from google.oauth2 import service_account

parser = argparse.ArgumentParser()
parser.add_argument("key", type=str, help="Service Account Key")
parser.add_argument("did", type=str, help="Dataset Id")
parser.add_argument("csv", type=str, help="GCS Path of CSV file")
args = parser.parse_args()

if len(vars(args)) == 3:
    if '=' in args.key:
        key = args.key.split('=')[-1]
    else:
        key = args.key
    if '=' in args.did:
        did = args.did.split('=')[-1]
    else:
        did = args.did
    if '=' in args.csv:
        csv = args.csv.split('=')[-1]
    else:
        csv = args.csv
    sclient = storage.Client()
    bucket_name = key.split('/')[2]
    blob_name = key.split('/')[3]
    bucket = sclient.get_bucket(bucket_name)
    blob = bucket.get_blob(blob_name)
    with open("/tmp/my-secure-file", "wb") as file_obj:
        blob.download_to_file(file_obj)
    credentials = service_account.Credentials.from_service_account_file('/tmp/my-secure-file')
    client = automl.AutoMlClient(credentials=credentials)
    gcs_source = automl.types.GcsSource(input_uris=[csv])
    input_config = automl.types.InputConfig(gcs_source=gcs_source)
    # input_config = {"gcs_source": {"input_uris": [CSV_DATASET]}}
    response = client.import_data(did, input_config)
    print("Data imported. {}".format(response.result()))
    with open('/tmp/data.txt', 'w') as dfile:
        dfile.write(did.split('/')[-1])
