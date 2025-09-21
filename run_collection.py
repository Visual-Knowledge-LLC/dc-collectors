#!/usr/bin/env python3
"""
Main runner script for DC collectors.
Runs all collectors for BBB 0241 (DC region).
"""

import sys
import logging
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main collection runner"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Run DC data collectors for BBB 0241',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all collectors
  %(prog)s

  # Run specific collector
  %(prog)s --collector dpor

  # Save to CSV only
  %(prog)s --save-csv

  # Upload to API (dry run)
  %(prog)s --upload --dry-run

  # Upload to API (live)
  %(prog)s --upload

  # Save and upload
  %(prog)s --save-csv --upload
        """
    )

    parser.add_argument('--collector', choices=['dpor', 'all'],
                        default='all', help='Which collector(s) to run')
    parser.add_argument('--save-csv', action='store_true',
                        help='Save collected data to CSV files')
    parser.add_argument('--upload', action='store_true',
                        help='Upload data to Visual Knowledge API')
    parser.add_argument('--dry-run', action='store_true',
                        help='Perform dry run (don\'t actually upload)')
    parser.add_argument('--headless', action='store_true', default=True,
                        help='Run Chrome in headless mode (default: True)')

    args = parser.parse_args()

    logger.info("=" * 70)
    logger.info("DC DATA COLLECTION RUNNER")
    logger.info("=" * 70)
    logger.info(f"Start time: {datetime.now()}")
    logger.info(f"BBB ID: 0241 (DC Region)")
    logger.info(f"Collector: {args.collector}")
    logger.info(f"Save CSV: {args.save_csv}")
    logger.info(f"Upload: {args.upload}")
    logger.info(f"Dry Run: {args.dry_run}")
    logger.info("=" * 70)

    total_records = 0
    collectors_run = []

    # Run DPOR collector
    if args.collector in ['dpor', 'all']:
        logger.info("\n" + "-" * 50)
        logger.info("Running VA DPOR Collector...")
        logger.info("-" * 50)

        try:
            from src.collectors.dpor.dpor_collector import VaDPORCollector

            collector = VaDPORCollector(headless=args.headless)
            data = collector.collect()

            if data:
                total_records += len(data)
                collectors_run.append(('VA DPOR', len(data)))

                # Save to CSV if requested
                if args.save_csv:
                    csv_file = collector.save_to_csv()
                    logger.info(f"✅ Data saved to: {csv_file}")

                # Upload to API if requested
                if args.upload:
                    success = collector.upload_to_api(dry_run=args.dry_run)
                    if success:
                        logger.info("✅ Upload completed successfully")
                    else:
                        logger.error("❌ Upload failed")
            else:
                logger.warning("⚠️ No data collected from VA DPOR")

        except Exception as e:
            logger.error(f"❌ Error running VA DPOR collector: {e}")
            import traceback
            traceback.print_exc()

    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("COLLECTION SUMMARY")
    logger.info("=" * 70)
    logger.info(f"Total records collected: {total_records}")
    logger.info("Collectors run:")
    for name, count in collectors_run:
        logger.info(f"  - {name}: {count} records")
    logger.info("=" * 70)
    logger.info(f"End time: {datetime.now()}")

    return 0 if total_records > 0 else 1


if __name__ == "__main__":
    sys.exit(main())