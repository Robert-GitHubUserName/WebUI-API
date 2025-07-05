# Flux Prompting Guidelines (AI Summary)

- **Be specific:** Clearly describe the main subject, scene, and key visual details.

- **Use natural language:** Write prompts as coherent sentences, not keyword lists.

- **Set the style and mood:** State desired style (photorealistic, painting, etc.), lighting, and atmosphere.

- **Structure visually:** Organize from foreground to background; clarify spatial relationships.

- **Emphasize focus:** Highlight the main subject and any actions or emotions.

- **Describe narrative and context:** Include emotional cues or interactions for storytelling.

- **Iterate and refine:** Adjust prompts based on output for better results.

---

## Windows Task Scheduler (PowerShell Example)

```
$Action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument '/c "D:\Files\Code\Python\WebUI-API\image_task_scheduler.bat"'
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).Date -RepetitionInterval (New-TimeSpan -Minutes 15) -RepetitionDuration (New-TimeSpan -Days 1)
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName "ImageGenerationBatch" -Action $Action -Trigger $Trigger -Settings $Settings -Description "Runs image_task_scheduler.bat every 15 minutes" -User "$env:USERNAME" -RunLevel Highest
```
