"""
GEOSPATIAL INTELLIGENCE UTILITIES
Western Sahara War Archive

This module caches heavy Shapefiles and configures global color 
dictionaries to prevent redundant memory loading in Streamlit.
"""

import os
import base64
from typing import Dict

import geopandas as gpd
import folium
import streamlit as st


def image_to_base64(img_path: str) -> str:
    """Read a local image file and return a base64-encoded data URI."""
    if not os.path.exists(img_path):
        return ""
    
    ext = os.path.splitext(img_path)[1].lower()
    if ext == '.svg':
        mime_type = 'image/svg+xml'
    elif ext in ['.jpg', '.jpeg']:
        mime_type = 'image/jpeg'
    else:
        mime_type = 'image/png'

    with open(img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:{mime_type};base64,{encoded_string}"

# ==========================================================
# BASE PROJECT PATH
# ==========================================================
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ==========================================================
# PATHS FOR SYMBOLS AND FLAGS
# ==========================================================
north_arrow_path = image_to_base64(os.path.join(BASE_PATH,"assets/symbols/NorthArrow_04.svg").replace("\\","/"))
flag_morocco = image_to_base64(os.path.join(BASE_PATH,"assets/flags/Flag_of_Morocco.svg.png").replace("\\","/"))
flag_sadr = image_to_base64(os.path.join(BASE_PATH,"assets/flags/Flag_of_the_Sahrawi_Arab_Democratic_Republic.svg.png").replace("\\","/"))
logo_wswa = image_to_base64(os.path.join(BASE_PATH,"assets/logos/logo_wswa.png").replace("\\","/"))

# ==========================================================
# CARTOGRAPHIC COLOR SYSTEM
# ==========================================================
mega_level_colors = {
    "C1": "#B22222",     # Morocco
    "C2": "#E6C78F",     # Occupied Western Sahara
    "SADR": "#50C878"
}
region_colors = {
    "MR1": "#E2EFD9",
    "MR2": "#FEF2CB",
    "MR3": "#FBE4D5"
}
sector_colors = {
    "S1": "#BED5B4","S2": "#90BB7A","S3": "#68A242","S4": "#568736",
    "S5": "#FFDDAD","S6": "#FFCA69","S7": "#EFB300","S8": "#C89600",
    "S9": "#FF6161","S10": "#FF3737","S11": "#FF1D1D","S12": "#D20000",
    "S13": "#A80000"
}

# ==========================================================
# TOOLTIP DATA & FUNCTION
# ==========================================================
sector_metadata = {
"S1": ("MR1 – Oued Daraa","Morocco","Aaga","No"),
"S2": ("MR1 – Oued Daraa","Morocco","Touizgui","No"),
"S3": ("MR1 – Oued Daraa","Morocco – Occupied Western Sahara","El Mahabas","Yes"),
"S4": ("MR2 – Saguia el Hamra","Morocco – Occupied Western Sahara","Farsia","Yes"),
"S5": ("MR2 – Saguia el Hamra","Morocco – Occupied Western Sahara","Haouza","Yes"),
"S6": ("MR2 – Saguia el Hamra","Morocco – Occupied Western Sahara","Smara","Yes"),
"S7": ("MR2 – Saguia el Hamra","Morocco – Occupied Western Sahara","Amgala","Yes"),
"S8": ("MR2 – Saguia el Hamra","Morocco – Occupied Western Sahara","Guelta Zemmour","Yes"),
"S9": ("MR3 – Rio de Oro","Morocco – Occupied Western Sahara","Oum Dreiga","Yes"),
"S10": ("MR3 – Rio de Oro","Morocco – Occupied Western Sahara","El Bagari","Yes"),
"S11": ("MR3 – Rio de Oro","Morocco – Occupied Western Sahara","Auserd","Yes"),
"S12": ("MR3 – Rio de Oro","Morocco – Occupied Western Sahara","Techla","Yes"),
"S13": ("MR3 – Rio de Oro","Morocco – Occupied Western Sahara","Bir Guendouz","Yes")
}

def sector_tooltip(sector: str) -> folium.Tooltip:
    region, territory, city, minurso_control = sector_metadata[sector]
    color_hex = sector_colors.get(sector, "#555")
    
    html = f"""
    <div style="font-family: Arial, sans-serif; font-size: 13px; width: 280px; padding: 6px; box-sizing: border-box;">
        <h4 style="margin-top: 0; margin-bottom: 8px; color: {color_hex}; text-align: center; border-bottom: 2px solid {color_hex}; padding-bottom: 5px; text-shadow: 1px 1px 1px rgba(0,0,0,0.2);">Sector <span style="font-weight: 800; color: #111;">{sector}</span></h4>
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span style="color: #666; font-weight: bold; font-size: 12px; width: 35%;">Region:</span>
            <span style="color: #111; text-align: right; width: 65%; word-wrap: break-word; white-space: normal;">{region}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span style="color: #666; font-weight: bold; font-size: 12px; width: 35%; font-style: italic;">Color Code:</span>
            <span style="color: #111; text-align: right; width: 65%; word-wrap: break-word; font-family: monospace;">{color_hex}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span style="color: #666; font-weight: bold; font-size: 12px; width: 35%;">Control:</span>
            <span style="color: #111; text-align: right; width: 65%; word-wrap: break-word; white-space: normal;">{territory}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span style="color: #666; font-weight: bold; font-size: 12px; width: 35%;">Key Location:</span>
            <span style="color: #111; text-align: right; width: 65%; word-wrap: break-word; white-space: normal;">{city}</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span style="color: #666; font-weight: bold; font-size: 12px; width: 35%;">MINURSO:</span>
            <span style="color: #111; text-align: right; width: 65%; word-wrap: break-word; white-space: normal;">{minurso_control}</span>
        </div>
    </div>
    """
    return folium.Tooltip(html, sticky=True)

# ==========================================================
# LOAD GEODATA (CACHED)
# ==========================================================
@st.cache_resource
def load_geodata() -> Dict:
    geo = {}
    geo["morocco"] = gpd.read_file(os.path.join(BASE_PATH,"data_geo/polygons/MAR_adm0.shp")).to_crs(epsg=4326)
    geo["occupied"] = gpd.read_file(os.path.join(BASE_PATH,"data_geo/polygons/esh_admin0.shp")).to_crs(epsg=4326)
    geo["rasd"] = gpd.read_file(os.path.join(BASE_PATH,"data_geo/polygons/whosonfirst-data-admin-eh-country-polygon.shp")).to_crs(epsg=4326)
    geo["wall"] = gpd.read_file(os.path.join(BASE_PATH,"data_geo/lines/Military Wall.shp")).to_crs(epsg=4326)
    geo["international_border"] = gpd.read_file(os.path.join(BASE_PATH,"data_geo/lines/Border Line.shp")).to_crs(epsg=4326)
    geo["mr1_mr2"] = gpd.read_file(os.path.join(BASE_PATH,"data_geo/lines/Oued Dara-Saguia El Hamara border line.shp")).to_crs(epsg=4326)
    geo["mr2_mr3"] = gpd.read_file(os.path.join(BASE_PATH,"data_geo/lines/Saguia El Hamara-Rio de Oro border line.shp")).to_crs(epsg=4326)
    
    geo["water_bodies"] = gpd.read_file(os.path.join(BASE_PATH,"data_geo/legend/Bodies of Water.shp")).to_crs(epsg=4326)
    geo["roads"] = gpd.read_file(os.path.join(BASE_PATH,"data_geo/legend/Roads.shp")).to_crs(epsg=4326)
    geo["water_lines"] = gpd.read_file(os.path.join(BASE_PATH,"data_geo/legend/Water Lines Symbol.shp")).to_crs(epsg=4326)
    geo["region_symbol"] = gpd.read_file(os.path.join(BASE_PATH,"data_geo/legend/Region Symbol.shp")).to_crs(epsg=4326)
    
    geo["regions"] = {
        "MR1": gpd.read_file(os.path.join(BASE_PATH,"data_geo/polygons/Oued Daraa Region Outline.shp")).to_crs(epsg=4326),
        "MR2": gpd.read_file(os.path.join(BASE_PATH,"data_geo/polygons/Saguia El Hamara Region Outline.shp")).to_crs(epsg=4326),
        "MR3": gpd.read_file(os.path.join(BASE_PATH,"data_geo/polygons/Rio de Oro Region Outline.shp")).to_crs(epsg=4326)
    }
    
    sector_paths = {
        "S1":"Sector 1- Aaga.shp", "S2":"Sector 2-Touizgui.shp", "S3":"Sector 3-El Mahabas.shp",
        "S4":"Sector 4- Farsia.shp", "S5":"Sector 5- Haouza.shp", "S6":"Sector 6-Smara.shp",
        "S7":"Sector 7-Amgala.shp", "S8":"Sector 8-Guelta Zemmour.shp", "S9":"Sector 9-Oum Dreiga.shp",
        "S10":"Sector 10-El Bagari.shp", "S11":"Sector 11- Auserd.shp", "S12":"Sector 12- Techla.shp",
        "S13":"Sector 13-Bir Guendouz.shp"
    }
    geo["sectors"] = {}
    for sid,shp in sector_paths.items():
        geo["sectors"][sid] = gpd.read_file(os.path.join(BASE_PATH,"data_geo/sectors",shp)).to_crs(epsg=4326)
        
    city_paths = {
        "Aaga":"Aaga City.shp", "Touizgui":"Touizgui City.shp", "El Mahabas":"El Mahabas City.shp",
        "Smara":"Smara City.shp", "Farsia":"Farsia City.shp", "Haouza":"Haouza City.shp",
        "Amgala":"Amgala City.shp", "Guelta Zemmour":"Guelta Zemmour City.shp", "Oum Dreiga":"Oum Dreiga City.shp",
        "El Bagari":"El Bagari City.shp", "Auserd":"Auserd City.shp", "Techla":"Techla City.shp",
        "Bir Guendouz":"Bir Guendouz City.shp"
    }
    geo["cities"] = {}
    for name,shp in city_paths.items():
        try:
            file_path = os.path.join(BASE_PATH,"data_geo/points",shp)
            if os.path.exists(file_path):
                geo["cities"][name] = gpd.read_file(file_path).to_crs(epsg=4326)
        except Exception as e:
            print(f"Warning: Could not load city shapefile {shp}: {e}")
            
    return geo
