# Forge WebUI Flux & Realistic Photo Scripts

This project provides Python scripts to automate the setup and image generation process for the Forge WebUI using both a custom Flux model and the Realistic Stock Photo model.

## Features
- Loads model components from a user-specified directory (set via `.env` file) for Flux scripts
- Configures the Forge WebUI API to use the specified model and components
- Generates images from text prompts and saves them to disk
- Supports negative prompts (for SRealistic Photo scripts)
- Provides detailed code comments for clarity
- Allows parameterized image generation (prompt, seed, width, height, negative_prompt)

## Requirements
- Python 3.8+
- [Forge WebUI](https://github.com/lllyasviel/stable-diffusion-webui-forge) running locally (default: `http://127.0.0.1:7860`)
- Required model files (see below)
- `python-dotenv` package (for .env support, Flux scripts only)
- `requests` package

## Setup
1. **Clone or copy this repository.**
2. **Install dependencies:**
   ```sh
   pip install requests python-dotenv
   ```
3. **For Flux scripts:**
   - **Create a `.env` file** in the project directory with the following content:
     ```env
     MODELS_DIR=D:/Path/To/Your/Forge/models
     ```
     Replace the path with the location of your Forge WebUI `models` directory.
   - **Ensure the following files exist in your models directory:**
     - `Stable-diffusion/flux1-schnell-bnb-nf4.safetensors`
     - `VAE/ae.safetensors`
     - `text_encoder/clip_l.safetensors`
     - `text_encoder/t5xxl_fp16.safetensors`
4. **For Realistic Photo scripts:**
   - Ensure the model file `realisticStockPhoto_v20.safetensors` is available in your Forge WebUI models directory.
   - No `.env` file is required for these scripts.
5. **Start the Forge WebUI server.**
6. **Run the desired script:**
   ```sh
   python flux.py --prompt "your prompt" [--seed 123 --width 1024 --height 768 --steps 20 --output "output_dir"]
   python realistic_photo.py --prompt "your prompt" [--negative "blurry, low quality" --seed 42 --width 512 --height 512 --steps 20 --output "output_dir"]
   python jugger.py --prompt "your prompt" [--negative "blurry, low quality" --seed 42 --width 1024 --height 1024 --steps 20 --output "output_dir"]
   ```
7. **Batch/Automated Usage:**
   - Use `run_image_generation.py` to call the scripts with all parameters, including output directory, from the command line or a batch file:
     ```sh
     python run_image_generation.py flux --prompt "your prompt" --seed 123 --width 1024 --height 768 --output "output_dir"
     python run_image_generation.py realistic --prompt "your prompt" --negative "blurry, low quality" --seed 42 --width 512 --height 512 --output "output_dir"
     python run_image_generation.py jugger --prompt "your prompt" --negative "blurry, low quality" --seed 42 --width 1024 --height 1024 --output "output_dir"
     ```
   - See `run_image_example.bat` for usage examples.

## Network/Remote Usage
- To run scripts or batch files from another computer on your network:
  1. Start the Forge WebUI server with `--host 0.0.0.0` (e.g., `python launch.py --api --host 0.0.0.0`).
  2. Find your host computer's local IP address (e.g., `192.168.1.100`).
  3. In all scripts, change `url = "http://127.0.0.1:7860"` to `url = "http://192.168.1.100:7860"` (replace with your actual IP).
  4. Ensure your firewall allows connections to port 7860.
  5. Run the scripts or batch file from any computer on your network.

## Customization
- Edit the prompt, negative prompt, seed, width, height, and output directory in the scripts or via command line to generate different images.
- Adjust model paths or settings as needed.

## Output
- By default, images are saved to the current directory.
- You can specify a custom output directory in `flux_05.py`, `realistic_photo_03.py`, or via the `--output` argument in `run_image_generation.py` and the batch file.
- The output directory will be created if it does not exist.

## Troubleshooting
- If you see a `FileNotFoundError`, check that all required model files exist and the `MODELS_DIR` is set correctly in your `.env` file (Flux scripts).
- The scripts wait a few seconds after model setup to allow the model to load into memory.
- If you get a connection error, ensure the Forge WebUI server is running with the `--api` flag.

## License
This project is provided as-is for educational and research purposes.
