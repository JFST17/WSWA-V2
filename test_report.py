import sys
import time
import pandas as pd
from unittest.mock import patch, MagicMock

sys.path.append(".")
import streamlit as st
import modules.overview_map_module as omm
from modules.statistical_module import render_statistical_module
from modules.methodology_module import render_methodology

df = pd.read_csv("data/Matrix_Database_2020_2024.csv", sep=";", low_memory=False)
df["Event_Date"] = pd.to_datetime(df["Event_Date"], dayfirst=True, errors="coerce")
df["N_of_Event"] = pd.to_numeric(df["N_of_Event"], errors="coerce").fillna(0)
df["Conflict_Year"] = 2021
df["Meso_Level_ID"] = df.get("Meso_Level_ID", "S1")

start = time.time()

collected = []
def mock_plotly(fig, **kwargs): collected.append("plotly")
def mock_folium(m, **kwargs): collected.append("folium")

class DummyCtx:
    def __enter__(self): return self
    def __exit__(self,*a): pass
    def metric(self,*a,**kw): pass
    def markdown(self,*a,**kw): pass
    def subheader(self,*a,**kw): pass

with patch.object(st, 'plotly_chart', side_effect=mock_plotly), \
     patch.object(omm, 'st_folium', side_effect=mock_folium), \
     patch.object(st, 'tabs', side_effect=lambda x: [DummyCtx() for _ in x]), \
     patch.object(st, 'columns', side_effect=lambda x: [DummyCtx() for _ in range(x) if isinstance(x, int)] or [DummyCtx() for _ in x]), \
     patch.object(st, 'expander', side_effect=lambda *a,**kw: DummyCtx()), \
     patch.object(st, 'metric', MagicMock()), \
     patch.object(st, 'markdown', MagicMock()), \
     patch.object(st, 'subheader', MagicMock()), \
     patch.object(st, 'caption', MagicMock()), \
     patch.object(st, 'write', MagicMock()), \
     patch.object(st, 'info', MagicMock()), \
     patch.object(st, 'warning', MagicMock()), \
     patch.object(st, 'error', MagicMock()), \
     patch.object(st, 'success', MagicMock()), \
     patch.object(st, 'divider', MagicMock()):
         
     try:
         render_statistical_module(df, "2021")
         for m in ["B1", "B2", "B3", "B4", "B5", "B6"]:
             omm.render_overview_map("2021", m)
         for mode in ["density", "hotspot", "wall_pressure", "actor"]:
             omm.render_analytical_map(df, mode)
         omm.render_control_zone_map(df, "z")
         omm.render_sector_pressure_map(df, "z")
         omm.render_regional_activity_map(df, "z")
         omm.render_operational_corridor_map(df, "z")
         render_methodology()
     except Exception as e:
         print("Error:", e)

print(f"Time: {time.time()-start:.2f}s, Items: {len(collected)}")
