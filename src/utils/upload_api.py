#!/usr/bin/env python3
"""
DC Data Uploader - API Version
Uses the Visual Knowledge API endpoint for reliable bulk uploads.
Based on oklahoma_collectors pattern.
"""

import sys
import json
import requests
import urllib3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from tqdm import tqdm
import logging

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VKBulkUploader:
    """Bulk uploader for Visual Knowledge API"""

    def __init__(self, dry_run: bool = False, batch_size: int = 5000):
        """
        Initialize the bulk uploader.

        Args:
            dry_run: If True, don't actually upload data
            batch_size: Number of records to upload per batch
        """
        self.api_url = 'https://api.visualknowledgeportal.com:5005/upload_point/false'
        self.dry_run = dry_run
        self.batch_size = batch_size
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Origin': 'https://visualknowledgeportal.com',
            'Referer': 'https://visualknowledgeportal.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Content-Type': 'application/json'
        }

    def clean_string(self, text: str) -> str:
        """Clean string for database insertion."""
        if not text:
            return 'NA'
        # Remove problematic characters
        return str(text).replace(',', '').replace("'", '').replace('"', '').strip()

    def format_date(self, date_str: str) -> str:
        """Format date string to MM/DD/YYYY or return NA."""
        if not date_str or date_str == 'NA':
            return 'NA'

        try:
            # Try parsing various date formats
            for fmt in ['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%d', '%b %d, %Y', '%m/%d/%Y']:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime('%m/%d/%Y')
                except:
                    continue
            return date_str  # Return as-is if no format matches
        except:
            return 'NA'

    def upload_batch(self, batch: List[Dict], batch_num: int, total_batches: int) -> bool:
        """
        Upload a single batch of records.

        Args:
            batch: List of records to upload
            batch_num: Current batch number
            total_batches: Total number of batches

        Returns:
            True if successful, False otherwise
        """
        payload = {"results": batch}

        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers=self.headers,
                verify=False,
                timeout=30
            )

            if response.status_code == 200:
                return True
            else:
                logger.warning(f"Batch {batch_num} failed with status {response.status_code}")
                return False

        except requests.exceptions.Timeout:
            logger.error(f"Batch {batch_num} timed out")
            return False
        except Exception as e:
            logger.error(f"Batch {batch_num} error: {str(e)}")
            return False

    def upload_data(self, records: List[Dict]) -> Dict[str, any]:
        """
        Upload data to Visual Knowledge API in batches.

        Args:
            records: List of standardized records to upload

        Returns:
            Dictionary with upload statistics
        """
        if not records:
            logger.warning("No records to upload")
            return {"success": False, "total": 0, "uploaded": 0}

        logger.info(f"Preparing to upload {len(records)} records")

        if self.dry_run:
            logger.info("DRY RUN MODE - Not uploading data")
            logger.info(f"Sample record:\n{json.dumps(records[0], indent=2)}")
            return {"success": True, "total": len(records), "uploaded": 0, "dry_run": True}

        # Calculate batches
        total_batches = (len(records) + self.batch_size - 1) // self.batch_size
        successful_batches = 0
        failed_batches = 0

        logger.info(f"Uploading in {total_batches} batches of up to {self.batch_size} records each")

        # Upload with progress bar
        with tqdm(total=total_batches, desc="Uploading batches") as pbar:
            for i in range(0, len(records), self.batch_size):
                batch = records[i:i + self.batch_size]
                batch_num = i // self.batch_size + 1

                success = self.upload_batch(batch, batch_num, total_batches)

                if success:
                    successful_batches += 1
                    pbar.set_postfix({"Success": successful_batches, "Failed": failed_batches})
                else:
                    failed_batches += 1
                    pbar.set_postfix({"Success": successful_batches, "Failed": failed_batches})

                pbar.update(1)

        # Calculate results
        total_records_uploaded = successful_batches * self.batch_size
        if successful_batches == total_batches:
            total_records_uploaded = len(records)

        success_rate = (successful_batches / total_batches) * 100 if total_batches > 0 else 0

        # Log summary
        logger.info("Upload Summary:")
        logger.info(f"  Total Records: {len(records)}")
        logger.info(f"  Successful Batches: {successful_batches}/{total_batches}")
        logger.info(f"  Failed Batches: {failed_batches}/{total_batches}")
        logger.info(f"  Success Rate: {success_rate:.1f}%")

        return {
            "success": successful_batches > 0,
            "total": len(records),
            "uploaded": total_records_uploaded,
            "successful_batches": successful_batches,
            "failed_batches": failed_batches,
            "success_rate": success_rate
        }