-- Add missing DPOR header mappings for BBB 0241 (DC region)
-- Generated from analysis of DPOR download files vs existing header_mappings
-- Date: 2025-09-19

-- Note: These INSERT statements assume the agency names already exist in licensing_agencies table
-- The field mappings follow the same pattern as existing entries for each board

-- ============================================================================
-- Board for Barbers and Cosmetology variants (1301 series)
-- ============================================================================

-- 1301B - Barber variant
INSERT INTO public.header_mappings (
    agency_name, state, business_name, street, zip, date_established,
    category, license_number, phone_number, owner_first_name, owner_last_name,
    expiration_date, license_status, email, dataset, tobid, agency_url, county
) VALUES (
    'VA - DPOR - Board for Barbers and Cosmetology',
    'VA',
    'Name',
    'MAILING ADDRESS',
    'ZIP CODE',
    'NA',
    'LICENSE SPECIALTY',
    'CERTIFICATE #',
    'NA',
    'NA',
    'NA',
    'EXPIRES',
    'STATUS',
    NULL,
    '1301 B',
    '',
    'https://www.dpor.virginia.gov/',
    'NA'
);

-- 1301BBI - Barber Instructor variant
INSERT INTO public.header_mappings (
    agency_name, state, business_name, street, zip, date_established,
    category, license_number, phone_number, owner_first_name, owner_last_name,
    expiration_date, license_status, email, dataset, tobid, agency_url, county
) VALUES (
    'VA - DPOR - Board for Barbers and Cosmetology',
    'VA',
    'Name',
    'MAILING ADDRESS',
    'ZIP CODE',
    'NA',
    'LICENSE SPECIALTY',
    'CERTIFICATE #',
    'NA',
    'NA',
    'NA',
    'EXPIRES',
    'STATUS',
    NULL,
    '1301 BBI',
    '',
    'https://www.dpor.virginia.gov/',
    'NA'
);

-- 1301MB - Master Barber variant
INSERT INTO public.header_mappings (
    agency_name, state, business_name, street, zip, date_established,
    category, license_number, phone_number, owner_first_name, owner_last_name,
    expiration_date, license_status, email, dataset, tobid, agency_url, county
) VALUES (
    'VA - DPOR - Board for Barbers and Cosmetology',
    'VA',
    'Name',
    'MAILING ADDRESS',
    'ZIP CODE',
    'NA',
    'LICENSE SPECIALTY',
    'CERTIFICATE #',
    'NA',
    'NA',
    'NA',
    'EXPIRES',
    'STATUS',
    NULL,
    '1301 MB',
    '',
    'https://www.dpor.virginia.gov/',
    'NA'
);

-- 1301MBBI - Master Barber Instructor variant
INSERT INTO public.header_mappings (
    agency_name, state, business_name, street, zip, date_established,
    category, license_number, phone_number, owner_first_name, owner_last_name,
    expiration_date, license_status, email, dataset, tobid, agency_url, county
) VALUES (
    'VA - DPOR - Board for Barbers and Cosmetology',
    'VA',
    'Name',
    'MAILING ADDRESS',
    'ZIP CODE',
    'NA',
    'LICENSE SPECIALTY',
    'CERTIFICATE #',
    'NA',
    'NA',
    'NA',
    'EXPIRES',
    'STATUS',
    NULL,
    '1301 MBBI',
    '',
    'https://www.dpor.virginia.gov/',
    'NA'
);

-- ============================================================================
-- Board for Waterworks and Sewage System Professionals (1940/1942/1944 series)
-- ============================================================================

-- 1940 variants
INSERT INTO public.header_mappings (agency_name, state, business_name, street, zip, date_established, category, license_number, phone_number, owner_first_name, owner_last_name, expiration_date, license_status, email, dataset, tobid, agency_url, county)
VALUES
('VA - DPOR - Board for Waterworks and Sewage System Professionals', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '1940 JAOE', '', 'https://www.dpor.virginia.gov/', 'NA'),
('VA - DPOR - Board for Waterworks and Sewage System Professionals', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '1940 JCOE', '', 'https://www.dpor.virginia.gov/', 'NA'),
('VA - DPOR - Board for Waterworks and Sewage System Professionals', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '1940 MAOE', '', 'https://www.dpor.virginia.gov/', 'NA'),
('VA - DPOR - Board for Waterworks and Sewage System Professionals', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '1940 MCOE', '', 'https://www.dpor.virginia.gov/', 'NA');

-- 1942 variants
INSERT INTO public.header_mappings (agency_name, state, business_name, street, zip, date_established, category, license_number, phone_number, owner_first_name, owner_last_name, expiration_date, license_status, email, dataset, tobid, agency_url, county)
VALUES
('VA - DPOR - Board for Waterworks and Sewage System Professionals', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '1942 JAOO', '', 'https://www.dpor.virginia.gov/', 'NA'),
('VA - DPOR - Board for Waterworks and Sewage System Professionals', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '1942 JCOO', '', 'https://www.dpor.virginia.gov/', 'NA'),
('VA - DPOR - Board for Waterworks and Sewage System Professionals', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '1942 MAOO', '', 'https://www.dpor.virginia.gov/', 'NA'),
('VA - DPOR - Board for Waterworks and Sewage System Professionals', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '1942 MCJA', '', 'https://www.dpor.virginia.gov/', 'NA'),
('VA - DPOR - Board for Waterworks and Sewage System Professionals', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '1942 MCOO', '', 'https://www.dpor.virginia.gov/', 'NA');

