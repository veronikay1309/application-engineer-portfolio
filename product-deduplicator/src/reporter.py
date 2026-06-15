import os
import json
from jinja2 import Environment, FileSystemLoader
import logging

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generates human-readable dashboards and machine-readable JSON reports."""
    
    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = templates_dir
        os.makedirs(self.templates_dir, exist_ok=True)
        self._create_template()
        self.env = Environment(loader=FileSystemLoader(self.templates_dir))

    def _create_template(self):
        """Creates the Jinja2 HTML template."""
        template_path = os.path.join(self.templates_dir, "dashboard.html.j2")
        if not os.path.exists(template_path):
            html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Data Quality: Duplicate Product Clusters</title>
                <style>
                    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 40px; color: #333; background-color: #f4f6f8; }
                    .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; border-left: 5px solid #3498db; }
                    .card.EXACT { border-left-color: #2ecc71; }
                    .card.FUZZY { border-left-color: #f1c40f; }
                    h1, h2 { color: #2c3e50; }
                    table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px; }
                    th, td { padding: 10px; text-align: left; border-bottom: 1px solid #eee; }
                    th { background-color: #fafafa; color: #7f8c8d; text-transform: uppercase; font-size: 12px;}
                    .badge { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; color: white; }
                    .EXACT { background: #2ecc71; }
                    .FUZZY { background: #f39c12; }
                    .confidence { font-weight: bold; color: #2980b9; }
                </style>
            </head>
            <body>
                <h1>🔍 Suspected Duplicate Clusters</h1>
                <p>Review the following product groupings. Items in the same cluster are suspected to be duplicates of each other.</p>
                
                {% for cluster in clusters %}
                <div class="card {{ cluster.match_type }}">
                    <h3>
                        <span class="badge {{ cluster.match_type }}">{{ cluster.match_type }}</span>
                        Match Key: {{ cluster.match_key }} 
                        | Confidence: <span class="confidence">{{ cluster.confidence }}%</span>
                    </h3>
                    
                    <table>
                        <tr>
                            <th>Product ID</th>
                            <th>Brand</th>
                            <th>Product Name</th>
                            <th>UPC</th>
                            <th>Price</th>
                        </tr>
                        {% for product in cluster.products %}
                        <tr>
                            <td>{{ product.product_id }}</td>
                            <td>{{ product.brand }}</td>
                            <td><strong>{{ product.product_name }}</strong></td>
                            <td>{{ product.upc }}</td>
                            <td>${{ product.price }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                </div>
                {% endfor %}

                {% if not clusters %}
                <div class="card">
                    <p>No duplicates found! Catalog is clean. 🎉</p>
                </div>
                {% endif %}
            </body>
            </html>
            """
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(html)

    def generate(self, exact_clusters: list, fuzzy_clusters: list, output_dir: str):
        """Outputs JSON and HTML reports."""
        os.makedirs(output_dir, exist_ok=True)
        all_clusters = exact_clusters + fuzzy_clusters

        # JSON Export
        json_path = os.path.join(output_dir, "duplicate_clusters.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(all_clusters, f, indent=4)
        logger.info(f"Saved JSON report to {json_path}")

        # HTML Export
        template = self.env.get_template("dashboard.html.j2")
        html = template.render(clusters=all_clusters)
        
        html_path = os.path.join(output_dir, "deduplication_dashboard.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        logger.info(f"Saved HTML dashboard to {html_path}")
