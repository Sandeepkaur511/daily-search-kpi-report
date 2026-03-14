import json
import psycopg2
import pandas as pd
from pathlib import Path
from emailer import send_failure_email

BASE_DIR = Path(__file__).resolve().parent.parent



def check_table_freshness(conn):
    """
    Checks if underlying tables have T-1 data.
    Returns a list of tables missing data.
    """

    freshness_checks = [
        (
            "im_datamart_bigquery.fact_bigquery_search_web_data",
            "date(search_web_date)"
        ),
        (
            "im_datamart_bigquery.fact_bigquery_android_ios_search_data",
            "date(search_date)"
        ),
        (
            "im_dwh_rpt.fact_dir_query",
            "date(date_r)"
        ),
        (
            "im_dwh_rpt.fact_c2c_records",
            "date(c2c_call_time)"
        ),
        (
            "im_dwh_rpt.fact_c2c_records_unidentified",
            "date(c2c_call_time)"
        )
    ]

    missing_tables = []
    cursor = conn.cursor()

    for table, date_col in freshness_checks:
        query = f"""
        SELECT 1
        FROM {table}
        WHERE {date_col} = date(getdate() + interval '330 minutes') - 4
        LIMIT 1
        """

        cursor.execute(query)
        row = cursor.fetchone()

        if row is None:
            missing_tables.append(table)

    cursor.close()
    return missing_tables


from emailer import send_failure_email

def get_redshift_df():
    creds_path = BASE_DIR / "config" / "redshift_creds.json"
    sql_path = BASE_DIR / "sql" / "base_query.sql"

    try:
        # Load creds
        with open(creds_path) as f:
            creds = json.load(f)

        # Load SQL
        with open(sql_path) as f:
            query = f.read()

        # Connect
        conn = psycopg2.connect(
            host=creds["host"],
            port=creds["port"],
            dbname=creds["dbname"],
            user=creds["user"],
            password=creds["password"]
        )

        print("Connected to Redshift")

        # ------------------------------------
        # 🔍 DATA FRESHNESS CHECK (T-1)
        # ------------------------------------
        missing_tables = check_table_freshness(conn)

        if missing_tables:
            report_date = (
                pd.to_datetime("today")
                .tz_localize("UTC")
                .tz_convert("Asia/Kolkata")
                .normalize()
                - pd.Timedelta(days=4)
            ).strftime("%d-%b-%Y")

            error_msg = (
                f"T-1 data missing for date {report_date}\n\n"
                "Tables not refreshed:\n"
                + "\n".join(missing_tables)
            )

            send_failure_email(error_msg)
            raise Exception(error_msg)

        # ------------------------------------
        # MAIN QUERY
        # ------------------------------------
        df = pd.read_sql(query, conn)
        conn.close()

        print(f"Fetched {len(df)} rows")
        return df

    except Exception as e:
        # If anything else fails
        send_failure_email(str(e))
        raise