-- 1944 variants
INSERT INTO public.header_mappings (agency_name, state, business_name, street, zip, date_established, category, license_number, phone_number, owner_first_name, owner_last_name, expiration_date, license_status, email, dataset, tobid, agency_url, county)
VALUES
('VA - DPOR - Board for Waterworks and Sewage System Professionals', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '1944 JAOI', '', 'https://www.dpor.virginia.gov/', 'NA'),
('VA - DPOR - Board for Waterworks and Sewage System Professionals', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '1944 JCOI', '', 'https://www.dpor.virginia.gov/', 'NA'),
('VA - DPOR - Board for Waterworks and Sewage System Professionals', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '1944 MAOI', '', 'https://www.dpor.virginia.gov/', 'NA'),
('VA - DPOR - Board for Waterworks and Sewage System Professionals', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '1944 MCJA', '', 'https://www.dpor.virginia.gov/', 'NA'),
('VA - DPOR - Board for Waterworks and Sewage System Professionals', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '1944 MCOI', '', 'https://www.dpor.virginia.gov/', 'NA');

-- ============================================================================
-- Board for Contractors (2705 variants)
-- ============================================================================

INSERT INTO public.header_mappings (agency_name, state, business_name, street, zip, date_established, category, license_number, phone_number, owner_first_name, owner_last_name, expiration_date, license_status, email, dataset, tobid, agency_url, county)
VALUES
('VA - DPOR - Board for Contractors', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '2705 A', '', 'https://www.dpor.virginia.gov/', 'NA'),
('VA - DPOR - Board for Contractors', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '2705 B', '', 'https://www.dpor.virginia.gov/', 'NA'),
('VA - DPOR - Board for Contractors', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '2705 C', '', 'https://www.dpor.virginia.gov/', 'NA');

-- ============================================================================
-- Board for Professional Soil Scientists, Wetland Professionals, and Geologists (2801 variants)
-- ============================================================================

INSERT INTO public.header_mappings (agency_name, state, business_name, street, zip, date_established, category, license_number, phone_number, owner_first_name, owner_last_name, expiration_date, license_status, email, dataset, tobid, agency_url, county)
VALUES
('VA - DPOR - Board for Professional Soil Scientists, Wetland Professionals, and Geologists', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '2801 CPG', '', 'https://www.dpor.virginia.gov/', 'NA'),
('VA - DPOR - Board for Professional Soil Scientists, Wetland Professionals, and Geologists', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '2801 GIT', '', 'https://www.dpor.virginia.gov/', 'NA');

-- ============================================================================
-- Real Estate Appraisers Board (4001 variants)
-- ============================================================================

INSERT INTO public.header_mappings (agency_name, state, business_name, street, zip, date_established, category, license_number, phone_number, owner_first_name, owner_last_name, expiration_date, license_status, email, dataset, tobid, agency_url, county)
VALUES
('VA - DPOR - Real Estate Appraisers Board', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '4001 C_ACT', '', 'https://www.dpor.virginia.gov/', 'NA'),
('VA - DPOR - Real Estate Appraisers Board', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '4001 C_INACT', '', 'https://www.dpor.virginia.gov/', 'NA'),
('VA - DPOR - Real Estate Appraisers Board', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '4001 G_ACT', '', 'https://www.dpor.virginia.gov/', 'NA'),
('VA - DPOR - Real Estate Appraisers Board', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '4001 G_INACT', '', 'https://www.dpor.virginia.gov/', 'NA'),
('VA - DPOR - Real Estate Appraisers Board', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '4001 L_ACT', '', 'https://www.dpor.virginia.gov/', 'NA'),
('VA - DPOR - Real Estate Appraisers Board', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '4001 L_INACT', '', 'https://www.dpor.virginia.gov/', 'NA');

-- ============================================================================
-- Auctioneers Board (2905-2908)
-- Note: These already exist in the database with more descriptive dataset names,
-- but the collector looks for simple numeric patterns like "2905" not "2905 Auctioneer Individual"
-- ============================================================================

INSERT INTO public.header_mappings (agency_name, state, business_name, street, zip, date_established, category, license_number, phone_number, owner_first_name, owner_last_name, expiration_date, license_status, email, dataset, tobid, agency_url, county)
VALUES
('VA - DPOR - Auctioneers Board', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '2905', '', 'https://www.dpor.virginia.gov/', 'NA'),
('VA - DPOR - Auctioneers Board', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '2906', '', 'https://www.dpor.virginia.gov/', 'NA'),
('VA - DPOR - Auctioneers Board', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '2907', '', 'https://www.dpor.virginia.gov/', 'NA'),
('VA - DPOR - Auctioneers Board', 'VA', 'Name', 'MAILING ADDRESS', 'ZIP CODE', 'NA', 'LICENSE SPECIALTY', 'CERTIFICATE #', 'NA', 'NA', 'NA', 'EXPIRES', 'STATUS', NULL, '2908', '', 'https://www.dpor.virginia.gov/', 'NA');

-- ============================================================================
-- Summary: Added 33 new header mappings
-- ============================================================================
-- 4 mappings for 1301 variants (Board for Barbers and Cosmetology)
-- 14 mappings for 1940/1942/1944 variants (Board for Waterworks and Sewage System Professionals)
-- 3 mappings for 2705 variants (Board for Contractors)
-- 2 mappings for 2801 variants (Board for Professional Soil Scientists)
-- 6 mappings for 4001 variants (Real Estate Appraisers Board)
-- 4 mappings for 2905-2908 (Auctioneers Board)