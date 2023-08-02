# Extending the App

!!! warning "Developer Note - Remove Me!"
    Information on how to extend the App functionality.

Extending the application is welcome, however it is best to open an issue first, to ensure that a PR would be accepted and makes sense in terms of features and design.

## Developing Against Secrets Backends

### AWS Secrets Manager

This assumes you are logged into the AWS Console.

- Navigate to AWS Console
- Navigate to AWS Secrets Manager
- Click "Store a new secret"
  - Select “Other type of secrets”
  - Use Secret key/value
  - Enter `hello=world`
  - Use "DefaultEncryptionKey" for now
  - Click "Next"
  - Under "Secret name" fill out `hello`
  - Click "Next"
  - Under "Configure automatic rotation"
    - Leave it as "Disable automatic rotation"
  - On "Store a new secret"
    - Copy the sample code (see below)
  - Click "Store"
- END

#### Install the AWS CLI

Next, install the [AWS CLI](https://aws.amazon.com/cli/).

On MacOS, this can be done using `brew install awscli`:

```
brew install awscli
```

On Linux, you will need to run a `curl` command (This assumes x86. Please see the docs for [AWS CLI on
Linux](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html) for ARM and other options):

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

#### Configure the AWS CLI

After installing the AWS CLI, you will need to configure it for authentication.

You may use an existing AWS access key or create a new one. For these instructions we cover the need to create a new access key that can be used for this.

- Navigate to AWS Console
- Click your username
  - Click "My security credentials"
  - Click "create access key"
- Save your "Access key ID" and "Secret access key" for use when configuring the AWS CLI

Now configure the CLI:

- Run `aws configure`
- Enter your credentials from above
- Choose your region
- Use output format: `json`

Example:

```no-highlight
$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-east-2
Default output format [None]: json
```

Now you are ready to use the sample code to retrieve your secret from AWS Secrets Manager!

#### Sample Code

Make sure that the `boto3` client is installed:

```no-highlight
poetry install --extras aws
```

Next, save this as `aws_secrets.py`:

```python
# Use this code snippet in your app.
# If you need more information about configurations or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developers/getting-started/python/

import boto3
import base64
from botocore.exceptions import ClientError


def get_secret():

    secret_name = "hello"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])

    # Your code goes here.

# ^ Above was generated by AWS.

# This was added by us so you can run this as a script:
if __name__ == "__main__":
    secret = get_secret()
    print(f"Secret = {secret}")
```

Run it with `python aws_secrets.py`:

```
$ python aws_secrets.py
Secret = {"hello":"world"}.
```

Note that this blob is JSON and will also need to be decoded if you want to extract the value.

### HashiCorp Vault

Make sure that the `hvac` client is installed:

```no-highlight
poetry install --extras hashicorp
```
