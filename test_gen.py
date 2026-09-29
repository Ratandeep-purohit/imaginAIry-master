import sys
import logging
logging.basicConfig(level=logging.DEBUG)

from imaginairy.schema import ImaginePrompt
from imaginairy.http_app.utils import generate_image

try:
    print("Creating prompt...")
    prompt = ImaginePrompt(
        prompt="a scenic landscape", 
        steps=5,
        size=(256, 256),
        model_weights="sd15"
    )
    print("Prompt created:", prompt)
    
    print("Generating image...")
    img_io = generate_image(prompt)
    print("Generated! Size of IO:", len(img_io.getvalue()))
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()
