# DC Collectors

License data collectors for Washington DC.

## Installation

```bash
pip install -r requirements.txt
pip install git+https://github.com/Visual-Knowledge-LLC/vk-api-utils.git
```

## Usage

```bash
# Run all collectors
python run.py all

# Run specific collector
python run.py business

# Disable Slack notifications
python run.py all --slack off

# Verbose output
python run.py all --verbose
```

## Collectors

### Business Licenses
- Source: DC Department of Consumer and Regulatory Affairs (DCRA)
- Status: Not yet implemented

## Slack Notifications

The collectors send status updates to Slack by default. To disable:
```bash
python run.py all --slack off
```

## Development

To add a new collector:
1. Create a new module in `src/`
2. Implement the collector class
3. Add a run function in `run.py`
4. Update this README