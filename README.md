# sitewatcher2-client

sitewatcher2-client is a Python CLI tool (`sw2`) for managing website monitoring. It interacts with a sitewatcher2 server via REST APIs to collect web resources and distribute notifications to Slack and MS Teams.

## Requirements

- Python 3.10+

## Installation

```bash
pip install .
```

## Configuration

The client reads configuration from `~/.sitewatcher` (JSON format). The server URL can also be set via the `SW2_SERVER` environment variable.

```bash
sw2 config server http://localhost:18085  # Set server URL
sw2 config                                # Show current configuration
```

Default server: `http://localhost:18085`

For local development, rename `_env` to `.env`.

## Usage

```bash
sw2 ping                              # Test server connection
sw2 config [name] [value]             # Get/set configuration
sw2 resource <resource-id>            # Retrieve a resource by ID
sw2 test <url>                        # Test links from a URL
sw2 channel list                      # List channels (alias: sw2 c list)
sw2 directory list                    # List directories (alias: sw2 d list)
sw2 site list                         # List sites (alias: sw2 s list)
sw2 site add <dir-id> "name" <url>    # Add a site
```

## Docker

```bash
docker build . --tag sw2:latest
```

## Running Tests

```bash
python -m unittest tests/test_directory.py
```
