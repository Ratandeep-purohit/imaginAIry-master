from imaginairy.api import imagine_image_files
from imaginairy.schema import ImaginePrompt

def generate_sun_image():
    # Prompt for the image you want to generate
    prompt_text = "A beautiful natural sun in the sky, realistic, highly detailed, nature photography"
    
    print(f"Generating image for: {prompt_text}")
    print("Please note: Since you don't have a CUDA GPU, this might take some time on the CPU.")
    
    # Create the prompt. We use size=512 for a standard image size.
    prompt = ImaginePrompt(prompt_text, size=512, seed=42)
    
    # Generate and save to the 'outputs' folder
    imagine_image_files([prompt], outdir="outputs")
    print("Image generation complete! Check the 'outputs' folder.")

if __name__ == "__main__":
    generate_sun_image()
