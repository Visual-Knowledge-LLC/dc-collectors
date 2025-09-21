#!/usr/bin/env python3
"""
Fast upload script for DC collectors using VK bulk upload infrastructure
This uses direct database connection for maximum speed
"""

import sys
import os
import csv
from pathlib import Path

# Add VK bulk upload to path
vk_bulk_path = '/Users/chriscowden/Dropbox (Personal)/Business/Cowden Operations Inc/Clients/2-Visual Knowledge/projects/visual_knowledge/vk_bulk_upload'
sys.path.insert(0, vk_bulk_path)
sys.path.insert(0, os.path.join(vk_bulk_path, 'src'))

from db_upload_module_enhanced import EnhancedDatabaseUploadModule, DatabaseConfig

def upload_dpor_data(csv_file):
    """Upload DPOR data using enhanced fast database connection"""

    print("="*60)
    print("ENHANCED VK BULK UPLOAD - DPOR DATA")
    print("="*60)
    print("Features: Deduplication, ON CONFLICT UPDATE, Better Monitoring")
    print("="*60)

    # Initialize enhanced database connection (uses SSH tunnel on port 5433)
    print("Initializing enhanced database connection...")
    db_config = DatabaseConfig(use_ssh_tunnel=True)
    uploader = EnhancedDatabaseUploadModule(db_config, pool_size=10)

    if not uploader.initialize_pool():
        print("❌ Failed to connect to database")
        print("Make sure SSH tunnel is running on port 5433")
        return False

    # Test connection
    success, count = uploader.test_connection()
    if not success:
        print("❌ Database connection test failed")
        return False

    print(f"✅ Connected to database. Current records: {count:,}")

    # Upload the CSV file
    print(f"\nUploading: {csv_file}")
    result = uploader.process_csv_file(
        csv_path=csv_file,
        agency_id="3838",  # VA DPOR
        bbb_id="0241",     # DC
        agency_name="VA - DPOR",
        batch_size=5000
    )

    # Display enhanced results
    print("\n" + "="*60)
    print("ENHANCED UPLOAD RESULTS")
    print("="*60)
    print(f"Status: {result.status.value}")
    print(f"New records inserted: {result.uploaded:,}")
    print(f"Existing records updated: {result.updated:,}")
    print(f"Total processed: {result.uploaded + result.updated:,}")
    print(f"Records failed: {result.failed:,}")
    print(f"Duplicates removed (pre-upload): {result.duplicates_removed:,}")
    print(f"Duration: {result.duration:.2f} seconds")

    if result.records_per_second > 0:
        print(f"Speed: {result.records_per_second:.0f} records/second")

    # Close connection (will print comprehensive statistics)
    uploader.close_pool()

    return (result.uploaded + result.updated) > 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Fast upload for DPOR data')
    parser.add_argument('csv_file', help='CSV file to upload')
    args = parser.parse_args()

    if not Path(args.csv_file).exists():
        print(f"❌ File not found: {args.csv_file}")
        sys.exit(1)

    success = upload_dpor_data(args.csv_file)
    sys.exit(0 if success else 1)