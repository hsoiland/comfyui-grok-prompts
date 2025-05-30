import requests
import json

class PonyXL:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "api_key": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("ponyxl_prompt", "wan_prompt")
    FUNCTION = "generate_prompts"
    CATEGORY = "GrokPrompts"
    OUTPUT_NODE = True

    def generate_prompts(self, prompt, api_key):
        if not api_key:
            return {"ui": {"text": ["No API key provided."]}, "result": (prompt, "")}
        try:
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
            data = {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert in crafting streamlined prompts for PonyXL and Wan video generation. For PonyXL, create a concise prompt using only essential Danbooru tags (e.g., blonde_hair, gigantic_breasts, indoor_bedroom), including score_9, score_8_up, score_7_up, source_realistic, rating_mature, without extra descriptors like 'ultra_detailed'. For Wan, create a short video prompt starting with 'a video of' followed by the subject and their action, avoiding extra details like camera or style. Provide a brief explanation of the optimization. Return a JSON object with 'ponyxl_prompt', 'wan_prompt', and 'explanation' keys."
                    },
                    {
                        "role": "user",
                        "content": f"Generate a streamlined PonyXL prompt and a Wan video prompt for: {prompt}"
                    }
                ],
                "model": "grok-3-latest",
                "stream": False,
                "temperature": 0
            }
            response = requests.post("https://api.x.ai/v1/chat/completions", json=data, headers=headers)
            response.raise_for_status()
            result = response.json().get("choices", [{}])[0].get("message", {}).get("content", "{}")
            result_dict = json.loads(result)
            ponyxl_prompt = result_dict.get("ponyxl_prompt", prompt)
            wan_prompt = result_dict.get("wan_prompt", "")
            explanation = result_dict.get("explanation", "Prompts streamlined for PonyXL and Wan.")
            return {"ui": {"text": [explanation]}, "result": (ponyxl_prompt, wan_prompt)}
        except Exception as e:
            error_msg = f"Error calling Grok API: {e}"
            print(error_msg)
            return {"ui": {"text": [error_msg]}, "result": (prompt, "")}

