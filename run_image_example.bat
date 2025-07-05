@echo on
REM Example batch file to call run_image_generation.py with different parameters and a single virtual environment

echo ==== [START] Batch execution at %DATE% %TIME% ====

REM Set virtual environment name
set VENV=venv_main

echo Checking for venv: %VENV%
if not exist %VENV% ( 
    echo Creating venv...
    python -m venv %VENV% 
    call %VENV%\Scripts\python.exe -m pip install -r requirements.txt
) else (
    echo venv already exists.
)

echo Running Flux image generation...
call %VENV%\Scripts\python.exe run_image_generation.py flux --prompt "a surreal city floating above a luminous ocean, giant clock towers, bioluminescent plants, and dreamlike clouds, ultra detailed, cinematic lighting" --seed -1 --width 1024 --height 768 --steps 25 --output "output_images"

echo Running Realistic Photo image generation...
call %VENV%\Scripts\python.exe run_image_generation.py realistic --prompt "a surreal city floating above a luminous ocean, giant clock towers, bioluminescent plants, and dreamlike clouds, ultra detailed, cinematic lighting" --negative "blurry, low quality" --seed -1 --width 512 --height 512 --steps 30 --output "output_images"

echo Running JuggernautXL image generation...
call %VENV%\Scripts\python.exe run_image_generation.py jugger --prompt "a surreal city floating above a luminous ocean, giant clock towers, bioluminescent plants, and dreamlike clouds, ultra detailed, cinematic lighting" --negative "blurry, low quality" --seed -1 --width 1024 --height 1024 --steps 30 --output "output_images"

echo ==== [END] Batch execution at %DATE% %TIME% ====

REM Optionally remove virtual environment
set /p REMOVE_VENV="Do you want to delete the virtual environment? (y/n): "
if /I "%REMOVE_VENV%"=="y" (
    echo Deleting %VENV% ...
    rmdir /s /q %VENV%
    echo Virtual environment deleted.
) else (
    echo Virtual environment was not deleted.
)

REM Keep the window open so you can see the logs
cmd /k
