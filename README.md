# 🧠 ComfyUI Grok Prompts

**AI-Powered Prompt Engineering Nodes for ComfyUI using xAI's Grok API.**  
Fine-tune your prompt craft with LLM intelligence, split, recombine, and visualize prompt transformations, all inside ComfyUI.

---

## 🔧 What is this?

**`comfyui-grok-prompts`** is a modular node suite for ComfyUI that uses xAI’s **Grok LLM API** to transform user input into optimized prompts for AI models like **PonyXL** and **Flux**. These nodes intelligently:

- ✂️ Split prompts into subject/scene (`text_l`) and style/mood (`text_g`)
- 🔀 Combine and rewrite them into **perfectly scored** Danbooru-tagged prompts
- 🎥 Output video prompts using **Wan’s Advanced Prompt Formula**
- 💬 Display a UI explanation of how the prompt was refined

---

## 🌈 Live Visual Demos

| Model | Image | Video |
|:-----:|:-----:|:-----:|
| **PonyXL** | ![Pony](https://raw.githubusercontent.com/babydjac/comfyui-grok-prompts/main/media/PonyExample.png) | <video src="https://raw.githubusercontent.com/babydjac/comfyui-grok-prompts/main/media/PonyVideo.mp4" autoplay loop muted playsinline width="320"></video> |
| **Flux** | ![Flux](https://raw.githubusercontent.com/babydjac/comfyui-grok-prompts/main/media/FluxExample.png) | <video src="https://raw.githubusercontent.com/babydjac/comfyui-grok-prompts/main/media/FluxVideo.mp4" autoplay loop muted playsinline width="320"></video> |

---

## 🧩 Node Packs Included

### 🔹 `PonyXL Grok Prompter`

- Inputs a messy or vague text prompt
- Outputs:
  - `ponyxl_prompt`: compact Danbooru-tagged string (e.g. `score_9, blonde_hair, gigantic_breasts, no_pants`)
  - `wan_prompt`: video prompt like `a video of a blonde futanari spreading her legs in a bedroom`
- Displays: UI explanation from Grok about how it processed your input

### 🔸 `Flux Grok Prompter`

- Similar to PonyXL node, but tuned for Flux aesthetic prompts (e.g., `liquid chrome surface, fractal blur`, no Danbooru tagging)
- Emphasis on:
  - experimental structure
  - abstract imagery
  - photoreal surrealist phrasing

---

## 📂 Media Folder Contents

All media live in [`/media`](https://github.com/babydjac/comfyui-grok-prompts/tree/main/media):

| File | Description |
|------|-------------|
| `PonyExample.png` | PonyXL still image output |
| `FluxExample.png` | Flux still image output |
| `PonyVideo.mp4`   | PonyXL prompt-to-video animation |
| `FluxVideo.mp4`   | Flux prompt-to-video animation |

---

## 🎨 Bonus UI/Visual Assets

Additional user assets, great for banners, README visuals, or thumbnails:
- ![Asset 1](https://github.com/user-attachments/assets/b3e1b7de-aa27-4172-b1b8-eba61548e2d9)
- ![Asset 2](https://github.com/user-attachments/assets/acc0ca68-ad93-41f9-a1be-8d695d141b9d)

---

## 🛠 Installation

```bash
git clone https://github.com/babydjac/comfyui-grok-prompts.git
cd comfyui-grok-prompts
# Then move custom_nodes/* to your ComfyUI/custom_nodes/
```

---


---

## 🔐 xAI API Required

To use these nodes, get your Grok API key from [x.ai](https://x.ai/api) and input it in the node's `api_key` field.

---

## 💬 Example Output

```json
{
  "ponyxl_prompt": "score_9, score_8_up, rating_mature, futanari, blonde_hair, yellow_crop_top, gigantic_breasts, no_pants, no_panties, legs_spread, huge_penis, indoor_bedroom",
  "wan_prompt": "a video of a blonde futanari spreading her legs in a bedroom",
  "explanation": "Combined and cleaned Danbooru tags for clarity, emphasis, and aesthetic scoring. Generated concise video scene prompt from subject + motion."
}
```

---

## 🚀 Use Case

- Generate highly-optimized, anime-styled render prompts (PonyXL)
- Build surreal abstract visuals (Flux)
- Animate scenes with natural language storytelling (Wan)
- Perfect for NSFW creators, experimental artists, or prompt engineers

---

## 💡 Inspiration

Born from the need to **bridge prompting with LLM intuition**, this project was sparked by curiosity, refined by obsession, and powered by Grok.

---

## 🫡 Credits

Brought to you by [@babydjac](https://github.com/babydjac)  
Powered by: [ComfyUI](https://github.com/comfyanonymous/ComfyUI) & [xAI's Grok](https://x.ai/)

---

**Prompt smarter. Generate harder.**
