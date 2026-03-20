import re

replacements = {
    'st.expander("Descriptive Statistics"': 'st.expander("[A1] Descriptive Statistics"',
    'st.subheader("Descriptive Statistics")': 'st.subheader("[A1] Descriptive Statistics")',
    
    'st.expander("Operational Tempo"': 'st.expander("[A2] Operational Tempo"',
    'st.subheader("Operational Tempo")': 'st.subheader("[A2] Operational Tempo & Rhythm")',
    
    'st.expander("Conflict Dynamics"': 'st.expander("[A3] Conflict Dynamics"',
    'st.subheader("Conflict Dynamics")': 'st.subheader("[A3] Conflict Dynamics (Streaks)")',
    
    'st.subheader("Conflict Intensity Index")': 'st.subheader("[I2] Conflict Intensity Index")',
    'st.subheader("Conflict Saturation Index")': 'st.subheader("[I4] Conflict Saturation Index")',
    
    'st.subheader("Temporal Distribution")': 'st.subheader("[A7] Temporal Distribution of Events")',
    'st.subheader("Monthly Distribution of Events")': 'st.subheader("[A10] Monthly Chronological Distribution")',
    'st.subheader("Structural Monthly Average")': 'st.subheader("[A9] Structural Monthly Average")',
    
    'st.subheader("Seasonal Analysis")': 'st.subheader("[A8] Seasonal Analysis")',
    'st.subheader("Annual Conflict Trend")': 'st.subheader("[A5 | A6] Annual Conflict Trend & Momentum")',
    
    'st.subheader("Advanced Visualizations")': 'st.subheader("[Advanced] Moving Averages & Event Distribution")',
    
    'st.subheader("Spatial Distribution")': 'st.subheader("[A11] Hierarchical Spatial Distribution (Treemap)")',
    'st.subheader("Sector Operational Ranking")': 'st.subheader("[A12] Sector Operational Ranking")',
    'st.subheader("Spatial Operational Metrics")': 'st.subheader("[A13] Spatial Operational Metrics")',
    'st.subheader("Temporal Progression of Conflict")': 'st.subheader("[A14*] Temporal Progression of Conflict")',
    
    'st.subheader("Shifting Center of Gravity")': 'st.subheader("[A14] Shifting Center of Gravity")',
    'st.subheader("Geographic Dispersion (HHI)")': 'st.subheader("[A15] Geographic Dispersion (HHI)")',
    'st.subheader("Operational Heatmap")': 'st.subheader("[A16] Operational Heatmap")',
    'st.subheader("Rhythm of War (Weekly Cycle)")': 'st.subheader("[A17] Rhythm of War (Weekly Cycle)")',
    'st.subheader("Escalation Typology (Intensity per Day)")': 'st.subheader("[A18] Escalation Typology (Intensity per Day)")',
    'st.subheader("MINURSO Compliance & Theater Depth")': 'st.subheader("[A19 | A20] MINURSO Compliance & Tactical Depth")',
    'st.subheader("Escalation Chains (Markov Probabilities)")': 'st.subheader("[A21] Escalation Chains (Markov Probabilities)")',
    'st.subheader("Geographic Contagion & Predictive Models")': 'st.subheader("[A22 | A24] Geographic Contagion & Predictive Models")'
}

with open(r'modules/statistical_module.py', 'r', encoding='utf-8') as f:
    text = f.read()

for k, v in replacements.items():
    text = text.replace(k, v)

with open(r'modules/statistical_module.py', 'w', encoding='utf-8') as f:
    f.write(text)
