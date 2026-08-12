import json
import re
import requests
from typing import List, Dict, Any

from scrapeforge.core import BaseModule
from .config import RuneScapeGEConfig

class RuneScapeGEScraper(BaseModule):
    def __init__(self, config: RuneScapeGEConfig):
        super().__init__(config)
        self.config = config

    def _extract_items(self, html: str) -> List[Dict[str, Any]]:
        items = []
        # The OSRS GE page embeds item data in structured format.
        # This regex captures the required fields from the HTML payload.
        pattern = re.compile(r'"name":"([^"]+)".*"price":(\d+).*?"volume":(\d+)', re.DOTALL)
        for match in pattern.finditer(html):
            items.append({
                "item_name": match.group(1),
                "current_price": int(match.group(2)),
                "daily_volume": int(match.group(3)),
                "price_trend": "unknown"
            })
            if len(items) >= self.config.max_items:
                break
        return items

    def run(self) -> List[Dict[str, Any]]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.0.0 Safari/537.36"
        }
        response = requests.get(self.config.url, headers=headers)
        response.raise_for_status()

        items = self._extract_items(response.text)
        return items
