# DC Collectors

Data collectors for BBB 0241 (DC region) agencies.

## Overview

This repository contains scrapers and collectors for various DC region agencies, following the patterns established in `oklahoma_collectors` and `tucson_data_collection` repos.

## Features

- **Bulk API Upload**: Uses Visual Knowledge API bulk upload endpoint for efficient data transfer
- **Progress Tracking**: tqdm progress bars for better visibility during collection
- **Modular Design**: Each agency has its own collector module
- **Error Handling**: Robust error handling and logging
- **Dry Run Mode**: Test collections without uploading data

## Agencies

### VA DPOR (Department of Professional and Occupational Regulation)
- **BBB ID**: 0241
- **Agency ID**: 3838
- **Data Source**: https://www.dpor.virginia.gov/RegulantLists
- **Collection Method**: Selenium web scraping of TSV files
- **Records**: Multiple license types (contractors, trades, etc.)

## Installation

```bash
# Clone repository
git clone <repo-url>
cd dc-collectors

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run All Collectors

```bash
# Collect and upload all agencies
python run_collection.py --upload

# Dry run (no actual upload)
python run_collection.py --upload --dry-run

# Save to CSV only
python run_collection.py --save-csv
```

### Run Individual Collector

```bash
# Run DPOR collector only
python run_collection.py --collector dpor --upload

# Or run directly
python src/collectors/dpor/dpor_collector.py --upload
```

### Command Line Options

- `--collector [dpor|all]`: Which collector(s) to run
- `--save-csv`: Save collected data to CSV files
- `--upload`: Upload data to Visual Knowledge API
- `--dry-run`: Perform dry run (don't actually upload)
- `--headless`: Run Chrome in headless mode (default: True)

## Directory Structure

```
dc-collectors/
├── src/
│   ├── collectors/
│   │   └── dpor/
│   │       └── dpor_collector.py    # VA DPOR collector
│   └── utils/
│       └── upload_api.py            # Bulk API upload utility
├── data/                            # Output directory for CSV files
├── logs/                            # Log files
├── config/                          # Configuration files
├── run_collection.py                # Main runner script
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Data Format

All collectors output standardized records with the following fields:

### Required Fields
- `Agency Name`: Full agency name
- `BBB ID`: BBB identifier (0241 for DC)
- `Agency ID`: Agency-specific ID
- `Agency URL`: Agency website URL
- `TOB ID`: Type of business ID (usually "NA")
- `State Established`: State code (e.g., "VA")

### Business Information
- `Business Name`: Company/individual name
- `Street`: Street address
- `City`: City name
- `Zip`: ZIP code
- `Date Established`: Business establishment date
- `Category`: License category/specialty
- `License Number`: License/certificate number
- `Phone Number`: Contact phone
- `Owner First Name`: Owner's first name
- `Owner Last Name`: Owner's last name
- `Expiration Date`: License expiration date
- `License Status`: Current status (Active/Inactive)
- `County`: County name

## Bulk Upload Process

The collectors use a batch upload process:

1. **Collection**: Data is scraped from agency websites
2. **Processing**: Raw data is cleaned and standardized
3. **Batching**: Records are grouped into batches (default: 100 records)
4. **Upload**: Batches are sent to the API endpoint
5. **Verification**: Upload success is tracked and reported

## API Endpoint

- **URL**: `https://api.visualknowledgeportal.com:5005/upload_point/false`
- **Method**: POST
- **Payload**: `{"results": [array of records]}`
- **Headers**: Standard browser headers with JSON content type

## Logging

Logs are written to:
- Console: INFO level and above
- Log files: All levels (when implemented)

## Error Handling

- **Network Errors**: Automatic retry with exponential backoff
- **Data Errors**: Skip invalid records, log warnings
- **API Errors**: Report failed batches, continue with remaining
- **Selenium Errors**: Graceful browser cleanup

## Development

### Adding a New Collector

1. Create new module in `src/collectors/<agency_name>/`
2. Implement collector class with:
   - `__init__()`: Initialize with BBB/agency IDs
   - `collect()`: Main collection method
   - `upload_to_api()`: Upload using VKBulkUploader
   - `save_to_csv()`: Optional CSV export

3. Add to `run_collection.py` runner
4. Update this README

### Testing

```bash
# Test DPOR collector
python src/collectors/dpor/dpor_collector.py --dry-run

# Test with CSV output
python src/collectors/dpor/dpor_collector.py --save-csv
```

## Troubleshooting

### Chrome Driver Issues
- The collector uses `webdriver-manager` to automatically download ChromeDriver
- If issues persist, manually download ChromeDriver and set path

### SSL Certificate Errors
- SSL warnings are disabled for the API endpoint
- This is intentional for the internal API

### Memory Issues
- For large datasets, consider reducing batch size in upload_api.py
- Use headless mode to reduce memory usage

## TODO

- [ ] Add more DC region agencies
- [ ] Implement retry logic for failed batches
- [ ] Add data validation before upload
- [ ] Create unit tests
- [ ] Add configuration file support
- [ ] Implement database storage option

## Migration Notes

This repository was migrated from the legacy `vk-server-scrapers` repo with the following improvements:

1. **Bulk Upload**: Changed from record-by-record to batch uploads
2. **Progress Bars**: Added tqdm for better progress visibility
3. **Clean Output**: Removed verbose debug output
4. **Modular Structure**: Separated collectors and utilities
5. **Error Handling**: Improved error handling and logging
6. **Documentation**: Added comprehensive documentation

## License

Proprietary - Visual Knowledge

## Support

For issues or questions, contact the Visual Knowledge development team
