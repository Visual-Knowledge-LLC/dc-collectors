#!/usr/bin/env python3
"""
Database Lookup Utilities for VK Collectors
=============================================
Reusable utilities for looking up header mappings, agency information,
and other database-driven configurations for collectors.
"""

import re
import logging
from typing import Optional, Dict, Any
from pathlib import Path
import sys

logger = logging.getLogger(__name__)


class VKDatabaseLookup:
    """Database lookup utilities for VK collectors"""

    def __init__(self):
        """Initialize database connection"""
        self.engine = None
        self._setup_database_connection()

    def _setup_database_connection(self):
        """Setup database connection using VK MCP tools"""
        # We'll use MCP tools for database access
        self.engine = "mcp"  # Flag to indicate we're using MCP tools
        logger.info("Using MCP tools for database access")

    def get_header_mapping(self, dataset_key: str, bbb_id: str = None) -> Optional[Dict[str, Any]]:
        """
        Get header mapping for a dataset from the database.

        Args:
            dataset_key: Dataset identifier (e.g., "0402", "contractors")
            bbb_id: BBB ID for additional filtering (optional)

        Returns:
            Dictionary with header mapping information or None if not found
        """
        if self.engine != "mcp":
            logger.warning("MCP database access not available")
            return None

        # Format the key like the old scraper (add spaces between numbers and letters)
        formatted_key = re.sub(r'(\d+)([a-zA-Z]+)', r'\1 \2', dataset_key).upper()

        # Build query for header_mappings table
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
            hm.agency_url AS "Agency URL",
            hm.county AS "County"
        FROM public.header_mappings AS hm
        JOIN licensing_agencies la ON hm.agency_name = la.agency_name
        WHERE hm.dataset LIKE '{formatted_key}%'
        """

        # Add BBB ID filter if provided
        if bbb_id:
            query += f" AND la.bbb_id = '{bbb_id}'"

        try:
            # Use external function to execute SQL via MCP
            result = self._execute_mcp_sql(query)

            if result and len(result) > 0:
                # Convert first result to dictionary
                row = result[0]
                header_mapping_dict = {
                    "Agency ID": row.get("Agency ID"),
                    "Agency Name": row.get("Agency Name"),
                    "State Established": row.get("State Established"),
                    "Business Name": row.get("Business Name"),
                    "Street": row.get("Street"),
                    "Zip": row.get("Zip"),
                    "Date Established": row.get("Date Established"),
                    "Category": row.get("Category"),
                    "License Number": row.get("License Number"),
                    "Phone Number": row.get("Phone Number"),
                    "Owner First Name": row.get("Owner First Name"),
                    "Owner Last Name": row.get("Owner Last Name"),
                    "Expiration Date": row.get("Expiration Date"),
                    "License Status": row.get("License Status"),
                    "TOB ID": row.get("TOB ID"),
                    "Agency URL": row.get("Agency URL"),
                    "County": row.get("County")
                }
                logger.debug(f"Found header mapping for {formatted_key}: {header_mapping_dict.get('Agency Name')}")
                return header_mapping_dict
            else:
                logger.warning(f"No header mapping found for dataset: {formatted_key}")
                return None

        except Exception as e:
            logger.error(f"Database query failed for {formatted_key}: {e}")
            return None

    def _execute_mcp_sql(self, query: str):
        """
        Execute SQL query via MCP tools.
        This is a placeholder - actual implementation needs to be external.
        """
        # This needs to be implemented externally since MCP tools aren't available in this context
        raise NotImplementedError("MCP SQL execution must be implemented externally")

    def get_agency_info(self, agency_name: str, bbb_id: str = None) -> Optional[Dict[str, Any]]:
        """
        Get agency information from licensing_agencies table.

        Args:
            agency_name: Agency name to search for
            bbb_id: BBB ID for filtering (optional)

        Returns:
            Dictionary with agency information or None if not found
        """
        if not self.engine:
            logger.warning("No database connection available")
            return None

        query = """
        SELECT bbb_id, agency_name, agency_id, agency_url, tob_id, state,
               agency_contact_email, agency_contact_phone, agency_address
        FROM licensing_agencies
        WHERE agency_name ILIKE %s
        """

        params = [f'%{agency_name}%']
        if bbb_id:
            query += " AND bbb_id = %s"
            params.append(bbb_id)

        try:
            from sqlalchemy import text
            with self.engine.connect() as connection:
                result = connection.execute(text(query), params)
                agency_info = result.fetchone()

                if agency_info:
                    agency_dict = {column: value for column, value in zip(result.keys(), agency_info)}
                    logger.debug(f"Found agency info for {agency_name}")
                    return agency_dict
                else:
                    logger.warning(f"No agency info found for: {agency_name}")
                    return None

        except Exception as e:
            logger.error(f"Database query failed for agency {agency_name}: {e}")
            return None

    def list_datasets_for_bbb(self, bbb_id: str) -> list:
        """
        List all available datasets for a BBB ID.

        Args:
            bbb_id: BBB ID to search for

        Returns:
            List of dataset names
        """
        if not self.engine:
            logger.warning("No database connection available")
            return []

        query = """
        SELECT DISTINCT hm.dataset
        FROM public.header_mappings AS hm
        JOIN licensing_agencies la ON hm.agency_name = la.agency_name
        WHERE la.bbb_id = %s
        ORDER BY hm.dataset
        """

        try:
            from sqlalchemy import text
            with self.engine.connect() as connection:
                result = connection.execute(text(query), [bbb_id])
                datasets = [row[0] for row in result.fetchall()]
                logger.info(f"Found {len(datasets)} datasets for BBB {bbb_id}")
                return datasets

        except Exception as e:
            logger.error(f"Database query failed for BBB {bbb_id}: {e}")
            return []


# Global instance for easy importing
db_lookup = VKDatabaseLookup()


def get_header_mapping(dataset_key: str, bbb_id: str = None) -> Optional[Dict[str, Any]]:
    """Convenience function for getting header mappings"""
    return db_lookup.get_header_mapping(dataset_key, bbb_id)


def get_agency_info(agency_name: str, bbb_id: str = None) -> Optional[Dict[str, Any]]:
    """Convenience function for getting agency information"""
    return db_lookup.get_agency_info(agency_name, bbb_id)


if __name__ == "__main__":
    # Test the module
    import argparse

    parser = argparse.ArgumentParser(description='Test VK Database Lookups')
    parser.add_argument('--dataset', help='Test header mapping for dataset')
    parser.add_argument('--agency', help='Test agency lookup')
    parser.add_argument('--bbb-id', default='0241', help='BBB ID for filtering')
    parser.add_argument('--list-datasets', action='store_true', help='List all datasets for BBB')

    args = parser.parse_args()

    lookup = VKDatabaseLookup()

    if args.dataset:
        mapping = lookup.get_header_mapping(args.dataset, args.bbb_id)
        if mapping:
            print(f"Header mapping for {args.dataset}:")
            for key, value in mapping.items():
                print(f"  {key}: {value}")
        else:
            print(f"No mapping found for {args.dataset}")

    if args.agency:
        info = lookup.get_agency_info(args.agency, args.bbb_id)
        if info:
            print(f"Agency info for {args.agency}:")
            for key, value in info.items():
                print(f"  {key}: {value}")
        else:
            print(f"No agency info found for {args.agency}")

    if args.list_datasets:
        datasets = lookup.list_datasets_for_bbb(args.bbb_id)
        print(f"Datasets for BBB {args.bbb_id}:")
        for dataset in datasets:
            print(f"  {dataset}")