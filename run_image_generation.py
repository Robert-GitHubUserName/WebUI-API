# run_image_generation.py
#
# This script allows you to call any of the image generation scripts (Flux or Realistic Photo)
# from the command line or a batch file, passing the prompt and other parameters as arguments.
#
# Usage example (PowerShell or CMD):
#   python run_image_generation.py flux "a beautiful landscape" --seed 123 --width 1024 --height 768
#   python run_image_generation.py realistic "a cat on a windowsill" --negative "blurry, low quality" --seed 42

import sys
import subprocess
import argparse

# Map script types to their corresponding Python files
SCRIPT_MAP = {
    'flux': 'flux.py',
    'realistic': 'realistic_photo.py',
    'jugger': 'jugger.py',
}

def main():
    parser = argparse.ArgumentParser(description="Run image generation scripts with custom prompts and parameters.")
    parser.add_argument('script', choices=SCRIPT_MAP.keys(), help="Which script to run: 'flux' or 'realistic'")
    parser.add_argument('--prompt', required=True, help="Prompt for image generation (named argument)")
    parser.add_argument('--negative', help="Negative prompt (named argument, only for realistic)")
    parser.add_argument('--seed', type=int, default=-1, help="Seed value (default: -1 for random)")
    parser.add_argument('--width', type=int, default=896, help="Image width (default: 896)")
    parser.add_argument('--height', type=int, default=1152, help="Image height (default: 1152)")
    parser.add_argument('--steps', type=int, default=20, help="Number of inference steps (default: 20)")
    parser.add_argument('--output', default=".", help="Output directory (default: current directory)")
    args = parser.parse_args()

    script_file = SCRIPT_MAP[args.script]

    prompt = args.prompt
    negative = args.negative

    # Build the command to call the target script with the right parameters
    if args.script == 'flux':
        cmd = [sys.executable, script_file, '--prompt', prompt, '--seed', str(args.seed), '--width', str(args.width), '--height', str(args.height), '--steps', str(args.steps), '--output', args.output]
    elif args.script == 'jugger':
        cmd = [sys.executable, script_file, '--prompt', prompt]
        if negative:
            cmd += ['--negative', negative]
        cmd += ['--seed', str(args.seed), '--width', str(args.width), '--height', str(args.height), '--steps', str(args.steps), '--output', args.output]
    else:
        cmd = [sys.executable, script_file, '--prompt', prompt]
        if negative:
            cmd += ['--negative', negative]
        cmd += ['--seed', str(args.seed), '--width', str(args.width), '--height', str(args.height), '--steps', str(args.steps), '--output', args.output]

    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd)

if __name__ == "__main__":
    main()
