import boto3


def file_to_s3(profile='', region='', file_object=None, bucket_name='', object_key='', s3_ExtraArgs={}):
  '''
  Upload file_object of type Bytes to S3.

  Args:
    profile (str):
      Name of awscli profile to be used.
    region (str):
      Name of AWS region in which the S3 bucket resides.
    file_object (Bytes):
      file_object to upload to S3.
    bucket_name (str):
      Name of bucket in which to upload file_object.
    object_key (str):
      Name to be given to the uploaded file_object. Known as a key in S3 documentation.
    s3_ExtraArgs (dict):
      Additional S3 arguments to add to the S3 API request. E.g. ACL

    Examples:
      - ('nse-ops', 'us-west-2', io.BytesIO(public_key), 'nse-ops-us-west-2-tenable-public-keys-bucket', 'file_name', {'ACL': 'public-read'})

  Returns:
    None

  Examples:
    - file_to_s3('nse-ops', 'us-west-2', io.BytesIO(public_key), 'nse-ops-us-west-2-tenable-public-keys-bucket', 'file_name', {'ACL': 'public-read'})
  '''
  session = boto3.Session(profile_name=profile)  # need this if wanting to use an awscli profile
  s3 = session.client('s3', region_name=region)
  s3.upload_fileobj(file_object, bucket_name, object_key, ExtraArgs=s3_ExtraArgs)