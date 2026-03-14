from db import get_datawarehouse_df
from kpi_engine import compute_kpis, build_html_table
from emailer import send_report_email


def run_pipeline():

    # -----------------------------
    # Fetch data from warehouse
    # -----------------------------
    df = get_datawarehouse_df()

    # -----------------------------
    # Compute KPIs
    # -----------------------------
    kpis = compute_kpis(df)

    # -----------------------------
    # Extract report date
    # -----------------------------
    report_date = df["event_date"].iloc[0].strftime("%d-%b-%Y")

    # -----------------------------
    # Build HTML report
    # -----------------------------
    html = build_html_table(kpis, report_date)

    # -----------------------------
    # Send report email
    # -----------------------------
    send_report_email(html, report_date)


if __name__ == "__main__":
    run_pipeline()
