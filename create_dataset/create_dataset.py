import argparse
from google.cloud import automl
from google.cloud import storage
from google.oauth2 import service_account

parser = argparse.ArgumentParser()
parser.add_argument("key", type=str, help="Service Account Key")
parser.add_argument("pid", type=str, help="Project Id")
parser.add_argument("dname", type=str, help="Dataset Name")
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
    if '=' in args.dname:
        dname = args.dname.split('=')[-1]
    else:
        dname = args.dname
    sclient = storage.Client()
    bucket_name = key.split('/')[2]
    blob_name = key.split('/')[3]
    bucket = sclient.get_bucket(bucket_name)
    blob = bucket.get_blob(blob_name)
    with open("/tmp/my-secure-file", "wb") as file_obj:
        blob.download_to_file(file_obj)
    credentials = service_account.Credentials.from_service_account_file('/tmp/my-secure-file')
    client_options = {'api_endpoint': 'automl.googleapis.com:443'}
    client = automl.AutoMlClient(credentials=credentials, client_options=client_options)
    project_location = client.location_path(pid, 'us-central1')
    DATASET_NAME = dname
    dataset_metadata = automl.types.ImageClassificationDatasetMetadata(classification_type=automl.enums.ClassificationType.MULTICLASS)
    my_dataset = {"display_name": DATASET_NAME, "image_classification_dataset_metadata": dataset_metadata}
    response = client.create_dataset(project_location, my_dataset)
    created_dataset = response.result()
    print(created_dataset.name)
    with open('/tmp/dataset.txt', 'w') as dfile:
        dfile.write(created_dataset.name)
