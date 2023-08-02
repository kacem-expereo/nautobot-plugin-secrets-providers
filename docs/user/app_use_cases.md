# Using the App

This document describes common use-cases and scenarios for this App.

## General Usage

Nautobot Secrets Providers is a plugin for [Nautobot](https://github.com/nautobot/nautobot) 1.2.0 or higher that bundles Secrets Providers for integrating with popular secrets backends. Nautobot 1.2.0 added support for integrating with retrieving secrets from various secrets providers.

This plugin publishes secrets providers that are not included in the within the Nautobot core software package so that it will be easier to maintain and extend support for various secrets providers without waiting on Nautobot software releases.

This plugin supports the following popular secrets backends:

| Secrets Backend                                              | Supported Secret Types                                       | Supported Authentication Methods                             |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/) | [Other: Key/value pairs](https://docs.aws.amazon.com/secretsmanager/latest/userguide/manage_create-basic-secret.html) | [AWS credentials](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html) (see Usage section below) |
| [AWS Systems Manager Parameter Store](https://aws.amazon.com/secrets-manager/) | [Other: Key/value pairs](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) | [AWS credentials](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html) (see Usage section below) |
| [HashiCorp Vault](https://www.vaultproject.io)               | [K/V Version 2](https://www.vaultproject.io/docs/secrets/kv/kv-v2)<br/>[K/V Version 1](https://developer.hashicorp.com/vault/docs/secrets/kv/kv-v1) | [Token](https://www.vaultproject.io/docs/auth/token)<br/>[AppRole](https://www.vaultproject.io/docs/auth/approle)<br/>[AWS](https://www.vaultproject.io/docs/auth/aws)<br/>[Kubernetes](https://www.vaultproject.io/docs/auth/kubernetes)         |
| [Delinea/Thycotic Secret Server](https://delinea.com/products/secret-server)               | [Secret Server Cloud](https://github.com/DelineaXPM/python-tss-sdk#secret-server-cloud)<br/>[Secret Server (on-prem)](https://github.com/DelineaXPM/python-tss-sdk#initializing-secretserver)| [Access Token Authorization](https://github.com/DelineaXPM/python-tss-sdk#access-token-authorization)<br/>[Domain Authorization](https://github.com/DelineaXPM/python-tss-sdk#domain-authorization)<br/>[Password Authorization](https://github.com/DelineaXPM/python-tss-sdk#password-authorization)<br/>         |

## Use-cases and common workflows

### AWS

AWS Secrets Manager and Systems Manager Parameter Store are supported. Both providers require the `boto3` library. This can be easily installed along with the plugin using the following command:

```no-highlight
pip install nautobot-secrets-providers[aws]
```

### HashiCorp Vault

The HashiCorp Vault provider requires the `hvac` library. This can easily be installed along with the plugin using the following command:

```no-highlight
pip install nautobot-secrets-providers[hashicorp]
```

### Delinea/Thycotic Secret Server

The Delinea/Thycotic Secret Server provider requires the `python-tss-sdk` library. This can easily be installed along with the plugin using the following command:

```no-highlight
pip install nautobot-secrets-providers[thycotic]
```

## Screenshots

![Screenshot of installed plugins](../images/screenshot01.png "Plugin landing page")

---

![Screenshot of plugin home page](../images/screenshot02.png "Plugin Home page")

---

![Screenshot of secret using AWS Secrets Manager](../images/screenshot03.png "Secret using AWS Secrets Manager")

---

![Screenshot of secret using HashiCorp Vault](../images/screenshot04.png "Secret using HashiCorp Vault")

---

![Screenshot of secret using Delinea/Thycotic Secret Server by ID](../images/screenshot05.png "Secret using Thycotic Secret Server by ID")

---

![Screenshot of secret using Delinea/Thycotic Secret Server by Path](../images/screenshot06.png "Secret using Thycotic Secret Server by Path")
