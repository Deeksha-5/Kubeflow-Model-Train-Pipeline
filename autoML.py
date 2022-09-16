import kfp
from kfp import dsl
from kfp.components import func_to_container_op
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('./pipeline-key.json')

PROJECT_ID = 'MY_PROJECT_ID'
COMPUTE_REGION = 'MY_COMPUTE_REGION'


@func_to_container_op
def create_dataset(Dname):
    import subprocess

    def install(name):
        subprocess.call(['pip', 'install', name])
    install('google-cloud-automl')
    import google.cloud.automl as automl
    client = automl.AutoMlClient(credentials=credentials)
    project_location = client.location_path(PROJECT_ID, COMPUTE_REGION)
    DATASET_NAME = Dname
    dataset_metadata = {}
    my_dataset = {"display_name": DATASET_NAME, "image_object_detection_dataset_metadata": dataset_metadata, }
    response = client.create_dataset(project_location, my_dataset)
    print("Dataset name: {}".format(response.name))
    print("Dataset id: {}".format(response.name.split("/")[-1]))
    print("Dataset display name: {}".format(response.display_name))
    print("Image classification dataset metadata:")
    print("\t{}".format(response.image_classification_dataset_metadata))
    print("Dataset example count: {}".format(response.example_count))
    dataset_id = response.name.split("/")[-1]
    print(type(dataset_id))
    return dataset_id


@func_to_container_op
def import_items(Id, url):
    import subprocess

    def install(name):
        subprocess.call(['pip', 'install', name])
    install('google-cloud-automl')
    import google.cloud.automl as automl
    client = automl.AutoMlClient(credentials=credentials)
    dataset_full_id = client.dataset_path(PROJECT_ID, COMPUTE_REGION, Id)
    CSV_DATASET = url
    input_config = {"gcs_source": {"input_uris": [CSV_DATASET]}}
    response = client.import_data(dataset_full_id, input_config)
    print("Data imported. {}".format(response.result()))


@func_to_container_op
def train_model(NAME, did):
    import subprocess

    def install(name):
        subprocess.call(['pip', 'install', name])
    install('google-cloud-automl')
    import google.cloud.automl as automl
    client = automl.AutoMlClient(credentials=credentials)
    project_location = client.location_path(PROJECT_ID, COMPUTE_REGION)
    MODEL_NAME = NAME
    my_model = {"display_name": MODEL_NAME, "dataset_id": did, "image_object_detection_model_metadata": {}}
    response = client.create_model(project_location, my_model)
    print("Training operation name: {}".format(response.operation.name))
    print("Training done. {}".format(response.result()))
    model_id = response.result().name.split("/")[-1]
    print(model_id)


@dsl.pipeline(
    name='AutoML Vision pipeline',
    description='A pipeline with AutoML Image Classification model training \
    steps.'
)
def sequential_pipeline(dname='NewDataset', url='gs://ml-pipeline/test.csv', mname='NewModel'):
    did = create_dataset(dname)
    import_items(did, url)
    train_model(mname, did)


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(sequential_pipeline, __file__ + '.tar.gz')
