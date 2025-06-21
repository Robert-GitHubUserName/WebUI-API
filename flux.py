# Flux Model Generation Script (flux_05.py)
#
# This script generates a single image using the Forge WebUI API and the Flux model.
# It allows passing prompt, seed, width, height, and output directory as parameters to the generate_image function.
#
# Usage:
#   python flux_05.py "prompt here" -1 1024 768 "output_dir"
#   (output_dir is optional; defaults to current directory)

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
    "model_filename": "flux1-schnell-bnb-nf4.safetensors",  # Main model file
    "model_hash": "7d3d1873",                              # Model hash for identification
    "vae": os.path.join(models_dir, "VAE", "ae.safetensors"),
    "clip": os.path.join(models_dir, "text_encoder", "clip_l.safetensors"),
    "t5": os.path.join(models_dir, "text_encoder", "t5xxl_fp16.safetensors"),
}

# List of required files for the model to function
required_files = [
    os.path.join(models_dir, "Stable-diffusion", paths["model_filename"]),
    paths["vae"],
    paths["clip"],
    paths["t5"]
]

# Check that all required files exist before proceeding
for path in required_files:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"❌ Missing required file: {path}")

def setup_flux_model():
    """
    Configure the Forge WebUI to use the specified Flux model and components.
    Sends a POST request to the /sdapi/v1/options endpoint.
    """
    checkpoint_name = f"{paths['model_filename']} [{paths['model_hash']}]"
    print("\n🔄 Setting up the Flux model via API...")
    payload = {
        "sd_model_checkpoint": checkpoint_name,
        "sd_vae": paths["vae"],
        "forge_additional_modules": [
            paths["clip"],
            paths["t5"]
        ]
    }
    response = requests.post(f"{url}/sdapi/v1/options", json=payload)
    response.raise_for_status()
    print(f"✅ Flux model set to: {checkpoint_name}")
    print("⏳ Waiting for model to load into memory (20 seconds)...")
    time.sleep(20)  # Wait for the model to load

def generate_image(prompt, seed=-1, width=896, height=1152, output_dir=".", steps=20):
    """
    Generate an image using the configured Flux model.
    Args:
        prompt (str): The text prompt for image generation.
        seed (int): Random seed for reproducibility (-1 for random).
        width (int): Image width.
        height (int): Image height.
        output_dir (str): Directory to save the output image.
        steps (int): Number of inference steps.
    """
    print("\n🖼️ Generating image...")
    scheduler_type = "Simple"  # Scheduler name is case-sensitive
    print(f"⚙️ Using Scheduler: {scheduler_type} (casing matters!)")
    payload = {
        "prompt": prompt,
        "negative_prompt": "blurry, dark, low quality",
        "steps": steps,
        "sampler_name": "Euler",
        "cfg_scale": 1.0,
        "width": width,
        "height": height,
        "scheduler": scheduler_type,
        "override_settings": {
            "CLIP_stop_at_last_layers": 1,
            "sd_vae_overrides": paths["vae"],
            "unet_substitute": "default"
        },
        "override_settings_restore_afterwards": False,
        "seed": seed
    }
    print(f"⚙️ Payload: {json.dumps(payload, indent=2)}")
    response = requests.post(f"{url}/sdapi/v1/txt2img", json=payload)
    response.raise_for_status()
    result = response.json()
    # Decode the base64 image data and save to disk
    img_data = base64.b64decode(result["images"][0])
    filename = datetime.now().strftime("flux_image_%Y%m%d_%H%M%S.png")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "wb") as f:
        f.write(img_data)
    print(f"✅ Image saved to disk: {filepath}")
    # Save prompt and metadata to a text file alongside the image
    meta_filename = os.path.splitext(filename)[0] + "_meta.txt"
    meta_filepath = os.path.join(output_dir, meta_filename)
    with open(meta_filepath, "w", encoding="utf-8") as meta_file:
        meta_file.write(f"Prompt: {prompt}\n")
        meta_file.write(f"Negative Prompt: blurry, dark, low quality\n")
        meta_file.write(f"Seed: {seed}\n")
        meta_file.write(f"Width: {width}\n")
        meta_file.write(f"Height: {height}\n")
        meta_file.write(f"Steps: {steps}\n")
        meta_file.write(f"Scheduler: {scheduler_type}\n")
        meta_file.write(f"Sampler: Euler\n")
        meta_file.write(f"VAE: {paths['vae']}\n")
        meta_file.write(f"Model: {paths['model_filename']} [{paths['model_hash']}]\n")
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
    print(f"📝 Metadata saved to: {meta_filepath}")
    # Display infotext metadata returned from the API
    if "info" in result:
        try:
            info = result["info"]
            print("\n📋 Generation Info (raw):")
            print(info)
            if isinstance(info, str):
                metadata = json.loads(info)
                print("\n📊 Parsed Metadata:")
                for key, value in metadata.items():
                    print(f"- {key}: {value}")
            else:
                print("ℹ️ Info object was not a string.")
        except Exception as e:
            print(f"⚠️ Failed to parse infotext: {str(e)}")

if __name__ == "__main__":
    print("🚀 Flux Generation Script Started")
    import argparse
    parser = argparse.ArgumentParser(description="Generate an image with the Flux model and optional output directory.")
    parser.add_argument('--prompt', required=True, help="Prompt for image generation (named argument)")
    parser.add_argument('--seed', type=int, default=-1, help="Seed value (default: -1)")
    parser.add_argument('--width', type=int, default=1024, help="Image width (default: 1024)")
    parser.add_argument('--height', type=int, default=768, help="Image height (default: 768)")
    parser.add_argument('--steps', type=int, default=20, help="Number of inference steps (default: 20)")
    parser.add_argument('--output', default=".", help="Output directory (default: current directory)")
    args = parser.parse_args()
    prompt = args.prompt
    setup_flux_model()
    generate_image(prompt, args.seed, args.width, args.height, args.output, args.steps)
