"""
GEOSPATIAL ANALYSIS MODULE
Analytical Dashboards (G1-G8)
"""

import pandas as pd
import folium
import streamlit as st
import branca.colormap as cm
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# Import shared resources from the centralized geo_utils
from modules.geo_utils import (
    load_geodata,
    sector_colors,
    region_colors
)

def render_folium_analytical_map_base(df: pd.DataFrame, mode: str = "density", timeframe: str = "2020-2024", key: str = "folium_map") -> None:
    """
    [G1-G8, B2-B6] Universal Folium Renderer (Style identical to G3).
    Includes the Base GeoJSON overlaps and custom HTML interactive Legends.
    """
    geo = load_geodata()
    m = folium.Map(
        location=[24.5, -13], 
        zoom_start=6, min_zoom=4, max_zoom=9, 
        control_scale=True, 
        tiles="CartoDB positron",
        max_bounds=True,
        min_lat=18, max_lat=32, min_lon=-20, max_lon=-3
    )
    
    # Add Moroccan Military Wall
    if "wall" in geo and not geo["wall"].empty:
        folium.GeoJson(
            geo["wall"], 
            style_function=lambda x: {"color": "#8B5A2B", "weight": 2.5, "opacity": 0.8},
            tooltip="Moroccan Military Wall"
        ).add_to(m)

    # Extract Data based on Sector-City Centroids
    sector_to_city = {
        "S1": "Aaga", "S2": "Touizgui", "S3": "El Mahabas", "S4": "Farsia", "S5": "Haouza",
        "S6": "Smara", "S7": "Amgala", "S8": "Guelta Zemmour", "S9": "Oum Dreiga",
        "S10": "El Bagari", "S11": "Auserd", "S12": "Techla", "S13": "Bir Guendouz"
    }
    
    centroids = {}
    for sid, city_name in sector_to_city.items():
        if "cities" in geo and city_name in geo["cities"] and not geo["cities"][city_name].empty:
            geom = geo["cities"][city_name].geometry.iloc[0]
            centroids[sid] = (geom.y, geom.x)
        else:
            centroids[sid] = (24.5, -13)

    df_agg = df[df["N_of_Event"] > 0].groupby("Meso_Level_ID")["N_of_Event"].sum().reset_index()
    if not df_agg.empty:
        df_agg["lat"] = df_agg["Meso_Level_ID"].map(lambda x: centroids.get(x, (24.5, -13))[0])
        df_agg["lon"] = df_agg["Meso_Level_ID"].map(lambda x: centroids.get(x, (24.5, -13))[1])
    else:
        df_agg = pd.DataFrame(columns=["Meso_Level_ID", "N_of_Event", "lat", "lon"])

    # Title Injector via HTML
    titles = {
        "density": "Map G4: Tactical Density Heatmap",
        "hotspot": "Map G5: Conflict Hotspots Map",
        "wall_pressure": "Map G6: Tactical Wall Pressure Map",
        "actor": "Map G8: Actor Activity Distribution Map",
        "sector_pressure": "Map G2: Sector Activity Pressure",
        "regional_activity": "Map G3: Regional Strategic Map",
        "control_zone": "Map G1: Control & Intensity Distribution",
        "corridors": "Map G7: Operational Corridors Map"
    }
    title_text = f"{titles.get(mode, 'Analytical Map')} ({timeframe})"
    
    title_html = f'''
        <div style="position: fixed; top: 15px; left: 50%; transform: translateX(-50%); z-index:9999; 
                    background: rgba(255,255,255,0.9); padding: 10px 20px; border-radius: 6px;
                    border: 1px solid rgba(0,0,0,0.1); box-shadow: 0px 3px 6px rgba(0,0,0,0.15); 
                    font-size: 15px; font-weight: bold; color: #2c3e50;">
            {title_text}
        </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))

    # Apply Data Layers and Legends
    max_ev = float(df_agg["N_of_Event"].max()) if not df_agg.empty else 1.0

    if mode in ["density", "hotspot", "wall_pressure", "corridors"]:
        for index, row in df_agg.iterrows():
            lat, lon = float(row['lat']), float(row['lon'])
            weight = float(row['N_of_Event']) / max_ev if max_ev > 0 else 0.1
            
            # Massive radius transforms clusters into an overarching continuous regional heat cloud.
            # 3-layer radial glow natively simulates a HeatMap without external JS dependencies.
            folium.CircleMarker(
                [lat, lon], radius=70 * weight + 25, stroke=False, 
                fill=True, fill_color="#ff0000", fill_opacity=0.1
            ).add_to(m)
            
            folium.CircleMarker(
                [lat, lon], radius=40 * weight + 15, stroke=False, 
                fill=True, fill_color="#ff4400", fill_opacity=0.25
            ).add_to(m)
            
            folium.CircleMarker(
                [lat, lon], radius=15 * weight + 5, stroke=False, 
                fill=True, fill_color="#ffaa00", fill_opacity=0.6,
                tooltip=f"<b>Sector:</b> {row['Meso_Level_ID']}<br><b>Density Events:</b> {int(row['N_of_Event'])}"
            ).add_to(m)
        
        legend_html = f"""
        <div style="position: fixed; bottom: 80px; left: 50px; width: 220px; 
        border:1px solid rgba(255,255,255,0.2); z-index:9999; font-size:12px; font-family: sans-serif;
        background: rgba(44, 62, 80, 0.9); backdrop-filter: blur(8px);
        padding: 12px; color: white; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
        <b style="border-bottom: 1px solid rgba(255,255,255,0.3); display: block; margin-bottom: 8px; padding-bottom: 4px;">Density Legend</b>
        <div style="margin-bottom: 6px;">Peak Frequency: <b>{int(max_ev)}</b></div>
        <i style="background: linear-gradient(to right, blue, cyan, lime, yellow, red); width: 100%; height: 14px; display: inline-block; border: 1px solid #777; border-radius: 3px;"></i>
        <div style="display: flex; justify-content: space-between; font-size: 10px; margin-top:4px;">
            <span>Low Intensity</span><span>High Intensity</span>
        </div>
        </div>
        """
        m.get_root().html.add_child(folium.Element(legend_html))
        
    else:
        for index, row in df_agg.iterrows():
            count = float(row["N_of_Event"])
            sector = row["Meso_Level_ID"]
            lat, lon = float(row["lat"]), float(row["lon"])
            
            radius = max(8, (count / max_ev) * 35) if max_ev > 0 else 8
            
            if mode == "actor":
                color = sector_colors.get(sector, "#3fa9f5")
            else:
                color = "#E74C3C" if count > (max_ev/3) else "#F1C40F"
                
            folium.CircleMarker(
                location=[lat, lon], radius=radius, color=color,
                fill=True, fill_color=color, fill_opacity=0.7, weight=1,
                tooltip=f"<b>Sector:</b> {sector}<br><b>Events:</b> {int(count)}"
            ).add_to(m)

        legend_html = f"""
        <div style="position: fixed; bottom: 80px; left: 50px; width: 220px; 
        border:1px solid rgba(255,255,255,0.2); z-index:9999; font-size:12px; font-family: sans-serif;
        background: rgba(44, 62, 80, 0.9); backdrop-filter: blur(8px);
        padding: 12px; color: white; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
        <b style="border-bottom: 1px solid rgba(255,255,255,0.3); display: block; margin-bottom: 8px; padding-bottom: 4px;">Node Legend</b>
        <div style="margin-bottom: 6px;">Absolute Peak: <b>{int(max_ev)}</b></div>
        <div style="margin-top: 8px;">
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <span style="color: #E74C3C; font-size:20px; margin-right: 8px;">●</span> Major Node
            </div>
            <div style="display: flex; align-items: center;">
                <span style="color: #F1C40F; font-size:14px; margin-right: 8px;">●</span> Minor Node
            </div>
        </div>
        </div>
        """
        m.get_root().html.add_child(folium.Element(legend_html))

    st_folium(m, use_container_width=True, height=650, key=key)


def render_analytical_map(df: pd.DataFrame, mode: str = "density", map_key: str = "analytical_heatmap_map", timeframe: str = "2020-2024") -> None:
    """[G4-G8] Render the Analytical Map Suite."""
    render_folium_analytical_map_base(df, mode=mode, timeframe=timeframe, key=map_key)

def render_sector_pressure_map(df: pd.DataFrame, map_key: str = "sector_pressure", timeframe: str = "2020-2024") -> None:
    """[G2] Render the Sector Activity Map."""
    render_folium_analytical_map_base(df, mode="sector_pressure", timeframe=timeframe, key=map_key)

def render_control_zone_map(df: pd.DataFrame, map_key: str = "control_zone", timeframe: str = "2020-2024") -> None:
    """[G1] Render the Event Distribution & Control Zone Map."""
    render_folium_analytical_map_base(df, mode="control_zone", timeframe=timeframe, key=map_key)

def render_operational_corridor_map(df: pd.DataFrame, map_key: str = "corridors", timeframe: str = "2020-2024") -> None:
    """[G7] Render the Operational Corridors & Logistics Map."""
    render_folium_analytical_map_base(df, mode="corridors", timeframe=timeframe, key=map_key)


def render_regional_activity_map(df: pd.DataFrame, map_key: str = "regional_activity", timeframe: str = "2020-2024") -> None:
    """[G3] Render the Military Region Activity Map (Strategic Scale)."""
    geo = load_geodata()
    m = folium.Map(
        location=[24.5, -13], zoom_start=6, min_zoom=4, max_zoom=9, 
        control_scale=True, tiles="CartoDB positron",
        max_bounds=True, min_lat=18, max_lat=32, min_lon=-20, max_lon=-3
    )
    
    if "wall" in geo and not geo["wall"].empty:
        folium.GeoJson(geo["wall"], style_function=lambda x: {"color": "#8B5A2B", "weight": 2.5, "opacity": 0.8}).add_to(m)

    region_counts = df.groupby("Macro_Level_ID")["N_of_Event"].sum().to_dict()
    max_ev = max(region_counts.values()) if region_counts else 100
    colormap = cm.linear.YlOrRd_09.scale(0, max_ev)
    colormap.caption = 'Total Conflict Events per Military Region'

    m.add_child(colormap)
    
    for rid, gdf in geo["regions"].items():
        val = region_counts.get(rid, 0)
        fill_color = colormap(val) if val > 0 else "#cccccc"
        border_color = region_colors.get(rid, "#333333")
        
        folium.GeoJson(
            gdf,
            style_function=lambda x, fc=fill_color, bc=border_color: {
                "fillColor": fc, 
                "color": bc, 
                "weight": 4, 
                "fillOpacity": 0.6 if fc != "#cccccc" else 0.2
            },
            tooltip=f"Region: {rid} | Total Events: {val}"
        ).add_to(m)

    legend_html = f"""
    <div style="position: fixed; bottom: 80px; left: 50px; width: 210px; 
    border:1px solid rgba(255,255,255,0.1); z-index:9999; font-size:12px; font-family: sans-serif;
    background: rgba(30,30,30, 0.8); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
    padding: 10px; color: white; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
    <b style="border-bottom: 1px solid rgba(255,255,255,0.2); display: block; margin-bottom: 5px;">Map G3: Regional Activity Scale</b>
    <div style="margin-bottom: 5px;">Events: <b>0 to {int(max_ev)}</b></div>
    <i style="background: linear-gradient(to right, #FFFFE5, #FFF7BC, #FEE391, #FEC44F, #FB9A29, #EC7014, #CC4C02, #993404, #662506); width: 140px; height: 12px; display: inline-block; border: 1px solid #777;"></i>
    <div style="display: flex; justify-content: space-between; width: 140px; font-size: 9px;">
        <span>Low</span><span>High</span>
    </div>
    <div style="margin-top: 5px; font-size: 10px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 5px;">© Jorge Teixeira | {timeframe}</div>
    <div style="margin-top: 8px; font-size: 10px;">
        <span style="color: {region_colors['MR1']};">●</span> MR1 | 
        <span style="color: {region_colors['MR2']};">●</span> MR2 | 
        <span style="color: {region_colors['MR3']};">●</span> MR3
    </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    m.fit_bounds([[20,-18], [30,-5]])
    st_folium(m, use_container_width=True, height=700, key=map_key)
