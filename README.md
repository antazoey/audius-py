# audius-py

A Python SDK and CLI for the Audius Platform.

## Installation

From pip:

```shell
pip install audius-py
```

From source (from the root project directory):

```shell
pip install .
```

**NOTE**: In order to user the media player functionality of the SDK, you must have [VLC media player](https://www.videolan.org/vlc/) installed.

## Quick Usage

It is recommended that you set the environment variable AUDIUS_APP_NAME prior to using the SDK:

```shell
export AUDIUS_APP_NAME="My_Audius_App"
```

You can also specify an app name when creating the SDK, like:

```python
from audius.sdk import Audius

sdk = Audius(app="my_app")
```

If you don't specify an app name, the default name `audius-py` will be used.
Additionally, specify your host URL via environment variable:

```shell
export AUDIUS_HOST_NAME="https://audius.example.com"
```

If you don't specify a host, `audius-py` will select a random host from the list of known hosts to the Audius app.
To see all available hosts, run command:

```shell
audius hosts
```

### CLI

See all commands by doing:

```shell
audius --help
```

This guide will show how to stream one of the top songs on Audius directly into your terminal.
First, browse top artists using the CLI:

```shell
audius users top
```

It should show output like this:

```shell
1: Zedd (id=XlJby)
2: Skrillex (id=eAZl3)
3: Aluna (id=5j9VM)
4: kennybeats (id=DrZwG)
5: trillsammy (id=NzMW8)
6: ODESZA (id=2oNg1)
7: noodles (id=b9w8J)
8: kayzo (id=LMdyZ)
9: Disclosure (id=E2O1R)
10: Fat Nick (id=oGKZd)
```

Next, select one of the user IDs by copying it and using it in the following command:

```shell
audius users tracks eAZl3
```

It should output track information like this:

```shell
Track: Kliptown Empyrean (id=G0wyE)
```

Finally, play the track by using its ID in the following command:

```shell
audius tracks play G0wyE
```

The song should now be streaming into your terminal!
And if you really enjoy the track, you can download it by doing:

```shell
audius tracks download G0wyE song.mp3
```

### Python SDK

Use the Python SDK directly:

```python
from audius.sdk import Audius

sdk = Audius(app="my_app")
for artist in sdk.users.top():
    print(artist["name"])
```
