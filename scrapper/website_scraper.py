import json
from typing import Dict
from scrapegraphai.graphs import SmartScraperMultiGraph


class PropertyWebsiteScrape:
    graph_config = {
        "llm": {"model": "ollama/llama3.2", "model_tokens": 8192},
        "verbose": True,
        "headless": False,
    }

    def __init__(self, source):
        self.prompt = """Extract all available floor plan details from the website. Structure the extracted data as follows:
        Property Information:
        - `property_name`: Name of the property.
        - `website`: Source website URL.

        Floor Plan Details:
        - `floorplan_name`: Name of the floorplan.
        - `price`: Price of the floorplan (if unavailable, return NULL).
        - `number_of_bedrooms`: Number of bedrooms (if unavailable, return NULL).
        - `number_of_bathrooms`: Number of bathrooms (if unavailable, return NULL).
        - `square_feet`: Square footage of the floorplan (if unavailable, return NULL).

        Ensure the extracted data is structured, accurate, and complete. If a field is missing from the website, return NULL instead of omitting it.
        """
        self.source = source
        self.config = self.graph_config

    def run(self):
        self.smart_scraper_graph = SmartScraperMultiGraph(
            self.prompt, self.source, self.config
        )
        return self.smart_scraper_graph.run()

    def get_result(self) -> Dict:

        answer = self.run()
        print("\nhello", answer)

        return json.dumps(answer)
