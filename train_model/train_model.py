import argparse
import time
from google.cloud import automl
from google.cloud import storage
from google.oauth2 import service_account

parser = argparse.ArgumentParser()
parser.add_argument("key", type=str, help="Service Account Key")
parser.add_argument("pid", type=str, help="Project Id")
parser.add_argument("did", type=str, help="Dataset Id")
parser.add_argument("mname", type=str, help="Model Name")
parser.add_argument("nodehrs", type=str, help="Node Hours for Model Training")
args = parser.parse_args()

if len(vars(args)) == 5:
    if '=' in args.key:
        key = args.key.split('=')[-1]
    else:
        key = args.key
    if '=' in args.pid:
        pid = args.pid.split('=')[-1]
    else:
        pid = args.pid
    if '=' in args.did:
        did = args.did.split('=')[-1]
    else:
        did = args.did
    if '=' in args.mname:
        mname = args.mname.split('=')[-1]
    else:
        mname = args.mname
    if '=' in args.nodehrs:
        nodehrs = args.nodehrs.split('=')[-1]
    else:
        nodehrs = args.nodehrs
    sclient = storage.Client()
    bucket_name = key.split('/')[2]
    blob_name = key.split('/')[3]
    bucket = sclient.get_bucket(bucket_name)
    blob = bucket.get_blob(blob_name)
    with open("/tmp/my-secure-file", "wb") as file_obj:
        blob.download_to_file(file_obj)
    credentials = service_account.Credentials.from_service_account_file('/tmp/my-secure-file')
    client = automl.AutoMlClient(credentials=credentials)
    project_location = client.location_path(pid, 'us-central1')
    nodehrs = int(nodehrs)
    metadata = automl.types.ImageClassificationModelMetadata(train_budget_milli_node_hours=nodehrs)
    model = automl.types.Model(display_name=mname, dataset_id=did, image_classification_model_metadata=metadata)
    response = client.create_model(project_location, model)
    print("Training operation name: {}".format(response.operation.name))
    print("Training started...")
    operation_full_id = response.operation.name
    train_done = False
    while (train_done is False):
        response = client.transport._operations_client.get_operation(operation_full_id)
        time.sleep(600)
        train_done = response.done
    mid = str(response.response.value, 'utf-8')
    with open('/tmp/model.txt', 'w') as mfile:
        mfile.write(mid)
