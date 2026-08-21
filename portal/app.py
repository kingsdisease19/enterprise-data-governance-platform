"""
app.py

Enterprise Data Governance Platform - Streamlit Governance Portal
A single interface for browsing the governance repository built in
Sprint 7.1-7.4 (data assets, dictionary, glossary, ownership,
classification, quality, policies, lineage, issues).

Usage:
    streamlit run portal/app.py
"""

import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

# ---------------------------------------------------------
# Database connection
# ---------------------------------------------------------

DB_USER = "postgres"
DB_PASSWORD = os.environ.get("PG_PASSWORD", "YOUR_PASSWORD_HERE")
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "governance_platform"

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


def run_query(sql):
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn)


# ---------------------------------------------------------
# Page setup
# ---------------------------------------------------------

st.set_page_config(page_title="Enterprise Data Governance Portal", layout="wide")

st.sidebar.title("Governance Portal")
page = st.sidebar.radio(
    "Navigate",
    [
        "Governance Dashboard",
        "Data Catalog",
        "Data Dictionary",
        "Business Glossary",
        "Ownership & Stewardship",
        "Data Classification",
        "Data Quality Monitoring",
        "Governance Policies",
        "Data Lineage",
        "Governance Issues",
    ],
)

# ---------------------------------------------------------
# 1. Governance Dashboard (overview / landing page)
# ---------------------------------------------------------

if page == "Governance Dashboard":
    st.title("Enterprise Data Governance Platform")
    st.caption("A single portal for data discovery, quality, and governance oversight")

    assets = run_query("SELECT * FROM data_assets")
    issues = run_query("SELECT * FROM governance_issues")
    rules = run_query("SELECT * FROM data_quality_rules")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Registered Data Assets", len(assets))
    col2.metric("Open Governance Issues", len(issues[issues["status"] == "Open"]))
    col3.metric("Quality Rules Defined", len(rules))
    col4.metric("Critical Severity Rules", len(rules[rules["severity"] == "Critical"]))

    st.subheader("Assets by Criticality")
    st.bar_chart(assets["criticality"].value_counts())

    st.subheader("Recent Governance Issues")
    st.dataframe(issues, use_container_width=True)

# ---------------------------------------------------------
# 2. Data Catalog
# ---------------------------------------------------------

elif page == "Data Catalog":
    st.title("Data Catalog")
    st.caption("Browse all registered data assets")

    assets = run_query("SELECT * FROM data_assets")
    search = st.text_input("Search by asset name")
    if search:
        assets = assets[assets["asset_name"].str.contains(search, case=False)]

    st.dataframe(assets, use_container_width=True)

# ---------------------------------------------------------
# 3. Data Dictionary
# ---------------------------------------------------------

elif page == "Data Dictionary":
    st.title("Data Dictionary")
    st.caption("Column-level definitions across all datasets")

    dictionary = run_query("SELECT * FROM data_dictionary")
    if dictionary.empty:
        st.warning("No entries found. The data_dictionary table needs to be populated.")
    else:
        dataset_filter = st.selectbox(
            "Filter by dataset", ["All"] + sorted(dictionary["dataset_name"].unique().tolist())
        )
        if dataset_filter != "All":
            dictionary = dictionary[dictionary["dataset_name"] == dataset_filter]
        st.dataframe(dictionary, use_container_width=True)

# ---------------------------------------------------------
# 4. Business Glossary
# ---------------------------------------------------------

elif page == "Business Glossary":
    st.title("Business Glossary")
    st.caption("Shared organizational definitions")

    glossary = run_query("SELECT term, definition FROM business_glossary ORDER BY term")
    search = st.text_input("Search a term")
    if search:
        glossary = glossary[glossary["term"].str.contains(search, case=False)]

    for _, row in glossary.iterrows():
        st.markdown(f"**{row['term']}** — {row['definition']}")

# ---------------------------------------------------------
# 5. Ownership & Stewardship
# ---------------------------------------------------------

