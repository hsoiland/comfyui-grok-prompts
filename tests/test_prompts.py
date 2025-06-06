import json
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import importlib.util

repo_root = Path(__file__).resolve().parents[1]

def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, repo_root / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

ponyxl = load_module("ponyxl", "ponyxl.py")
flux = load_module("flux", "flux.py")
PonyXL = ponyxl.PonyXL
Flux = flux.Flux

class TestPromptNodes(unittest.TestCase):
    def _mock_response(self, content):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "choices": [{"message": {"content": content}}]
        }
        mock_resp.raise_for_status.return_value = None
        return mock_resp

    @patch("requests.post")
    def test_ponyxl_extracts_json_from_codeblock(self, mock_post):
        content = "```json\n{\"ponyxl_prompt\": \"tag1\"}\n```"
        mock_post.return_value = self._mock_response(content)
        node = PonyXL()
        result = node.generate_prompts("test", "key", "motion")
        self.assertIn("tag1", result["result"][0])

    @patch("requests.post")
    def test_flux_extracts_json_from_codeblock(self, mock_post):
        content = "```json\n{\n    \"flux_prompt\": \"tag2\"\n}\n```"
        mock_post.return_value = self._mock_response(content)
        node = Flux()
        result = node.generate_prompts("test", "key", "motion")
        self.assertIn("tag2", result["result"][0])

if __name__ == "__main__":
    unittest.main()
