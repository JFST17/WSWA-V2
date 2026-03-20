"""
TABLE MODULE
Western Sahara War Archive

Renders the interactive conflict event database table.

Inputs
------
df : pd.DataFrame
    Globally filtered dataframe from app.py. Contains all CSV columns
    after temporal standardization and coordinate cleaning.

Outputs
-------
None — renders Streamlit UI components (dataframe + CSV download button).
"""

import streamlit as st
import pandas as pd


def render_table_module(df: pd.DataFrame) -> None:
    """
    Render the full interactive conflict event database table.

    Displays all 33 CSV columns in the canonical archival order with
    clean human-readable headers. Provides a full-text search box and
    a CSV export button filtered to the current selection.

    Parameters
    ----------
    df : pd.DataFrame
        Filtered event dataframe from the global sidebar selections.

    Returns
    -------
    None
    """
    st.header("Conflict Event Database")
    st.info(f"© 2024 Jorge Teixeira | Archive Platform Database")
    st.markdown("Explore and filter the raw event data used in the archive.")

    # Summary count based on active filters
    st.info(f"Showing **{len(df)}** records based on current filters.")

    # Full-text search across all string columns
    search_query = st.text_input("Search in database (Location, Sector, Description...)", "")

    if search_query:
        mask = df.apply(
            lambda row: row.astype(str).str.contains(search_query, case=False).any(),
            axis=1
        )
        df_display = df[mask]
    else:
        df_display = df

    # Render the full database table with canonical column ordering
    st.dataframe(
        df_display,
        width='stretch',
        hide_index=True,
        column_order=[
            "ID", "Event_Date", "Attacker", "Attacked",
            "Conflict_Year", "Conflict_Month", "Conflict_Quarter", "Conflict_Semester",
            "Conflict_Season", "Conflict_Week", "Conflict_Day",
            "Calender_Year", "Calender_Month", "Calender_Quarter", "Calender_Semester",
            "Calender_Season", "Calender_Week", "Calender_Week_Day",
            "Micro_Level_Name", "N_of_Event", "Micro_Level_ID", "Meso_Level_ID",
            "Macro_Level_ID", "Mega_Level_ID",
            "Mega_Level_Name", "Macro_Level_Name", "Macro_Level_Geographical_Location",
            "Macro_Level_Latitude", "Macro_Level_Longitude",
            "Meso_Level_Name", "Meso_Level_Important_Location",
            "Meso_Level_Geographical_Location", "Meso_Level_Longitude",
            "Meso_Level_Latitude", "Meso_Level_MINURSO_control"
        ],
        column_config={
            "Event_Date": st.column_config.DateColumn("Event Date", format="DD/MM/YYYY"),
            "N_of_Event": st.column_config.NumberColumn("Events", format="%d"),
            "Macro_Level_Latitude": st.column_config.NumberColumn("Macro Latitude", format="%.4f"),
            "Macro_Level_Longitude": st.column_config.NumberColumn("Macro Longitude", format="%.4f"),
            "Meso_Level_Latitude": st.column_config.NumberColumn("Meso Latitude", format="%.4f"),
            "Meso_Level_Longitude": st.column_config.NumberColumn("Meso Longitude", format="%.4f"),
            # Canonical temporal column labels (Conflict Time)
            "Conflict_Year": "Conflict Year",
            "Conflict_Month": "Conflict Month",
            "Conflict_Quarter": "Conflict Quarter",
            "Conflict_Semester": "Conflict Semester",
            "Conflict_Season": "Conflict Season",
            "Conflict_Week": "Conflict Week",
            "Conflict_Day": "Conflict Day",
            # Canonical temporal column labels (Civil Time)
            "Calender_Year": "Civil Year",
            "Calender_Month": "Civil Month",
            "Calender_Quarter": "Civil Quarter",
            "Calender_Semester": "Civil Semester",
            "Calender_Season": "Civil Season",
            "Calender_Week": "Civil Week",
            "Calender_Week_Day": "Civil Week Day",
        }
    )

    # CSV export of the current filtered/searched selection
    csv = df_display.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download Selection as CSV",
        csv,
        "wswa_filtered_data.csv",
        "text/csv",
        key='download-csv'
    )
