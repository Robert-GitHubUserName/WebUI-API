# image_task_batch_runner.py
# Batch runner for image generation tasks from a queue file.
# Reads each line from the queue file, runs the image generation command,
# logs output, moves successful tasks to the done file, and leaves failed tasks in the queue.

import argparse
import subprocess
import os
import sys
from datetime import datetime

# Parse command-line arguments for queue and done files
parser = argparse.ArgumentParser(description="Batch runner for image generation tasks.")
parser.add_argument('--queue', required=True, help='Path to the queue file (tasks to run)')
parser.add_argument('--done', required=True, help='Path to the done file (completed tasks)')
args = parser.parse_args()

queue_file = args.queue
done_file = args.done

# Exit if the queue file does not exist
if not os.path.exists(queue_file):
    print(f"No queue file found: {queue_file}")
    sys.exit(0)

# Read all non-empty, non-comment lines from the queue file
with open(queue_file, 'r', encoding='utf-8') as f:
    tasks = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

if not tasks:
    print("No tasks to process.")
    sys.exit(0)

# Create a directory for per-task logs
log_dir = os.path.join(os.path.dirname(done_file), "task_logs")
os.makedirs(log_dir, exist_ok=True)

remaining_tasks = []  # Will hold any failed tasks to retry next run
for idx, task in enumerate(tasks, 1):
    print(f"\n[Task {idx}/{len(tasks)}] Running: {task}")
    # Log file for this task, timestamped for uniqueness
    log_file = os.path.join(log_dir, f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{idx}.log")
    try:
        # Run the image generation command as a subprocess
        # The task line should be the arguments for run_image_generation.py
        result = subprocess.run(f"python run_image_generation.py {task}", shell=True, capture_output=True, text=True, cwd=os.path.dirname(__file__))
        # Write stdout and stderr to the log file
        with open(log_file, 'w', encoding='utf-8') as lf:
            lf.write(f"COMMAND: python run_image_generation.py {task}\n\n")
            lf.write(f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}\n")
        if result.returncode == 0:
            print(f"Task succeeded. Log: {log_file}")
            # Append the successful task to the done file
            with open(done_file, 'a', encoding='utf-8') as df:
                df.write(task + '\n')
        else:
            print(f"Task failed (see log). Will keep in queue. Log: {log_file}")
            remaining_tasks.append(task)
    except Exception as e:
        print(f"Exception running task: {e}")
        remaining_tasks.append(task)

# Rewrite the queue file with any failed tasks for the next run
if remaining_tasks:
    with open(queue_file, 'w', encoding='utf-8') as f:
        for t in remaining_tasks:
            f.write(t + '\n')
    print(f"{len(remaining_tasks)} task(s) left in queue for next run.")
else:
    # If all tasks succeeded, remove the queue file
    os.remove(queue_file)
    print("All tasks completed and queue file removed.")
