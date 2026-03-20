"""
STATISTICAL MODULE
Western Sahara War Archive

Objectives
----------
Analyze three fundamental dimensions of the armed conflict:
1. Intensity  -> Number of events occurring
2. Frequency  -> Rate of occurrence over time
3. Distribution -> Spatial and temporal patterns

Input
-----
df_filtered (from app.py)

Temporal Parameters
------------------
time_mode: str
    - "Conflict Time" -> Conflict_Year columns
    - "Civil Time"    -> Calender_Year columns
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

from streamlit_folium import st_folium

# ==========================================================
# CONSTANTS & GIS DATA
# ==========================================================
TOTAL_POSSIBLE_SECTORS = 13  # S1 – S13
MONTH_NAMES = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
               7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

# Precise City-Based Coordinates extracted from data_geo/points/*.shp
SECTOR_CENTROIDS = {
    'S1': (28.616658, -9.438911),   # Aaga
    'S2': (28.416937, -9.219461),   # Touizgui
    'S3': (27.416300, -9.049609),   # El Mahabas
    'S4': (27.253146, -9.475866),   # Farsia
    'S5': (27.112875, -10.971020),  # Haouza
    'S6': (26.766251, -11.684224),  # Smara
    'S7': (26.078262, -11.784921),  # Amgala
    'S8': (25.161644, -12.377480),  # Guelta Zemmour
    'S9': (24.102168, -13.273637),  # Oum Dreiga
    'S10': (23.096332, -14.144866),  # El Bagari
    'S11': (22.569825, -14.312385),  # Auserd
    'S12': (21.633499, -14.888934),  # Techla
    'S13': (21.616973, -16.470845),  # Bir Guendouz
}

# ==========================================================
# GLOBAL WRAPPER FOR SELECTBOX (unique keys)
# ==========================================================
_widget_counter = 0
_original_selectbox = st.selectbox

def selectbox_unique(label, options, **kwargs):
    global _widget_counter
    _widget_counter += 1
    if "key" not in kwargs:
        kwargs["key"] = f"selectbox_{_widget_counter}"
    return _original_selectbox(label, options, **kwargs)

st.selectbox = selectbox_unique

# ==========================================================
# METHODOLOGICAL COLOR SYSTEM
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

sector_to_region = {
    "S1": "MR1", "S2": "MR1", "S3": "MR1",
    "S4": "MR2", "S5": "MR2", "S6": "MR2", "S7": "MR2", "S8": "MR2",
    "S9": "MR3", "S10": "MR3", "S11": "MR3", "S12": "MR3", "S13": "MR3"
}

mega_level_colors = {
    "C1": "#B22222",
    "C2": "#E6C78F"
}

# ==========================================================
# WRAPPER FOR FOLIUM/STREAMLIT (ensures unique keys)
# ==========================================================

_map_counter = 0
_original_st_folium = st_folium

def _st_folium_unique(map_object, **kwargs):
    global _map_counter
    _map_counter += 1
    if "key" not in kwargs:
        kwargs["key"] = f"folium_unique_{_map_counter}"
    return _original_st_folium(map_object, **kwargs)

st_folium = _st_folium_unique

# ==========================================================
# MAIN RENDERING FUNCTION
# ==========================================================

def render_statistical_module(df: pd.DataFrame, time_mode: str = "Conflict Time", timeframe: str = "2020-2024") -> None:
    st.header(f"Conflict Statistical Analysis")
    st.caption(f"**Period:** {timeframe}")
    
    df, daily = prepare_data(df)
    year_col = "Conflict_Year" if time_mode == "Conflict Time" else "Calender_Year"
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Intensity & Rhythm", 
        "Timeline Trends", 
        "Spatial Dynamics", 
        "Tactical & Compliance",
        "Predictive Analytics",
        "Operational Heatmap"
    ])
    
    with tab1:
        with st.expander("[A1] Descriptive Statistics", expanded=True):
            descriptive_statistics(daily)
        st.markdown("---")
        with st.expander("[A2] Operational Tempo", expanded=True):
            operational_tempo(daily)
        st.markdown("---")
        with st.expander("[A3] Conflict Dynamics", expanded=True):
            conflict_dynamics(daily)
        st.markdown("---")
        st.subheader("Intensity & Coverage Indices")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            conflict_intensity_index(df)
        with col_c2:
            conflict_saturation_index(df)

    with tab2:
        temporal_distribution(df)
        monthly_distribution(df)
        structural_monthly_average(df)
        seasonal_analysis(df)
        conflict_trend(df, daily, year_col)
        st.markdown("---")
        advanced_visualizations(daily)

    with tab3:
        spatial_distribution(df)
        sector_ranking(df)
        st.markdown("---")
        intensity_pareto_regional(df)
        spatial_operational_metrics(df, year_col)
        shifting_center_of_gravity(df, year_col)
        geographic_dispersion_hhi(df)
        temporal_slider_conflict(df)

    with tab4:
        rhythm_of_war_weekly(df)
        st.markdown("---")
        escalation_typology(daily)
        st.markdown("---")
        compliance_and_depth(df)

    with tab5:
        markov_escalation_chains(daily)
        st.markdown("---")
        advanced_predictive_metrics(df, daily)

    with tab6:
        st.subheader("[A16] Operational Heatmap")
        st.info("This heatmap illustrates the operational density across different sectors over time.")
        operational_heat_map(df)

# ==========================================================
# DATA PREPARATION
# ==========================================================

def prepare_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = df.copy()
    df["Event_Date"] = pd.to_datetime(df["Event_Date"]).dt.date
    df["Event_Binary"] = (df["N_of_Event"] > 0).astype(int)
    
    if "Calender_Quarter" in df.columns:
        df["Quarter"] = df["Calender_Quarter"]
    if "Calender_Semester" in df.columns:
        df["Semester"] = df["Calender_Semester"]
        
    daily = (
        df.groupby("Event_Date")["N_of_Event"]
        .sum()
        .reset_index()
        .sort_values("Event_Date")
    )
    if not daily.empty:
        # Reindexing to ensure all dates are present in the 'daily' series
        all_dates = pd.date_range(start=daily["Event_Date"].min(), end=daily["Event_Date"].max()).date
        daily.set_index("Event_Date", inplace=True)
        daily = daily.reindex(all_dates, fill_value=0).reset_index()
        daily.rename(columns={"index": "Event_Date"}, inplace=True)
        
    daily["Combat"] = (daily["N_of_Event"] > 0).astype(int)
    return df, daily

# ==========================================================
# DESCRIPTIVE STATISTICS
# ==========================================================

def descriptive_statistics(daily: pd.DataFrame) -> None:
    st.subheader("[A1] Descriptive Statistics")
    
    mean_value = daily["N_of_Event"].mean()
    median_value = daily["N_of_Event"].median()
    mode_value = daily["N_of_Event"].mode()[0]
    std_dev = daily["N_of_Event"].std()
    variance_value = daily["N_of_Event"].var()
    minimum = daily["N_of_Event"].min()
    maximum = daily["N_of_Event"].max()
    range_value = maximum - minimum
    percentile_75 = daily["N_of_Event"].quantile(0.75)
    percentile_95 = daily["N_of_Event"].quantile(0.95)
    skewness = round(stats.skew(daily["N_of_Event"]), 3)
    kurtosis = round(stats.kurtosis(daily["N_of_Event"]), 3)
    
    # Distribution Curve (Histogram + Box)
    fig_dist = px.histogram(
        daily, x="N_of_Event", nbins=40, marginal="box",
        title="Daily Event Distribution & Variance",
        color_discrete_sequence=["#34495E"], template="plotly_white"
    )
    fig_dist.update_layout(title_pad=dict(b=20), margin=dict(t=70, b=20, l=10, r=10), height=350)
    st.plotly_chart(fig_dist, width="stretch")
    
    # Bullet Chart for Means and Extremes
    fig_bullet = go.Figure(go.Indicator(
        mode = "number+gauge", value = mean_value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Average Daily Events<br><span style='font-size:0.8em;color:gray'>vs Max & Percentiles</span>"},
        gauge = {
            'shape': "bullet",
            'axis': {'range': [0, maximum]},
            'threshold': {
                'line': {'color': "#D9534F", 'width': 3},
                'thickness': 0.75,
                'value': percentile_95
            },
            'steps': [
                {'range': [0, percentile_75], 'color': "#EAECEE"},
                {'range': [percentile_75, percentile_95], 'color': "#ABB2B9"}
            ],
            'bar': {'color': "#2C3E50"}
        }
    ))
    fig_bullet.update_layout(height=200, margin=dict(t=50, b=40, l=180, r=30), template="plotly_white")
    st.plotly_chart(fig_bullet, width="stretch")

    st.markdown("#### Tabular Summary")
    metrics_a1 = pd.DataFrame({
        "Metric": ["Mean", "Median", "Mode", "Std Dev", "Variance", "Min", "Max", "Range", "75th Percentile", "95th Percentile", "Skewness", "Kurtosis"],
        "Value": [round(mean_value, 2), round(median_value, 2), mode_value, round(std_dev, 2), round(variance_value, 2), minimum, maximum, range_value, round(percentile_75, 2), round(percentile_95, 2), skewness, kurtosis]
    })
    st.dataframe(metrics_a1, use_container_width=True, hide_index=True)

    with st.expander("Metodologia A1", expanded=False):
        st.markdown(r"""
        **O que mede:** A tendência central e dispersão estatística da intensidade do conflito.
        **Como mede:** Aplica funções estatísticas sobre a série diária de eventos.
        **Fórmulas:** $\mu = \frac{\sum x}{n}$ (Média), $\sigma = \sqrt{VAR}$ (Desvio Padrão).
        **Aplicação:** Define se a guerra é estável (baixa variância) ou imprevisível (alta variância).
        """)

# ==========================================================
# OPERATIONAL TEMPO
# ==========================================================
def operational_tempo(daily: pd.DataFrame) -> None:
    st.subheader("[A2] Operational Tempo & Rhythm")
    
    total_days = len(daily)
    combat_days = int(daily["Combat"].sum())
    peace_days = total_days - combat_days
    optempo = combat_days / total_days if total_days > 0 else 0
    total_events = daily["N_of_Event"].sum()
    combat_pressure = total_events / combat_days if combat_days > 0 else 0
    z00_ratio = peace_days / total_days if total_days > 0 else 0
    conflict_rhythm_index = combat_days / peace_days if peace_days > 0 else 0
    
    # Gauge Chart for OpTempo
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = optempo * 100,
        number = {'suffix': "%"},
        title = {'text': "Operational Tempo Index"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "#2C3E50"},
            'steps' : [
                {'range': [0, 30], 'color': "#EAEDED"},
                {'range': [30, 70], 'color': "#F5B041"},
                {'range': [70, 100], 'color': "#E74C3C"}
            ],
            'threshold' : {'line': {'color': "#922B21", 'width': 4}, 'thickness': 0.75, 'value': 80}
        }
    ))
    fig_gauge.update_layout(height=350, margin=dict(t=70, b=20, l=30, r=30), template="plotly_white")
    st.plotly_chart(fig_gauge, width="stretch")
    
    # Core Supporting Metrics
    st.markdown("---")
    st.markdown("#### Tabular Summary")
    metrics_a2 = pd.DataFrame({
        "Metric": ["Total Days", "Combat Days", "Peace Days", "Operational Tempo (%)", "Combat Pressure (Events/Day)", "Z00 Ratio", "Conflict Rhythm Index"],
        "Value": [total_days, combat_days, peace_days, round(optempo * 100, 2), round(combat_pressure, 2), round(z00_ratio, 2), round(conflict_rhythm_index, 2)]
    })
    st.dataframe(metrics_a2, use_container_width=True, hide_index=True)

    with st.expander("Metodologia A2", expanded=False):
        st.markdown(r"""
        **O que mede:** A cadência operacional das forças em combate.
        **Como mede:** Relação entre dias com atividade (*Combat*) vs dias sem atividade (*Peace/Z00*).
        **Fórmula:** $Tempo = \frac{Dias_{Combat}}{Dias_{Total}} \times 100$.
        **Aplicação:** Identifica a capacidade de sustentar pressão contínua sobre o inimigo.
        """)

# ==========================================================
# CONFLICT DYNAMICS
# ==========================================================
def conflict_dynamics(daily: pd.DataFrame) -> None:
    st.subheader("[A3] Conflict Dynamics (Streaks)")
    
    # --- Identificar sequências de combate e paz ---
    daily["group"] = (daily["Combat"] != daily["Combat"].shift()).cumsum()
    combat_streaks = daily[daily["Combat"] == 1].groupby("group").size()
    peace_streaks = daily[daily["Combat"] == 0].groupby("group").size()
    
    # Barcode Timeline Chart (Visual Streaks)
    fig_barcode = px.bar(
        daily, x="Event_Date", y="Combat", color="Combat",
        color_continuous_scale=["#EAECEE", "#E74C3C"],
        title="Conflict Consistency (Timeline Barcode)",
        template="plotly_white"
    )
    fig_barcode.update_layout(
        coloraxis_showscale=False,
        yaxis=dict(showticklabels=False, title=""),
        xaxis=dict(title="", type="date"),
        height=250, margin=dict(t=50, b=30, l=10, r=10),
        plot_bgcolor="#FFFFFF",
        bargap=0
    )
    fig_barcode.update_traces(marker_line_width=0)
    st.plotly_chart(fig_barcode, width="stretch")
    
    st.markdown("---")
    st.markdown("#### Tabular Summary")
    metrics_a3 = pd.DataFrame({
        "Metric": ["Max Combat Streak (Days)", "Avg Combat Streak (Days)", "Max Peace Streak (Days)", "Avg Peace Streak (Days)"],
        "Value": [
            int(combat_streaks.max()) if not combat_streaks.empty else 0,
            round(combat_streaks.mean(), 2) if not combat_streaks.empty else 0,
            int(peace_streaks.max()) if not peace_streaks.empty else 0,
            round(peace_streaks.mean(), 2) if not peace_streaks.empty else 0
        ]
    })
    st.dataframe(metrics_a3, use_container_width=True, hide_index=True)

    with st.expander("Metodologia A3", expanded=False):
        st.markdown(r"""
        **O que mede:** A persistência temporal da violência.
        **Como mede:** Identifica sequências consecutivas (Rachas) de dias de combate ou paz.
        **Fórmula:** $Streak = \sum t_i$ onde $Combat(t_i) = 1$.
        **Aplicação:** Avalia ciclos de fadiga e reabastecimento logístico.
        """)

# ==========================================================
# TEMPORAL DISTRIBUTION
# ==========================================================

def temporal_distribution(df: pd.DataFrame) -> None:
    st.subheader("[A7] Temporal Distribution of Events")
    
    selected_dim = "Month (Civil)"
    col = "Calender_Month"
    
    if col in df.columns:
        data = df.groupby(col)["N_of_Event"].sum().reset_index()
        fig = px.bar(
            data, x=col, y="N_of_Event",
            title=f"Events per {selected_dim}",
            color_discrete_sequence=["#4C72B0"],
            template="plotly_white"
        )
        fig.update_layout(xaxis_title=selected_dim, yaxis_title="Total Events", title_pad=dict(b=25), margin=dict(t=75))
        st.plotly_chart(fig, width='stretch', key=f"bar_{col}")
        
        with st.expander("Metodologia A7", expanded=False):
            st.markdown("""
            **O que mede:** A distribuição absoluta de eventos em diferentes escalas temporais.
            **Como mede:** Agregamento (Soma) de eventos por unidade de tempo selecionada.
            **Aplicação:** Permite identificar picos de atividade sazonais ou anuais.
            """)
        st.caption("Figure A7: Temporal Distribution of Events")

# ==========================================================
# MONTHLY DISTRIBUTION
# ==========================================================

def monthly_distribution(df: pd.DataFrame) -> None:
    st.subheader("[A10] Monthly Chronological Distribution")
    monthly_events = df.groupby(["Calender_Year", "Calender_Month"])["N_of_Event"].sum().reset_index()
    monthly_events["Year_Month"] = (
        monthly_events["Calender_Year"].astype(str) + "-" +
        monthly_events["Calender_Month"].astype(str).str.zfill(2)
    )
    fig_monthly = px.bar(
        monthly_events, x="Year_Month", y="N_of_Event",
        title="Monthly Distribution of Conflict Events",
        color_discrete_sequence=["#5A7DC2"],
        template="plotly_white"
    )
    fig_monthly.update_layout(xaxis_tickangle=-45, xaxis_title="Year-Month", yaxis_title="Total Events", title_pad=dict(b=25), margin=dict(t=75))
    st.plotly_chart(fig_monthly, width='stretch')
    
    with st.expander("Metodologia A8", expanded=False):
        st.markdown("""
        **O que mede:** A evolução cronológica mensal do conflito.
        **Como mede:** Soma mensal absoluta de eventos reportados.
        **Aplicação:** Visualização da "pulsação" da guerra ao longo dos anos.
        """)
    st.caption("Figure A8: Monthly Chronological Distribution")

# ==========================================================
# STRUCTURAL MONTHLY AVERAGE
# ==========================================================

def structural_monthly_average(df: pd.DataFrame) -> None:
    st.subheader("[A9] Structural Monthly Average")
    monthly_avg = df.groupby("Calender_Month")["N_of_Event"].mean().reset_index()
    month_names = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                   7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
    monthly_avg["Month_Name"] = monthly_avg["Calender_Month"].map(month_names)
    fig_avg = px.bar(
        monthly_avg, x="Month_Name", y="N_of_Event",
        title="Structural Monthly Average of Conflict Events",
        category_orders={"Month_Name": list(month_names.values())},
        color_discrete_sequence=["#6A9FC0"],
        template="plotly_white"
    )
    fig_avg.update_layout(xaxis_title="Month", yaxis_title="Average Events", title_pad=dict(b=25), margin=dict(t=75))
    st.plotly_chart(fig_avg, width='stretch')
    
    with st.expander("Metodologia A9", expanded=False):
        st.markdown(r"""
        **O que mede:** A intensidade média "típica" de cada mês civíl.
        **Fórmula:** $\\overline{x}_{month} = \\frac{\\sum E}{(Years)}$.
        **Aplicação:** Identifica meses historicamente mais violentos (ex: impacto do clima nas operações).
        """)
    st.caption("Figure A9: Structural Monthly Average")

# ==========================================================
# SEASONAL ANALYSIS — Donut Chart
# ==========================================================

def seasonal_analysis(df: pd.DataFrame) -> None:
    st.subheader("[A8] Seasonal Analysis")
    if "Calender_Season" not in df.columns:
        st.warning("Season data not available.")
        return
    
    seasonal = df.groupby("Calender_Season")["N_of_Event"].sum().reset_index()
    if seasonal.empty:
        return
    
    seasonal["Share_%"] = (seasonal["N_of_Event"] / seasonal["N_of_Event"].sum() * 100).round(1)
    
    season_colors_map = {
        "Winter": "#A8C8E8",
        "Spring": "#8DC96E",
        "Summer": "#F5C542",
        "Autumn": "#D4845A"
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=seasonal["Calender_Season"],
        values=seasonal["N_of_Event"],
        hole=0.45,
        marker_colors=[season_colors_map.get(s, "#aaa") for s in seasonal["Calender_Season"]],
        textinfo="label+percent",
        hovertemplate="%{label}: %{value} events (%{percent})<extra></extra>"
    )])
    fig.update_layout(title="Conflict Intensity by Season", title_pad=dict(b=25), margin=dict(t=75), template="plotly_white")
    st.plotly_chart(fig, width='stretch')
    
    with st.expander("Metodologia A4", expanded=False):
        st.markdown("""
        **O que mede:** A participação relativa das estações do ano na violência total.
        **Aplicação:** Determina se existe uma "Guerra de Verão" ou "Guerra de Inverno".
        """)
    st.caption("Figure A4: Seasonal Analysis")
    st.dataframe(seasonal, hide_index=True)

# ==========================================================
# CONFLICT TREND — Dual-axis + Annotations
# ==========================================================

def conflict_trend(df: pd.DataFrame, daily: pd.DataFrame, year_col: str) -> None:
    if df.empty:
        st.warning("No data available for conflict trend analysis.")
        return
    st.subheader("[A5 | A6] Annual Conflict Trend & Momentum")
    
    annual_trend = df.groupby(year_col)["N_of_Event"].sum().reset_index()
    annual_trend["YoY_Change_%"] = annual_trend["N_of_Event"].pct_change() * 100
    annual_trend["Momentum"] = annual_trend["N_of_Event"].diff()
    
    peak_idx = annual_trend["N_of_Event"].idxmax()
    peak_year = annual_trend.loc[peak_idx, year_col]
    peak_val = annual_trend.loc[peak_idx, "N_of_Event"]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=annual_trend[year_col],
        y=annual_trend["YoY_Change_%"],
        name="YoY Change (%)",
        marker_color="#FFBA49",
        opacity=0.6,
        yaxis="y2"
    ))
    fig.add_trace(go.Scatter(
        x=annual_trend[year_col],
        y=annual_trend["N_of_Event"],
        name="Total Events",
        mode="lines+markers",
        line=dict(color="#4C72B0", width=2.5),
        marker=dict(size=8)
    ))
    
    if len(annual_trend) > 1:
        z = np.polyfit(range(len(annual_trend)), annual_trend["N_of_Event"], 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(
            x=annual_trend[year_col],
            y=p(range(len(annual_trend))),
            name="OLS Trend",
            line=dict(dash="dash", color="grey")
        ))
        
    fig.add_annotation(
        x=peak_year, y=peak_val,
        text=f"Peak: {int(peak_val)}",
        showarrow=True, arrowhead=2,
        bgcolor="#4C72B0", font=dict(color="white"),
        arrowcolor="#4C72B0"
    )
    fig.update_layout(yaxis=dict(title="Total Events"), yaxis2=dict(title="YoY Change (%)", overlaying="y", side="right", showgrid=False), legend=dict(orientation="h", y=-0.2), hovermode="x unified", title_pad=dict(b=25), margin=dict(t=75), template="plotly_white")
    st.plotly_chart(fig, width='stretch')
    
    with st.expander("Metodologia A5", expanded=False):
        st.markdown("""
        **O que mede:** A evolução anual absoluta e a variação percentual Ano-a-Ano (YoY).
        **Aplicação:** Identifica o crescimento ou retração estrutural do conflito.
        """)
    st.caption("Figure A5: Annual Conflict Trend")
    
    fig_momentum = px.line(
        annual_trend, x=year_col, y="Momentum",
        markers=True, title="Conflict Momentum (Δ Events vs Previous Year)",
        color_discrete_sequence=["#C75B7A"],
        template="plotly_white"
    )
    fig_momentum.add_hline(y=0, line_dash="dash", line_color="grey")
    fig_momentum.update_layout(title_pad=dict(b=25), margin=dict(t=75))
    st.plotly_chart(fig_momentum, width='stretch')
    
    with st.expander("Metodologia A6", expanded=False):
        st.markdown("""
        **O que mede:** A aceleração ou desaceleração do conflito (Δ Eventos).
        **Fórmula:** $Momentum = E_t - E_{t-1}$.
        **Aplicação:** Diferencia entre "Guerra Estacionária" (Momentum ~0) e "Escalada Rápida".
        """)
    st.caption("Figure A6: Conflict Momentum")
    
    volatility = annual_trend["N_of_Event"].std()
    st.metric("Conflict Volatility (Std Dev)", round(volatility, 2))

# ==========================================================
# SPATIAL DISTRIBUTION — Treemap
# ==========================================================

def spatial_distribution(df: pd.DataFrame) -> None:
    if df.empty:
        st.warning("No data available for spatial distribution analysis.")
        return
    st.subheader("[A11] Hierarchical Spatial Distribution (Treemap)")
    
    sector_data = df.groupby("Meso_Level_ID")["N_of_Event"].sum().reset_index()
    sector_data["Military_Region"] = sector_data["Meso_Level_ID"].map(sector_to_region).fillna("Unknown")
    
    fig = px.treemap(
        sector_data,
        path=["Military_Region", "Meso_Level_ID"],
        values="N_of_Event",
        color="N_of_Event",
        color_continuous_scale="Oranges",
        title="Conflict Events by Military Region & Sector (Treemap)",
        template="plotly_white"
    )
    fig.update_traces(textinfo="label+value+percent root")
    fig.update_layout(title_pad=dict(b=25), margin=dict(t=75))
    st.plotly_chart(fig, width='stretch')
    
    with st.expander("Metodologia A11", expanded=False):
        st.markdown("""
        **O que mede:** A hierarquia espacial do conflito por Região e Setor.
        **Aplicação:** Visualização proporcional de onde a violência está "ancorada".
        """)
    st.caption("Figure A11: Spatial Distribution Treemap")

# ==========================================================
# SECTOR RANKING TABLE
# ==========================================================

def sector_ranking(df: pd.DataFrame) -> None:
    if df.empty:
        st.warning("No data available for sector ranking analysis.")
        return
    st.subheader("[A12] Sector Operational Ranking")
    with st.expander("Metodologia A12", expanded=False):
        st.markdown("""
        **O que mede:** O ranking de agressividade por setor.
        **Aplicação:** Identifica os "Setores Quentes" que dominam as estatísticas operacionais.
        """)
    ranked = (
        df.groupby("Meso_Level_ID")["N_of_Event"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    ranked.index = ranked.index + 1
    ranked.columns = ["Sector", "Total Events"]
    ranked["Military Region"] = ranked["Sector"].map(sector_to_region).fillna("–")
    ranked["Share (%)"] = (ranked["Total Events"] / ranked["Total Events"].sum() * 100).round(1)
    st.dataframe(ranked[["Sector", "Military Region", "Total Events", "Share (%)"]], hide_index=False)

# ==========================================================
# SPATIAL OPERATIONAL METRICS
# ==========================================================

def spatial_operational_metrics(df: pd.DataFrame, year_col: str) -> None:
    st.subheader("[A13] Spatial Operational Metrics")
    
    regional_density = df.groupby("Macro_Level_ID")["N_of_Event"].mean().reset_index()
    fig2 = px.bar(
        regional_density, x="Macro_Level_ID", y="N_of_Event",
        color="Macro_Level_ID", color_discrete_map=region_colors,
        title="Regional Combat Density (Average Events per Record)"
    )
    fig2.update_layout(title_pad=dict(b=25), margin=dict(t=75))
    st.plotly_chart(fig2, width='stretch')
    
    with st.expander("Metodologia A13", expanded=False):
        st.markdown(r"""
        **O que mede:** A densidade de combate regional e o alcance geográfico.
        **Fórmulas:** $Expansion = \\frac{Sectores_{Ativos}}{Sectores_{Totais}}$.
        **Aplicação:** Mede se o conflito está a saturar novas áreas (Expansão) ou a repetir setores (Consolidação).
        """)
    st.caption("Figure A13: Spatial Operational Metrics")
    
    total_sectors = df["Meso_Level_ID"].nunique()
    active_sectors = df[df["N_of_Event"] > 0]["Meso_Level_ID"].nunique()
    expansion_index = active_sectors / total_sectors if total_sectors > 0 else 0
    st.metric("Spatial Expansion Index", round(expansion_index, 2))

# ==========================================================
# ADVANCED VISUALIZATIONS (Moving Averages)
# ==========================================================

def advanced_visualizations(daily: pd.DataFrame) -> None:
    st.subheader("[Advanced] Moving Averages & Event Distribution")
    daily["MA7"] = daily["N_of_Event"].rolling(7).mean()
    daily["MA30"] = daily["N_of_Event"].rolling(30).mean()
    
    fig = px.line(daily, x="Event_Date", y=["N_of_Event", "MA7", "MA30"],
                  title="Conflict Trend (Moving Averages)",
                  color_discrete_sequence=["#4C72B0", "#F0AD4E", "#D9534F"])
    fig.update_layout(title_pad=dict(b=25), margin=dict(t=75))
    
    fig_hist = px.histogram(daily, x="N_of_Event", nbins=30,
                            title="Daily Event Intensity Distribution",
                            color_discrete_sequence=["#D9534F"])
    fig_hist.update_layout(title_pad=dict(b=25), margin=dict(t=75))
    
    fig_binary = px.line(daily, x="Event_Date", y="Combat",
                         title="Combat vs Peace Sequence",
                         color_discrete_sequence=["#5CB85C"])
    fig_binary.update_layout(title_pad=dict(b=25), margin=dict(t=75))
    
    st.plotly_chart(fig_hist, width='stretch')
    with st.expander("Metodologia A10.1", expanded=False):
        st.markdown("""
        **O que mede:** A frequência de dias por volume de eventos.
        **Aplicação:** Mostra se a maioria dos dias são de baixa intensidade ou se há picos frequentes.
        """)
    st.caption("Figure A10.1: Daily Event Intensity Distribution")
    
    st.plotly_chart(fig_binary, width='stretch')
    with st.expander("Metodologia A11.1", expanded=False):
        st.markdown("""
        **O que mede:** A alternância entre estados de guerra e paz ao longo do tempo.
        **Aplicação:** Visualiza a densidade cronológica dos períodos de atividade.
        """)
    st.caption("Figure A11.1: Combat vs Peace Sequence")
    
    st.plotly_chart(fig, width='stretch')
    with st.expander("Metodologia A9.1", expanded=False):
        st.markdown("""
        **O que mede:** A tendência suavizada do conflito usando Médias Móveis (7 e 30 dias).
        **Aplicação:** Elimina o ruído diário para mostrar a direção estrutural da guerra.
        """)
    st.caption("Figure A9.1: Conflict Trend (Moving Averages)")

# ==========================================================
# CONFLICT INTENSITY INDEX — Gauge
# ==========================================================

def conflict_intensity_index(df: pd.DataFrame) -> None:
    st.subheader("[I2] Conflict Intensity Index")
    total_events = df["N_of_Event"].sum()
    daily_sum = df.groupby("Event_Date")["N_of_Event"].sum().reset_index()
    combat_days = (daily_sum["N_of_Event"] > 0).sum()
    total_days = len(daily_sum)
    operational_tempo = combat_days / total_days if total_days > 0 else 0
    event_intensity = daily_sum["N_of_Event"].mean()
    spatial_spread = df["Meso_Level_ID"].nunique()
    norm_spread = spatial_spread / TOTAL_POSSIBLE_SECTORS
    
    # Normalization (Scaling based on conflict historical peaks for Western Sahara)
    max_theoretical_events = total_days * 5.0  # Assumes 5 events/day is high intensity
    max_theoretical_intensity = 15.0           # Assumes 15 events in a single day is extreme
    
    norm_events = min(total_events / max_theoretical_events, 1.0) if max_theoretical_events > 0 else 0
    norm_intensity = min(event_intensity / max_theoretical_intensity, 1.0) if max_theoretical_intensity > 0 else 0
    
    # Combined Intensity Index (Average of 4 normalized dimensions)
    CII = (norm_events + operational_tempo + norm_intensity + norm_spread) / 4
    
    # Ensure CII is a valid float for Plotly
    if pd.isna(CII) or np.isinf(CII): CII = 0.0
    CII = float(max(0, min(CII, 1.0)))
    
    # Classification
    if CII < 0.25:
        label, color = "LOW", "#5CB85C"
    elif CII < 0.50:
        label, color = "MEDIUM", "#F0AD4E"
    elif CII < 0.75:
        label, color = "HIGH", "#D9534F"
    else:
        label, color = "CRITICAL", "#7D0000"
    
    # Reference Baseline (e.g., 0.5 represents a balanced state of attrition/active war)
    reference_cii = 0.5
    
    # Delta Calculation (Metric Display)
    delta_val = CII - reference_cii

    # Render Metric separately for stability
    st.metric(label=f"CII Indicator (vs {reference_cii} Baseline)", value=round(CII, 3), delta=round(delta_val, 3))

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=CII,
        title={"text": f"CII - {label}", "font": {"size": 18}},
        gauge={
            "axis": {"range": [0, 1], "tickwidth": 1},
            "bar": {"color": color},
            "steps": [
                {"range": [0, 0.25], "color": "#d4edda"},
                {"range": [0.25, 0.50], "color": "#fff3cd"},
                {"range": [0.50, 0.75], "color": "#f8d7da"},
                {"range": [0.75, 1.0], "color": "#7D0000"}
            ],
            "threshold": {
                "line": {"color": "black", "width": 3},
                "thickness": 0.75,
                "value": CII
            }
        }
    ))
    fig.update_layout(height=280, margin=dict(t=50, b=20, l=20, r=20), template="plotly_white")
    st.plotly_chart(fig, width='stretch')
    
    with st.expander("Metodologia I2", expanded=False):
        st.markdown(r"""
        **O que mede:** Intensidade combinada do conflito (Volume, Tempo, Escala e Espaço).
        **Fórmulas:** $CII = \\frac{E_{norm} + T_{op} + I_{norm} + S_{norm}}{4}$
        **Aplicação:** O valor de **0.50** é o benchmark estratégico para Guerra Ativa.
        """)
    st.caption("Figure I2: Conflict Intensity Index Gauge")
    st.latex(r"CII = \\frac{E_{norm} + T_{op} + I_{norm} + S_{norm}}{4}")

# ==========================================================
# CONFLICT SATURATION INDEX
# ==========================================================

def conflict_saturation_index(df: pd.DataFrame) -> None:
    st.subheader("[I4] Conflict Saturation Index")
    daily_sum = df.groupby("Event_Date")["N_of_Event"].sum().reset_index()
    combat_days = (daily_sum["N_of_Event"] > 0).sum()
    total_events = daily_sum["N_of_Event"].sum()
    active_sectors = (df.groupby("Meso_Level_ID")["N_of_Event"].sum() > 0).sum()
    avg_daily_intensity = total_events / combat_days if combat_days > 0 else 0
    spatial_coverage = active_sectors / TOTAL_POSSIBLE_SECTORS
    CSI = round(avg_daily_intensity * spatial_coverage, 4)
    st.metric("Conflict Saturation Index", CSI)
    
    with st.expander("Metodologia I4", expanded=False):
        st.markdown(r"""
        **O que mede:** A densidade de saturação do conflito (Intensidade Diária $\\times$ Cobertura Espacial).
        **Fórmula:** $CSI = \\overline{E}_{combat} \\times \\frac{S_{active}}{S_{total}}$.
        **Aplicação:** Mede o "Stress" imposto ao sistema defensivo inimigo em cada dia de combate.
        """)
    st.caption("Figure I4: Conflict Saturation Index")

# ==========================================================
# OPERATIONAL HEATMAP — Month × Sector
# ==========================================================

def operational_heat_map(df: pd.DataFrame) -> None:
    time_unit = st.radio(
        "Aggregate by:",
        ["Month", "Quarter", "Semester"],
        horizontal=True,
        key="heatmap_time_unit"
    )
    
    col_map = {
        "Month": "Calender_Month",
        "Quarter": "Calender_Quarter",
        "Semester": "Calender_Semester"
    }
    group_col = col_map[time_unit]
    
    if group_col not in df.columns:
        st.warning(f"Column '{group_col}' not available.")
        return
    
    heatmap_data = df.groupby([group_col, "Meso_Level_ID"])["N_of_Event"].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index="Meso_Level_ID", columns=group_col, values="N_of_Event").fillna(0)
    
    fig = px.imshow(
        heatmap_pivot,
        color_continuous_scale="OrRd",
        title=f"Conflict Events by Sector × {time_unit}",
        labels={"x": time_unit, "y": "Sector", "color": "Events"},
        template="plotly_white",
        aspect="auto"
    )
    fig.update_xaxes(side="bottom")
    fig.update_layout(title_pad=dict(b=25), margin=dict(t=75))
    st.plotly_chart(fig, width='stretch')
    
    with st.expander("Metodologia A17", expanded=False):
        st.markdown("""
        **O que mede:** A densidade operacional (Setor vs Tempo).
        **Aplicação:** Identifica a "migração" da violência entre setores ao longo do tempo.
        """)
    st.caption("Figure A17: Sector-wise Heatmap")

def intensity_pareto_regional(df: pd.DataFrame) -> None:
    st.subheader("[A16] Regional Intensity Pareto")
    region_data = df.groupby("Macro_Level_ID")["N_of_Event"].sum().sort_values(ascending=False).reset_index()
    region_data['cum_sum'] = region_data['N_of_Event'].cumsum()
    region_data['cum_perc'] = 100 * region_data['cum_sum'] / region_data['N_of_Event'].sum()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=region_data["Macro_Level_ID"], y=region_data["N_of_Event"], name="Events Intensity", marker_color="#4C72B0"))
    fig.add_trace(go.Scatter(x=region_data["Macro_Level_ID"], y=region_data["cum_perc"], name="Cumulative %", yaxis="y2", line=dict(color="#C75B7A", width=3)))
    
    fig.update_layout(
        title="Regional Operational Intensity (Pareto)",
        yaxis=dict(title="Number of Events"),
        yaxis2=dict(title="Cumulative Percent (%)", overlaying="y", side="right", range=[0, 105], showgrid=False),
        legend=dict(orientation="h", y=-0.2),
        title_pad=dict(b=25), margin=dict(t=75),
        template="plotly_white"
    )
    st.plotly_chart(fig, width='stretch')
    
    with st.expander("Metodologia A16", expanded=False):
        st.markdown("""
        **O que mede:** A concentração regional de eventos seguindo o Princípio de Pareto (80/20).
        **Aplicação:** Confirma se a maioria dos eventos está concentrada em poucas regiões (ex: Norte vs Sul).
        """)
    st.caption("Figure A16: Regional Intensity per Region (Pareto)")


# ==========================================================
# CONFLICT TEMPORAL SLIDER
# ==========================================================

def temporal_slider_conflict(df: pd.DataFrame) -> None:
    st.subheader("[A14] Temporal Progression of Conflict")
    df_copy = df.copy()
    df_copy["Event_Date"] = pd.to_datetime(df_copy["Event_Date"]).dt.date
    dates = df_copy["Event_Date"].sort_values().unique()
    
    if len(dates) < 2:
        st.info("Not enough date range to display slider.")
        return
    
    selected_date = st.slider(
        "Select Date for Snapshot Analysis",
        min_value=dates.min(),
        max_value=dates.max(),
        value=dates.max()
    )
    
    df_selected = df_copy[df_copy["Event_Date"] <= selected_date]
    agg_data = df_selected.groupby("Meso_Level_ID")["N_of_Event"].sum().reset_index()
    
    fig = px.bar(
        agg_data,
        x="Meso_Level_ID",
        y="N_of_Event",
        color="N_of_Event",
        color_continuous_scale="Plasma",
        title=f"Cumulative Conflict Intensity up to {selected_date}",
        template="plotly_white"
    )
    fig.update_layout(title_pad=dict(b=25), margin=dict(t=75))
    st.plotly_chart(fig, width='stretch')
    
    with st.expander("Metodologia A14", expanded=False):
        st.markdown("""
        **O que mede:** A progressão acumulada da intensidade do conflito até uma data específica.
        **Como mede:** Soma todos os eventos registados desde o início do dataset até à data selecionada no slider.
        **Aplicação:** Permite reconstruir o estado operacional do campo de batalha em momentos históricos específicos.
        """)
    st.caption("Figure A14: Temporal Progression of Conflict")



def shifting_center_of_gravity(df: pd.DataFrame, year_col: str) -> None:
    st.subheader("[A14] Shifting Center of Gravity")
    
    # Use hardcoded centroids for sector-level estimation to ensure precision
    df_coords = df[df["N_of_Event"] > 0].copy()
    if df_coords.empty:
        st.warning("No combat data available for CoG calculation.")
        return

    df_coords["lat"] = df_coords["Meso_Level_ID"].map(lambda x: SECTOR_CENTROIDS.get(x, (0,0))[0])
    df_coords["lon"] = df_coords["Meso_Level_ID"].map(lambda x: SECTOR_CENTROIDS.get(x, (0,0))[1])
    
    cog_data = df_coords.groupby(year_col).apply(
        lambda x: pd.Series({
            "Lat_CoG": np.average(x["lat"], weights=x["N_of_Event"]),
            "Lon_CoG": np.average(x["lon"], weights=x["N_of_Event"]),
            "Total_Events": x["N_of_Event"].sum()
        }), include_groups=False
    ).reset_index()
    
    # Sort by year for the trajectory line
    cog_data = cog_data.sort_values(by=year_col)
    # Convert year to string for discrete color scale
    cog_data[year_col] = cog_data[year_col].astype(str)
    
    fig = px.scatter_mapbox(
        cog_data, lat="Lat_CoG", lon="Lon_CoG", color=year_col, size="Total_Events",
        title="Centroid-Based Center of Gravity Evolution (City-Point Weighted Mean)", 
        zoom=5, mapbox_style="carto-positron",
        color_discrete_sequence=px.colors.qualitative.Bold,
        center={"lat": 24.5, "lon": -13}
    )
    
    # Add trajectory line
    fig.add_trace(go.Scattermapbox(
        lat=cog_data["Lat_CoG"],
        lon=cog_data["Lon_CoG"],
        mode='lines',
        line=dict(width=2, color="gray"),
        name="Evolution Path",
        showlegend=False
    ))
    
    fig.update_layout(
        title_pad=dict(b=25),
        margin=dict(t=80, b=0, l=0, r=0),
        height=620,
        paper_bgcolor="white",
        plot_bgcolor="white",
        mapbox=dict(
            bounds={"west": -22, "east": -5, "south": 18, "north": 33}
        )
    )
    st.plotly_chart(fig, width='stretch')
    
    with st.expander("Metodologia A14 (Shifting CoG)", expanded=False):
        st.markdown(r"""
        **O que mede:** A evolução do Centro de Gravidade (CoG) operacional do conflito.
        **Como mede:** Calcula a Média Aritmética Ponderada das coordenadas geográficas (Localização das Cidades) de todos os ataques anuais.
        **Fórmula:** $Lat_{CoG} = \\frac{\\sum (Lat_i \\times Events_i)}{\\sum Events_i}$.
        **Pontos de Referência:** Utiliza as coordenadas exactas das cidades principais de cada setor (Touizgui, Mahabas, Smara, etc.).
        **Aplicação:** Trata a guerra como um sistema físico; o CoG mostra para onde o esforço militar se está a deslocar (Norte vs Sul).
        """)
    st.caption("Figure A14: Shifting Center of Gravity")

def geographic_dispersion_hhi(df: pd.DataFrame) -> None:
    st.subheader("[A10] Geographic Dispersion (HHI)")
    sector_shares = df.groupby("Meso_Level_ID")["N_of_Event"].sum()
    total = sector_shares.sum()
    if total == 0: return
    shares_pct = (sector_shares / total) * 100
    hhi = (shares_pct ** 2).sum()
    if pd.isna(hhi) or np.isinf(hhi): hhi = 0.0
    
    st.metric("HHI Index (vs 1500 Baseline)", value=int(hhi), delta=int(hhi - 1500), delta_color="inverse")
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=float(hhi),
        title={"text": "Geographic Concentration Index (HHI)", "font": {"size": 18}},
        gauge={"axis": {"range": [0, 10000]},
               "bar": {"color": "#4C72B0"},
               "steps": [{"range": [0, 1500], "color": "#d4edda"},
                         {"range": [1500, 2500], "color": "#fff3cd"},
                         {"range": [2500, 10000], "color": "#f8d7da"}]}
    ))
    fig.update_layout(height=280, title_pad=dict(b=25), margin=dict(t=50, b=20))
    st.plotly_chart(fig, width='stretch')
    
    with st.expander("Metodologia A10 (HHI)", expanded=False):
        st.markdown(r"""
        **O que mede:** A concentração espacial da violência (Monopólio Geográfico).
        **Fórmula:** $HHI = \\sum (Share_i^2)$ onde $Share$ é % de eventos por setor.
        **Aplicação:** <1500 = Guerrilha Dispersa; >2500 = Ofensiva Concentrada de Alta Intensidade.
        """)
    st.caption("Figure A10: Geographic Concentration Index (HHI)")

def rhythm_of_war_weekly(df: pd.DataFrame) -> None:
    st.subheader("[A17] Rhythm of War (Weekly Cycle)")
    df["Weekday"] = pd.to_datetime(df["Event_Date"]).dt.day_name()
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekly = df.groupby("Weekday")["N_of_Event"].sum().reindex(days_order).fillna(0).reset_index()
    
    fig = px.line_polar(weekly, r="N_of_Event", theta="Weekday", line_close=True,
                        title="Tactical Rhythm (Events by Day of Week)",
                        color_discrete_sequence=["#8E44AD"])
    fig.update_traces(fill='toself', fillcolor='rgba(142, 68, 173, 0.3)')
    fig.update_layout(title_pad=dict(b=25), margin=dict(t=75))
    st.plotly_chart(fig, width="stretch")
    
    with st.expander("Metodologia A17.1", expanded=False):
        st.markdown("""
        **O que mede:** O ritmo tático semanal das operações.
        **Aplicação:** Identifica padrões de "pausa de fim de semana" ou picos em dias de ressuprimento.
        """)
    st.caption("Figure A17.1: Rhythm of War (Weekly Cycle)")

def escalation_typology(daily: pd.DataFrame) -> None:
    st.subheader("[A18] Escalation Typology (Intensity per Day)")
    daily["Typology"] = pd.cut(
        daily["N_of_Event"], bins=[-1, 0, 3, 10, float('inf')],
        labels=["Peace", "Harassment (1-3)", "Sustained Combat (4-10)", "Heavy Barrage (>10)"]
    )
    counts = daily[daily["Typology"] != "Peace"]["Typology"].value_counts().reset_index()
    counts.columns = ["Typology", "Days"]
    
    # Explicit Strategic mapping for colors to prevent "black" rendering
    color_map = {
        "Peace": "#D3D3D3",
        "Harassment (1-3)": "#FFEEBB",
        "Sustained Combat (4-10)": "#FFCC00",
        "Heavy Barrage (>10)": "#FF0000"
    }
    
    fig = px.bar(
        counts, x="Typology", y="Days", 
        color="Typology", 
        color_discrete_map=color_map,
        title="Escalation Typology",
        template="plotly_white"
    )
    fig.update_layout(title_pad=dict(b=30), margin=dict(t=100))
    st.plotly_chart(fig, width="stretch")
    
    with st.expander("Metodologia A18", expanded=False):
        st.markdown("""
        **O que mede:** A tipologia de escalada baseada no volume diário de fogo.
        **Classificação:** Harassment (1-3), Sustained (4-10), Heavy Barrage (>10).
        **Aplicação:** Define a natureza da guerra (Atrito vs Ofensiva de Larga Escala).
        """)
    st.caption("Figure A18: Escalation Typology")

def compliance_and_depth(df: pd.DataFrame) -> None:
    st.subheader("[A19 | A20] MINURSO Compliance & Tactical Depth")
    
    col1, col2 = st.columns(2)
    
    with col1:
        c_col = "Meso_Level_MINURSO_control"
        if c_col in df.columns:
            comp_data = df[df["N_of_Event"] > 0].groupby(c_col)["N_of_Event"].sum().reset_index()
            fig1 = px.pie(comp_data, names=c_col, values="N_of_Event", title="A19: MINURSO Compliance",
                          color_discrete_sequence=["#B22222", "#E6C78F"])
            fig1.update_layout(title_pad=dict(b=25), margin=dict(t=75))
            st.plotly_chart(fig1, width='stretch')
            
            with st.expander("Metodologia A19", expanded=False):
                st.markdown("""
                **O que mede:** O cumprimento legal dos acordos de cessar-fogo (Zonas de Amortecimento).
                **Aplicação:** Quantifica a pressão sobre a Berma (Muro) vs ataques em zonas restritas.
                """)
            st.caption("Figure A19: MINURSO Zone Compliance")

    with col2:
        d_col = "Mega_Level_Name"
        if d_col in df.columns:
            depth_data = df[df["N_of_Event"] > 0].groupby(d_col)["N_of_Event"].sum().reset_index()
            # Shorten labels for readability
            depth_data[d_col] = depth_data[d_col].replace({
                "External Front: Morocco Proper (Deep Strike)": "External: Morocco (Deep)",
                "Internal Front: Western Sahara (Standard Theater)": "Internal: Sahara (Std)"
            })
            
            fig2 = px.bar(depth_data, x=d_col, y="N_of_Event", title="A20: Strategic Operational Depth",
                         color=d_col, color_discrete_sequence=["#FF0000", "#FFA500"],
                         template="plotly_white")
            fig2.update_layout(title_pad=dict(b=25), margin=dict(t=75))
            fig2.update_xaxes(tickangle=30)
            st.plotly_chart(fig2, width='stretch')
            
            with st.expander("Metodologia A20", expanded=False):
                st.markdown("""
                **O que mede:** A profundidade estratégica e o risco político dos alvos.
                **Teatros:** *Standard Theater* (Sahara) vs *Deep Strike* (Marrocos).
                **Aplicação:** Avalia se o conflito está a romper as fronteiras internacionais reconhecidas.
                """)
            st.caption("Figure A20: Strategic Operational Depth")

def markov_escalation_chains(daily: pd.DataFrame) -> None:
    st.subheader("[A21] Escalation Chains (Markov Probabilities)")
    daily["Next_Day_Combat"] = daily["Combat"].shift(-1)
    dropna_daily = daily.dropna(subset=["Next_Day_Combat"])
    
    if len(dropna_daily) > 0:
        transitions = pd.crosstab(dropna_daily["Combat"], dropna_daily["Next_Day_Combat"], normalize='index') * 100
        transitions = transitions.reindex(index=[0, 1], columns=[0, 1]).fillna(0)
        heatmap_data = transitions.values
        fig = px.imshow(heatmap_data, text_auto=".1f", labels=dict(x="Tomorrow", y="Today", color="Probability %"),
                        x=["Peace", "Combat"], y=["Peace", "Combat"], title="1st Order Markov Transition Matrix",
                        color_continuous_scale="Blues", template="plotly_white")
        fig.update_layout(title_pad=dict(b=25), margin=dict(t=75))
        st.plotly_chart(fig, width="stretch")
        
        with st.expander("Metodologia A21", expanded=False):
            st.markdown("""
            **O que mede:** A probabilidade de transição entre estados de Combate e Paz.
            **Modelo:** Cadeia de Markov de 1ª Ordem (Memória de 1 dia).
            **Aplicação:** Responde: "Qual a probabilidade de haver um ataque amanhã, dado que houve um hoje?".
            """)
        st.caption("Figure A21: Escalation Chains (Markov)")

def advanced_predictive_metrics(df: pd.DataFrame, daily: pd.DataFrame) -> None:
    st.subheader("[A22 | A24] Geographic Contagion & Predictive Models")
    
    # Geographic Contagion
    sectors_per_day = df[df["N_of_Event"] > 0].groupby("Event_Date")["Meso_Level_ID"].nunique().reset_index()
    fig1 = px.line(sectors_per_day, x="Event_Date", y="Meso_Level_ID", title="Geographic Contagion Index (Sectors Active per Day)", color_discrete_sequence=["#E67E22"])
    fig1.update_layout(title_pad=dict(b=25), margin=dict(t=75))
    st.plotly_chart(fig1, width="stretch")
    
    with st.expander("Metodologia A22", expanded=False):
        st.markdown("""
        **O que mede:** A coordenação geográfica dos ataques (Sectores Ativos por Dia).
        **Aplicação:** Índices altos sugerem ofensivas coordenadas em múltiplas frentes simultâneas.
        """)
    st.caption("Figure A22: Geographic Contagion Index")
    
    # Operational Pause
    if "Meso_Level_ID" in df.columns:
        df_sorted = df[df["N_of_Event"] > 0].sort_values(by=["Meso_Level_ID", "Event_Date"])
        df_sorted["Event_Date_P"] = pd.to_datetime(df_sorted["Event_Date"])
        df_sorted["Days_Since_Last"] = df_sorted.groupby("Meso_Level_ID")["Event_Date_P"].diff().dt.days
        pause_avg = df_sorted.groupby("Meso_Level_ID")["Days_Since_Last"].mean().reset_index().fillna(0)
        fig2 = px.bar(pause_avg, x="Meso_Level_ID", y="Days_Since_Last", title="Operational Pause Analysis (Avg Days Between Attacks)", color_discrete_sequence=["#3498DB"])
        fig2.update_layout(title_pad=dict(b=25), margin=dict(t=75))
        st.plotly_chart(fig2, width="stretch")
        
        with st.expander("Metodologia A23", expanded=False):
            st.markdown(r"""
            **O que mede:** O tempo médio de "recarga" ou logística entre ataques no mesmo setor.
            **Fórmula:** $Pause = \\overline{t_{i} - t_{i-1}}$ por setor.
            **Aplicação:** Identifica a capacidade de regeneração operacional de cada frente.
            """)
        st.caption("Figure A23: Operational Pause Analysis")
    
    # Predictive Forecast (Simple Momentum logic)
    recent_momentum = daily["N_of_Event"].tail(30).mean()
    if pd.isna(recent_momentum): recent_momentum = 0.0
    
    # Scale: Average of 2+ events/day over 30 days is high momentum (score 100)
    forecast_score = min(recent_momentum / 2.0 * 100, 100.0)
    
    st.metric("Initiative Likelihood (vs 50% Baseline)", value=f"{round(forecast_score, 1)}%", delta=f"{round(forecast_score - 50, 1)}%")

    fig3 = go.Figure(go.Indicator(
        mode="gauge+number", value=round(float(forecast_score), 1),
        title={"text": "Initiative Likelihood Score", "font": {"size": 18}},
        gauge={"axis": {"range": [0, 100]},
               "bar": {"color": "#D9534F"},
               "steps": [{"range": [0, 50], "color": "#f2f2f2"},
                         {"range": [50, 80], "color": "#ffebcc"},
                         {"range": [80, 100], "color": "#f8d7da"}]}
    ))
    fig3.update_layout(height=280, title_pad=dict(b=25), margin=dict(t=50, b=20), template="plotly_white")
    st.plotly_chart(fig3, width='stretch')
    
    with st.expander("Metodologia A24", expanded=False):
        st.markdown(r"""
        **O que mede:** A probabilidade de continuidade da ofensiva (Dominância de Escala).
        **Como mede:** Momentum de 30 dias + Probabilidades de Transição de Markov.
        **Fórmula:** $Forecast = \\min(\\frac{MA_{30}}{2.0} \\times 100, 100)$.
        **Aplicação:** >50% indica que o partido iniciante mantém a iniciativa tática.
        """)
    st.caption("Figure A24: Predictive Tactical Forecasting")

# This will get injected into render_statistical_module
