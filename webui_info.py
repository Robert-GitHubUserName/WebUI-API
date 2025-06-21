import requests
import json

# Configuration
url = "http://127.0.0.1:7860"

def get_samplers():
    """Get a list of all available samplers"""
    try:
        response = requests.get(f"{url}/sdapi/v1/samplers")
        response.raise_for_status()
        samplers = response.json()
        return samplers
    except Exception as e:
        print(f"Error getting samplers: {str(e)}")
        return []

def get_model_info():
    """Get information about the current model settings"""
    try:
        response = requests.get(f"{url}/sdapi/v1/options")
        response.raise_for_status()
        options = response.json()
        
        # Extract relevant information
        model_info = {
            "sd_model_checkpoint": options.get("sd_model_checkpoint", "unknown"),
            "sd_vae": options.get("sd_vae", "unknown"),
        }
        
        # Check if forge_additional_modules exists
        if "forge_additional_modules" in options:
            model_info["forge_additional_modules"] = options["forge_additional_modules"]
        
        return model_info
    except Exception as e:
        print(f"Error getting model info: {str(e)}")
        return {}
        
def get_forge_status():
    """Check if we're using Forge WebUI based on API endpoints"""
    try:
        # Try a Forge-specific endpoint
        response = requests.get(f"{url}/sdapi/v1/forge/version")
        if response.status_code == 200:
            version_info = response.json()
            return f"Forge WebUI detected: {version_info}"
        else:
            return "Not using Forge WebUI or endpoint not available"
    except Exception as e:
        return f"Couldn't determine Forge status: {str(e)}"

def list_available_models():
    """Get a list of all available models from the WebUI API."""
    try:
        response = requests.get(f"{url}/sdapi/v1/sd-models")
        response.raise_for_status()
        models = response.json()
        return models
    except Exception as e:
        print(f"Error getting models: {str(e)}")
        return []

if __name__ == "__main__":
    print("=== WebUI API Information Tool ===")
    
    # Check if server is running
    try:
        samplers = get_samplers()
        if samplers:
            print("\n=== Available Samplers ===")
            for s in samplers:
                print("-", s.get("name", "Unknown"))
        
        print("\n=== Available Models ===")
        models = list_available_models()
        for m in models:
            print(f"- {m.get('title', m.get('model_name', 'Unknown'))}")
        
        print("\n=== Current Model Information ===")
        model_info = get_model_info()
        for key, value in model_info.items():
            print(f"{key}: {value}")
        
        print("\n=== Forge Status ===")
        forge_status = get_forge_status()
        print(forge_status)
        
    except Exception as e:
        print(f"Error connecting to WebUI server: {str(e)}")
        print("Make sure the WebUI is running with the --api flag")
