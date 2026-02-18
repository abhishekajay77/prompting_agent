import os
import sys
import base64
from groq import Groq
from dotenv import load_dotenv
import PIL.Image

# Load environment variables
load_dotenv()

# STRICT COPYRIGHT SAFETY RULES (USER MANDATE)
COPYRIGHT_SAFETY_RULES = """
CRITICAL LEGAL REQUIREMENT:
1. **NO IP PREDICATION**: If the image contains a known character (e.g., Marvel, DC, Disney, Anime), you MUST acknowledge it internally but **NEVER** name it in the output.
2. **VISUAL MUTATION (MANDATORY)**:
   - **SYMBOLS**: Remove ALL logos, emblems, and chest symbols. Replace with generic tactical detailing or smooth textures.
   - **COLORS**: You MUST shift iconic color palettes. (e.g., If the source is Red/Gold [Iron Man], describe it as "Gunmetal Grey and Neon Blue" or "Matte Black and Bronze"). Do NOT output the exact IP colors.
   - **PATTERNS**: Remove specific web patterns, bat symbols, or "S" shields. Replace with "hexagonal nano-weave" or "industrial plating".
3. **GENERIC NOMENCLATURE**:
   - NEVER use terms like "Iron Man suit", "Jedi Robe", "Spider-Suit".
   - USE: "Heavy exo-skeletal armor", "Flowing monk garments", "Tight tactical stealth suit".
4. **PRESERVE ONLY**: Pose, Lighting, Composition, and Gender/Body Type.
5. **DESTROY**: Identity, Specific Costume Details, and Proper Names.
"""

# PROMPT MODES DICTIONARY
PROMPT_MODES = {
    "Human-Aesthetic Narrative": f"""
SYSTEM ROLE:
You are a Concept Description Algorithm designed to generate 100% Copyright-Free assets with EXTREME focus on clothing and environment.

{COPYRIGHT_SAFETY_RULES}

**CRITICAL INSTRUCTION: IGNORE FACE & HAIR**
- Do NOT describe the facial features, eye color, or hairstyle in detail.
- Focus 100% of your processing power on the **COSTUME TEXTURE**, **ACCESSORIES**, **LIGHTING**, and **POSE**.

**EXECUTION STEPS**:
1. **SCAN**: Identify the subject's pose and clothing.
2. **MUTATE**: Mentally strip away IP properties (Logos, Names).
3. **ZOOM IN**: Describe the material weave, scratches on armor, dust particles, and light reflections.

**OUTPUT FORMAT**:
A series of 3-4 clean paragraphs.
- **Para 1 (Subject)**: Generic pose and physical presence (NO Face/Hair details).
- **Para 2 (Costume Micro-Detail)**: Extreme focus on fabric, metal, leather, and weathering.
- **Para 3 (Environment)**: Lighting, atmosphere, and background elements.
- **Para 4 (Prompt)**: The final safe generation string.
""",

    "Forensic (Extreme Detail)": f"""
SYSTEM ROLE:
You are an Elite Forensic Imaging Scientist. Analyze the image with microscopic precision, IGNORING the face and hair.

{COPYRIGHT_SAFETY_RULES}

**CONTENT REQUIREMENTS**:
1. **BODY MECHANICS**: Exact joint angles and skeletal distribution.
2. **MATERIAL FORENSICS**: Analyze the weave, stitching, and material physics (e.g., "matte carbon fiber", "distressed denim").
3. **NO BIOMETRICS**: Do NOT analyze facial features or hair.

**OUTPUT FORMAT**:
A single, high-density block of technical visual data focusing on materials and physics.
""",

    "Artistic (Creative Style)": """
SYSTEM ROLE:
You are a Cinematic Visionary. Translate the image into a high-aesthetic masterpiece.

**CONTENT REQUIREMENTS**:
1. **AURA**: Mood and cinematic resonance.
2. **COSTUME STYLE**: Name the dress style and its movement.
3. **OPTICS**: Lens flare, bokeh, and color grading.

**OUTPUT FORMAT**:
A seamless artistic description followed by the generation prompt. No technical tags.
"""
}

def copyright_guardian(text):
    """
    Uses Llama 3 70B to audit the prompt for copyright infringement and
    ensure facial/hair details are minimized in favor of costume/environmental micro-details.
    """
    api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=api_key)
    
    guardian_system = """
    You are a STRICT Copyright Compliance Officer and Detail Architect.
    
    **YOUR MANDATE**:
    1. **IP ANNIHILATION**: You must scrub ANY potential copyright infringement. 
       - If the text mentions "Iron Man", change it to "High-tech heavy armor". 
       - If it mentions "Jedi", change it to "Mystic Sci-Fi Monk".
       - If it describes a specific logo (e.g., "Bat symbol"), change it to "generic tactical geometric plate".
    2. **DETAIL PRESERVATION**: You MUST preserve every single ounce of descriptive detail about the *Background*, *Pose*, and *Costume Texture*. 
    3. **FACE/HAIR REDACTION**: The user explicitly wants "minute details EXCLUDING facial/hair". Redact any mention of "blue eyes", "scar on cheek", "messy bun". Keep it generic: "face obscured by helmet/shadow" or "neutral expression".
    4. **OUTPUT**: Return the rewritten, safe, high-detail prompt. Do not output anything else.
    """
    
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": guardian_system},
                {"role": "user", "content": f"SANITIZE AND ENHANCE this prompt:\n\n{text}"}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"GUARDIAN ERROR: {e}") # Log error for debugging
        return text # Fallback to original if Guardian fails

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_prompt(image_path, mode="Human-Aesthetic Narrative"):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    client = Groq(api_key=api_key)
    base64_image = encode_image(image_path)
    
    # Use Human-Aesthetic Narrative as the primary fallback to avoid KeyErrors
    system_instruction = PROMPT_MODES.get(mode, PROMPT_MODES["Human-Aesthetic Narrative"])

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_instruction
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model="meta-llama/llama-4-scout-17b-16e-instruct", # Optimized Llama 4 Vision model for forensic accuracy
        temperature=0.05, # Near-zero temperature for absolute objective precision
    )
    
    raw_content = chat_completion.choices[0].message.content.strip()
    
    # RUN COPYRIGHT GUARDIAN
    sanitized_content = copyright_guardian(raw_content)
    
    # Fidelity Lock Header (Modified for Body/Costume priority)
    fidelity_lock = "**COPYRIGHT NEUTRALIZED & DETAILED**\n*Face/Hair redacted | Background & Pose prioritized*\n\n"
    
    return fidelity_lock + sanitized_content

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prompt_gen.py <path_to_image>")
        sys.exit(1)
        
    image_input = sys.argv[1]
    
    try:
        result = generate_prompt(image_input)
        print("\n" + "="*50)
        print("GENERATED PROMPTS (Groq)")
        print("="*50 + "\n")
        print(result)
    except Exception as e:
        print(f"Error: {e}")
