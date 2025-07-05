# JuggernautXL Model Generation Script (jugger.py)
#
# This script generates a single image using the Forge WebUI API and the JuggernautXL v8 Rundiffusion model.
# Usage:
#   python jugger.py --prompt "your prompt" [--negative "bad, blurry" --seed 123 --width 1024 --height 1024 --steps 20 --output "output_dir"]

import requests, base64, time, os, json, sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base URL for the Forge WebUI API
url = "http://127.0.0.1:7860"

# Get the models directory from the environment variable
models_dir = os.getenv("MODELS_DIR")
if not models_dir:
    raise EnvironmentError("MODELS_DIR not set in .env file.")

# Define paths for model components
paths = {
    "model_filename": "juggernautXL_v8Rundiffusion.safetensors",  # Main model file
    "model_hash": "",  # Fill in the model hash if known
    "vae": os.path.join(models_dir, "VAE", "ae.safetensors"),
}

# List of required files for the model to function
required_files = [
    os.path.join(models_dir, "Stable-diffusion", paths["model_filename"]),
    paths["vae"]
]

# Check that all required files exist before proceeding
for path in required_files:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"❌ Missing required file: {path}")

def setup_jugger_model():
    """
    Configure the Forge WebUI to use the specified JuggernautXL model and components.
    Sends a POST request to the /sdapi/v1/options endpoint.
    """
    checkpoint_name = paths['model_filename'] if not paths['model_hash'] else f"{paths['model_filename']} [{paths['model_hash']}]"
    print("\nSetting up the JuggernautXL model via API...")
    payload = {
        "sd_model_checkpoint": checkpoint_name,
        "sd_vae": paths["vae"]
    }
    response = requests.post(f"{url}/sdapi/v1/options", json=payload)
    response.raise_for_status()
    print(f"JuggernautXL model set to: {checkpoint_name}")
    print("Waiting for model to load into memory (10 seconds)...")
    time.sleep(10)  # Wait for the model to load

def generate_image(prompt, negative_prompt=None, seed=-1, width=1024, height=1024, output_dir=".", steps=20):
    """
    Generate an image using the configured JuggernautXL model.
    Args:
        prompt (str): The text prompt for image generation.
        negative_prompt (str or None): Negative prompt to avoid certain features.
        seed (int): Random seed for reproducibility.
        width (int): Image width.
        height (int): Image height.
        output_dir (str): Directory to save the output image.
        steps (int): Number of inference steps.
    """
    print("\nGenerating image...")
    payload = {
        "prompt": prompt,
        "steps": steps,
        "sampler_name": "Euler",
        "cfg_scale": 7,
        "seed": seed,
        "width": width,
        "height": height
    }
    if negative_prompt:
        payload["negative_prompt"] = negative_prompt
    print(f"Payload: {json.dumps(payload, indent=2)}")
    response = requests.post(f"{url}/sdapi/v1/txt2img", json=payload)
    response.raise_for_status()
    result = response.json()
    # Decode the base64 image data and save to disk
    img_data = base64.b64decode(result["images"][0])
    filename = datetime.now().strftime("jugger_image_%Y%m%d_%H%M%S.png")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "wb") as f:
        f.write(img_data)
    print(f"Image saved to disk: {filepath}")
    # Save prompt and metadata to a text file alongside the image
    meta_filename = os.path.splitext(filename)[0] + "_meta.txt"
    meta_filepath = os.path.join(output_dir, meta_filename)
    with open(meta_filepath, "w", encoding="utf-8") as meta_file:
        meta_file.write(f"Prompt: {prompt}\n")
        meta_file.write(f"Negative Prompt: {negative_prompt if negative_prompt else ''}\n")
        meta_file.write(f"Seed: {seed}\n")
        meta_file.write(f"Width: {width}\n")
        meta_file.write(f"Height: {height}\n")
        meta_file.write(f"Steps: {steps}\n")
        meta_file.write(f"Sampler: Euler\n")
        meta_file.write(f"Model: {paths['model_filename']}\n")
        meta_file.write(f"Date: {datetime.now().isoformat()}\n")
        if "info" in result:
            meta_file.write("\n[API Info/Metadata]\n")
            try:
                info = result["info"]
                if isinstance(info, str):
                    meta_file.write(info + "\n")
                else:
                    meta_file.write(str(info) + "\n")
            except Exception as e:
                meta_file.write(f"Failed to parse infotext: {str(e)}\n")
    print(f"Metadata saved to: {meta_filepath}")
    # Display infotext metadata returned from the API
    if "info" in result:
        try:
            info = result["info"]
            print("\nGeneration Info (raw):")
            print(info)
            if isinstance(info, str):
                metadata = json.loads(info)
                print("\nParsed Metadata:")
                for key, value in metadata.items():
                    print(f"- {key}: {value}")
            else:
                print("Info object was not a string.")
        except Exception as e:
            print(f"Failed to parse infotext: {str(e)}")

if __name__ == "__main__":
    print("JuggernautXL Generation Script Started")
    import argparse
    parser = argparse.ArgumentParser(description="Generate an image with the JuggernautXL model and optional output directory.")
    parser.add_argument('--prompt', required=True, help="Prompt for image generation (named argument)")
    parser.add_argument('--negative', help="Negative prompt (named argument, optional)")
    parser.add_argument('--seed', type=int, default=-1, help="Seed value (default: -1)")
    parser.add_argument('--width', type=int, default=1024, help="Image width (default: 1024)")
    parser.add_argument('--height', type=int, default=1024, help="Image height (default: 1024)")
    parser.add_argument('--steps', type=int, default=20, help="Number of inference steps (default: 20)")
    parser.add_argument('--output', default=".", help="Output directory (default: current directory)")
    args = parser.parse_args()
    prompt = args.prompt
    negative_prompt = args.negative
    if not prompt:
        parser.error("A prompt must be provided via --prompt.")
    setup_jugger_model()
    generate_image(prompt, negative_prompt, args.seed, args.width, args.height, args.output, args.steps)
