def build_html_table(kpis, report_date):

    def section(title):
        return f"""
        <tr>
            <td colspan="2"
                style="padding:10px;font-weight:bold;
                       background-color:#fff3cd;color:#000;">
                {title}
            </td>
        </tr>
        """

    def row(label, value, indent=False):

        padding_left = "30px" if indent else "8px"

        return f"""
        <tr>
            <td style="padding:8px 8px 8px {padding_left};
                       border:1px solid #ccc;text-align:right;">
                {label}
            </td>

            <td style="padding:8px;border:1px solid #ccc;text-align:right;">
                {value}
            </td>
        </tr>
        """

    rows = ""

    rows += row("Total Searches", format_int(kpis["core"]["Total Searches"]), True)
    rows += row("Total Users", format_int(kpis["core"]["Total Users"]), True)
    rows += row("Engagement %", format_pct(kpis["core"]["Engagement %"]), True)
    rows += row("Conversion %", format_pct(kpis["core"]["Conversion %"]), True)

    rows += section("Search Distribution – Region")
    for k, v in kpis["search_region_pct"].items():
        rows += row(k, format_pct(v))

    rows += section("Search Distribution – Platform")
    for k, v in kpis["search_platform_pct"].items():
        rows += row(k, format_pct(v))

    rows += section("Engagement Rate – Region")
    for k, v in kpis["engagement_region_pct"].items():
        rows += row(k, format_pct(v))

    rows += section("Engagement Rate – Platform")
    for k, v in kpis["engagement_platform_pct"].items():
        rows += row(k, format_pct(v))

    return f"""
    <html>
    <body style="font-family:Arial, sans-serif;">

        <table style="border-collapse:collapse;border:1px solid #ccc;">

            <tr style="background-color:#393f86;color:#ffffff;font-weight:bold;">
                <th style="padding:10px;border:1px solid #ccc;text-align:left;">
                    KPI
                </th>

                <th style="padding:10px;border:1px solid #ccc;text-align:right;">
                    {report_date}
                </th>
            </tr>

            {rows}

        </table>

    </body>
    </html>
    """
