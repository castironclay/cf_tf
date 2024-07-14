import boto3
import yaml

def read_creds_file():
    with open("cf_config.yaml", "r") as creds_file:
        all_creds = yaml.safe_load(creds_file)

    return all_creds

creds = read_creds_file()

def upload_file(file_contents: str) -> str:
    s3 = boto3.client(
            service_name ="s3",
            endpoint_url = creds.get('r2_endpoint'),
            aws_access_key_id = creds.get('r2_access_key'),
            aws_secret_access_key = creds.get('r2_secret_key'),
            region_name="auto"
    )

    s3.put_object(
        Body=file_contents.encode(),
        Bucket=creds.get('r2_bucket'),
        Key='objectkey',
    )

    response = s3.generate_presigned_url('get_object', Params={'Bucket': 'zerotrust', 'Key': 'objectkey'}, ExpiresIn=600)

    print(f"{response}")
