# audius-py

A Python SDK for the Audius Platform

## Installation

From pip:

```shell
pip install audius-py
```

From source:

```shell
pip install poetry && poetry install
```

## Quick Usage

You must set the environment variable AUDIUS_APP_NAME prior to using the SDK:

```shell
export AUDIUS_APP_NAME="My_Audius_App"
```

### CLI

Browse top artists using the CLI:

```shell
audius users top
```

Check information about a specific user by doing:

```shell
audius users get <user-id>
```

### Python SDK

Use the Python SDK directly:

```python
from audius.sdk import Audius

sdk = Audius.from_env()
for artist in sdk.users.top():
    print(artist["name"])
```
