# Nautilus - AzuraCast Bot for Radionautica.Net

Nautilus is an AzuraCast module for [Sopel](https://sopel.chat/), an extensible IRC bot written in Python.
It's made to help manage the Radionautica.Net radio station.

## Development

### Pre-requisites

- [Poetry](https://python-poetry.org/)
- [Poe the Poet](https://poethepoet.natn.io/poetry_plugin.html)
- [entr](https://github.com/eradman/entr)
- [fd](https://github.com/sharkdp/fd?tab=readme-ov-file#installation)

### Run the bot in development mode

First install the dependencies:

```sh
poetry install
```

Then copy `config.example.cfg` to `config.cfg` and make any necessary changes.

Finally, run the bot:

```sh
poetry poe dev
```

This will run the bot and restart it whenever you make any changes to any file
inside the `nautilus/` directory.
