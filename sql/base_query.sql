WITH unified_events AS (

-- =========================
-- WEB SEARCH EVENTS
-- =========================
SELECT
    DATE(event_timestamp) AS event_date,
    1 AS source_type,
    platform,
    CASE WHEN user_country = 'CountryA' THEN 1 ELSE 2 END AS country_flag,
    search_scope,
    city_tier,
    user_id,
    0 AS conversion_user_id,
    SUM(page_views) AS page_views,
    SUM(product_clicks) AS product_clicks,
    SUM(listing_clicks) AS listing_clicks,
    0 AS enquiries,
    0 AS calls
FROM (
    SELECT
        event_timestamp,
        platform,
        user_id,

        CASE
            WHEN page_url LIKE '%city:%'
              OR page_url LIKE '%city"":""%'
            THEN 'City'
            ELSE 'National'
        END AS search_scope,

        page_views,
        product_clicks,
        listing_clicks,

        CAST(
            CASE
                WHEN page_url LIKE '%tier"":""%'
                    THEN SPLIT_PART(SPLIT_PART(page_url,'tier"":""',2),'|',1)
                WHEN page_url LIKE '%tier:%'
                    THEN SPLIT_PART(SPLIT_PART(page_url,'tier:',2),'|',1)
                ELSE NULL
            END AS TEXT
        ) AS city_tier,

        user_country
    FROM analytics_schema.web_search_events
    WHERE DATE(event_timestamp) = DATE(CURRENT_DATE - INTERVAL '4 day')
      AND page_views < 10000
      AND product_clicks < 10000
      AND listing_clicks < 10000
) web
GROUP BY event_date, source_type, platform, country_flag,
         search_scope, city_tier, user_id


UNION ALL


-- =========================
-- APP SEARCH EVENTS
-- =========================
SELECT
    event_date,
    2 AS source_type,
    platform,
    country_flag,
    search_scope,
    city_tier,
    user_id,
    0 AS conversion_user_id,
    SUM(page_views),
    SUM(product_clicks),
    SUM(listing_clicks),
    0,
    0
FROM (
    SELECT
        event_timestamp AS event_date,
        platform,
        search_scope,
        CASE WHEN user_country = 'CountryA' THEN 1 ELSE 2 END AS country_flag,
        page_views,
        product_clicks,
        listing_clicks,
        user_id,

        CAST(
            CASE
                WHEN page_metadata LIKE '%tier"":""%'
                    THEN SPLIT_PART(SPLIT_PART(page_metadata,'tier"":""',2),'|',1)
                WHEN page_metadata LIKE '%tier:%'
                    THEN SPLIT_PART(SPLIT_PART(page_metadata,'tier:',2),'|',1)
                ELSE NULL
            END AS TEXT
        ) AS city_tier

    FROM analytics_schema.app_search_events
    WHERE DATE(event_timestamp) = DATE(CURRENT_DATE - INTERVAL '4 day')
) app
GROUP BY event_date, source_type, platform, country_flag,
         search_scope, city_tier, user_id


UNION ALL


-- =========================
-- ENQUIRY EVENTS
-- =========================
SELECT
    event_date,
    3 AS source_type,
    platform,
    country_flag,
    search_scope,
    city_tier,
    NULL AS user_id,
    conversion_user_id,
    0,
    0,
    0,
    SUM(enquiries),
    0
FROM analytics_schema.search_enquiry_events
WHERE DATE(event_date) = DATE(CURRENT_DATE - INTERVAL '4 day')
GROUP BY event_date, source_type, platform,
         country_flag, search_scope,
         city_tier, conversion_user_id


UNION ALL


-- =========================
-- CALL EVENTS
-- =========================
SELECT
    event_date,
    4 AS source_type,
    platform,
    country_flag,
    search_scope,
    city_tier,
    NULL,
    conversion_user_id,
    0,
    0,
    0,
    0,
    SUM(call_count)
FROM analytics_schema.search_call_events
WHERE DATE(event_date) = DATE(CURRENT_DATE - INTERVAL '4 day')
GROUP BY event_date, source_type, platform,
         country_flag, search_scope,
         city_tier, conversion_user_id

)


-- =========================
-- FINAL AGGREGATION
-- =========================
SELECT
    event_date,
    platform,
    conversion_user_id,
    user_id,

    CASE
        WHEN city_tier LIKE '1%' THEN 'Tier 1'
        WHEN city_tier LIKE '2%' THEN 'Tier 2'
        WHEN city_tier LIKE '3%' THEN 'Tier 3'
        WHEN search_scope = 'City' THEN 'Tier Unknown'
        ELSE search_scope
    END AS city_segment,

    SUM(page_views) AS total_pageviews,
    SUM(product_clicks) AS product_clicks,
    SUM(listing_clicks) AS listing_clicks,
    SUM(enquiries) AS enquiries,
    SUM(calls) AS calls

FROM unified_events
WHERE platform IN ('Mobile','Desktop','Android','iOS')

GROUP BY
    event_date,
    platform,
    city_segment,
    conversion_user_id,
    user_id
;
