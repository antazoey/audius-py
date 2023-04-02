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

To create an `audius` SDK instance, do:

```python
from audius.sdk import Audius

audius = Audius()
```

It is recommended that you set a custom app name (the default is `audius-py`).
One way to do this is via an environment variable:

```shell
export AUDIUS_APP_NAME="My_Audius_App"
```

Then, when you create an Audius SDK object, it will automatically use this value instead.

You can also specify an app name (and other configuration) when creating the SDK, like:

```python
from audius.config import Config
from audius.sdk import Audius

config = Config(app_name="my_app")
sdk = Audius(config=config)
```

Another example config value is the host, e.g.:

```shell
export AUDIUS_HOST_NAME="https://audius.example.com"
```

or:

```python
from audius.config import Config

Config(host="https://audius.exmaple.com")
```

If you don't specify a host, `audius-py` will select a random host from the list of known hosts to the Audius app.
To see all available hosts, run the following command:

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

By default, `audius-py` tries to find the best player.
However, specify your player of choice using the `--player` flag:

```shell
audius tracks play G0wyE --player vlc
```

### Python SDK

Use the Python SDK directly:

```python
from audius.sdk import Audius

sdk = Audius(app="my_app")
for artist in sdk.users.top():
    print(artist["name"])
```
