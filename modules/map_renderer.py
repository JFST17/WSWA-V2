import tempfile
import time
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class MapRenderer:

    def __init__(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1400,1000")
        self.driver = webdriver.Chrome(options=options)

    def render(self, folium_map) -> str:
        tmp_html = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        folium_map.save(tmp_html.name)

        self.driver.get(f"file://{tmp_html.name}")
        time.sleep(2.5)  # tiles loading

        output_path = f"/tmp/map_{uuid.uuid4().hex}.png"
        self.driver.save_screenshot(output_path)

        return output_path

    def close(self):
        self.driver.quit()