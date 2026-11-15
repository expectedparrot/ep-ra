# Slide Template Schema

Full schema for `<study_root>/refs/slide_template/template.json`.
Each property group has a `verified` boolean — set `false` when inferred
from examples, `true` once the user has confirmed it.

```json
{
  "name": "Acme Corp",
  "last_updated": "2026-04-04",
  "verified": false,

  "colors": {
    "verified": false,
    "primary": "#1a3c6e",
    "secondary": "#f5a623",
    "background_content": "#ffffff",
    "background_title": "#1a3c6e",
    "background_section": "#1a3c6e",
    "text_dark": "#1a1a1a",
    "text_light": "#ffffff",
    "accent": "#e8f0fe",
    "chart_palette": ["#1a3c6e", "#f5a623", "#4caf50", "#e53935", "#9c27b0"]
  },

  "fonts": {
    "verified": false,
    "title_face": "Calibri",
    "title_size_pt": 36,
    "subtitle_face": "Calibri",
    "subtitle_size_pt": 24,
    "body_face": "Calibri",
    "body_size_pt": 18,
    "caption_face": "Calibri",
    "caption_size_pt": 12
  },

  "layouts": {
    "verified": false,
    "title_slide": "centered title and subtitle on primary-color background",
    "section_divider": "left-aligned section title, white text on primary background",
    "content": "top-aligned title, left-aligned body text, white background",
    "two_column": "title at top, two equal columns below",
    "chart": "title at top, full-width chart below, caption at bottom",
    "table": "title at top, table fills content area"
  },

  "logo": {
    "verified": false,
    "path": "refs/slide_template/logo.png",
    "position": "top_right",
    "applies_to": "all",
    "width_pct": 0.12
  },

  "footer": {
    "verified": false,
    "show_slide_number": true,
    "show_date": true,
    "show_company_name": false,
    "custom_text": "",
    "position": "bottom_right"
  },

  "notes": "Section slides use white text on primary blue. Content slides use dark text on white. Charts always include a one-line takeaway caption below the image. Confidentiality notice in footer on all slides."
}
```

## Extracting colors from a PPTX

```python
from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor

prs = Presentation("example.pptx")

for slide in prs.slides:
    # Background fill
    bg = slide.background.fill
    if bg.type is not None:
        print("Background:", bg.fore_color.rgb if hasattr(bg, 'fore_color') else bg.type)

    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    if run.font.color and run.font.color.type:
                        print("Text color:", run.font.color.rgb)
                    if run.font.name:
                        print("Font:", run.font.name, run.font.size)
        if shape.fill.type is not None:
            try:
                print("Shape fill:", shape.fill.fore_color.rgb)
            except Exception:
                pass
```

## What to do when extracting from images only

Font names cannot be reliably identified from images. Record:
- `"verified": false` on the fonts block
- `"notes"`: "Font names inferred visually — confirm with user"
- Use a safe fallback (Calibri or Arial) until confirmed

Colors can be sampled from images using PIL:

```python
from PIL import Image
import numpy as np

img = Image.open("slide_01.png")
arr = np.array(img)
# Sample the header bar region (top 15% of slide)
header = arr[:int(arr.shape[0] * 0.15), :, :3]
# Most common color in header
colors, counts = np.unique(
    header.reshape(-1, 3), axis=0, return_counts=True
)
top_color = colors[counts.argmax()]
print(f"#{top_color[0]:02x}{top_color[1]:02x}{top_color[2]:02x}")
```
