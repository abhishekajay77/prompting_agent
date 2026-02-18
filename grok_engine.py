import os
import json
import base64
import time
import re
from groq import Groq

class GrokAgenticEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Groq API Key not found. Please provide it in settings.")
        
        self.client = Groq(
            api_key=self.api_key
        )
        self.primary_model = "llama-3.3-70b-versatile"
        self.fallback_model = "qwen/qwen3-32b" # Upgraded from 8B for better accuracy
        self.vision_model = "meta-llama/llama-4-scout-17b-16e-instruct"

    def _safe_call(self, model, messages, temperature=0.2, response_format=None):
        """Standard API call with retry and fallback for rate limits."""
        max_retries = 3
        retry_delay = 2 
        
        for attempt in range(max_retries):
            try:
                params = {
                    "model": model,
                    "messages": messages,
                    "temperature": temperature
                }
                if response_format:
                    params["response_format"] = response_format
                
                response = self.client.chat.completions.create(**params)
                content = response.choices[0].message.content
                
                # Clean up <think> tags if present
                if "<think>" in content:
                    content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
                
                return content.strip()
            except Exception as e:
                error_str = str(e)
                if "rate_limit_exceeded" in error_str or "429" in error_str:
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay *= 2
                        continue
                    elif model == self.primary_model:
                        # Fallback to Qwen 32B if primary exhausted
                        return self._safe_call(self.fallback_model, messages, temperature, response_format)
                raise e

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def agent_1_vision(self, base64_image):
        """Analyze image and generate detailed prompt."""
        system_prompt = """
You are Agent 1 of a Three-Agent Autonomous Prompt Engineering System.

Your Task:
Analyze this image with extreme visual precision.
Describe ONLY what is visually observable.
Generate a single ultra-detailed paragraph that includes:
- The subject type (generic, identity-neutral)
- Exact body position and orientation in space
- Limb placement and posture alignment
- Relative position within the frame (center, left, foreground, background)
- Body proportions (without biometric facial identity)
- Clothing type, structure, stitching, folds, tension points
- Fabric texture and material realism
- Surface reflections, roughness, shine level
- Micro-details like wrinkles, creases, fabric layering
- Background environment with full depth description
- Spatial layering (foreground, midground, background)
- Shape geometry of objects (curved, angular, sharp, soft edges)
- Object distances and perspective
- Lighting direction, intensity, softness, diffusion
- Shadow depth and falloff behavior
- Highlights and reflection points
- Atmospheric elements (dust, fog, particles, haze)
- Color tones and gradient transitions
- Camera angle and perspective type
- Framing composition and balance
- Depth of field and focus clarity
- Overall mood created by visual elements
- Art style: explicitly identify the medium (e.g., "photorealistic", "cartoon", "3D render", "oil painting")
- Art style: explicitly identify the medium (e.g., "photorealistic", "cartoon", "3D render", "oil painting")
- Demographic markers: apparent age, gender, and ethnic features (identity-neutral)

IMPORTANT:
- You MAY identify specific characters, brands, or famous settings IF it helps describe the visual accuracy (e.g., "Spider-Man suit texture", "Nike logo stitching").
- Do NOT be vague. If it looks like a specific IP, name it so the next agent knows exactly what textures to look for.

Write in natural, professional descriptive language.
Do not use bullet points.
Return one cohesive, generator-ready paragraph.
"""
        return self._safe_call(
            model=self.vision_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                }
            ],
            temperature=0.2
        )

    def agent_2_enhance_accuracy(self, prompt):
        """Enhance prompt with hyper-accurate minute details, handling collages and grids."""
        system_prompt = """
You are Agent 2: The Hyper-Fidelity Physics Engine & Grid Architect.

Your task:
Take the prompt from Agent 1 and perform a "Total Reconstruction" of the scene with 1000% more detail. 

SPECIAL INSTRUCTIONS FOR COLLAGES/GRIDS:
- If Agent 1 mentions a collage or multiple panels, you MUST maintain that structure. 
- Detail each segment of the grid with independent Microscopic Texture Mapping. 
- Ensure the relationship between panels is described (e.g., "The top-left panel's cool blue lighting contrasts with the bottom-right panel's warm amber glow").

MANDATORY EXECUTION PROTOCOL:
1. 100% KEYWORD ACCOUNTING: Every single style marker, age description, and placement detail from Agent 1 MUST be retained.
2. STYLISTIC PURITY: If Agent 1 says "cartoon", you must expand on the animation style (e.g., "thick cel-shaded outlines", "bright saturated primary colors characteristic of 90s animation").
3. DEMOGRAPHIC FIDELITY: Maintain and ground the apparent age and features described.
4. COMPOSITIONAL PRECISION: Detail the framing and suggested aspect ratio as core components of the output.
5. MICROSCOPIC TEXTURE MAPPING: Describe grain, weave, micro-scratches, moisture, and porosity.
6. RAY-TRACED LIGHTING: Detail how every light source interacts with the scene. Mention "global illumination", "bounce light", and "ambient occlusion".

Rule:
- BRUTAL DETAIL: Describe every button, every stitch, every shadow.
- NO HALLUCINATIONS: Stay grounded in the visual data, but "zoom in" on it for maximum accuracy.
- Output ONE single, massive, hyper-dense, cinematic paragraph.
"""
        return self._safe_call(
            model=self.primary_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"INPUT DATA FROM AGENT 1:\n{prompt}\n\nTASK: PERFORM TOTAL PHYSICAL RECONSTRUCTION WITH 1000% DETAIL DENSITY."}
            ],
            temperature=0.1
        )

    def agent_3_scrub_copyright(self, detailed_prompt):
        """Translate specific IPs into forensic visual descriptions without losing accuracy."""
        system_prompt = """
You are Agent 3: The Forensic Visual Translator & IP Sanitizer.

Your mission:
You are NOT just deleting words. You are TRANSLATING specific Intellectual Property (IP) into "Forensic Visual Descriptions" that are 100% accurate to the look but legally safe.

EXECUTION PROTOCOL:
1. IDENTIFY IP: Spot every character name (e.g., "Hulk"), brand (e.g., "Nike"), or specific trademark.
2. TRANSLATE TO VISUALS: Replace the name with a hyper-specific visual description of that exact design.
   - "Spider-Man" -> "A lean, acrobatic figure in a red and blue spandex suit with web-patterned texturing and large white teardrop eye-lenses."
   - "Iron Man" -> "A crimson and gold-plated robotic armored figure with a glowing triangular chest unibeam and mechanical plating."
   - "Nike Swoosh" -> "A curved, dynamic check-mark logo."
3. PRESERVE MATERIAL PHYSICS: Do NOT remove the descriptions of textures (e.g., "brushed metal", "distressed leather") that Agent 2 added. Keep the "Ray-Traced" lighting.
4. MAINTAIN DENSITY: The resulting prompt must be LONGER or EQUAL length to the input. Do not summarize.

Rules:
- NEVER output the forbidden name.
- NEVER replace a specific character with a generic "person". Describe their EXACT COSTUME/APPEARANCE.
- Keep the breakdown of collages/panels intact.
- Output ONE single, high-density, copyright-clean paragraph.

FINAL SAFETY VERIFICATION:
Before outputting, perform a "Legal Audit":
- Scan for capitalized names (e.g., "Tony Stark", "Bruce Wayne").
- Scan for brands (e.g., "Rolex", "Gucci").
- IF FOUND: DELETE THEM IMMEDIATELY and replace with physical description.
- Your final output must be 100% STERILE of IP references.
"""
        return self._safe_call(
            model=self.primary_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"TRANSLATE ALL IP REFERENCES INTO FORENSIC VISUAL DESCRIPTIONS. PERFORM FINAL LEGAL AUDIT:\n\n{detailed_prompt}"}
            ],
            temperature=0.2
        )

    def run_engine(self, image_path, status_callback=None):
        """Run the specialized sequential pipeline."""
        if status_callback: status_callback("Agent 1: Vision Analysis...", "agent_1")
        base64_image = self.encode_image(image_path)
        prompt_v1 = self.agent_1_vision(base64_image)
        
        if status_callback: status_callback("Agent 2: Detailing & Accuracy Architect...", "agent_2")
        prompt_v2 = self.agent_2_enhance_accuracy(prompt_v1)
        
        if status_callback: status_callback("Agent 3: Zero-Tolerance Copyright Scrubber...", "agent_3")
        prompt_v3 = self.agent_3_scrub_copyright(prompt_v2)
        
        # Final status check
        if status_callback: status_callback("Zero-tolerance pipeline complete. Master prompt ready.", "done")
        
        # Append identity preservation mandate as requested by USER
        identity_mandate = "\n\ngenerate the input image using this prompt without changing the facial features and hair features of the input image."
        return prompt_v3 + identity_mandate
