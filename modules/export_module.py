import os
import datetime
from typing import Optional
import pandas as pd

from weasyprint import HTML


class ExportModule:
    """
    Central export module for all report outputs.
    Handles PDF, CSV, TXT, BibTeX and RIS exports.
    """

    def __init__(self, output_dir: str = "exports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    # =========================
    # 📄 PDF EXPORT
    # =========================
    def export_pdf(self, html_string: str, filename: str) -> str:
        output_path = os.path.join(self.output_dir, f"{filename}.pdf")
        HTML(string=html_string).write_pdf(output_path)
        return output_path

    # =========================
    # 📊 CSV EXPORT
    # =========================
    def export_csv(self, df: pd.DataFrame, filename: str) -> str:
        output_path = os.path.join(self.output_dir, f"{filename}.csv")
        df.to_csv(output_path, index=False, sep=";", encoding="utf-8")
        return output_path

    # =========================
    # 📝 TXT CITATION EXPORT
    # =========================
    def export_citation_txt(self, df: pd.DataFrame, timeframe: str, filename: str) -> str:
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        content = f"""# WESTERN SAHARA WAR ARCHIVE - CITATION REPORT
Generated on: {now} (Local Time)

## 1. RESEARCH DATA ARCHIVE
- Lead Investigator: Jorge Teixeira (CEAUP)
- Host Institution: Centro de Estudos Africanos da Universidade do Porto (CEAUP)
- Copyright: © 2024–2026 Jorge Teixeira
- License: CC BY-NC 4.0
- DOI: https://doi.org/10.5281/zenodo.19041041

## 2. ANALYTICAL CONTEXT
- Study Period: {timeframe}
- Data Universe: {len(df)} Conflict Events
- Total Kinetic Events: {int(df['N_of_Event'].sum())}
- Active Operational Sectors: {df['Meso_Level_ID'].nunique()}

## 3. FORMAL CITATION
Teixeira, Jorge (2024). Western Sahara War Archive (2020-2024): Geospatial Conflict Observatory.
Data generated for period {timeframe}. Retrieved {now} from https://westernsaharawararchive.com/

## 4. METHODOLOGICAL NOTE
This report contains a subset of the archival database filtered according to current user parameters.
The information is subject to continuous correction and institutional review.
"""

        output_path = os.path.join(self.output_dir, f"{filename}.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        return output_path

    # =========================
    # 📚 BIBTEX EXPORT
    # =========================
    def export_bibtex(self, timeframe: str, filename: str) -> str:
        now_year = datetime.datetime.now().year
        now_date = datetime.datetime.now().strftime("%Y-%m-%d")

        content = f"""@misc{{teixeira_wswa_{now_year},
  author       = {{Teixeira, Jorge}},
  title        = {{Western Sahara War Archive (2020-2024): Geospatial Conflict Observatory}},
  year         = {{2024}},
  howpublished = {{\\url{{https://westernsaharawararchive.com/}}}},
  note         = {{Data generated for period {timeframe}. Accessed: {now_date}}},
  organization = {{Centro de Estudos Africanos da Universidade do Porto (CEAUP)}},
  doi          = {{10.5281/zenodo.19041041}}
}}"""

        output_path = os.path.join(self.output_dir, f"{filename}.bib")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        return output_path

    # =========================
    # 📖 RIS EXPORT
    # =========================
    def export_ris(self, timeframe: str, filename: str) -> str:
        now_date = datetime.datetime.now().strftime("%Y/%m/%d")

        content = f"""TY  - COMP
AU  - Teixeira, Jorge
PY  - 2024
TI  - Western Sahara War Archive (2020-2024): Geospatial Conflict Observatory
UR  - https://westernsaharawararchive.com/
Y2  - {now_date}
N1  - Data generated for period {timeframe}.
DO  - 10.5281/zenodo.19041041
PB  - Centro de Estudos Africanos da Universidade do Porto (CEAUP)
ER  - 
"""

        output_path = os.path.join(self.output_dir, f"{filename}.ris")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        return output_path

    # =========================
    # 🚀 FULL EXPORT PIPELINE
    # =========================
    def export_all(
        self,
        df: pd.DataFrame,
        html_string: str,
        timeframe: str,
        base_filename: Optional[str] = None
    ) -> dict:

        if base_filename is None:
            base_filename = f"wswa_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

        results = {}

        results["pdf"] = self.export_pdf(html_string, base_filename)
        results["csv"] = self.export_csv(df, base_filename)
        results["txt"] = self.export_citation_txt(df, timeframe, base_filename)
        results["bibtex"] = self.export_bibtex(timeframe, base_filename)
        results["ris"] = self.export_ris(timeframe, base_filename)

        return results