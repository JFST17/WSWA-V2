import plotly.io as pio
import uuid

class ChartRenderer:

    def render(self, fig) -> str:
        output_path = f"/tmp/chart_{uuid.uuid4().hex}.png"
        
        pio.write_image(fig, output_path, format="png", scale=3)  
        # scale=3 = qualidade alta para PDF
        
        return output_path