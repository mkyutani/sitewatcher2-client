# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

sitewatcher2-client is a Python CLI tool (`sw2`) for managing website monitoring. It interacts with a sitewatcher2 server via REST APIs to collect web resources and distribute notifications to Slack and MS Teams.

## Commands

### Installation
```bash
pip install .
```

### Running Tests
```bash
python -m unittest tests/test_directory.py
```

### Docker Build
```bash
docker build . --tag sw2:latest
```

### CLI Usage Examples
```bash
sw2 ping                              # Test server connection
sw2 config SW2_SERVER                 # Get/set configuration
sw2 c list                            # List channels (alias for 'channel')
sw2 d list                            # List directories (alias for 'directory')
sw2 s list                            # List sites (alias for 'site')
sw2 s add <dir-id> "site-name" <url>  # Add a site
```

## Architecture

### Command Pattern
Each command module follows a consistent pattern with two functions:
- `sw2_<category>_<command>()` - Executes the command
- `sw2_parser_<category>_<command>()` - Registers argparse arguments

New commands must follow this naming convention and be added to the module's `function_map` in `__init__.py`.

### Source Structure
- `src/sw2/main.py` - CLI entry point with argparse setup
- `src/sw2/env.py` - Configuration management (reads `~/.sitewatcher` or `SW2_SERVER` env var)
- `src/sw2/channel/` - Channel management (Slack, MS Teams interfaces)
- `src/sw2/site/` - Site management commands
- `src/sw2/directory/` - Directory management commands
- `src/sw2/util.py` - Utilities (UUID validation, rule expression parsing)

### Channel Interfaces
- **Slack**: Uses `slack_sdk`, sends text messages
- **MS Teams**: Uses adaptive cards format (`application/vnd.microsoft.card.adaptive`), includes rate-limit handling

### Configuration
- Config file: `~/.sitewatcher` (JSON format)
- Default server: `http://localhost:18085`
- Environment override: `SW2_SERVER`
- Local dev: rename `_env` to `.env`

## API Endpoints
The client communicates with these server endpoints:
- `/api/v1/directories/`
- `/api/v1/sites/`
- `/api/v1/channels/`
- `/api/v1/resources/`
