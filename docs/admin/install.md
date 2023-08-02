# Installing the App in Nautobot

Here you will find detailed instructions on how to **install** and **configure** the App within your Nautobot environment.

## Prerequisites

- The plugin is compatible with Nautobot 1.4.0 and higher.
- Databases supported: PostgreSQL, MySQL

!!! note
    Please check the [dedicated page](compatibility_matrix.md) for a full compatibility matrix and the deprecation policy.

### Access Requirements

## Install Guide

!!! note
    Before you proceed, you must have **at least one** of the dependent libaries installed as detailed above.

!!! warning
    Please do not enable this plugin until you are able to install the dependencies, as it will block Nautobot from starting.

!!! note
    Plugins can be installed manually or using Python's `pip`. See the [nautobot documentation](https://nautobot.readthedocs.io/en/latest/plugins/#install-the-package) for more details. The pip package name for this plugin is [`nautobot-secrets-providers`](https://pypi.org/project/nautobot-secrets-providers/).

The plugin is available as a Python package via PyPI and can be installed with `pip`:

```shell
pip install nautobot-secrets-providers
```

To ensure Nautobot's Secrets Providers Plugin is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the Nautobot root directory (alongside `requirements.txt`) and list the `nautobot-secrets-providers` package:

```shell
echo nautobot-secrets-providers >> local_requirements.txt
```

Once installed, the plugin needs to be enabled in your Nautobot configuration. The following block of code below shows the additional configuration required to be added to your `nautobot_config.py` file:

- Append `"nautobot_secrets_providers"` to the `PLUGINS` list.
- Append the `"nautobot_secrets_providers"` dictionary to the `PLUGINS_CONFIG` dictionary and override any defaults.

```python
# In your nautobot_config.py
PLUGINS = ["nautobot_secrets_providers"]

# PLUGINS_CONFIG = {
#   "nautobot_secrets_providers": {
#     ADD YOUR SETTINGS HERE
#   }
# }
```

Once the Nautobot configuration is updated, run the Post Upgrade command (`nautobot-server post_upgrade`) to run migrations and clear any cache:

```shell
nautobot-server post_upgrade
```

Then restart (if necessary) the Nautobot services which may include:

- Nautobot
- Nautobot Workers
- Nautobot Scheduler

```shell
sudo systemctl restart nautobot nautobot-worker nautobot-scheduler
```

### AWS

#### Authentication

