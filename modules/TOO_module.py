"""
THEATRE OF OPERATIONS (TOO) MODULE
Strategic Base Maps (B1-B6)
"""

import folium
import streamlit as st
from streamlit_folium import st_folium

# Import shared resources from the centralized geo_utils
from modules.geo_utils import (
    load_geodata,
    mega_level_colors,
    region_colors,
    sector_colors,
    sector_tooltip,
    flag_morocco,
    flag_sadr,
    logo_wswa,
    north_arrow_path
)

def render_overview_map(timeframe: str = "2020-2024", mode: str = "B1") -> None:
    """
    [B1-B6] Render the Operational Theatre Overview Map (Base Maps Suite).
    
    Modes:
    B1: Operational Theater (Full Overview)
    B2: Territorial Control (Sovereignty Focus)
    B3: Military Regions (Macro-Strategic Focus)
    B4: Operational Sectors (Meso-Tactical Focus)
    B6: Logistics & Hydrography (Terrain/Geography Focus)
    """
    geo = load_geodata()
    m = folium.Map(
        location=[24.5,-13],
        zoom_start=6,
        min_zoom=4,
        max_zoom=9,
        tiles="CartoDB positron",
        control_scale=True,
        max_bounds=True,
        min_lat=18,
        max_lat=32,
        min_lon=-20,
        max_lon=-3
    )
# ==========================================================
# HILLSHADE / TERRAIN
# ==========================================================
    opacity_terrain = 0.6 if mode == "B6" else 0.35
    if mode == "B6":
        folium.TileLayer(
            tiles="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
            attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
            name="Topographic Terrain"
        ).add_to(m)
    else:
        folium.TileLayer(
            tiles="https://tiles.wmflabs.org/hillshading/{z}/{x}/{y}.png",
            attr="Hillshade",
            overlay=True,
            opacity=opacity_terrain
        ).add_to(m)