elif page == "Ownership & Stewardship":
    st.title("Data Ownership & Stewardship")
    st.caption("Who is accountable for each data asset")

    query = """
        SELECT a.asset_name, o.owner_name, o.department AS owner_dept,
               s.steward_name, s.department AS steward_dept
        FROM data_assets a
        JOIN data_owners o ON a.asset_id = o.asset_id
        JOIN data_stewards s ON a.asset_id = s.asset_id
        ORDER BY a.asset_name
    """
    st.dataframe(run_query(query), use_container_width=True)

# ---------------------------------------------------------
# 6. Data Classification
# ---------------------------------------------------------

elif page == "Data Classification":
    st.title("Data Classification")
    st.caption("Sensitivity and criticality of each asset")

    assets = run_query("SELECT asset_name, classification, criticality FROM data_assets")

    classification_filter = st.multiselect(
        "Filter by classification",
        options=sorted(assets["classification"].unique().tolist()),
        default=sorted(assets["classification"].unique().tolist()),
    )
    filtered = assets[assets["classification"].isin(classification_filter)]
    st.dataframe(filtered, use_container_width=True)

# ---------------------------------------------------------
# 7. Data Quality Monitoring
# ---------------------------------------------------------

elif page == "Data Quality Monitoring":
    st.title("Data Quality Monitoring")
    st.caption("Live results from the data quality engine")

    findings = run_query("SELECT * FROM quality_findings")

    avg_score = findings["pass_rate"].mean()
    st.metric("Overall Quality Score", f"{avg_score:.2f}%")

    st.subheader("Score by Dimension")
    st.bar_chart(findings.groupby("dimension")["pass_rate"].mean())

    st.subheader("Failed Rules")
    failed = findings[findings["violations"] > 0]
    st.dataframe(failed, use_container_width=True)

# ---------------------------------------------------------
# 8. Governance Policies
# ---------------------------------------------------------

elif page == "Governance Policies":
    st.title("Governance Policies")
    st.caption("Rules governing how data must be handled")

    policies = run_query("SELECT * FROM governance_policies")

    for _, row in policies.iterrows():
        with st.expander(row["policy_name"]):
            st.write(row["description"])
            linked = run_query(f"""
                SELECT a.asset_name FROM policy_asset_links pal
                JOIN data_assets a ON pal.asset_id = a.asset_id
                WHERE pal.policy_id = {row['policy_id']}
            """)
            st.write("Applies to:", ", ".join(linked["asset_name"].tolist()))

# ---------------------------------------------------------
# 9. Data Lineage
# ---------------------------------------------------------

elif page == "Data Lineage":
    st.title("Data Lineage")
    st.caption("Trace each asset's journey from source to portal")

    assets = run_query("SELECT asset_id, asset_name FROM data_assets")
    selected_asset = st.selectbox("Select an asset", assets["asset_name"].tolist())
    asset_id = int(assets[assets["asset_name"] == selected_asset]["asset_id"].iloc[0])

    lineage = run_query(f"""
        SELECT stage_order, stage_name, stage_description
        FROM data_lineage
        WHERE asset_id = {asset_id}
        ORDER BY stage_order
    """)

    for _, row in lineage.iterrows():
        st.markdown(f"**Stage {row['stage_order']}: {row['stage_name']}**")
        st.write(row["stage_description"])
        st.divider()

# ---------------------------------------------------------
# 10. Governance Issues
# ---------------------------------------------------------

elif page == "Governance Issues":
    st.title("Governance Issues")
    st.caption("Open and resolved data quality/governance problems")

    query = """
        SELECT a.asset_name, i.issue_description, i.severity, i.status, i.recommendation
        FROM governance_issues i
        JOIN data_assets a ON i.asset_id = a.asset_id
        ORDER BY i.severity
    """
    issues = run_query(query)

    status_filter = st.selectbox("Filter by status", ["All"] + sorted(issues["status"].unique().tolist()))
    if status_filter != "All":
        issues = issues[issues["status"] == status_filter]

    st.dataframe(issues, use_container_width=True)