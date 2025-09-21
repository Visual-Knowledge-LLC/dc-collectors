#!/usr/bin/env python3
"""
Virginia DPOR (Department of Professional and Occupational Regulation) Collector
Collects license data from VA DPOR for BBB 0241 (DC region)
"""

import re
import logging
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from sqlalchemy import text

# Import database connection module
from src.utils import db_connect

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VaDPORCollector:
    """Collector for Virginia DPOR license data"""

    def __init__(self, headless: bool = True, output_dir: str = "data"):
        """
        Initialize the DPOR collector.

        Args:
            headless: Run Chrome in headless mode
            output_dir: Directory to save collected data
        """
        self.base_url = "https://www.dpor.virginia.gov/RegulantLists#:~:text=Registered%20Athlete%20Agents-"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.headless = headless
        self.collected_data = []

        # Agency information for DC region
        self.bbb_id = "0241"
        self.agency_id = "3838"
        self.agency_name = "VA - DPOR"

        # Setup database connection
        self.engine = db_connect.PGconnection()

    def setup_driver(self) -> webdriver.Chrome:
        """Setup Chrome driver with options"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        # Use webdriver manager to handle driver installation (suppress logging)
        import os
        os.environ['WDM_LOG'] = '0'  # Suppress webdriver-manager logs
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())

        return webdriver.Chrome(service=service, options=chrome_options)

    def get_data_links(self) -> List[str]:
        """Get all TSV data file links from DPOR website"""
        logger.info("Fetching data links from DPOR website...")

        driver = self.setup_driver()
        links = []

        try:
            driver.get(self.base_url)
            driver.implicitly_wait(10)

            # Find all anchor tags that end with 'crnt.txt'
            anchor_tags = driver.find_elements(By.TAG_NAME, "a")
            for tag in anchor_tags:
                href = tag.get_attribute('href')
                if href and href.endswith('crnt.txt'):
                    links.append(href)

            logger.info(f"Found {len(links)} data file links")

        except Exception as e:
            logger.error(f"Error fetching links: {e}")
        finally:
            driver.quit()

        return links

    def fetch_tsv_data(self, links: List[str]) -> Dict[str, str]:
        """Fetch TSV data from all links"""
        logger.info("Downloading TSV data files...")
        csv_data_dict = {}

        pattern = re.compile(r'/(\w+?)__crnt.txt')

        with tqdm(total=len(links), desc="Downloading files") as pbar:
            for link in links:
                match = pattern.search(link)
                if match:
                    extracted_part = match.group(1)

                    try:
                        response = requests.get(link, timeout=30)
                        if response.status_code == 200:
                            csv_data_dict[extracted_part] = response.text
                            pbar.set_postfix({"Current": extracted_part})
                        else:
                            logger.warning(f"Failed to download: {link} (Status: {response.status_code})")
                    except requests.exceptions.RequestException as e:
                        logger.error(f"Error downloading {link}: {e}")
                else:
                    logger.warning(f"No match found for link: {link}")

                pbar.update(1)

        return csv_data_dict

    def get_header_mapping(self, dataset_key: str) -> Optional[Dict]:
        """
        Get header mapping for a dataset from the database.
        Uses the same query as the old DPOR scraper.
        """
        # Format the key by adding a space and capitalizing if it contains alpha characters
        key = re.sub(r'(\d+)([a-zA-Z]+)', r'\1 \2', dataset_key).upper()

        # Use ID from URL to get header mappings from DB (same query as old scraper)
        query = f"""
        SELECT la.agency_id AS "Agency ID",
            hm.agency_name AS "Agency Name",
            hm.state AS "State Established",
            hm.business_name AS "Business Name",
            hm.street AS "Street",
            hm.zip AS "Zip",
            hm.date_established AS "Date Established",
            hm.category AS "Category",
            hm.license_number AS "License Number",
            hm.phone_number AS "Phone Number",
            hm.owner_first_name AS "Owner First Name",
            hm.owner_last_name AS "Owner Last Name",
            hm.expiration_date AS "Expiration Date",
            hm.license_status AS "License Status",
            hm.email,
            hm.dataset,
            hm.id,
            hm.tobid AS "TOB ID",
            hm.agency_url AS "Agency URL"
        FROM public.header_mappings AS hm
        JOIN licensing_agencies la ON hm.agency_name = la.agency_name
        WHERE hm.dataset LIKE '{key}%'
        """

        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query))
                header_mappings = result.fetchone()

                if header_mappings:
                    # Convert header_mappings to a dictionary using the column names
                    header_mapping_dict = {column: value for column, value in zip(result.keys(), header_mappings)}
                    logger.debug(f"Found header mapping for {key}: {header_mapping_dict.get('Agency Name')}")
                    return header_mapping_dict
                else:
                    # Don't log warnings for missing mappings - too noisy
                    logger.debug(f"No header mappings found for dataset: {key}")

        except Exception as e:
            logger.error(f"Database query failed for {key}: {e}")

        # Fallback to basic mapping if database lookup fails
        logger.debug(f"Using fallback mapping for dataset {dataset_key}")
        return {
            'Agency Name': self.agency_name,
            'Agency ID': self.agency_id,
            'Agency URL': 'https://www.dpor.virginia.gov/',
            'TOB ID': '',
            'State Established': 'VA',
            'Business Name': 'Name',
            'Street': 'MAILING ADDRESS',
            'City': 'CITY',
            'Zip': 'ZIP CODE',
            'Date Established': 'NA',
            'Category': 'LICENSE SPECIALTY',
            'License Number': 'CERTIFICATE #',
            'Phone Number': 'NA',
            'Owner First Name': 'NA',
            'Owner Last Name': 'NA',
            'Expiration Date': 'EXPIRES',
            'License Status': 'STATUS',
            'County': 'NA'
        }

    def process_tsv_data(self, dataset_key: str, tsv_data: str) -> List[Dict]:
        """Process TSV data into structured records"""
        records = []

        # Format the key
        key = re.sub(r'(\d+)([a-zA-Z]+)', r'\1 \2', dataset_key).upper()

        # Get header mapping
        header_mapping = self.get_header_mapping(key)
        if not header_mapping:
            logger.debug(f"No header mapping found for {key}")
            return records

        # Parse TSV data
        tsv_lines = tsv_data.splitlines()
        if not tsv_lines:
            return records

        tsv_headers = tsv_lines[0].split('\t')
        tsv_data_rows = tsv_lines[1:]

        # Process silently without logging each dataset
        for row in tsv_data_rows:
            fields = row.split('\t')

            try:
                # Build license number from board, occupation, and certificate
                board_idx = tsv_headers.index("BOARD") if "BOARD" in tsv_headers else -1
                occupation_idx = tsv_headers.index("OCCUPATION") if "OCCUPATION" in tsv_headers else -1
                certificate_idx = tsv_headers.index("CERTIFICATE #") if "CERTIFICATE #" in tsv_headers else -1

                if board_idx >= 0 and occupation_idx >= 0 and certificate_idx >= 0:
                    board = fields[board_idx] if board_idx < len(fields) else ""
                    occupation = fields[occupation_idx] if occupation_idx < len(fields) else ""
                    certificate = fields[certificate_idx] if certificate_idx < len(fields) else ""
                    license_number = f"{board}{occupation}{certificate}"
                else:
                    # Fallback to just certificate number
                    license_number = fields[certificate_idx] if certificate_idx >= 0 and certificate_idx < len(fields) else ""

                # Get license specialty if available
                license_specialty = ""
                if "LICENSE SPECIALTY" in tsv_headers:
                    specialty_idx = tsv_headers.index("LICENSE SPECIALTY")
                    if specialty_idx < len(fields):
                        license_specialty = fields[specialty_idx]

                # Get other fields safely
                def safe_get_field(header_name: str, default: str = "") -> str:
                    if header_name in tsv_headers:
                        idx = tsv_headers.index(header_name)
                        if idx < len(fields):
                            return fields[idx].strip()
                    return default

                # Build record
                record = {
                    "Agency Name": header_mapping['Agency Name'],
                    "BBB ID": self.bbb_id,
                    "Agency ID": self.agency_id,
                    "Agency URL": header_mapping['Agency URL'],
                    "TOB ID": "",
                    "State Established": "VA",
                    "Business Name": safe_get_field("Name", ""),
                    "Street": safe_get_field("MAILING ADDRESS", ""),
                    "City": safe_get_field("CITY", ""),
                    "Zip": safe_get_field("ZIP CODE", ""),
                    "Date Established": "",
                    "Category": license_specialty,
                    "License Number": license_number,
                    "Phone Number": safe_get_field("PHONE", ""),
                    "Owner First Name": safe_get_field("FIRST NAME", ""),
                    "Owner Last Name": safe_get_field("LAST NAME", ""),
                    "Expiration Date": safe_get_field("EXPIRES", ""),
                    "License Status": safe_get_field("STATUS", "Active"),
                    "County": ""
                }

                records.append(record)

            except Exception as e:
                logger.debug(f"Error processing row in {key}: {e}")
                continue

        return records

    def collect(self) -> List[Dict]:
        """Main collection method"""
        logger.info("="*60)
        logger.info("Starting VA DPOR Data Collection")
        logger.info(f"BBB ID: {self.bbb_id}, Agency ID: {self.agency_id}")
        logger.info("="*60)

        # Get data links
        links = self.get_data_links()
        if not links:
            logger.error("No data links found")
            return []

        # Fetch TSV data
        csv_data_dict = self.fetch_tsv_data(links)

        # Process each dataset silently
        all_records = []
        logger.info("Processing downloaded data...")
        for dataset_key, tsv_data in csv_data_dict.items():
            records = self.process_tsv_data(dataset_key, tsv_data)
            all_records.extend(records)

        self.collected_data = all_records
        logger.info(f"Total records collected: {len(all_records):,}")

        return all_records

    def upload_to_api(self, dry_run: bool = False) -> bool:
        """
        Upload collected data to Visual Knowledge API.

        Args:
            dry_run: If True, don't actually upload data

        Returns:
            True if successful, False otherwise
        """
        if not self.collected_data:
            logger.warning("No data to upload")
            return False

        # Import the uploader
        from src.utils.upload_api import VKBulkUploader

        logger.info("="*60)
        logger.info("Starting API Upload")
        logger.info("="*60)

        uploader = VKBulkUploader(dry_run=dry_run)
        result = uploader.upload_data(self.collected_data)

        if result["success"]:
            logger.info(f"✅ Upload successful: {result['uploaded']} records uploaded")
        else:
            logger.error("❌ Upload failed")

        return result["success"]

    def save_to_csv(self, filename: Optional[str] = None) -> str:
        """Save collected data to CSV file"""
        if not self.collected_data:
            logger.warning("No data to save")
            return ""

        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dpor_data_{timestamp}.csv"

        filepath = self.output_dir / filename

        # Write CSV
        import csv
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            if self.collected_data:
                fieldnames = self.collected_data[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.collected_data)

        logger.info(f"Data saved to: {filepath}")
        return str(filepath)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='VA DPOR Data Collector for BBB 0241')
    parser.add_argument('--headless', action='store_true', default=True,
                        help='Run Chrome in headless mode (default: True)')
    parser.add_argument('--save-csv', action='store_true',
                        help='Save collected data to CSV file')
    parser.add_argument('--upload', action='store_true',
                        help='Upload data to Visual Knowledge API')
    parser.add_argument('--dry-run', action='store_true',
                        help='Perform dry run (don\'t actually upload)')

    args = parser.parse_args()

    # Run collector
    collector = VaDPORCollector(headless=args.headless)
    data = collector.collect()

    if data:
        # Save to CSV if requested
        if args.save_csv:
            csv_file = collector.save_to_csv()
            # Don't double-log, save_to_csv already logs the file path

        # Upload to API if requested
        if args.upload:
            success = collector.upload_to_api(dry_run=args.dry_run)
            if success:
                logger.info("✅ Upload completed successfully")
            else:
                logger.error("❌ Upload failed")
    else:
        logger.error("No data collected")