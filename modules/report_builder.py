import pandas as pd
import datetime
import os
import base64
import numpy as np

def generate_csv(df: pd.DataFrame) -> bytes:
    """Generate CSV string for the given dataframe."""
    return df.to_csv(index=False, sep=";").encode('utf-8')

def generate_citation_txt(df: pd.DataFrame, timeframe: str) -> str:
    """Generate APA formatted citation report in TXT format."""
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return f"""# WESTERN SAHARA WAR ARCHIVE - CITATION REPORT
Generated on: {now} (Local Time)

## 1. RESEARCH DATA ARCHIVE
- **Lead Investigator:** Jorge Teixeira (CEAUP)
- **Host Institution:** Centro de Estudos Africanos da Universidade do Porto (CEAUP)
- **Copyright:** © 2024–2026 Jorge Teixeira
- **License:** Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
- **DOI:** https://doi.org/10.5281/zenodo.19041041

## 2. ANALYTICAL CONTEXT
- **Study Period:** {timeframe}
- **Data Universe:** {len(df)} Conflict Events
- **Total Kinetic Events (N_of_Event sum):** {int(df['N_of_Event'].sum())}
- **Active Operational Sectors:** {df['Meso_Level_ID'].nunique()}

## 3. FORMAL CITATION
Teixeira, Jorge (2024). Western Sahara War Archive (2020-2024): Geospatial Conflict Observatory. 
Data generated for period {timeframe}. Retrieved {now} from https://westernsaharawararchive.com/ https://doi.org/10.5281/zenodo.19041041

## 4. METHODOLOGICAL NOTE
This report contains a subset of the archival database filtered according to current user parameters. 
The information is subject to continuous correction and institutional review.
"""

def generate_bibtex(timeframe: str) -> str:
    """Generate BibTeX formatted citation."""
    now_year = datetime.datetime.now().year
    now_date = datetime.datetime.now().strftime("%Y-%m-%d")
    return f"""@misc{{teixeira_wswa_{now_year},
  author       = {{Teixeira, Jorge}},
  title        = {{Western Sahara War Archive (2020-2024): Geospatial Conflict Observatory}},
  year         = {{2024}},
  howpublished = {{\\url{{https://westernsaharawararchive.com/}}}},
  note         = {{Data generated for period {timeframe}. Accessed: {now_date}}},
  organization = {{Centro de Estudos Africanos da Universidade do Porto (CEAUP)}},
  doi          = {{10.5281/zenodo.19041041}}
}}"""

def generate_ris(timeframe: str) -> str:
    """Generate RIS formatted citation."""
    now_year = datetime.datetime.now().year
    now_date = datetime.datetime.now().strftime("%Y/%m/%d")
    return f"""TY  - COMP
AU  - Teixeira, Jorge
PY  - 2024
TI  - Western Sahara War Archive (2020-2024): Geospatial Conflict Observatory
UR  - https://westernsaharawararchive.com/
Y2  - {now_date}
N1  - Data generated for period {timeframe}.
DO  - 10.5281/zenodo.19041041
PB  - Centro de Estudos Africanos da Universidade do Porto (CEAUP)
ER  - """

def generate_mla(timeframe: str) -> str:
    """Generate MLA 9th Edition formatted citation."""
    now_date = datetime.datetime.now().strftime("%d %b. %Y")
    return f"Teixeira, Jorge. Western Sahara War Archive (2020-2024): Geospatial Conflict Observatory. Centro de Estudos Africanos da Universidade do Porto (CEAUP), 2024. Web. {now_date}. Data generated for period {timeframe}. https://doi.org/10.5281/zenodo.19041041."

def generate_chicago(timeframe: str) -> str:
    """Generate Chicago 17th Edition formatted citation."""
    now_date = datetime.datetime.now().strftime("%B %d, %Y")
    return f'Teixeira, Jorge. "Western Sahara War Archive (2020-2024): Geospatial Conflict Observatory." Centro de Estudos Africanos da Universidade do Porto (CEAUP). 2024. Data generated for period {timeframe}. Accessed {now_date}. https://doi.org/10.5281/zenodo.19041041.'

def generate_numbered(timeframe: str) -> str:
    """Generate Numbered (IEEE) formatted citation."""
    now_date = datetime.datetime.now().strftime("%B %d, %Y")
    return f'[1] J. Teixeira, "Western Sahara War Archive (2020-2024): Geospatial Conflict Observatory," Centro de Estudos Africanos da Universidade do Porto (CEAUP), 2024. [Online]. Available: https://westernsaharawararchive.com/. Data generated for period {timeframe}. [Accessed: {now_date}].'

