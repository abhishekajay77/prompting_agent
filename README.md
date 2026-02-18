# AI Image Prompt Generator 🎨

An accurate, premium tool to transform any image into high-fidelity image generation prompts using Gemini 1.5 Flash.

## ✨ Features
- **Intelligent Reverse-Engineering**: Extracts subject, lighting, environment, and technical details from any image.
- **Multiple Prompt Formats**:
  - **Master Prompt**: Cinematic paragraph style for Midjourney/SDXL/Flux.
  - **Technical Breakdown**: Granular details for subjects, lighting, colors, and optics.
  - **Negative Prompt**: Commas-separated list of exclusions.
- **Modern Web Interface**: Clean, responsive Streamlit UI with image preview.
- **One-Click Copy**: Built-in copy-to-clipboard for all generated prompts.

## 🚀 Getting Started

### 1. Setup Environment
Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Create a `.env` file and add your Google Gemini API Key:
```env
GEMINI_API_KEY=AIzaSyCMQjsApvvUIQhqOOCDOGz1m3hKeAVk3f8
```
*Get your key at [Google AI Studio](https://aistudio.google.com/app/apikey)*

### 3. Run the Application
Start the Streamlit web app:
```bash
streamlit run app.py
```

## 🛠️ Tech Stack
- **AI Model**: Gemini 1.5 Flash
- **Backend/UI**: Streamlit
- **SDK**: Google Gen AI (v1.0+)
- **Imaging**: Pillow

## 📜 Usage
1. Upload your image (JPG, PNG, WEBP).
2. Click **🚀 Architect Prompts**.
3. Expand any section to view the prompt.
4. Click **Copy** and paste into your favorite image generator.
