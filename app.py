# ==========================================================
# CONFLICT OBSERVATORY – MAIN APPLICATION
# ==========================================================
# Streamlit application core
#
# Responsibilities:
# - Data loading
# - Temporal preparation
# - Analytical filters
# - Strategic dashboard
# - Module navigation
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import os
import hashlib
import uuid
import base64

from streamlit_folium import st_folium

from modules.statistical_module import render_statistical_module
from modules.methodology_module import render_methodology
from modules.TOO_module import render_overview_map
from modules.Geospatial_analysis_module import (
    render_analytical_map,
    render_sector_pressure_map,
    render_regional_activity_map,
    render_control_zone_map,
    render_operational_corridor_map
)
from modules.table_module import render_table_module
from modules.report_builder import (
    generate_csv, 
    generate_citation_txt, 
    generate_bibtex, 
    generate_ris, 
    generate_mla,
    generate_chicago,
    generate_numbered,
    generate_html_report
)

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Western Sahara War Archive (2020–2024)",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "### Western Sahara War Archive\nA Digital Humanities research project by Jorge Teixeira (CEAUP)."
    }
)

# ==========================================================
# PREMIUM CSS INJECTION
# ==========================================================

st.markdown("""
<style>
    /* Styling for the Sidebar */
    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(128, 128, 128, 0.2);
        width: 442px !important;
        min-width: 442px !important;
        max-width: 442px !important;
    }
    
    /* Elegant Sidebar Headers */
    [data-testid="stSidebarNav"] h1, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    /* Enhancing Multiselect appearance */
    .stMultiSelect, .stSelectbox, .stRadio {
        border-radius: 8px !important;
    }

    /* Style for the Select All Checkboxes */
    .stCheckbox {
        padding-bottom: 0px !important;
        margin-bottom: -5px !important;
    }
    
    .stCheckbox label div p {
        font-size: 11px !important;
        font-style: italic;
        opacity: 0.7;
    }

    /* Expander styling */
    .st-emotion-cache-p5msec {
        border-radius: 10px !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
    }

    /* Small text for methodological sidebar section */
    .framework-text {
        font-size: 0.8rem !important;
        line-height: 1.3 !important;
        opacity: 0.9;
    }
    
    .framework-text h3 {
        font-size: 0.9rem !important;
        margin-top: 10px !important;
        margin-bottom: 5px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================================
# GLOBAL UNIQUE KEY SYSTEM
# ==========================================================

_visual_counter = 0

def get_unique_key(prefix: str = "viz") -> str:
    """
    Generate a globally unique, stable widget key.

    Uses a monotonically incrementing counter to produce deterministic
    keys that remain stable across reruns as long as render order is unchanged.

    Parameters
    ----------
    prefix : str
        Human-readable prefix to identify the widget type (e.g. 'selectbox').

    Returns
    -------
    str
        A unique key string in the format '<prefix>_<counter>'.
    """
    global _visual_counter
    _visual_counter += 1
    return f"{prefix}_{_visual_counter}"

def st_selectbox_unique(label: str, options: list, **kwargs) -> object:
    """Wrapper for st.selectbox that auto-assigns a unique key if none is provided."""
    if "key" not in kwargs:
        kwargs["key"] = get_unique_key("selectbox")
    return st.selectbox(label, options, **kwargs)

def st_multiselect_unique(label: str, options: list, default: list = None, **kwargs) -> list:
    """Wrapper for st.multiselect that auto-assigns a unique key if none is provided."""
    if "key" not in kwargs:
        kwargs["key"] = get_unique_key("multiselect")
    return st.multiselect(label, options, default=default, **kwargs)

def st_radio_unique(label: str, options: list, **kwargs) -> object:
    """Wrapper for st.radio that auto-assigns a unique key if none is provided."""
    if "key" not in kwargs:
        kwargs["key"] = get_unique_key("radio")
    return st.radio(label, options, **kwargs)

_original_st_folium = st_folium
def st_folium_unique(map_object, **kwargs) -> dict:
    """Wrapper for st_folium that auto-assigns a unique key if none is provided."""
    if "key" not in kwargs:
        kwargs["key"] = get_unique_key("folium")
    return _original_st_folium(map_object, **kwargs)

st_folium = st_folium_unique

# ==========================================================
# ARCHIVAL INFRASTRUCTURE (DATA & HELPERS)
# ==========================================================

@st.cache_data
def load_events() -> pd.DataFrame:
    """
    Load and pre-process the conflict event dataset from CSV.

    Reads the archival CSV, parses dates, cleans coordinate strings,
    and converts all temporal columns to integer types.
    Results are cached by Streamlit to avoid redundant I/O on reruns.

    Returns
    -------
    pd.DataFrame
        Fully cleaned and typed event dataframe ready for analysis.
    """
    df = pd.read_csv("data/Matrix_Database_2020_2024.csv", sep=";", low_memory=False)

    df["Event_Date"] = pd.to_datetime(df["Event_Date"], dayfirst=True, errors="coerce")
    df["N_of_Event"] = pd.to_numeric(df["N_of_Event"], errors="coerce").fillna(0)

    def clean_coord(val: object, pos_suffix: str, neg_suffix: str) -> float:
        """Parse a coordinate string with cardinal direction suffix to float."""
        if pd.isna(val) or not isinstance(val, str): return 0.0
        val = val.replace("°", "")
        if pos_suffix in val: return float(val.replace(pos_suffix, ""))
        if neg_suffix in val: return -float(val.replace(neg_suffix, ""))
        try: return float(val)
        except: return 0.0

    df["Meso_Level_Latitude"] = df["Meso_Level_Latitude"].apply(lambda x: clean_coord(x, "N", "S"))
    df["Meso_Level_Longitude"] = df["Meso_Level_Longitude"].apply(lambda x: clean_coord(x, "E", "W"))
    
    # Convert temporal columns to numeric/int safely
    temp_cols = [
        "Calender_Year", "Calender_Month", "Calender_Quarter", "Calender_Semester", "Calender_Week",
        "Conflict_Year", "Conflict_Month", "Conflict_Quarter", "Conflict_Semester", "Conflict_Week"
    ]
    for c in temp_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)
    
    return df

def sort_sectors(sectors: list) -> list:
    """
    Sort sector IDs numerically (e.g. S1, S2, ..., S13).

    Extracts the numeric suffix from each sector label and sorts
    accordingly, avoiding the alphabetical mismatch of 'S10' < 'S2'.

    Parameters
    ----------
    sectors : list
        List of sector ID strings (e.g. ['S3', 'S10', 'S1']).

    Returns
    -------
    list
        Sorted list of sector IDs in natural numeric order.
    """
    def get_num(s: str) -> int:
        """Extract the numeric suffix from a sector ID string."""
        if not isinstance(s, str): return 0
        num_part = ''.join(filter(str.isdigit, s))
        return int(num_part) if num_part else 0
    return sorted(sectors, key=get_num)

df = load_events()

# ==========================================================
# INSTITUTIONAL HEADER
# ==========================================================

st.title("Western Sahara War Archive (2020–2024)")
st.markdown("### Interactive Geospatial Conflict Observatory")
st.markdown("*Note: This information is subject to continuous update and institutional review.*")
st.markdown("[Visit Project Page](https://westernsaharawararchive.com/)")

# ==========================================================
# CENTRALIZED NAVIGATION
# ==========================================================

menu = st.radio(
    "Explore the Observatory",
    [
        "Theatre of Operations Overview", 
        "Strategic Bird's-Eye View",
        "Table/Database",
        "Geospatial Conflict Analysis", 
        "Analytical Framework", 
        "Methodological Reference",
        "Documents",
        "About Us"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

# ==========================================================
# GLOBAL SIDEBAR FILTERS
# ==========================================================

st.sidebar.header("Global Analytical Filters")

with st.sidebar:
    st.markdown("---")
    
    # Global Reset Button
    if st.button("**Reset All Filters**", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    # Selection Summary Placeholder (will be filled after filters calculation)
    summary_placeholder = st.empty()
    st.markdown("---")
    
    with st.expander("**Temporal Framework**", expanded=True):
        time_mode = st_radio_unique(
            "Select Framework", 
            ["Conflict Time", "Civil Time"],
            key="global_time_framework"
        )
        year_col = "Conflict_Year" if time_mode == "Conflict Time" else "Calender_Year"
        
        available_years = sorted(df[year_col].dropna().unique())
        sel_all_years = st.checkbox("Select All Years", value=True, key="sel_all_years")
        selected_years = st_multiselect_unique(
            "Select Year(s)", 
            available_years, 
            default=available_years if sel_all_years else [],
            key="global_years_filter"
        )
        
        st.markdown("---")
        
        # Quarter Filter
        q_col = "Conflict_Quarter" if time_mode == "Conflict Time" else "Calender_Quarter"
        available_quarters = sorted(df[q_col].dropna().unique())
        selected_quarters = st_multiselect_unique(
            "Select Quarter(s)", 
            available_quarters,
            default=available_quarters,
            key="global_quarter_filter"
        )
        
        # Semester Filter
        sem_col = "Conflict_Semester" if time_mode == "Conflict Time" else "Calender_Semester"
        available_semesters = sorted(df[sem_col].dropna().unique())
        selected_semesters = st_multiselect_unique(
            "Select Semester(s)", 
            available_semesters,
            default=available_semesters,
            key="global_semester_filter"
        )
        
        # Season Filter
        sea_col = "Conflict_Season" if time_mode == "Conflict Time" else "Calender_Season"
        available_seasons = sorted(df[sea_col].dropna().unique())
        selected_seasons = st_multiselect_unique(
            "Select Season(s)", 
            available_seasons,
            default=available_seasons,
            key="global_season_filter"
        )
    
    with st.expander("**Territorial Structure**", expanded=False):
        st.markdown("### Macro Level")
        available_mrs = sorted(df["Macro_Level_ID"].unique())
        sel_all_mrs = st.checkbox("Select All MRs", value=True, key="sel_all_mrs")
        mr_filter = st_multiselect_unique(
            "Military Region", 
            available_mrs,
            default=available_mrs if sel_all_mrs else [],
            key="global_mr_filter"
        )
        
        st.markdown("---")
        st.markdown("### Meso Level")
        sector_options = sort_sectors(df["Meso_Level_ID"].unique())
        sel_all_sectors = st.checkbox("Select All Sectors", value=True, key="sel_all_sectors")
        sector_filter = st_multiselect_unique(
            "Sector", 
            sector_options,
            default=sector_options if sel_all_sectors else [],
            key="global_sector_filter"
        )
    
    with st.expander("**Actor & Initiative**", expanded=False):
        if "Attacker" in df.columns:
            # Filter out empty or NA values for the UI
            available_actors = sorted([str(x) for x in df["Attacker"].dropna().unique() if str(x).strip() != ""])
            actor_filter = st_multiselect_unique(
                "Initiating Party (Attacker)", 
                available_actors,
                default=available_actors,
                key="global_actor_filter"
            )
        else:
            actor_filter = []

# Global data filtering
df_f = df[
    (df[year_col].isin(selected_years)) &
    (df[q_col].isin(selected_quarters)) &
    (df[sem_col].isin(selected_semesters)) &
    (df[sea_col].isin(selected_seasons))
]

if mr_filter:
    df_f = df_f[df_f["Macro_Level_ID"].isin(mr_filter)]
if sector_filter:
    df_f = df_f[df_f["Meso_Level_ID"].isin(sector_filter)]
if actor_filter:
    # Preserve Z records (Peace Days) even when filtering by actor
    # so statistics modules like 'Operational Tempo' can compute Z00 ratio.
    df_f = df_f[
        (df_f["Attacker"].isin(actor_filter)) | 
        (df_f["N_of_Event"] == 0)
    ]

def get_timeframe_str() -> str:
    """Generate a readable string of the current temporal selection."""
    years = sorted(selected_years)
    if not years: return "No Period Selected"
    if len(years) == 1: return str(years[0])
    return f"{min(years)}-{max(years)}"

timeframe_str = get_timeframe_str()

# Populate the Selection Summary Widget at the top
summary_placeholder.markdown(f"""
<div style="background-color: rgba(128, 128, 128, 0.05); border-radius: 10px; padding: 15px; border: 1px solid rgba(128, 128, 128, 0.1);">
    <p style="margin:0; font-size: 0.8rem; opacity: 0.7;">Selection Summary</p>
    <h3 style="margin:5px 0; font-size: 1.2rem;">{int(df_f['N_of_Event'].sum())} <span style="font-size: 0.8rem; font-weight: normal;">Events found</span></h3>
    <p style="margin:0; font-size: 0.75rem;"><b>Logic:</b> {time_mode}</p>
</div>
<div style="margin-top: 15px;">
    <h3 style="margin-bottom: 5px; font-size: 1.1rem; font-weight: bold;">Filters</h3>
    <p style="font-size: 0.9rem; line-height: 1.4; font-weight: 500;">Use these filters to refine the data across all observatory modules.</p>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# EXPORT & REPORTING TOOLS
# ==========================================================
with st.sidebar.expander("**Export & Citation Tools**", expanded=True):
    st.markdown("<p style='font-size: 0.85em; color: gray;'>Downloads reflect currently active filters.</p>", unsafe_allow_html=True)
    
    # 1. Raw Dataset
    st.download_button(
        label="Download Dataset (CSV)",
        data=generate_csv(df_f),
        file_name=f"WSWA_Data_{timeframe_str.replace('-','_')}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    # 2. Comprehensive HTML Report
    current_hash = hash(timeframe_str + str(len(df_f)))
    if "report_hash" not in st.session_state or st.session_state.report_hash != current_hash:
        st.session_state.report_html = None
        st.session_state.report_hash = current_hash
        
    if st.session_state.report_html is None:
        if st.button("Compile Full Report (HTML/PDF)", use_container_width=True, help="Extracts ALL Maps, Charts, and Metrics. Takes ~10s."):
            with st.spinner("Compiling full analytical report..."):
                st.session_state.report_html = generate_html_report(df_f, timeframe_str, time_mode)
            st.rerun()
    else:
        st.download_button(
            label="Download Full Report",
            data=st.session_state.report_html,
            file_name=f"WSWA_Report_{timeframe_str.replace('-','_')}.html",
            mime="text/html",
            use_container_width=True
        )
        if st.button("Reset Report", use_container_width=True):
            st.session_state.report_html = None
            st.rerun()
    
    st.markdown("---")
    st.markdown("<b style='font-size: 0.85em;'>Scientific Citation</b>", unsafe_allow_html=True)
    
    # 3. BibTeX
    st.download_button(
        label="BibTeX",
        data=generate_bibtex(timeframe_str),
        file_name="wswa_citation.bib",
        mime="text/plain",
        use_container_width=True
    )
    # 4. RIS
    st.download_button(
        label="RIS",
        data=generate_ris(timeframe_str),
        file_name="wswa_citation.ris",
        mime="text/plain",
        use_container_width=True
    )
    # 5. TXT APA
    st.download_button(
        label="APA Format (TXT)",
        data=generate_citation_txt(df_f, timeframe_str),
        file_name="wswa_apa_citation.txt",
        mime="text/plain",
        use_container_width=True
    )
    # 6. MLA
    st.download_button(
        label="MLA 9th (TXT)",
        data=generate_mla(timeframe_str),
        file_name="wswa_mla_citation.txt",
        mime="text/plain",
        use_container_width=True
    )
    # 7. Chicago
    st.download_button(
        label="Chicago 17th (TXT)",
        data=generate_chicago(timeframe_str),
        file_name="wswa_chicago_citation.txt",
        mime="text/plain",
        use_container_width=True
    )
    # 8. Numbered / IEEE
    st.download_button(
        label="Numbered (TXT)",
        data=generate_numbered(timeframe_str),
        file_name="wswa_numbered_citation.txt",
        mime="text/plain",
        use_container_width=True
    )

st.markdown("---")


# ==========================================================
# COLOR SYSTEM
# ==========================================================

region_colors = {
    "MR1": "#E2EFD9",
    "MR2": "#FEF2CB",
    "MR3": "#FBE4D5"
}

sector_colors = {
    "S1": "#BED5B4", "S2": "#90BB7A", "S3": "#68A242", "S4": "#568736",
    "S5": "#FFDDAD", "S6": "#FFCA69", "S7": "#EFB300", "S8": "#C89600",
    "S9": "#FF6161", "S10": "#FF3737", "S11": "#FF1D1D", "S12": "#D20000",
    "S13": "#A80000"
}

# ==========================================================
# CONFLICT TIMELINE (FUNCTION)
# ==========================================================

def render_timeline():
    st.subheader("Conflict Chronology Since 13 November 2020")
    
    timeline_data = pd.DataFrame({
        "Phase":[
            "Ceasefire Breakdown (Guerguerat)",
            "Initial Low Intensity Exchange Phase",
            "Sustained Attritional Phase",
            "Current Operational Phase"
        ],
        "Start":[pd.to_datetime(d) for d in [
            "2020-11-13",
            "2021-01-01",
            "2022-01-01",
            "2023-01-01"
        ]],
        "End":[
            pd.to_datetime("2020-12-31"),
            pd.to_datetime("2021-12-31"),
            pd.to_datetime("2022-12-31"),
            pd.Timestamp.today()
        ]
    })
    
    fig_timeline = px.timeline(
        timeline_data,
        x_start="Start",
        x_end="End",
        y="Phase"
    )
    
    fig_timeline.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_timeline, width="stretch")

# ==========================================================
# ABOUT US (TEAM & PROJECT)
# ==========================================================

def render_about_us():
    st.header("About the Project")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Western Sahara War Archive (WSWA)
        The **Western Sahara War Archive** is a Digital Humanities research project dedicated to the documentation and geospatial analysis of the conflict in Western Sahara since the breakdown of the ceasefire on November 13, 2020.
        
        Our mission is to provide an open-access, academically rigorous platform for researchers, analysts, and the public to understand the operational dynamics and human impact of this protracted war.
        """)
        
        st.subheader("Project Team")
        
        team_col1, team_col2 = st.columns(2)
        
        with team_col1:
            st.image("https://www.cienciavitae.pt/portal/FB17-55DF-0E11/foto", width=150) # Fallback image if possible or just text
            st.markdown("""
            **Jorge Teixeira**  
            *Lead Investigator & PI*  
            [CiênciaVitae Profile](https://www.cienciavitae.pt/portal/FB17-55DF-0E11)
            """)
            
        with team_col2:
            st.markdown("""
            <br><br>
            """, unsafe_allow_html=True) # Spacer
            st.markdown("""
            **Isabel Lourenço**  
            *Researcher & Contributor*  
            [CiênciaVitae Profile](https://www.cienciavitae.pt/portal/6E15-6D4A-6324)
            """)
            
    with col2:
        st.info("**Support the Research**")
        st.markdown("""
        This archive is hosted at the **Centro de Estudos Africanos da Universidade do Porto (CEAUP)**. 
        
        For inquiries or data contributions, please visit our [official website](https://westernsaharawararchive.com/).
        """)
        
        st.subheader("Multimedia")
        st.markdown("[![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/channel/UCDtLsJ05L5EblXSzfcKbRkA)")

# ==========================================================
# DOCUMENTS (FILE MANAGER)
# ==========================================================

def render_documents():
    st.header("Institutional & Research Documents")
    st.markdown("""
    This repository contains official documents and authorizations granted by the **Sahrawi Press Service (SPS)** and the **Sahrawi Arab Democratic Republic (SADR)**. 
    
    These documents formally authorize the research team to utilize, archive, analyse, and publish conflict data, official communiqués, and news released through their institutional platforms for academic and historical documentation.
    """)
    
    docs_dir = "docs"
    if not os.path.exists(docs_dir):
        st.error(f"Directory '{docs_dir}' not found.")
        return
        
    files = [f for f in os.listdir(docs_dir) if os.path.isfile(os.path.join(docs_dir, f))]
    
    if not files:
        st.info("No documents currently available in this section.")
        return
        
    for file in files:
        col1, col2 = st.columns([3, 1])
        file_path = os.path.join(docs_dir, file)
        with col1:
            st.write(f"**{file}**")
        with col2:
            with open(file_path, "rb") as f:
                st.download_button(
                    label="Download PDF",
                    data=f,
                    file_name=file,
                    mime="application/pdf",
                    key=f"dl_{file}"
                )
        st.markdown("---")

# Logic replaced and moved to the infrastructure section above

# Rendering Logic - Replaced by global sidebar and direct module calls in selection blocks

# ==========================================================
# RENDERING LOGIC
# ==========================================================

if menu == "Theatre of Operations Overview":
    st.header("Theatre of Operations Overview")
    
    # --- Strategic Metrics ---
    with st.container():
        m1, m2, m3, m4 = st.columns(4)
        total_ev = int(df_f["N_of_Event"].sum())
        active_sectors = df_f[df_f["N_of_Event"] > 0]["Meso_Level_ID"].nunique()
        total_sectors = df_f["Meso_Level_ID"].nunique()
        territorial_spread = (active_sectors / total_sectors) * 100 if total_sectors > 0 else 0
        
        # Combat Pressure (Avg events per day in selection)
        days_in_selection = df_f["Event_Date"].nunique()
        strategic_tempo = total_ev / days_in_selection if days_in_selection > 0 else 0

        m1.metric("Total Conflict Events", total_ev)
        m2.metric("Sectors with combat", active_sectors)
        m3.metric("Territorial Spread", f"{territorial_spread:.1f}%")
        m4.metric("Strategic Tempo (Ev/Day)", f"{strategic_tempo:.2f}")
    
    st.markdown("---")
    st.subheader("B1: Full Operational Theater Overview")
    render_overview_map(timeframe_str, mode="B1")
    st.caption("**How to read (B1):** Displays the comprehensive geographic layout of the operational theater. © Jorge Teixeira")
    
    st.markdown("---")
    render_timeline()
    st.caption("**How to read (Timeline):** Displays key milestones and chronological progression.")

elif menu == "Strategic Bird's-Eye View":
    st.header("Strategic Bird's-Eye View")
    st.markdown("Detailed strategic layers (B2-B6) for a comprehensive overview of the conflict's spatial structure.")
    
    b_tabs = st.tabs([
        "B2: Territorial Control", 
        "B3: Military Regions", 
        "B4: Operational Sectors", 
        "B5: Military Wall", 
        "B6: Logistics & Hydro"
    ])
    
    with b_tabs[0]:
        st.subheader("B2: Territorial Control Map")
        render_overview_map(timeframe_str, mode="B2")
        st.caption("**Methodology (B2):** Highlights legal sovereignty and actual territorial control zones (Macro Level).")

    with b_tabs[1]:
        st.subheader("B3: Military Regions Map")
        render_overview_map(timeframe_str, mode="B3")
        st.caption("**Methodology (B3):** Visualizes the strategic command boundaries (Macro Regions).")

    with b_tabs[2]:
        st.subheader("B4: Operational Sectors Map")
        render_overview_map(timeframe_str, mode="B4")
        st.caption("**Methodology (B4):** Displays the meso-level tactical division of the theater.")

    with b_tabs[3]:
        st.subheader("B5: Moroccan Military Wall Map")
        render_overview_map(timeframe_str, mode="B5")
        st.caption("**Methodology (B5):** Focuses on the defensive system and barrier infrastructure.")

    with b_tabs[4]:
        st.subheader("B6: Logistics & Strategic Geography")
        render_overview_map(timeframe_str, mode="B6")
        st.caption("**Methodology (B6):** Correlates terrain, hydrography, and logistics with the theater of war.")

elif menu == "Table/Database":
    # Global filters are already applied to df_f
    render_table_module(df_f)

elif menu == "Geospatial Conflict Analysis":
    st.header("Geospatial Analytical Dashboard")
    
    # Global filters are already applied to df_f
    if df_f.empty:
        st.warning("No events for the selected filters.")
    else:
        # Use unique key based on filter hash to prevent reload state persistence
        selection_hash = hashlib.md5(str(selected_years + mr_filter + sector_filter + actor_filter).encode()).hexdigest()[:8]
        
        # Dashboard Header with Metrics
        st.metric("Total Engagements (Filtered)", int(df_f["N_of_Event"].sum()))
        
        # Build Dynamic Map Title/Summary
        years_list = sorted(df_f["Calender_Year"].dropna().unique()) if "Calender_Year" in df_f.columns else []
        year_str = f"{int(years_list[0])} - {int(years_list[-1])}" if len(years_list) > 1 else str(int(years_list[0])) if years_list else "All Years"
        
        mrs_list = sorted(df_f["Macro_Level_ID"].dropna().unique())
        mr_str = ", ".join(mrs_list) if len(mrs_list) > 0 and len(mrs_list) < 3 else "All Regions"
        
        sec_list = sorted(df_f["Meso_Level_ID"].dropna().unique())
        sec_str = "All Sectors" if len(sec_list) > 5 else ", ".join(sec_list)
        
        st.markdown(f"<p style='text-align: center; color: grey; margin-top: -20px;'><b>Period:</b> {year_str} &nbsp;|&nbsp; <b>Regions:</b> {mr_str} &nbsp;|&nbsp; <b>Sectors:</b> {sec_str}</p>", unsafe_allow_html=True)

        # Analytical Perspective Tabs (G-Suite)
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "G1: Control Zones", "G2: Sector Pressure", "G3: Regional Activity", 
            "G4: Tactical Density", "G5: Hotspots", "G6: Wall Pressure", 
            "G7: Corridors", "G8: Actor Activity"
        ])
        
        with tab1:
            st.markdown(f"### G1: Control Zone Conflict Map | {timeframe_str}")
            render_control_zone_map(df_f, map_key=f"control_{selection_hash}", timeframe=timeframe_str)
            st.caption(f"**How to read (G1):** Highlights whether engagements fall inside the Moroccan-controlled zone, SADR areas, or the Buffer Strip. © Jorge Teixeira")
        
        with tab2:
            st.markdown(f"### G2: Sector Pressure Map | {timeframe_str}")
            render_sector_pressure_map(df_f, map_key=f"sector_{selection_hash}", timeframe=timeframe_str)
            st.caption(f"**How to read (G2):** A choropleth map coloring the 13 defined military Sectors according to their total events. © Jorge Teixeira")
            
        with tab3:
            st.markdown(f"### G3: Regional Activity Map | {timeframe_str}")
            render_regional_activity_map(df_f, map_key=f"region_{selection_hash}", timeframe=timeframe_str)
            st.caption(f"**How to read (G3):** Aggregates conflict events at the Strategic Level across the 3 Macro Regions (MR1, MR2, MR3). © Jorge Teixeira")
            
        with tab4:
            st.markdown(f"### G4: Tactical Density Map | {timeframe_str}")
            render_analytical_map(df_f, mode="density", map_key=f"heat_{selection_hash}", timeframe=timeframe_str)
            st.info(f"**Methodology (G4):** Translates event coordinates into a kernel density layer (Heatmap). Red identifies peak kinetic friction. © Jorge Teixeira")
            
        with tab5:
            st.markdown(f"### G5: Conflict Hotspots Map | {timeframe_str}")
            render_analytical_map(df_f, mode="hotspot", map_key=f"hotspot_{selection_hash}", timeframe=timeframe_str)
            st.info(f"**Methodology (G5):** Uses cluster analysis to pinpoint high-frequency tactical nodes. © Jorge Teixeira")
            
        with tab6:
            st.markdown(f"### G6: Tactical Wall Pressure Map | {timeframe_str}")
            render_analytical_map(df_f, mode="wall_pressure", map_key=f"wall_p_{selection_hash}", timeframe=timeframe_str)
            st.info(f"**Methodology (G6):** Filters and visualizes engagements occurring in the immediate vicinity of the Moroccan Military Wall. © Jorge Teixeira")
            
        with tab7:
            st.markdown(f"### G7: Operational Corridors Map | {timeframe_str}")
            render_operational_corridor_map(df_f, map_key=f"corridor_{selection_hash}", timeframe=timeframe_str)
            st.info(f"**Methodology (G7):** Spatially correlates transit lines and water sources with conflict nodes to identify logistical chokepoints. © Jorge Teixeira")
            
        with tab8:
            st.markdown(f"### G8: Actor Activity Distribution Map | {timeframe_str}")
            render_analytical_map(df_f, mode="actor", map_key=f"actor_{selection_hash}", timeframe=timeframe_str)
            st.info(f"**Methodology (G8):** Categorizes and maps incidents by the initiating party to reveal territorial initiative patterns. © Jorge Teixeira")


elif menu == "Analytical Framework":
    st.subheader("Conflict Intensity & Analytical Framework")
    # Global filters (df_f) are already applied. 
    # Now we add the Phase 9 Analytical Perspectives:
    
    analysis_mode = st.radio(
        "**Analytical Perspective**", 
        ["Accumulated Period", "Single Year Focus"],
        horizontal=True
    )
    
    if analysis_mode == "Single Year Focus":
        target_year = st.selectbox("Select Year for Focus", selected_years)
        df_stat = df_f[df_f[year_col] == target_year]
    else:
        df_stat = df_f.copy()

    # ==========================================================
    # STRUCTURAL INTENSITY CLASSIFICATION
    # ==========================================================
    sector_totals = df_stat.groupby("Meso_Level_ID")["N_of_Event"].sum().reset_index()
    if not sector_totals.empty:
        low_q, high_q = sector_totals["N_of_Event"].quantile([0.33, 0.66])
        def classify_intensity(x):
            if x <= low_q: return "Low Intensity"
            elif x <= high_q: return "Medium Intensity"
            else: return "High Intensity"
        
        sector_totals["Intensity_Class"] = sector_totals["N_of_Event"].apply(classify_intensity)
        
        # Merge back to df_stat for use in statistical module
        df_stat = df_stat.merge(sector_totals[["Meso_Level_ID", "Intensity_Class"]], on="Meso_Level_ID", how="left")
        
        # Elegant multiselect for Intensity
        intensity_filter = st.multiselect(
            "Filter by Structural Intensity Level", 
            ["Low Intensity", "Medium Intensity", "High Intensity"],
            placeholder="Showing all sectors..."
        )
        
        if intensity_filter:
            valid_sectors = sector_totals[sector_totals["Intensity_Class"].isin(intensity_filter)]["Meso_Level_ID"]
            df_stat = df_stat[df_stat["Meso_Level_ID"].isin(valid_sectors)]

    if df_stat.empty:
        st.warning("No events correspond to the selected analytical configuration.")
    else:
        # Ensure columns for Statistical Module
        for col, default in [("Micro_Level_Name", "Unknown"), ("Meso_Level_Name", "Unknown"),
                            ("Macro_Level_Name", "Unknown"), ("Country", "Unknown")]:
            if col not in df_stat.columns:
                df_stat[col] = default

        # Display Metrics
        num_years = max(len(df_stat[year_col].unique()), 1)
        total_ev = df_stat["N_of_Event"].sum()
        avg_annual = total_ev / num_years

        m_col1, m_col2 = st.columns(2)
        m_col1.metric("Total Events (Analytical Selection)", int(total_ev))
        m_col2.metric("Avg Events (per year in selection)", f"{avg_annual:.2f}")

        render_statistical_module(df_stat, timeframe=timeframe_str)

elif menu == "Methodological Reference":
    render_methodology()

elif menu == "Documents":
    render_documents()

elif menu == "About Us":
    render_about_us()

# ==========================================================
# FOOTER (LOGOS)
# ==========================================================

st.markdown("---")
footer_col1, footer_col2, footer_col3, footer_col4 = st.columns([1,1,1,3])
logo_path = os.path.join("assets", "logos")

with footer_col1:
    if os.path.exists(os.path.join(logo_path, "logo_wswa.png")):
        with open(os.path.join(logo_path, "logo_wswa.png"), "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            st.markdown(f'<div style="background: white; padding: 12px; border-radius: 10px; display: inline-block; box-shadow: 0 4px 8px rgba(0,0,0,0.3);"><img src="data:image/png;base64,{encoded}" width="180"></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("[![YouTube](https://img.shields.io/badge/YouTube-red?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/channel/UCDtLsJ05L5EblXSzfcKbRkA)")

with footer_col2:
    if os.path.exists(os.path.join(logo_path, "logo_ceaup.jpg")):
        with open(os.path.join(logo_path, "logo_ceaup.jpg"), "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            st.markdown(f'<div style="background: white; padding: 12px; border-radius: 10px; display: inline-block; box-shadow: 0 4px 8px rgba(0,0,0,0.3);"><img src="data:image/jpeg;base64,{encoded}" width="180"></div>', unsafe_allow_html=True)
    st.markdown("<p style='font-size:20px; margin-top:8px;'><b>Host Institution</b></p>", unsafe_allow_html=True)

with footer_col3:
    if os.path.exists(os.path.join(logo_path, "logo_fct.jpg")):
        with open(os.path.join(logo_path, "logo_fct.jpg"), "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            st.markdown(f'<div style="background: white; padding: 12px; border-radius: 10px; display: inline-block; box-shadow: 0 4px 8px rgba(0,0,0,0.3);"><img src="data:image/jpeg;base64,{encoded}" width="180"></div>', unsafe_allow_html=True)
    st.markdown("<p style='font-size:20px; margin-top:8px;'><b>Funding Agency</b></p>", unsafe_allow_html=True)

with footer_col4:
    st.markdown("""
    <div style="font-size: 18px; line-height: 1.8; color: #EEE; background: rgba(0,0,0,0.2); padding: 20px; border-radius: 10px;">
        <b style="color: #FFF;">© 2024 Jorge Teixeira / Western Sahara War Archive.</b> All rights reserved.<br>
        <i style="color: #CCC;">Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)</i><br><br>
        This work is funded by Portuguese national funds through **FCT – Fundação para a Ciência e a Tecnologia, I.P.**, 
        under the Project **UIDB/00495/2020** (DOI: <a href="https://doi.org/10.54499/UIDB/00495/2020" target="_blank" style="color: #64B5F6; text-decoration: none; font-weight: bold;">10.54499/UIDB/00495/2020</a>).
    </div>
    """, unsafe_allow_html=True)

