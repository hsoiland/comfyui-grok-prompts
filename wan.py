import requests
import json
import base64
import io
from PIL import Image

class Wan:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "api_key": ("STRING", {"default": ""}),
                "motion_type": ("STRING", {"default": "hair swaying slightly"}),
            },
            "optional": {
                "image": ("IMAGE",),
                "imagine": ("STRING", {"default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("wan_prompt", "explanation")
    FUNCTION = "generate_wan_prompt"
    CATEGORY = "GrokPrompts"
    OUTPUT_NODE = True

    def generate_wan_prompt(self, prompt, api_key, motion_type, image=None, imagine=""):
        if not api_key:
            return {"ui": {"text": ["No API key provided."]}, "result": (prompt, "No API key provided.")}
        
        try:
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
            
            # Prepare the messages
            messages = []
            
            # System message with the specialized Wan prompt
            system_content = f"""You are a prompt optimization specialist whose goal is to rewrite the user's input prompts into high-quality English prompts for Wan video generation, making them more complete and expressive while maintaining the original meaning. You need to integrate visual details with the input prompt for the rewrite.

Task Requirements:
1. For overly brief user inputs, reasonably infer and supplement details without changing the original meaning, making the video more complete and visually appealing;
2. Improve the characteristics of the main subject in the user's description (such as appearance, expression, quantity, ethnicity, posture, etc.), rendering style, spatial relationships, and camera angles;
3. The overall output should be in English, retaining original text in quotes and book titles as well as important input information;
4. The prompt should match the user's intent and provide a precise and detailed style description. If the user has not specified a style, choose the most appropriate style for the video content;
5. Emphasize movement information and different camera angles, incorporating the motion type '{motion_type}';
6. Your output should convey natural movement attributes, incorporating natural actions related to the described subject category, using simple and direct verbs as much as possible;
7. If an image is provided, reference the detailed information in the image, such as character actions, clothing, backgrounds, and emphasize the details visible in the photo;
8. Control the rewritten prompt to around 80-100 words;
9. Always output in English regardless of input language.

Return a JSON object with 'wan_prompt' and 'explanation' keys."""

            messages.append({
                "role": "system",
                "content": system_content
            })
            
            # User message
            user_content = f"Generate a detailed Wan video prompt for: {prompt}"
            if imagine.strip():
                user_content += f"\n\nCreative direction/imagination: {imagine}"
            
            # If image is provided, convert to base64 and include in the message
            if image is not None:
                # Convert ComfyUI image tensor to PIL Image
                pil_image = Image.fromarray((image.squeeze().cpu().numpy() * 255).astype('uint8'))
                
                # Convert to base64
                buffer = io.BytesIO()
                pil_image.save(buffer, format="PNG")
                img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                
                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_content + "\n\n[Image provided for reference - please analyze the visual details and incorporate them into the video prompt.]"
                        },
                        {
                            "type": "image",
                            "image": f"data:image/png;base64,{img_base64}"
                        }
                    ]
                })
            else:
                messages.append({
                    "role": "user",
                    "content": user_content
                })
            
            data = {
                "messages": messages,
                "model": "grok-3-latest",
                "stream": False,
                "temperature": 0.7
            }
            
            response = requests.post("https://api.x.ai/v1/chat/completions", json=data, headers=headers)
            response.raise_for_status()
            result = response.json().get("choices", [{}])[0].get("message", {}).get("content", "{}")
            
            try:
                result_dict = json.loads(result)
                wan_prompt = result_dict.get("wan_prompt", prompt)
                explanation = result_dict.get("explanation", "Wan video prompt optimized with motion and visual details.")
            except json.JSONDecodeError:
                # If JSON parsing fails, treat the entire response as the wan_prompt
                wan_prompt = result
                explanation = "Wan video prompt generated successfully."
            
            return {"ui": {"text": [explanation]}, "result": (wan_prompt, explanation)}
            
        except Exception as e:
            error_msg = f"Error calling Grok API: {e}"
            print(error_msg)
            return {"ui": {"text": [error_msg]}, "result": (prompt, error_msg)}
