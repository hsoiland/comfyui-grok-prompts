import requests
import json
import re

class PonyXL:
    def __init__(self):
        pass

    @staticmethod
    def _extract_json(text: str) -> str:
        """Return the first JSON object found in the text."""
        match = re.search(r"{.*}", text, re.DOTALL)
        return match.group(0) if match else "{}"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "api_key": ("STRING", {"default": ""}),
                "motion_type": ("STRING", {"default": "hair swaying slightly"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("ponyxl_prompt", "wan_prompt", "negative_prompt")
    FUNCTION = "generate_prompts"
    CATEGORY = "GrokPrompts"
    OUTPUT_NODE = True

    def generate_prompts(self, prompt, api_key, motion_type):
        if not api_key:
            return {"ui": {"text": ["No API key provided."]}, "result": (prompt, "", "blurry, low_quality, bad_anatomy, oversaturated")}
        try:
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
            data = {
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are an expert in crafting detailed prompts for PonyXL and Wan video generation. For PonyXL, create a detailed prompt with essential and descriptive Danbooru tags (e.g., blonde_hair, gigantic_breasts, indoor_bedroom, detailed_background, intricate_clothing, dynamic_pose), comma-separated, including score_9, score_8_up, score_7_up, source_realistic, rating_mature, and avoiding vague descriptors like 'ultra_detailed'. For Wan, create a short video prompt starting with 'a video of' with the subject, their primary action, and a user-defined visual motion ('{motion_type}'). Also, provide a negative prompt for PonyXL (e.g., blurry, low_quality, bad_anatomy, oversaturated). Provide a brief explanation of the optimization. Return a JSON object with 'ponyxl_prompt', 'wan_prompt', 'negative_prompt', and 'explanation' keys."
                    },
                    {
                        "role": "user",
                        "content": f"Generate a detailed PonyXL prompt, a Wan video prompt, and a negative prompt for: {prompt}"
                    }
                ],
                "model": "grok-3-latest",
                "stream": False,
                "temperature": 0
            }
            response = requests.post("https://api.x.ai/v1/chat/completions", json=data, headers=headers)
            response.raise_for_status()
            result = response.json().get("choices", [{}])[0].get("message", {}).get("content", "{}")
            clean_json = self._extract_json(result)
            try:
                result_dict = json.loads(clean_json)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON returned: {clean_json}") from e
            ponyxl_prompt = result_dict.get("ponyxl_prompt", prompt)
            wan_prompt = result_dict.get("wan_prompt", "")
            negative_prompt = result_dict.get("negative_prompt", "blurry, low_quality, bad_anatomy, oversaturated")
            explanation = result_dict.get("explanation", "Prompts optimized with detailed Danbooru tags for PonyXL and custom Wan motion.")
            return {"ui": {"text": [explanation]}, "result": (ponyxl_prompt, wan_prompt, negative_prompt)}
        except Exception as e:
            error_msg = f"Error calling Grok API: {e}"
            print(error_msg)
            return {"ui": {"text": [error_msg]}, "result": (prompt, "", "blurry, low_quality, bad_anatomy, oversaturated")}
