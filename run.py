#!/usr/bin/env python3
"""
Main runner for DC license data collectors.
"""

import sys
import argparse
import logging
from datetime import datetime
from pathlib import Path

try:
    from vk_api_utils import SlackNotifier
except ImportError:
    print("Warning: vk-api-utils not installed. Run: pip install git+https://github.com/Visual-Knowledge-LLC/vk-api-utils.git")
    SlackNotifier = None


def setup_logging(verbose=False):
    """Set up logging configuration."""
    log_level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def run_dc_business_licenses(slack=None):
    """Run DC Business License collector."""
    print("\n" + "="*70)
    print("  DC BUSINESS LICENSE COLLECTOR")
    print("="*70)

    if slack:
        slack.notify_progress("Starting DC Business License collector...")

    try:
        # TODO: Implement DC Business License collector
        print("DC Business License collector not yet implemented")

        if slack:
            slack.notify_warning("⚠️ DC Business License collector not yet implemented")

        return False

    except Exception as e:
        logging.error(f"Error in DC Business License collector: {e}")
        if slack:
            slack.notify_error("DC Business License collector failed", exception=e)
        return False


def run_all(slack=None):
    """Run all DC collectors."""
    print("\n" + "="*70)
    print("  RUNNING ALL DC COLLECTORS")
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    results = {
        'Business Licenses': run_dc_business_licenses(slack)
    }

    # Print summary
    print("\n" + "="*70)
    print("  SUMMARY")
    print("="*70)
    for collector, success in results.items():
        status = "✅ Success" if success else "❌ Failed"
        print(f"  {collector}: {status}")
    print("="*70)

    return all(results.values())


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="DC License Data Collectors")
    parser.add_argument(
        "collector",
        choices=["business", "all"],
        help="Which collector to run"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--slack",
        default="on",
        choices=["on", "off"],
        help="Enable/disable Slack notifications (default: on)"
    )

    args = parser.parse_args()

    # Set up logging
    setup_logging(args.verbose)

    # Set up Slack notifications
    slack = None
    if args.slack.lower() != "off" and SlackNotifier:
        slack = SlackNotifier("DC Collectors")
        slack.notify_start({
            "Collector": args.collector.upper(),
            "Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    # Run selected collector
    success = False
    try:
        if args.collector == "business":
            success = run_dc_business_licenses(slack)
        elif args.collector == "all":
            success = run_all(slack)

        # Send final notification
        if slack:
            if success:
                slack.notify_success("DC collectors completed successfully")
            else:
                slack.notify_warning("DC collectors completed with errors")

    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        if slack:
            slack.notify_error("DC collectors failed", exception=e)
        success = False

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()