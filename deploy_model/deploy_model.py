import argparse
from google.cloud import automl
from google.cloud import storage
from google.oauth2 import service_account

parser = argparse.ArgumentParser()
parser.add_argument("key", type=str, help="Service Account Key")
parser.add_argument("pid", type=str, help="Project Id")
parser.add_argument("mid", type=str, help="Model Id")
args = parser.parse_args()

if len(vars(args)) == 3:
    if '=' in args.key:
        key = args.key.split('=')[-1]
    else:
        key = args.key
    if '=' in args.pid:
        pid = args.pid.split('=')[-1]
    else:
        pid = args.pid
    if '=' in args.mid:
        mid = args.mid.split('=')[-1]
    else:
        mid = args.mid
    sclient = storage.Client()
    bucket_name = key.split('/')[2]
    blob_name = key.split('/')[3]
    bucket = sclient.get_bucket(bucket_name)
    blob = bucket.get_blob(blob_name)
    with open("/tmp/my-secure-file", "wb") as file_obj:
        blob.download_to_file(file_obj)
    credentials = service_account.Credentials.from_service_account_file('/tmp/my-secure-file')
    client = automl.AutoMlClient(credentials=credentials)
    mid = mid.split('/')[-1]
    model_full_id = client.model_path(pid, "us-central1", mid)
    response = client.deploy_model(model_full_id)
    print("Model deployment finished. {}".format(response.result()))