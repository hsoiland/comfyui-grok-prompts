# Grok Prompts

A ComfyUI custom node pack for generating optimized prompts for PonyXL and Flux using the Grok API.

Installation
1. Clone the repository into `ComfyUI/custom_nodes`:
   git clone https://github.com/babydjac/comfyui-grok-prompts.git
2. Install dependencies:
   pip install -r ComfyUI/custom_nodes/grok_prompts/requirements.txt
3. Restart ComfyUI.

Usage
- Add the `PonyXL` or `Flux` node from the `GrokPrompts` category.
- Input a prompt (e.g., "futanari, blonde hair, yellow crop top, gigantic breasts, no pants, no panties, legs spread, indoor bedroom") and your xAI API key (obtainable from https://x.ai/api).
- Connect the `ponyxl_prompt` or `flux_prompt` to a `CLIPTextEncode` node, and `wan_prompt` to a text node for Wan video generation.
- Check the node's display box for Grok's explanation of the prompt optimization.

Requirements
- Python 3.12
- ComfyUI
- xAI API key

requirements.txt
requests>=2.31.0

License
MIT License