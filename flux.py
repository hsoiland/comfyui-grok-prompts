import requests
import json

class Flux:
    def __init__(self):
        pass

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
    RETURN_NAMES = ("flux_prompt", "wan_prompt", "negative_prompt")
    FUNCTION = "generate_prompts"
    CATEGORY = "GrokPrompts"
    OUTPUT_NODE = True

    def generate_prompts(self, prompt, api_key, motion_type):
        if not api_key:
            return (prompt, "", "blurry, low_detail, bad_anatomy"), {"ui": {"text": ["No API key provided."]}}
        try:
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
            data = {
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are an expert in crafting streamlined prompts for Flux and Wan video generation. For Flux, create a concise prompt optimized for Flux's style, using descriptive natural language tags focused on subject, scene, and style (e.g., blonde hair, cozy bedroom, photorealistic), avoiding Danbooru-specific tags like score_9, and emphasizing clarity for high-quality output. For Wan, create a short video prompt starting with 'a video of' with the subject, their primary action, and a user-defined visual motion ('{motion_type}'). Also, provide a negative prompt for Flux (e.g., blurry, low_detail, bad_anatomy). Provide a brief explanation of the optimization. Return a JSON object with 'flux_prompt', 'wan_prompt', 'negative_prompt', and 'explanation' keys."
                    },
                    {
                        "role": "user",
                        "content": f"Generate a streamlined Flux prompt, a Wan video prompt, and a negative prompt for: {prompt}"
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
            flux_prompt = result_dict.get("flux_prompt", prompt)
            wan_prompt = result_dict.get("wan_prompt", "")
            negative_prompt = result_dict.get("negative_prompt", "blurry, low_detail, bad_anatomy")
            explanation = result_dict.get("explanation", "Prompts streamlined for Flux and Wan with custom motion.")
            return (flux_prompt, wan_prompt, negative_prompt), {"ui": {"text": [explanation]}}
        except Exception as e:
            error_msg = f"Error calling Grok API: {e}"
            print(error_msg)
            return (prompt, "", "blurry, low_detail, bad_anatomy"), {"ui": {"text": [error_msg]}}
