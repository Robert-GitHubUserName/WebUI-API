import requests
import json
import time
from datetime import datetime

# === CONFIG ===
url = "http://127.0.0.1:7860"

def get_current_options():
    """Get all current WebUI options"""
    try:
        response = requests.get(f"{url}/sdapi/v1/options")
        response.raise_for_status()
        options = response.json()
        return options
    except Exception as e:
        print(f"Error getting options: {str(e)}")
        return {}

def get_txt2img_default_params():
    """Get the default parameters for txt2img"""
    try:
        response = requests.get(f"{url}/sdapi/v1/txt2img")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error getting txt2img params: {str(e)}")
        return {}

def monitor_progress():
    """Monitor progress of current generation"""
    try:
        response = requests.get(f"{url}/sdapi/v1/progress")
        response.raise_for_status()
        progress = response.json()
        return progress
    except Exception as e:
        print(f"Error getting progress: {str(e)}")
        return {}

def save_config_to_file(config, filename):
    """Save configuration to a JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ Saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving to file: {str(e)}")

if __name__ == "__main__":
    print("=== WebUI Configuration Capture Tool ===")
    print("This tool captures the current WebUI configuration and default parameters.")
    print("Use this after successfully generating an image with Flux in the WebUI.")
    
    # Get timestamp for filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Get and save current options
    print("\nFetching current WebUI options...")
    options = get_current_options()
    if options:
        # Extract important model info
        model_info = {
            "current_model": options.get("sd_model_checkpoint", "unknown"),
            "current_vae": options.get("sd_vae", "unknown"),
        }
        
        # Check for Forge modules
        if "forge_additional_modules" in options:
            model_info["additional_modules"] = options["forge_additional_modules"]
            
        print("\n=== Current Model Configuration ===")
        print(json.dumps(model_info, indent=2))
        
        # Save all options to file
        options_file = f"webui_options_{timestamp}.json"
        save_config_to_file(options, options_file)
    
    # Get and save txt2img default parameters
    print("\nFetching txt2img default parameters...")
    txt2img_params = get_txt2img_default_params()
    if txt2img_params:
        # Save to file
        params_file = f"txt2img_params_{timestamp}.json"
        save_config_to_file(txt2img_params, params_file)
        
        # Display key parameters
        key_params = {k: txt2img_params.get(k) for k in [
            "prompt", "negative_prompt", "steps", "sampler_name", 
            "sampler_index", "cfg_scale", "denoising_strength"
        ] if k in txt2img_params}
        
        print("\n=== Current txt2img Parameters ===")
        print(json.dumps(key_params, indent=2))
    
    print("\n=== INSTRUCTIONS ===")
    print("1. Generate a successful image with Flux in the WebUI interface")
    print("2. Run this script immediately after to capture the working configuration")
    print("3. Use the captured configuration in your API scripts")
    print("4. Look for differences between your API payload and the WebUI defaults")
    
    # Check if generation is in progress
    print("\nChecking if generation is in progress...")
    progress = monitor_progress()
    if progress and progress.get("progress", 0) > 0:
        print("Generation in progress. Progress info:")
        print(json.dumps(progress, indent=2))
    else:
        print("No generation currently in progress")
