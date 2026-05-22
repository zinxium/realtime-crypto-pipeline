-- ============================================================
-- Contrôles qualité données — ECOMMERCE_DB
-- ============================================================

USE DATABASE ECOMMERCE_DB;

-- ── Vue de monitoring qualité ────────────────────────────────
CREATE OR REPLACE VIEW ANALYTICS.DATA_QUALITY_REPORT AS
SELECT
    'RAW_ORDERS'                                    AS table_name,
    COUNT(*)                                        AS total_rows,
    SUM(CASE WHEN order_id IS NULL THEN 1 END)      AS null_order_ids,
    SUM(CASE WHEN customer_id IS NULL THEN 1 END)   AS null_customer_ids,
    SUM(CASE WHEN order_status IS NULL THEN 1 END)  AS null_statuses,
    COUNT(DISTINCT order_id)                        AS unique_orders,
    COUNT(*) - COUNT(DISTINCT order_id)             AS duplicate_orders
FROM RAW.RAW_ORDERS

UNION ALL

SELECT
    'RAW_CUSTOMERS'                                         AS table_name,
    COUNT(*)                                                AS total_rows,
    SUM(CASE WHEN customer_id IS NULL THEN 1 END)           AS null_order_ids,
    SUM(CASE WHEN customer_unique_id IS NULL THEN 1 END)    AS null_customer_ids,
    SUM(CASE WHEN customer_state IS NULL THEN 1 END)        AS null_statuses,
    COUNT(DISTINCT customer_id)                             AS unique_orders,
    COUNT(*) - COUNT(DISTINCT customer_id)                  AS duplicate_orders
FROM RAW.RAW_CUSTOMERS

UNION ALL

SELECT
    'RAW_CRYPTO_PRICES'                                 AS table_name,
    COUNT(*)                                            AS total_rows,
    SUM(CASE WHEN id IS NULL THEN 1 END)                AS null_order_ids,
    SUM(CASE WHEN current_price IS NULL THEN 1 END)     AS null_customer_ids,
    SUM(CASE WHEN last_updated IS NULL THEN 1 END)      AS null_statuses,
    COUNT(DISTINCT id)                                  AS unique_orders,
    0                                                   AS duplicate_orders
FROM RAW.RAW_CRYPTO_PRICES;

-- ── Vérification des résultats ───────────────────────────────
SELECT * FROM ANALYTICS.DATA_QUALITY_REPORT;