def generate_html_report(df: pd.DataFrame, timeframe: str, time_mode: str) -> str:
    """
    Generate an HTML report integrating basic text and placeholder 
    areas for charts/maps to be exported as a comprehensive analysis.
    """
    import plotly.io as pio
    import time
    from unittest.mock import patch, MagicMock
    import streamlit as st
    import modules.TOO_module as omm_b
    import modules.Geospatial_analysis_module as omm_g
    from modules.statistical_module import render_statistical_module
    from modules.methodology_module import render_methodology
    from modules.chart_renderer import ChartRenderer
    from modules.map_renderer import MapRenderer
    
    chart_renderer = ChartRenderer()
    map_renderer = MapRenderer()
    
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    collected_html = []
    
    # --- Utils ---
    def get_base64_img(path):
        if os.path.exists(path):
            with open(path, "rb") as f:
                return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
        return ""

    logo_b64 = get_base64_img(os.path.join("assets", "logos", "logo_wswa.png"))

    # counters for scientific labeling
    counters = {"S": 0, "B": 0, "G": 0}

    # --- Mocks ---
    def mock_plotly(fig, **kwargs):
        counters["S"] += 1
        
        # S17 and S18 spacing fixes
        margin_t = 90 if counters["S"] in [17, 18] else 50
        
        chart_name = "Analytical Visualization"
        if hasattr(fig, 'layout') and hasattr(fig.layout, 'title') and getattr(fig.layout.title, 'text', None):
            import re
            raw_title = fig.layout.title.text
            raw_title = re.sub(r'\[A\d+\]\s*', '', raw_title)
            chart_name = raw_title.strip()

        # Ensure Pie charts (like Minurso compliance) get consistent coloring without crashing other charts
        if hasattr(fig, 'data') and len(fig.data) > 0:
            if getattr(fig.data[0], 'type', None) == 'pie':
                try:
                    # Forces explicit colors specifically on Pie traces
                    fig.update_traces(marker=dict(colors=["#007BFF", "#28A745", "#DC3545", "#6C757D"]))
                except Exception:
                    pass

        # S20 long labels shortening fix
        if hasattr(fig, 'data') and len(fig.data) > 0:
            for trace in fig.data:
                if hasattr(trace, 'x') and trace.x is not None:
                    try:
                        trace.x = [label.replace("External Front: Morocco Proper (Deep Strike)", "External: Morocco (Deep)")
                                         .replace("Internal Front: Western Sahara (Standard Theater)", "Internal: Sahara (Std)") 
                                   if isinstance(label, str) else label 
                                   for label in trace.x]
                    except Exception:
                        pass

        fig.update_layout(
            template="plotly_white",
            paper_bgcolor="white",
            plot_bgcolor="white",
            title_pad=dict(b=20),
            margin=dict(l=100, r=50, t=margin_t + 30, b=80), 
            autosize=True,
            title_font=dict(size=18),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        img_path = chart_renderer.render(fig)
        img_b64 = get_base64_img(img_path)

        collected_html.append(f"""
        <div class='figure-box'>
            <img src="{img_b64}" style="width:100%;">
            <div class='scientific-caption'>
                <b>Figure A{counters['S']}:</b> {chart_name} <br>
                <i>Timeframe of Analysis: {timeframe} | © 2024–2026 Jorge Teixeira | Western Sahara War Archive</i>
            </div>
        </div>
        """)

    current_map_context = {"id": "", "name": ""}

    def mock_folium(m, width=None, height=None, **kwargs):
        img_path = map_renderer.render(m)
        img_b64 = get_base64_img(img_path)
        collected_html.append(f"""
        <div class='figure-box map-container'>
            <img src='{img_b64}' style='width:100%;'>
            <div class='scientific-caption'>
                <b>Map {current_map_context['id']}:</b> {current_map_context['name']} <br>
                <i>Timeframe of Analysis: {timeframe} | © 2024–2026 Jorge Teixeira | Western Sahara War Archive</i>
            </div>
        </div>
        """)

    def mock_metric(label, value, delta=None, **kwargs):
        # Metrics are largely removed from page 1 but might appear in statistical module
        collected_html.append(f"<div class='metric-card'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div></div>")

    def mock_dataframe(data, **kwargs):
        if isinstance(data, pd.DataFrame):
            df_to_render = data
        elif isinstance(data, pd.Series):
            df_to_render = data.to_frame()
        else:
            try:
                df_to_render = pd.DataFrame(data)
            except:
                return
        html_table = df_to_render.to_html(classes='data-table', index=False, border=0)
        collected_html.append(f"<div class='table-container' style='margin: 15px 0; overflow-x: auto;'>{html_table}<div class='scientific-caption' style='margin-top: 5px; font-size: 9pt;'><i>Timeframe of Analysis: {timeframe} | © 2024–2026 Jorge Teixeira | Western Sahara War Archive</i></div></div>")

    import re
    def render_markdown_server(text):
        """Simple server-side markdown to clean HTML converter."""
        # Convert Markdown Tables to HTML Tables
        def md_table_to_html(match):
            raw = match.group(0).strip()
            lines = [line.strip() for line in raw.split('\n') if line.strip()]
            if len(lines) < 3:
                return raw
            
            def parse_row(line):
                # Strip leading/trailing | then split
                return [c.strip() for c in line.strip().strip('|').split('|')]
            
            html = ['<table class="data-table" style="border-collapse:collapse;width:100%;margin:10px 0;">']
            headers = parse_row(lines[0])
            html.append('<thead><tr style="background-color:#2c3e50;color:white;">')
            for h in headers:
                html.append(f'<th style="border:1px solid #ccc;padding:8px 12px;text-align:left;">{h}</th>')
            html.append('</tr></thead><tbody>')
            for line in lines[2:]:
                cols = parse_row(line)
                html.append('<tr>')
                for c in cols:
                    html.append(f'<td style="border:1px solid #ddd;padding:7px 12px;">{c}</td>')
                html.append('</tr>')
            html.append('</tbody></table>')
            return '\n'.join(html)
        
        # Match: header row | separator row | data rows
        table_pattern = r'((?:\|[^\n]+\|\s*\n)+\|[-:| ]+\|\s*\n(?:\|[^\n]+\|\s*\n?)+)'
        text = re.sub(table_pattern, md_table_to_html, text + '\n')

        # Clean lines and spacing
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)
        
        # Headers
        text = re.sub(r'^### (.*)', r'<h4>\1</h4>', text, flags=re.M)
        text = re.sub(r'^## (.*)', r'<h3>\1</h3>', text, flags=re.M)
        text = re.sub(r'^# (.*)', r'<h2>\1</h2>', text, flags=re.M)
        
        # Bold and Italic
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        
        # Lists
        text = re.sub(r'^• (.*)', r'<li>\1</li>', text, flags=re.M)
        text = re.sub(r'^\* (.*)', r'<li>\1</li>', text, flags=re.M)
        text = re.sub(r'^- (.*)', r'<li>\1</li>', text, flags=re.M)
        
        # Wrap lists
        text = re.sub(r'(<li>.*</li>)+', r'<ul>\g<0></ul>', text, flags=re.S)
        
        # Paragraphs (br for single breaks, p for double)
        paragraphs = text.split('\n\n')
        wrapped_p = []
        for p in paragraphs:
            if not p.strip(): continue
            # If it's already a tag (h or ul), don't wrap in <p>
            if p.strip().startswith('<h') or p.strip().startswith('<ul') or p.strip().startswith('<ol') or p.strip().startswith('<dl') or p.strip().startswith('<table') or p.strip().startswith('<div') or p.strip().startswith('<p'):
                wrapped_p.append(p)
            else:
                wrapped_p.append(f"<p>{p.strip().replace('\\n', '<br>')}</p>")
        
        return "".join(wrapped_p)

    def mock_markdown(text, **kwargs):
        if not isinstance(text, str): return
        
        # Swallow layout leaks
        if "YouTube" in text or "Host Institution" in text or "Funding Agency" in text or "Creative Commons" in text or "---" == text.strip():
            return
            
        # User Header Promotions
        processed_text = text.replace("### Intensity Classification", "## Intensity Classification")
        processed_text = processed_text.replace("### Digital Humanities Standards", "## Digital Humanities Standards")
        
        # Server-side rendering to clean HTML
        html_text = render_markdown_server(processed_text)
        
        # Professional justified text block
        collected_html.append(f"<div class='markdown-text-container justified-text'>{html_text}</div>")
        
    def mock_title(text, **kwargs):
        collected_html.append(f"<h1 class='report-main-title'>{text}</h1>")

    def mock_subheader(text, **kwargs):
        # Chapter titles mapping
        main_titles = ["Observatory Framework", "Data Sources", "Academic Resources", 
                       "Academic Publications & Research Outputs", "Digital Archives", 
                       "Methodological Approach", "Citation", "Analytical Catalog"]
        if text in main_titles:
            collected_html.append(f"<h2 class='chapter-header'>{text}</h2>")
        else:
            collected_html.append(f"<h3 class='section-header'>{text}</h3>")
        
    def mock_caption(text, **kwargs):
        # Ignore Timeline metadata leaking from app.py
        if isinstance(text, str):
            if "Timeline" in text or "B1" in text or "Jorge Teixeira" in text:
                return
        collected_html.append(f"<div class='context-caption'>{text}</div>")
        
    class DummyExpander:
        def __init__(self, title):
            self.title = title
        def __enter__(self):
            # Flattened: just a box with a title
            collected_html.append(f"<div class='static-expander-box'><div class='expander-fixed-title'>{self.title}</div><div class='expander-content'>")
            return DummyCtx()
        def __exit__(self,*a):
            collected_html.append("</div></div>")

    class DummyCtx:
        def __enter__(self): return self
        def __exit__(self,*a): pass
        def write(self,*a,**kw): pass
        def metric(self, *a, **kw): mock_metric(*a, **kw)
        def markdown(self, *a, **kw): mock_markdown(*a, **kw)
        def subheader(self, *a, **kw): mock_subheader(*a, **kw)
        def title(self, *a, **kw): mock_title(*a, **kw)
        def latex(self, text, **kw): collected_html.append(f"<div class='equation-box'>$${text}$$</div>")
        def plotly_chart(self, *a, **kw): mock_plotly(*a, **kw)
        def dataframe(self, *a, **kw): mock_dataframe(*a, **kw)
        def table(self, *a, **kw): mock_dataframe(*a, **kw)
        def __getattr__(self, name):
            return lambda *args, **kwargs: DummyCtx()

    from contextlib import ExitStack
    
    with ExitStack() as stack:
        stack.enter_context(patch.object(st, 'plotly_chart', side_effect=mock_plotly))
        stack.enter_context(patch.object(omm_b, 'st_folium', side_effect=mock_folium))
        stack.enter_context(patch.object(omm_g, 'st_folium', side_effect=mock_folium))
        stack.enter_context(patch.object(st, 'tabs', side_effect=lambda x: [DummyCtx() for _ in x]))
        stack.enter_context(patch.object(st, 'columns', side_effect=lambda x: [DummyCtx() for _ in range(x)] if isinstance(x, int) else [DummyCtx() for _ in x]))
        stack.enter_context(patch.object(st, 'expander', side_effect=lambda title, **kw: DummyExpander(title)))
        stack.enter_context(patch.object(st, 'metric', side_effect=mock_metric))
        stack.enter_context(patch.object(st, 'markdown', side_effect=mock_markdown))
        stack.enter_context(patch.object(st, 'subheader', side_effect=mock_subheader))
        stack.enter_context(patch.object(st, 'title', side_effect=mock_title))
        stack.enter_context(patch.object(st, 'header', side_effect=mock_title))
        stack.enter_context(patch.object(st, 'caption', side_effect=mock_caption))
        stack.enter_context(patch.object(st, 'latex', side_effect=lambda t,**kw: collected_html.append(f"<div class='equation-box'>$${t}$$</div>")))
        stack.enter_context(patch.object(st, 'dataframe', side_effect=mock_dataframe))
        stack.enter_context(patch.object(st, 'table', side_effect=mock_dataframe))
        stack.enter_context(patch.object(st, 'latex', side_effect=lambda t,**kw: collected_html.append(f"<div class='equation-box'>$${t}$$</div>")))
        
        # Add mock_image to swallow st.image() calls coming from footer logos
        def mock_image(*a, **kw):
            pass
        stack.enter_context(patch.object(st, 'image', side_effect=mock_image))
        stack.enter_context(patch.object(st.sidebar, 'image', side_effect=mock_image))
        
        stack.enter_context(patch.object(st, 'write', MagicMock()))
        stack.enter_context(patch.object(st, 'info', MagicMock()))
        stack.enter_context(patch.object(st, 'warning', side_effect=mock_caption))
        stack.enter_context(patch.object(st, 'error', MagicMock()))
        stack.enter_context(patch.object(st, 'success', MagicMock()))
        stack.enter_context(patch.object(st, 'divider', side_effect=lambda *a,**kw: collected_html.append("<hr class='section-divider'>")))
             
        try:
            # Selection Context Page (Page 1)
            collected_html.append("<div class='page-break'>")
            collected_html.append("<h1>Selection Context, Parameters & Formal Citation</h1><hr>")
            collected_html.append(f"""
            <div class='justified-text' style='margin-top:20px;'>
               <div style='background:#fdf2f2; padding:15px; border-left: 5px solid #c0392b; margin-bottom: 25px;'>
                  <b>Formal Citation:</b><br>
                  Teixeira, Jorge (2024). Western Sahara War Archive (2020-2024): Geospatial Conflict Observatory. 
                  Data generated for period {timeframe}. Retrieved {now} from https://westernsaharawararchive.com/ https://doi.org/10.5281/zenodo.19041041
               </div>

               <p>This report presents an analytical subset of the Western Sahara War Archive database, 
               restricted by the specific filters selected during the observatory session.</p>
               
               <div style='background:#f9f9f9; padding:20px; border-radius:10px; border:1px solid #eee; margin-bottom: 30px;'>
                   <p><b>Temporal Framework:</b> {timeframe} (Filtered by <i>{time_mode}</i>)</p>
                   <p><b>Geospatial Scope:</b> Filtered by Military Regions (Macro Level) and Sectors (Meso Level).</p>
               </div>
               
               <h3>Terminology & Methodology</h3>
               <p><b>Mega Level:</b> Geopolitical entities involved in the theater of operations.</p>
               <p><b>Macro Level:</b> Military Regions providing strategic operational command.</p>
               <p><b>Meso Level:</b> Tactical sectors where kinetic events are documented.</p>
               <p><b>Intensity Classification:</b> Mathematical categorization of sectors into Low, Medium, and High 
               intensity based on event distribution quantiles.</p>
            </div>
            </div>
            """)

            # Table of contents (Hierarchical)
            collected_html.append("<div class='page-break'>")
            collected_html.append("<h1>Table of Contents</h1><hr>")
            collected_html.append("""
            <ul class='toc-list' style='list-style: none; padding: 0;'>
               <li class='toc-item'><span>1. Methodology & Documentation</span><span>3</span></li>
               
               <li class='toc-item' style='font-weight:bold; margin-top:10px;'><span>2. Analytical Framework [A1-A25]</span><span>5</span></li>
               <li class='toc-sub-grid'>
                   <span>2.1: A1-A4 Rhythm & Persistence</span>
                   <span>2.2: A5-A10 Trends & Seasonality</span>
               </li>
               <li class='toc-sub-grid'>
                   <span>2.3: A11-A15 Spatial & Centers</span>
                   <span>2.4: A16-A20 Typology & Compliance</span>
               </li>
               <li class='toc-sub-grid'>
                   <span>2.5: A21-A25 Predictive & Volatility</span>
                   <span></span>
               </li>

               <li class='toc-item' style='font-weight:bold; margin-top:15px;'><span>3. Base Maps (Theater Overview) [B1-B6]</span><span>15</span></li>
               <li class='toc-sub-grid'>
                   <span>3.1: B1 Theater Overview</span>
                   <span>3.2: B2 Territorial Control</span>
               </li>
               <li class='toc-sub-grid'>
                   <span>3.3: B3 Military Regions</span>
                   <span>3.4: B4 Operational Sectors</span>
               </li>
               <li class='toc-sub-grid'>
                   <span>3.5: B5 Moroccan Military Wall</span>
                   <span>3.6: B6 Logistics & Hydrography</span>
               </li>

               <li class='toc-item' style='font-weight:bold; margin-top:15px;'><span>4. Geospatial Analytical Dashboard [G1-G8]</span><span>22</span></li>
               <li class='toc-sub-grid'>
                   <span>4.1: G1 Control Zones Map</span>
                   <span>4.2: G2 Sector Pressure Map</span>
               </li>
               <li class='toc-sub-grid'>
                   <span>4.3: G3 Regional Activity Map</span>
                   <span>4.4: G4 Tactical Density Map</span>
               </li>
               <li class='toc-sub-grid'>
                   <span>4.5: G5 Conflict Hotspots Map</span>
                   <span>4.6: G6 Wall Pressure Map</span>
               </li>
               <li class='toc-sub-grid'>
                   <span>4.7: G7 Operational Corridors Map</span>
                   <span>4.8: G8 Actor Activity Distribution</span>
               </li>
            </ul>
            """)

            # Content
            collected_html.append("<h1 class='page-break'>1. Methodology & Documentation</h1><hr>")
            render_methodology()
            
            collected_html.append("<h1 class='page-break'>2. Analytical Framework</h1><hr>")
            render_statistical_module(df.copy(), timeframe)
            
            collected_html.append("<h1 class='page-break'>3. Base Maps (Theater Overview)</h1><hr>")
            b_names = {
                "B1": "Theater Overview", "B2": "Territorial Control", 
                "B3": "Military Regions", "B4": "Operational Sectors", 
                "B5": "Moroccan Military Wall", "B6": "Logistics & Hydrography"
            }
            for m in ["B1", "B2", "B3", "B4", "B5", "B6"]:
                name = b_names[m]
                current_map_context["id"] = m
                current_map_context["name"] = name
                collected_html.append(f"<h2 class='map-title-outside'>Map {m}: {name}</h2>")
                omm_b.render_overview_map(timeframe, mode=m)
                
            collected_html.append("<h1 class='page-break'>4. Geospatial Analytical Dashboard</h1><hr>")
            for g_id, g_func, g_df in [
                ("G1: Control Zones", omm_g.render_control_zone_map, df),
                ("G2: Sector Pressure", omm_g.render_sector_pressure_map, df),
                ("G3: Regional Activity", omm_g.render_regional_activity_map, df),
                ("G4: Tactical Density", omm_g.render_analytical_map, (df, "density")),
                ("G5: Conflict Hotspots", omm_g.render_analytical_map, (df, "hotspot")),
                ("G6: Wall Pressure", omm_g.render_analytical_map, (df, "wall_pressure")),
                ("G7: Operational Corridors", omm_g.render_operational_corridor_map, df),
                ("G8: Actor Activity Distribution", omm_g.render_analytical_map, (df, "actor")),
            ]:
                parts = g_id.split(":", 1)
                map_id = parts[0].strip()
                map_name = parts[1].strip()
                current_map_context["id"] = map_id
                current_map_context["name"] = map_name
                collected_html.append(f"<h2 class='map-title-outside'>{g_id}</h2>")
                if isinstance(g_df, tuple):
                    g_func(g_df[0], g_df[1])
                else:
                    g_func(g_df)
            
        except Exception as e:
            collected_html.append(f"<div style='color:red;'>Error during rendering: {e}</div>")
        finally:
            map_renderer.close()

    body_content = "".join(collected_html)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>WSWA Analytical Report - {timeframe}</title>
        <style>
            @page {{ 
                size: A4; 
                margin: 25mm 15mm 25mm 15mm; 
                @top-left {{ content: "{now} | Interactive Geospatial Conflict Observatory"; font-family: 'Calibri', sans-serif; font-size: 9px; color: #888; }}
                @top-right {{ content: "WSWA Analytical Report"; font-family: 'Calibri', sans-serif; font-size: 9px; color: #888; }}
                @bottom-left {{ content: "© 2024 Jorge Teixeira | Western Sahara War Archive"; font-family: 'Calibri', sans-serif; font-size: 9px; color: #888; }}
                @bottom-right {{ content: "Page " counter(page); font-family: 'Calibri', sans-serif; font-size: 9px; color: #888; }}
            }}
            body {{ 
                font-family: 'Calibri', 'Trebuchet MS', sans-serif; 
                margin: 0; padding: 0; color: #333; line-height: 1.5; background-color: #fafafa; 
                font-size: 11pt;
            }}
            .paper {{ background-color: #fff; padding: 30mm 15mm; min-height: 297mm; box-shadow: 0 0 10px rgba(0,0,0,0.1); box-sizing: border-box; }}
            
            h1, h2, h3, h4 {{ color: #2c3e50; page-break-after: avoid; }}
            h1 {{ font-size: 24pt; border-bottom: 3px solid #2c3e50; padding-bottom: 10px; margin-top: 40px; }}
            h2 {{ font-size: 18pt; border-bottom: 1px solid #eee; margin-top: 45px; }}
            h2.chapter-header {{ font-size: 20pt; color: #2c3e50; border-bottom: 2px solid #2c3e50; margin-top: 50px; padding-bottom: 5px; }}
            h3.section-header {{ font-size: 14pt; color: #34495e; margin-top: 35px; border-left: 5px solid #2c3e50; padding-left: 10px; }}
            
            .justified-text {{ text-align: justify; font-size: 12pt; }}
            .markdown-text-container p {{ margin-bottom: 15px; }}
            .markdown-text-container ul {{ margin-bottom: 15px; padding-left: 20px; }}
            
            /* Cover Page */
            .cover-page {{ height: 90vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; page-break-after: always; }}
            .cover-logo {{ max-width: 350px; margin-bottom: 50px; }}
            .cover-title {{ font-size: 36pt; font-weight: bold; margin-bottom: 10px; border:none; }}
            .cover-subtitle {{ font-size: 20pt; color: #555; margin-bottom: 60px; border:none; }}
            
            /* TOC */
            .toc-item {{ display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 13pt; border-bottom: 2px solid #eee; padding-bottom: 3px; }}
            .toc-sub-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding-left: 20px; font-size: 10pt; color: #555; margin-bottom: 10px; }}
            .toc-sub-grid span {{ border-bottom: 1px dotted #ddd; }}

            /* Table Styles (Catalog) */
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 10pt; }}
            th {{ background-color: #f2f2f2; border: 1px solid #ddd; padding: 12px; text-align: left; }}
            td {{ border: 1px solid #ddd; padding: 10px; }}
            tr:nth-child(even) {{ background-color: #fafafa; }}

            /* Static Expander */
            .static-expander-box {{ border: 1px solid #ddd; border-radius: 8px; margin: 20px 0; overflow: hidden; }}
            .expander-fixed-title {{ background: #f8f9fa; padding: 12px 20px; font-weight: bold; border-bottom: 1px solid #ddd; color: #1a252f; }}
            .expander-content {{ padding: 20px; }}

            /* Visuals */
            .figure-box {{ margin: 40px auto; page-break-inside: avoid; border: 1px solid #f0f0f0; padding: 15px; background: #fff; max-width: 95%; }}
            .chart-container {{ width: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; }}
            .map-container {{ width: 100%; display: flex; flex-direction: column; align-items: center; border: none; overflow: hidden; }}
            .scientific-caption {{ width: 100%; font-size: 10pt; color: #444; margin-top: 15px; padding-top: 10px; border-top: 1px solid #eee; font-style: italic; text-align: center; }}
            .map-title-outside {{ font-size: 16pt; margin-bottom: 15px; color: #2980b9; text-align: center; }}

            /* Legend Fixes */
            .leaflet-control-layers {{ background: rgba(255,255,255,0.7) !important; filter: drop-shadow(0 0 5px rgba(0,0,0,0.1)); }}
            .leaflet-control-layers-list {{ background: none !important; }}

            .page-break {{ page-break-before: always; }}
            
            @media print {{
                body {{ background: white; }}
                .paper {{ box-shadow: none; padding: 0; width: 100%; }}
                .no-print {{ display: none; }}
                .figure-box {{ border: none; padding: 0; width: 100% !important; }}
                svg {{ max-width: 100% !important; height: auto !important; }}
            }}
        </style>
        <script type="text/javascript" id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    </head>
    <body>
        <div class="no-print" style="text-align: right; margin-bottom: 20px; position: sticky; top: 10px; z-index: 10000;">
            <button onclick="window.print()" style="padding: 12px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">Print to PDF</button>
        </div>
        
        <div class="paper">
            <div class="cover-page">
                <img src="{logo_b64}" class="cover-logo" alt="WSWA Logo">
                <h1 class="cover-title">Western Sahara War Archive</h1>
                <h2 class="cover-subtitle">Comprehensive Analytical Report</h2>
                
                <div class="cover-meta">
                    <p><strong>Period of Analysis:</strong> {timeframe}</p>
                    <p><strong>Generated on:</strong> {now}</p>
                    <br>
                    <p style="font-size: 14px; margin-top: 30px;">© 2024 Jorge Teixeira</p>
                </div>
            </div>

            <div class="body-content">
                {body_content}
            </div>

            <footer style="margin-top: 50px; font-size: 11px; text-align: center; color: #999;">
                © 2024 Jorge Teixeira | Western Sahara War Archive
            </footer>
        </div>
    </body>
    </html>
    """
    return html_content
