import requests
import json
import base64
import io
from PIL import Image

class Audio:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "api_key": ("STRING", {"default": ""}),
            },
            "optional": {
                "image": ("IMAGE",),
                "imagine": ("STRING", {"default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("audio_prompt", "explanation")
    FUNCTION = "generate_audio_prompt"
    CATEGORY = "GrokPrompts"
    OUTPUT_NODE = True

    def generate_audio_prompt(self, prompt, api_key, image=None, imagine=""):
        if not api_key:
            return {"ui": {"text": ["No API key provided."]}, "result": (prompt, "No API key provided.")}
        
        try:
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
            
            # Prepare the messages
            messages = []
            
            # System message for audio prompt generation
            system_content = """You are an audio prompt specialist who generates detailed prompts for audio generation models based on visual descriptions or images. Your goal is to create immersive audio prompts that describe sounds, music, ambiance, and effects matching the scene.

Task Requirements:
1. Analyze the input prompt and optional image to infer audio elements like background sounds, actions with audio cues, music style, and atmosphere.
2. For images, describe sounds implied by visual elements (e.g., waves crashing for ocean scenes, footsteps for walking characters).
3. Output a detailed audio prompt in English, 80-100 words, including timing, layers, and intensity.
4. If creative direction is provided, incorporate it.
5. Return a JSON object with 'audio_prompt' and 'explanation' keys."""

            messages.append({
                "role": "system",
                "content": system_content
            })
            
            # User message
            user_content = f"Generate an audio prompt for: {prompt}"
            if imagine.strip():
                user_content += f"\n\nCreative direction: {imagine}"
            
            # If image is provided, add it
            if image is not None:
                pil_image = Image.fromarray((image.squeeze().cpu().numpy() * 255).astype('uint8'))
                buffer = io.BytesIO()
                pil_image.save(buffer, format="PNG")
                img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                
                messages.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_content + "\n\nAnalyze this image for audio elements."},
                        {"type": "image", "image": f"data:image/png;base64,{img_base64}"}
                    ]
                })
            else:
                messages.append({
                    "role": "user",
                    "content": user_content
                })
            
            data = {
                "messages": messages,
                "model": "grok-4-latest",
                "stream": False,
                "temperature": 0
            }
            
            response = requests.post("https://api.x.ai/v1/chat/completions", json=data, headers=headers)
            response.raise_for_status()
            result = response.json().get("choices", [{}])[0].get("message", {}).get("content", "{}")
            
            try:
                result_dict = json.loads(result)
                audio_prompt = result_dict.get("audio_prompt", prompt)
                explanation = result_dict.get("explanation", "Audio prompt generated.")
            except json.JSONDecodeError:
                audio_prompt = result.strip()
                explanation = "Audio prompt generated successfully."
            
            return {"ui": {"text": [explanation]}, "result": (audio_prompt, explanation)}
            
        except Exception as e:
            error_msg = f"Error: {e}"
            print(error_msg)
            return {"ui": {"text": [error_msg]}, "result": (prompt, error_msg)}