No configuration is needed within Nautobot for this provider to operate. Instead you must provide [AWS credentials in one of the methods supported by the `boto3` library](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#configuring-credentials).

Boto3 credentials can be configured in multiple ways (eight as of this writing) that are mirrored here:

1. Passing credentials as parameters in the `boto.client()` method
2. Passing credentials as parameters when creating a Session object
3. Environment variables
4. Shared credential file (`~/.aws/credentials`)
5. AWS config file (`~/.aws/config`)
6. Assume Role provider
7. Boto2 config file (`/etc/boto.cfg` and `~/.boto`)
8. Instance metadata service on an Amazon EC2 instance that has an IAM role configured.

**The AWS providers only support methods 3-8. Methods 1 and 2 ARE NOT SUPPORTED at this time.**

We highly recommend you defer to using environment variables for your deployment as specified in the credentials documentation linked above. The values specified in the linked documentation should be [set within your `~.bashrc`](https://nautobot.readthedocs.io/en/latest/installation/nautobot/#update-the-nautobot-bashrc) (or similar profile) on your system.

#### Configuration

This is an example based on our recommended deployment pattern in the section above (item 3) that is using [environment variables](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#environment-variables). You will need to set these in the environment prior to starting Nautobot:

```no-highlight
export AWS_ACCESS_KEY_ID=foo      # The access key for your AWS account.
export AWS_SECRET_ACCESS_KEY=bar  # The secret key for your AWS account.
```

Please refer to the [Nautobot documentation on updating your `.bashrc`](https://nautobot.readthedocs.io/en/latest/installation/nautobot/#update-the-nautobot-bashrc) for how to do this for production Nautobot deployments.

### HashiCorp Vault

#### Configuration

You must provide a mapping in `PLUGINS_CONFIG` within your `nautobot_config.py`, for example:

```python
PLUGINS_CONFIG = {
    "nautobot_secrets_providers": {
        "hashicorp_vault": {
            "url": "http://localhost:8200",
            "auth_method": "token",
            "token": os.getenv("NAUTOBOT_HASHICORP_VAULT_TOKEN"),
        }
    },
}
```

- `url` - (required) The URL to the HashiCorp Vault instance (e.g. `http://localhost:8200`).
- `auth_method` - (optional / defaults to "token") The method used to authenticate against the HashiCorp Vault instance. Either `"approle"`, `"aws"`, `"kubernetes"` or `"token"`.  For information on using AWS authentication with vault see the [authentication](#authentication) section above.
- `ca_cert` - (optional) Path to a PEM formatted CA certificate to use when verifying the Vault connection.  Can alternatively be set to `False` to ignore SSL verification (not recommended) or `True` to use the system certificates.
- `default_mount_point` - (optional / defaults to "secret") The default mount point of the K/V Version 2 secrets engine within Hashicorp Vault.
- `kv_version` - (optional / defaults to "v2") The version of the KV engine to use, can be `v1` or `v2`
- `k8s_token_path` - (optional) Path to the kubernetes service account token file.  Defaults to "/var/run/secrets/kubernetes.io/serviceaccount/token".
- `token` - (optional) Required when `"auth_method": "token"` or `auth_method` is not supplied. The token for authenticating the client with the HashiCorp Vault instance. As with other sensitive service credentials, we recommend that you provide the token value as an environment variable and retrieve it with `{"token": os.getenv("NAUTOBOT_HASHICORP_VAULT_TOKEN")}` rather than hard-coding it in your `nautobot_config.py`.
- `role_name` - (optional) Required when `"auth_method": "kubernetes"`, optional when `"auth_method": "aws"`.  The Vault Kubernetes role or Vault AWS role to assume which the pod's service account has access to.
- `role_id` - (optional) Required when `"auth_method": "approle"`. As with other sensitive service credentials, we recommend that you provide the role_id value as an environment variable and retrieve it with `{"role_id": os.getenv("NAUTOBOT_HASHICORP_VAULT_ROLE_ID")}` rather than hard-coding it in your `nautobot_config.py`.
- `secret_id` - (optional) Required when `"auth_method": "approle"`.As with other sensitive service credentials, we recommend that you provide the secret_id value as an environment variable and retrieve it with `{"secret_id": os.getenv("NAUTOBOT_HASHICORP_VAULT_SECRET_ID")}` rather than hard-coding it in your `nautobot_config.py`.
- `login_kwargs` - (optional) Additional optional parameters to pass to the login method for [`approle`](https://hvac.readthedocs.io/en/stable/source/hvac_api_auth_methods.html#hvac.api.auth_methods.AppRole.login), [`aws`](https://hvac.readthedocs.io/en/stable/source/hvac_api_auth_methods.html#hvac.api.auth_methods.Aws.iam_login) and [`kubernetes`](https://hvac.readthedocs.io/en/stable/source/hvac_api_auth_methods.html#hvac.api.auth_methods.Kubernetes.login) authentication methods.
- `namespace` - (optional) Namespace to use for the [`X-Vault-Namespace` header](https://github.com/hvac/hvac/blob/main/hvac/adapters.py#L287) on all hvac client requests. Required when the [`Namespaces`](https://developer.hashicorp.com/vault/docs/enterprise/namespaces#usage) feature is enabled in Vault Enterprise.
 
### Delinea/Thycotic Secret Server (TSS)

The Delinea/Thycotic Secret Server plugin includes two providers:

- **`Thycotic Secret Server by ID`**

    This provider uses the `Secret ID` to specifiy the secret that is selected. The `Secret ID` is displayed in the browser's URL field if you `Edit` the data in Thycotic Secret Server.

    - Example:

        The url is: _https://pw.example.local/SecretServer/app/#/secret/**1234**/general_

        In this example the value for `Secret ID` is **1234**.

- **`Thycotic Secret Server by Path`**

    This provider allows to select the secret by folder-path and secret-name. The path delimiter is a '\\'.

    The `Secret path` is displayed as page header when `Edit` a secret.

    - Example:

        The header is: **NET-Automation > Nautobot > My-Secret**

        In this example the value for `Secret path` is **`\NET-Automation\Nautobot\My-Secret`**.

## App Configuration

!!! warning "Developer Note - Remove Me!"
    Any configuration required to get the App set up. Edit the table below as per the examples provided.

The plugin behavior can be controlled with the following list of settings:

| Key     | Example | Default | Description                          |
| ------- | ------ | -------- | ------------------------------------- |
| `enable_backup` | `True` | `True` | A boolean to represent whether or not to run backup configurations within the plugin. |
| `platform_slug_map` | `{"cisco_wlc": "cisco_aireos"}` | `None` | A dictionary in which the key is the platform slug and the value is what netutils uses in any "network_os" parameter. |
| `per_feature_bar_width` | `0.15` | `0.15` | The width of the table bar within the overview report |
