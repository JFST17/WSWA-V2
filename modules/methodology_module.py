"""
MÓDULO DE METODOLOGIA
Western Sahara War Archive

Este módulo apresenta ao público a metodologia científica do observatório, as fontes de dados e os arquivos digitais
utilizados no projeto.

Todo o conteúdo apresentado ao utilizador está em inglês, enquanto os comentários técnicos permanecem em português.
"""

import streamlit as st

def render_methodology():

    # ======================================================
    # PAGE TITLE
    # ======================================================

    st.header("Methodology")
    st.markdown("<b>Institutional Note:</b><br> The datasets and analyses presented here are subject to continuous update and archival review as new conflict data and primary documents are integrated. | © 2024–2026 Jorge Teixeira", unsafe_allow_html=True)

    # ======================================================
    # OBSERVATORY FRAMEWORK
    # ======================================================
    st.subheader("Observatory Framework")
    
    st.markdown("""
<b>Temporal Framework</b><br>
<dl>
<dt><b>Civil Time: </b></dt>
<dd>-Standard calendar (year/month). For external/diplomatic comparison.</dd>
<dt><b>Conflict Time: </b></dt> 
<dd>-Internal chronology of the war. For operational analysis.</dd>
</dl>
<b>Territorial Structure Countries (Mega)</b> The overarching geopolitical entity.<br>
<b>Military Regions (Macro)</b> Large operational strategic zones.<br>
<b>Sectors (Meso)</b> Tactical subdivisions within each Region.<br>
<b>Intensity Classification: </b> Sectors are classified into <b>Low, Medium, and High</b> based on relative distribution (quantiles). This ensures mathematical rather than arbitrary analysis.<br><br>

This observatory applies quantitative conflict analysis to study the dynamics of the war in Western Sahara.
The project combines historical documentation, military communiqués and structured datasets in order to produce spatial and temporal analysis of conflict events.<br><br>

The analytical framework focuses on three dimensions:
<ul>
<li>Conflict Intensity </li>
<li>Operational Tempo </li>
<li>Spatial Distribution</li>
</ul>
""", unsafe_allow_html=True)
    st.divider()
    # ======================================================
    # DATA SOURCES
    # ======================================================
    st.subheader("Data Sources")
    st.markdown(
    """
    The statistical dataset used in this observatory is derived from the systematic collection of official military communiqués and archival material related to the Western Sahara conflict.
    The database records daily attack events and allows the reconstruction of operational patterns across time and space.
    """
    )
    # --- Header Section ---
    st.title("Academic Resources")
    
    st.markdown(
        """
<b>Academic Publications & Research Outputs:</b>
<ul>
<li>• <b>Silva Teixeira, Jorge Fernando.</b> (2025). Tension Return to the Sands: An Analytical Framework for the Analysis of the Third Stage of the Western Sahara Conflict (2020–2024). Master's Thesis, University of Porto. [DOI: 10.5281/zenodo.18877015] (https://doi.org/10.5281/zenodo.18877015)</li>
<li>• <b>Teixeira, Jorge. (2024).</b> 'Western Sahara War Archives, Between Archives and GIS: How to Map a War Remotely'. Tifariti, no. 1, pp. 116–38. [DOI: 10.21747/3078-431X/tifa5] (https://doi.org/10.21747/3078-431X/tifa5)</li>
<li>• <b>Teixeira, Jorge. (2022). </b>'Statistical Report: 1st Semester of the II Western Sahara War'. African Studies Center of the University of Porto (CEAUP). [DOI: 10.5281/zenodo.17885545] (https://doi.org/10.5281/zenodo.17885545)</li>
<li>• <b>Teixeira, Jorge F. (2022). </b>'Project Monitoring Report: Western Sahara War Archives - A Monitoring Database for the II War in Western Sahara'. CEAUP / westernsaharawararchive.com. [DOI: 10.5281/zenodo.17885259] (https://doi.org/10.5281/zenodo.17885259)</li>
<li>• <b>Silva Teixeira, Jorge Fernando. </b>(2026). JFST17/Western-Sahara-War-Archives--WSWA-: WSWA Database_V1.1. [DOI: 10.5281/zenodo.19041041] (https://doi.org/10.5281/zenodo.19041041)</li>
</ul>
        """, unsafe_allow_html=True
    )
    st.divider()
    st.caption("All research outputs are archived via Zenodo to ensure long-term preservation, transparency, and scientific reproducibility.")
    # ======================================================
    # DIGITAL ARCHIVES
    # ======================================================
    st.subheader("Digital Archives")
    st.markdown(
    """
    This observatory is connected to a broader effort to create digital archives related to the Western Sahara conflict.

    These archives preserve historical documentation, official military communiqués and structured relational datasets.
    """
    )

    st.markdown(
    """
    • Western Sahara War Archive: https://westernsaharawararchive.com/
    """
    )

    st.info(
    """
    The Western Sahara War Archive publishes official war communiqués, maps and statistical material documenting the ongoing conflict.
    """
    )
    st.write("")
    # ======================================================
    # METHODOLOGICAL APPROACH
    # ======================================================
    st.subheader("Methodological Approach")
    st.markdown(
    """
The analytical framework combines methods from:
<ul> 
<li>Conflict Studies</li>
<li>Military History</li>
<li>Quantitative Event Analysis</li>
<li>Geospatial Analysis</li>
</ul>
Each event recorded in the database corresponds to a documented military attack reported in official communiqués.<br>

The database structure allows the reconstruction of:
<ul> 
<li>Operational Tempo</li>
<li>Campaign Dynamics</li>
<li>Seasonal Patterns</li>
<li>Spatial Distribution of Attacks</li>
</ul>

<b>Temporal Framework</b><br>
<dl>
<dt><b>Civil Time: </b></dt>
<dd>-Standard calendar (year/month). For external/diplomatic comparison.</dd>
<dt><b>Conflict Time: </b></dt> 
<dd>-Internal chronology of the war. For operational analysis.</dd>
</dl>
<dt><b>Territorial Structure Countries (Mega Level):</b></dt> <dd>The overarching geopolitical entity.</dd>
<dt><b>Military Regions (Macro Level):</b></dt> 
<dd>-Large operational strategic zones.</dd>
<dt><b>Sectors (Meso Level):</b></dt> 
<dd>-Tactical subdivisions within each Region.</dd>
<dt><b>Intensity Classification:</b></dt> 
<dd>-Sectors are classified into <b>Low, Medium, and High</b> based on relative distribution (quantiles). This ensures mathematical rather than arbitrary analysis.</dd><br><br>
    """, unsafe_allow_html=True
    )
    
    st.header("Digital Humanities Standards")
    st.markdown("""
The platform is developed following the **FAIR principles** (Findable, Accessible, Interoperable, Reusable):
<ul> 
<li>Zenodo Integration: Persistent DOIs for all datasets.</li>
<li>Analytical Catalog: Standardized identifiers [A1-A25], [G1-G8] and [I1-I5] for academic citation.</li>
<li>Transparency: Mathematical models and formulas are explicitly documented within each visualization.</li>
<li>Sustainability: Hosted within the institutional framework of CEAUP (University of Porto).</li>
</ul>
""", unsafe_allow_html=True)
    st.divider()
    # ======================================================
    # CITATION
    # ======================================================
    st.subheader("Citation")
    st.markdown(
    """
    If you use data or visualizations from this observatory in academic research, please cite the Zenodo datasets listed above and the Western Sahara War Archive.

    The datasets are archived with persistent DOI identifiers, ensuring long-term accessibility and reproducibility.
    """
    )
    # ======================================================
    # ANALYTICAL CATALOG
    # ======================================================
    st.write(" ")
    st.subheader("Analytical Catalog")
    st.markdown("The platform provides a comprehensive suite of indices, charts, and maps to dissect the conflict's tactical and strategic behavior.")
    
    with st.expander("1 — Strategic Indices (5)"):
        st.markdown("""
| # | Index | What it Measures |
|---|---|---|
| **I1** | Moroccan Military Wall Pressure Index | Military pressure on the defensive infrastructure |
| **I2** | Operational Intensity Index | Degree of engagement per sector |
| **I3** | Geographic Concentration (HHI) | Spatial dispersion vs concentration of conflict |
| **I4** | Conflict Saturation Index | Proportion of days with combat activity |
| **I5** | Shifting Center of Gravity | Spatio-temporal drift of the war's midpoint |
        """)    
    with st.expander("2 — Statistical Analysis Suite (6 Tabs)"):
        st.markdown("""
<h3>Tab 1: Intensity & Operational Rhythm</h3>
| ID | Analysis | Measurement Focus |
|---|---|---|
| **A1** | Descriptive Statistics | Fundamental metrics (Mean, Median, Std Dev, Variance) |
| **A2** | Operational Tempo | Combat/Peace day ratio and Zero-Activity (Z₀₀) persistence |
| **A3** | Conflict Dynamics | High-resolution combat and silence streaks |
| **A4** | Combat Pressure | Events per combat day intensity |
<h3>Tab 2: Chronological & Seasonal Trends</h3>
| ID | Analysis | Measurement Focus |
|---|---|---|
| **A5** | Annual Conflict Trend | Yearly events vs accumulation curve |
| **A6** | Conflict Momentum | Year-on-Year variation in operational initiative |
| **A7** | Temporal Distribution | Multi-scalar aggregation (Week, Quarter, Semester) |
| **A8** | Seasonal Pattern Analysis | Donut distribution by meteorological seasons |
| **A9** | Structural Monthly Average | Long-term average per calendar month |
| **A10** | Monthly Chronological Distribution | Longitudinal monthly event flow |
<h3>Tab 3: Spatial & Strategic Dynamics</h3>
| ID | Analysis | Measurement Focus |
|---|---|---|
| **A11** | Segmented Spatial Distribution | Hierarchical tree-map (Region > Sector) |
| **A12** | Sector Operational Ranking | Absolute event ranking per tactical sector |
| **A13** | Regional Activity Ranking | Strategic level analysis across 3 MRs |
| **A14** | Shifting Center of Gravity (Analytics) | Statistical calculation of operational center |
| **A15** | Geographic Concentration (HHI) | Spatial monopoly index of theater events |
<h3>Tab 4: Operational Micro-Spatio-Temporal Analysis</h3>
| ID | Analysis | Measurement Focus |
|---|---|---|
| **A16** | Operational Heatmap | Multi-year matrix of Sectors vs Time (Horizontal Flow) |
<h3>Tab 5: Tactical Typology & Compliance Analysis</h3>
| ID | Analysis | Measurement Focus |
|---|---|---|
| **A17** | Rhythm of War | Distribution of combat events by Day of the Week |
| **A18** | Escalation Typology | Categorization by Intensity Bands (Harassment, Barrage) |
| **A19** | MINURSO Zone Compliance | Geopolitical analysis of strikes per control zone |
| **A20** | Strategic Target Typology | Operational depth analysis (Theatre vs Deep Strike) |

<h3>Tab 6: Predictive Modeling & Operational Probability</h3>
| ID | Analysis | Measurement Focus |
|---|---|---|
| **A21** | Escalation Chains (Markov) | Transition probability: Peace ➔ Combat |
| **A22** | Geographic Contagion Index | Probability of spatial spread within 48h |
| **A23** | Operational Pause (Time-to-Event) | Logistical 'reload' time per tactical sector |
| **A24** | Predictive Tactical Forecasting | Future initiative likelihood based on historical patterns |
| **A25** | Conflict Volatility Analysis | Measurement of operational instability over time |
        """, unsafe_allow_html=True)    
    with st.expander("3 — Analytical Map Suite (8 Perspective Tabs)"):
        st.markdown("""
| # | Map Lens | Analytical Perspective |
|---|---|---|
| **G1** | Control Zones Map | Ceasefire Compliance & Geopolitical status |
| **G2** | Sector Pressure Map | Operational intensity at meso level (Choropleth) |
| **G3** | Regional Activity Map | Strategic aggregation by Military Regions |
| **G4** | Tactical Density Map | Kernel Density Estimation (Heatmap) |
| **G5** | Conflict Hotspots Map | Spatial cluster and tactical node identification |
| **G6** | Strategic Frontline Pressure Map | Analysis of intensity at the Wall-Sector intersections |
| **G7** | Operational Corridors Map | Logistical correlation (Roads & Hydrography) |
| **G8** | Actor Activity Distribution | Spatial initiative by force (Polisario vs Morocco) |
        
**Spatial Methods Used:** Kernel Density Estimation (KDE), Statistical Cluster Analysis, Nearest Neighbor Analysis, Spatio-Temporal Dispersion Index.
        """)
        
    with st.expander("4 — Base Maps (6 Modes)"):
        st.markdown("""
| # | Map Mode | Operational Function |
|---|---|---|
| **B1** | Full Operational Theater | Comprehensive situational awareness (Full Layers) |
| **B2** | Territorial Control Map | Sovereignty and legal status focus (Macro Level) |
| **B3** | Military Regions Map | Strategic command and control boundaries |
| **B4** | Operational Sectors Map | Meso-level tactical division of the front |
| **B5** | Moroccan Military Wall Map | Defensive system and barrier infrastructure |
| **B6** | Logistics & Hydrography | Topography and terrain relief (Strategic Geography) |
        """)