# ==========================================================
# COORDINATE GRID
# ==========================================
    # Manual grid disabled to keep the map cleaner
    # Criar HTML
    title_html = f"""
    <div style="
    position: fixed;
    top: 20px;
    left: 35%;
    transform: translateX(-50%);
    z-index: 9999;
    background-color: rgba(10,10,10,0.96);
    color:white;
    padding: 16px 32px;
    border-radius: 10px;
    font-size: 22px;
    font-weight: 600;
    text-align:center;
    box-shadow: 0 0 15px rgba(0,0,0,0.4);
    ">
    Western Sahara War Archive<br>
    <span style="font-size:16px; font-weight:400; color:#ccc;">
    General Operational Theatre
    </span>
    </div>
    """
    # Adicionar HTML ao mapa
    m.get_root().html.add_child(folium.Element(title_html))

    # Injetar CSS para Tooltips interativos e JS para Escala Dinamica
    custom_assets = """
    <style>
    .leaflet-container {
        background-color: #f5f5f5 !important;
    }
    .leaflet-tooltip {
        pointer-events: auto !important;
        background-color: rgba(255, 255, 255, 0.98) !important;
        border: 1px solid #777 !important;
        border-radius: 6px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        padding: 12px !important;
        font-family: Arial, sans-serif !important;
    }
    .dynamic-scaling {
        transition: transform 0.2s cubic-bezier(0, 0, 0.2, 1);
        transform-origin: center center;
        will-change: transform;
    }
    </style>
    <script>
    (function() {
        function updateScaling() {
            var maps = document.querySelectorAll('.folium-map');
            if (maps.length === 0) return;
            
            maps.forEach(function(m_el) {
                var map = m_el._leaflet_map;
                if (!map) return;
                
                var zoom = map.getZoom();
                // Agressividade aumentada para garantir escala visivel
                // Zoom 6 = 1.0. Zoom 4 = 0.4. Zoom 9 = 2.8.
                var scale = Math.pow(1.65, zoom - 6);
                scale = Math.max(0.15, Math.min(4.0, scale));
                
                var elements = document.querySelectorAll('.dynamic-scaling');
                elements.forEach(function(el) {
                    el.style.transform = 'scale(' + scale + ')';
                });
            });
        }
        setInterval(updateScaling, 300); // Frequencia aumentada para maior fluidez
    })();
    </script>
    """
    m.get_root().html.add_child(folium.Element(custom_assets))
    # ======================================================
    # 1 TERRITORIAL CONTROL
    # ======================================================
    # B6 is "clean" - no territory polygons
    if mode != "B6":
        # Morocco
        folium.GeoJson(
            geo["morocco"],
            style_function=lambda x: {
                "fillColor": mega_level_colors["C1"],
                "color": mega_level_colors["C1"],
                "weight": 1,
                "fillOpacity": 0.4 if mode == "B2" else 0.15
            },
            name="Morocco",
            tooltip=folium.Tooltip(
                f"""
                <div style="text-align: center; width: 180px;">
                    <img src="{flag_morocco}" width="60" style="margin-bottom: 5px; border: 1px solid #ddd;"><br>
                    <b style="color: #B22222; font-size: 14px;">Kingdom of Morocco</b><br>
                    <span style="color: #555; font-size: 11px;">Legal Status: Occupier de jure</span><br>
                    <div style="margin-top: 6px;">
                        <a href="https://westernsaharawararchive.com/category/morocco/" target="_blank" style="color: #3fa9f5; text-decoration: none; font-weight: bold;">View Documents</a>
                    </div>
                </div>
                """, sticky=False
            )
        ).add_to(m)
        # Occupied Western Sahara
        folium.GeoJson(
            geo["occupied"],
            style_function=lambda x: {
                "fillColor": mega_level_colors["C2"],
                "color": mega_level_colors["C2"],
                "weight": 1,
                "fillOpacity": 0.5 if mode == "B2" else 0.2
            },
            name="Occupied Western Sahara",
            tooltip=folium.Tooltip(
                f"""
                <div style="text-align: center; width: 220px;">
                    <img src="{logo_wswa}" width="80" style="margin-bottom: 5px;"><br>
                    <b style="color: #111; font-size: 14px;">Occupied Western Sahara</b><br>
                    <div style="text-align: left; margin-top: 5px;">
                        <span style="color: #666; font-size: 11px;"><b>Occupation Date:</b> 1975</span><br>
                        <span style="color: #666; font-size: 11px;"><b>Status:</b> Non-Self Governing Territory (since 1963)</span>
                    </div>
                </div>
                """, sticky=False
            )
        ).add_to(m)
        folium.GeoJson(
            geo["rasd"],
            style_function=lambda x:{
                "fillColor": mega_level_colors["SADR"],
                "color": mega_level_colors["SADR"],
                "weight":1,
                "fillOpacity": 0.25 if mode in ["B1", "B2"] else 0.05
            },
            name="Liberated Areas (SADR)",
            tooltip=folium.Tooltip(
                f"""
                <div style="text-align: center; width: 180px;">
                    <img src="{flag_sadr}" width="60" style="margin-bottom: 5px; border: 1px solid #ddd;"><br>
                    <b style="color: #50C878; font-size: 14px;">Liberated Areas (SADR)</b><br>
                    <span style="color: #555; font-size: 11px;">Polisario Front Control</span><br>
                    <div style="margin-top: 6px;">
                        <a href="https://westernsaharawararchive.com/category/sadr/" target="_blank" style="color: #3fa9f5; text-decoration: none; font-weight: bold;">View Documents</a>
                    </div>
                </div>
                """, sticky=False
            )
        ).add_to(m)
    # ======================================================
    # 2 Mega Levels Labels
    # ======================================================
    if mode in ["B1", "B2", "B3"]:
        # Morocco Label
        folium.Marker([30.5,-8.5], icon=folium.DivIcon(html="""<div class="dynamic-scaling" style="font-size:18px; font-weight:900; color:#111; text-shadow:2px 2px 4px rgba(255,255,255,0.8); text-transform:uppercase; letter-spacing: 2px;">Morocco</div>""")).add_to(m)
    
    if mode in ["B1", "B2", "B3"]:
        # Occupied Western Sahara
        folium.Marker([27.19459519984905, -18.8], icon=folium.DivIcon(html="""
        <div class="dynamic-scaling" style="position:relative; width:250px; left:-80px; top:-40px;">
            <div style="font-size:16px; font-weight:800; color:#111; text-shadow:1px 1px 3px rgba(255,255,255,0.9); text-align:right; text-transform:uppercase; line-height: 1.1;">
                Occupied<br>Western Sahara
            </div>
            <svg width="250" height="200" style="position:absolute; top:-15px; left:50px; pointer-events:none; z-index:999; overflow:visible;">
                 <path d="M 215 5 C 215 -35, 230 -40, 310 -30" fill="transparent" stroke="#111" stroke-width="2.5" marker-end="url(#arrowhead)"/>
                 <path d="M 195 60 C 195 85, 215 85, 260 85" fill="transparent" stroke="#111" stroke-width="2.5" marker-end="url(#arrowhead)"/>
                 <path d="M 140 80 C 130 110, 120 140, 150 180" fill="transparent" stroke="#111" stroke-width="2.5" marker-end="url(#arrowhead)"/>
                 <defs>
                     <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                         <polygon points="0 0, 10 3.5, 0 7" fill="#111" />
                     </marker>
                 </defs>
            </svg>
        </div>
        """),
            tooltip=folium.Tooltip(
                f"""
                <div style="text-align: center; width: 220px;">
                    <img src="{logo_wswa}" width="80" style="margin-bottom: 5px;"><br>
                    <b style="color: #111; font-size: 14px;">Occupied Western Sahara</b><br>
                    <div style="text-align: left; margin-top: 5px;">
                        <span style="color: #666; font-size: 11px;"><b>Occupation Date:</b> 1975</span><br>
                        <span style="color: #666; font-size: 11px;"><b>Status:</b> Non-Self Governing Territory (since 1963)</span>
                    </div>
                </div>
                """, sticky=False
            )
        ).add_to(m)

        # SADR Label
        folium.Marker([23.5,-11.5], icon=folium.DivIcon(html="""
        <div class="dynamic-scaling" style="position:relative; width: 250px; left:-80px;">
            <div style="font-size:16px; font-weight:800; color:#111; text-shadow:1px 1px 3px rgba(255,255,255,0.9); text-align:center; text-transform:uppercase; line-height: 1.1;">
                Liberated Areas<br>(SADR)
            </div>
            <svg width="150" height="300" style="position:absolute; top:-60px; left:160px; pointer-events:none; z-index:999; overflow:visible;">
                 <!-- North Arrow -->
                 <path d="M 0 65 L 20 -20" fill="transparent" stroke="#111" stroke-width="2.5" marker-end="url(#arrowhead)"/>
                 <!-- West Arrow (Change direction to <-) -->
                 <path d="M -60 85 L -110 85" fill="transparent" stroke="#111" stroke-width="2.5" marker-end="url(#arrowhead)"/>
            </svg>
        </div>
        """),
            tooltip=folium.Tooltip(
                f"""
                <div style="text-align: center; width: 180px;">
                    <img src="{flag_sadr}" width="60" style="margin-bottom: 5px; border: 1px solid #ddd;"><br>
                    <b style="color: #50C878; font-size: 14px;">Liberated Areas (SADR)</b><br>
                    <span style="color: #555; font-size: 11px;">Polisario Front Control</span><br>
                    <div style="margin-top: 6px;">
                        <a href="https://westernsaharawararchive.com/category/sadr/" target="_blank" style="color: #3fa9f5; text-decoration: none; font-weight: bold;">View Documents</a>
                    </div>
                </div>
                """, sticky=False
            )
        ).add_to(m)
    # ======================================================
    # 3 INTERNATIONAL BORDER
    # ======================================================
    folium.GeoJson(
        geo["international_border"],
        style_function=lambda x:{
            "color":"#800080",
            "weight":3
        }
    ).add_to(m)
    # ======================================================
    # 4 MILITARY REGIONS E TOOLTIPS DAS MR
    # ======================================================
    mr_sectors = {
        "MR1": "S1, S2, S3, S4",
        "MR2": "S5, S6, S7, S8",
        "MR3": "S9, S10, S11, S12, S13"
    }
    
    opacity_mr = 0.35 if mode in ["B1", "B3"] else 0.0
    weight_mr = 3 if mode in ["B1", "B3"] else 0
    for mr,gdf in geo["regions"].items():
        color = region_colors[mr]
        sectors_text = mr_sectors.get(mr, "")
        
        # Tooltip para Militar Regions
        mr_html = f"""
        <div style="font-family: Arial, sans-serif; font-size: 12px; width: 220px; padding: 5px; border-left: 4px solid {color};">
            <h4 style="margin: 0; padding-bottom: 4px; border-bottom: 1px solid #ddd; color: #333;">{mr} Region</h4>
            <div style="margin-top: 6px;">
                <b>Sectors:</b> {sectors_text}
            </div>
            <div style="margin-top: 6px;">
                <b>Dominant terrain:</b> {"Hamada (Rocky Plateau)" if mr=="MR1" else "Saguia (River basin)" if mr=="MR2" else "Sandy plains / dunes"}
            </div>
        </div>
        """
        mr_tooltip = folium.Tooltip(mr_html, sticky=True)
        
        folium.GeoJson(
            gdf,
            style_function=lambda x,color=region_colors[mr]:{
                "fillColor":color,
                "color":color,
                "weight":weight_mr,
                "fillOpacity":opacity_mr
            },
            tooltip=mr_tooltip
        ).add_to(m)
        p = gdf.geometry.representative_point().iloc[0]
        
        import base64
        honeycomb_svg = f"""<svg width="40" height="40" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
            <g fill="none" fill-rule="evenodd" stroke-linecap="square" stroke-linejoin="bevel">
                <g fill="{color}" stroke="#ffffff" stroke-opacity="1" stroke-width="2.83465">
                    <path d="M5.19887,9.76378 L5.19887,22.2362 L16,28.4724 L26.8011,22.2362 L26.8011,9.76378 L16,3.52756 L5.19887,9.76378"/>
                </g>
                <g fill="#ffffff" stroke="#ffffff" stroke-width="0.566929">
                    <path d="M11.5814,13.4488 L11.5814,18.5512 L16,21.1024 L20.4186,18.5512 L20.4186,13.4488 L16,10.8976 L11.5814,13.4488"/>
                </g>
            </g>
        </svg>"""
        encoded_svg = base64.b64encode(honeycomb_svg.encode('utf-8')).decode('utf-8')
        uri_svg = f"data:image/svg+xml;base64,{encoded_svg}"
        
        icon_html = f"""
        <div style="display:flex; flex-direction:column; align-items:center; transform: translate(-50%, -100%); width:60px;">
            <div style="font-size:14px; font-weight:900; color:#111; text-shadow:1px 1px 3px rgba(255,255,255,0.9); margin-bottom:2px;">
                {mr}
            </div>
            <img src="{uri_svg}" width="25" />
        </div>
        """
        
        if mode in ["B1", "B3"]:
            folium.Marker(
                [p.y,p.x],
                icon=folium.DivIcon(icon_anchor=(0,-10), html=icon_html)
            ).add_to(m)
    # ======================================================
    # 5 SECTORS
    # ======================================================
    opacity_sec = 0.45 if mode in ["B1", "B4"] else 0.15 if mode == "B5" else 0.05 if mode == "B3" else 0.0
    weight_sec = 1.5 if mode in ["B1", "B4"] else 1.0 if mode == "B5" else 0.5 if mode == "B3" else 0
    for sid,gdf in geo["sectors"].items():
        folium.GeoJson(
            gdf,
            style_function=lambda x,color=sector_colors[sid]:{
                "fillColor":color,
                "color":"#222",
                "weight":weight_sec,
                "fillOpacity":opacity_sec
            },
            tooltip=sector_tooltip(sid) if mode in ["B1", "B4"] else None
        ).add_to(m)
        p = gdf.geometry.representative_point().iloc[0]
        if mode in ["B1", "B4"]:
            folium.Marker(
                [p.y,p.x],
                icon=folium.DivIcon(html=f"""
                <div style="font-size:12px; font-weight:800; color:#111; text-shadow:1px 1px 2px rgba(255,255,255,0.8); text-align:center;">
                {sid}
                </div>
                """)
            ).add_to(m)
    # ======================================================
    # 6 MR BORDERS
    # ======================================================
    if mode in ["B1", "B3"]:
        folium.GeoJson(
            geo["mr1_mr2"],
            style_function=lambda x:{
                "color":"#222",
                "weight":4,
                "dashArray":"15,10"
            }
        ).add_to(m)
        folium.GeoJson(
            geo["mr2_mr3"],
            style_function=lambda x:{
                "color":"#222",
                "weight":4,
                "dashArray":"15,10"
            }
        ).add_to(m)
    # ======================================================
    # 7 CITIES
    # ======================================================
    if mode in ["B1", "B6"]:
        folium.GeoJson(
            geo["roads"],
            style_function=lambda x:{"color":"#666","weight":1.5}
        ).add_to(m)
        folium.GeoJson(
            geo["water_lines"],
            style_function=lambda x:{"color":"#3fa9f5","weight":2}
        ).add_to(m)
        folium.GeoJson(
            geo["water_bodies"],
            style_function=lambda x:{"fillColor":"#7ec8ff","color":"#7ec8ff","fillOpacity":0.6}
        ).add_to(m)
    # ======================================================
    # 8 MOROCCAN MILITARY WALL (OPTIMIZED RENDERING)
    # Camada de brilho reduzida para evitar sombras negras e lag
    weight_wall = 6 if mode in ["B1", "B5", "B6"] else 2.5
    glow_opacity = 0.45 if mode in ["B1", "B5"] else 0.05
    folium.GeoJson(
        geo["wall"],
        style_function=lambda x:{
            "color":"#ff0000",
            "weight":weight_wall * 2,
            "opacity":glow_opacity
        }
    ).add_to(m)
    # Linha principal
    folium.GeoJson(
        geo["wall"],
        style_function=lambda x:{
            "color":"#8B5A2B",
            "weight":weight_wall,
            "opacity":1.0
        }
    ).add_to(m)
    # ======================================================
    # NORTH ARROW
    # ======================================================
    north_arrow = f"""
    <div style="
    position: fixed;
    top: 30px;
    right: 30px;
    z-index: 9999;">
    <img src="{north_arrow_path}" width="50">
    </div>
    """
    m.get_root().html.add_child(folium.Element(north_arrow))
    # Callout antigo foi removido pois a Label SADR em DivIcon cumpre a funÃƒÂ§ÃƒÂ£o de forma mais organica.
    # ======================================================
    legend_title = f"[{mode}] Operational Legend"
    
    # Conditional content for B-modes
    b_focus = ""
    if mode == "B1": b_focus = "<i>Current Focus: Theater Overview</i>"
    elif mode == "B2": b_focus = "<i>Current Focus: Territorial Sovereignity</i>"
    elif mode == "B3": b_focus = "<i>Current Focus: Strategic Military Regions</i>"
    elif mode == "B4": b_focus = "<i>Current Focus: Tactical Sectors</i>"
    elif mode == "B5": b_focus = "<i>Current Focus: Defensive Infrastructure</i>"
    elif mode == "B6": b_focus = "<i>Current Focus: Logistical Geography</i>"

    legend_html = f"""
    <div style="
    position: fixed;
    bottom: 30px;
    left: 30px;
    width: 220px;
    background: rgba(15, 15, 15, 0.7);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    padding: 15px;
    color: white;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    font-size: 13px;
    z-index: 9999;
    box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.4);
    ">
    <b style="font-size: 14px; border-bottom: 1px solid rgba(255,255,255,0.2); display: block; margin-bottom: 8px; padding-bottom: 4px;">Map {mode}: {legend_title.split('] ')[1]}</b>
    <div style="margin-bottom: 0px; font-size: 10px; color: #ffba49; font-weight: bold;">{b_focus}</div>
    
    <b>Territorial Control</b><br>
    <div><span style="background:#B22222;width:16px;height:16px;display:inline-block;margin-right:8px;vertical-align:middle;border:1px solid #999;"></span> Morocco<br></div>
    <div><span style="background:#E6C78F;width:16px;height:16px;display:inline-block;margin-right:8px;vertical-align:middle;border:1px solid #999;"></span> Occupied Western Sahara<br></div>
    <div><span style="background:#50C878;width:16px;height:16px;display:inline-block;margin-right:8px;vertical-align:middle;border:1px solid #999;"></span> Liberated Areas (SADR)<br><br></div>
    
    <b>Military Infrastructure</b><br>
    <div><span style="background:#8B5A2B;width:24px;height:4px;display:inline-block;margin-right:8px;vertical-align:middle;box-shadow:0 0 4px #ff0000;"></span> Moroccan Military Wall<br></div>
    <div><span style="background:#800080;width:24px;height:2px;display:inline-block;margin-right:8px;vertical-align:middle;"></span> International Border<br></div>
    
    <b>Military Regions</b><br>
    <div><span style="background:{region_colors['MR1']};width:14px;height:14px;display:inline-block;margin-right:8px;vertical-align:middle;border:1px solid #999;"></span> MR1 | <span style="background:{region_colors['MR2']};width:14px;height:14px;display:inline-block;margin-right:8px;vertical-align:middle;border:1px solid #999;"></span> MR2 | <span style="background:{region_colors['MR3']};width:14px;height:14px;display:inline-block;margin-right:8px;vertical-align:middle;border:1px solid #999;"></span> MR3</div>
    """
    if mode in ["B1", "B4"]:
        legend_html += "<br><b>Operational Sectors</b><br>"
        for s, color in sector_colors.items():
            legend_html += f'<div><span style="background:{color};width:14px;height:14px;display:inline-block;margin-right:8px;vertical-align:middle;border:1px solid #444;"></span>{s}</div>'
    
    legend_html += f'<div style="border-top: 1px solid rgba(255,255,255,0.1); margin-top: 10px; padding-top: 5px; font-size: 10px; opacity: 0.7;">© 2024–2026 Jorge Teixeira | Timeframe: {timeframe}</div>'
    legend_html += "</div>"
    m.get_root().html.add_child(folium.Element(legend_html))
    # ======================================================
    # FIT BOUNDS
    # ======================================================
    m.fit_bounds([
        [20,-18],
        [30,-5]
    ])
    # ======================================================
    # RENDER MAP
    # ======================================================
    st_folium(
        m,
        use_container_width=True,
        height=900,
        key=f"overview_map_{mode}"
    )
