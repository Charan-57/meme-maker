
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
import json
from datetime import datetime

# Title
st.title("🧠 Desi Meme Maker")
st.subheader("Caption memes in your own language and contribute to AI training!")

# Upload meme template
uploaded_image = st.file_uploader("📷 Upload a meme template", type=["jpg", "jpeg", "png"])

# Caption input
caption = st.text_input("✍️ Enter your caption in your local language")
language = st.selectbox("🌐 Choose your language", ["Telugu", "Hindi", "Tamil", "Kannada", "Malayalam", "Other"])

# Output directory for corpus
output_dir = "meme_corpus"
os.makedirs(output_dir, exist_ok=True)

# Font settings (adjust path for deployment if needed)
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DEFAULT_FONT = ImageFont.truetype(FONT_PATH, 32)

# Save and render meme
if uploaded_image and caption:
    image = Image.open(uploaded_image).convert("RGB")
    draw = ImageDraw.Draw(image)

    # Get image dimensions and wrap text
    width, height = image.size
    max_width = width - 40

    def wrap_text(text, font, max_width):
        words = text.split()
        lines, line = [], ""
        for word in words:
            if font.getlength(line + word + " ") <= max_width:
                line += word + " "
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)
        return "\n".join(lines)

    wrapped_caption = wrap_text(caption, DEFAULT_FONT, max_width)
    text_height = DEFAULT_FONT.getbbox(wrapped_caption)[3] * wrapped_caption.count("\n")
    text_y = height - text_height - 20
    draw.text((20, text_y), wrapped_caption, fill="white", font=DEFAULT_FONT, stroke_width=2, stroke_fill="black")

    st.image(image, caption="Generated Meme", use_column_width=True)

    # Save image
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    meme_filename = f"meme_{timestamp}.png"
    image.save(os.path.join(output_dir, meme_filename))

    # Save caption + metadata to JSON
    record = {
        "filename": meme_filename,
        "caption": caption,
        "language": language,
        "timestamp": timestamp
    }

    json_file = os.path.join(output_dir, "captions.json")
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(record)
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    st.success("✅ Meme saved and data recorded!")
else:
    st.info("Upload a meme template and add a caption to get started.")
