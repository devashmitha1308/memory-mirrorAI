<#
.SYNOPSIS
    Automated GitHub Push & Collaborator Setup Helper for MemoryMirror AI
    SparkX 3.0 | Gauri Dwivedi & Nuka Devashmitha Reddy
#>

param(
    [string]$RepoUrl = "",
    [string]$CollaboratorUsername = ""
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   MemoryMirror AI - GitHub Push & Collaborator Setup    " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Prompt for Repository URL if not provided
if (-not $RepoUrl) {
    Write-Host "Please create a new repository on your GitHub account (e.g., named 'memory-mirror-ai')." -ForegroundColor Yellow
    Write-Host "Then copy the repository URL (HTTPS or SSH)."
    $RepoUrl = Read-Host "Enter your GitHub Repository URL"
}

if (-not $RepoUrl) {
    Write-Host "[!] Repository URL cannot be empty. Aborting." -ForegroundColor Red
    exit 1
}

# 2. Configure Git Remote
Write-Host ""
Write-Host "[*] Configuring Git remote 'origin'..." -ForegroundColor Cyan
$existingRemote = git remote get-url origin 2>$null
if ($LASTEXITCODE -eq 0) {
    git remote set-url origin $RepoUrl
    Write-Host "[+] Updated existing remote 'origin' to: $RepoUrl" -ForegroundColor Green
} else {
    git remote add origin $RepoUrl
    Write-Host "[+] Added remote 'origin': $RepoUrl" -ForegroundColor Green
}

# 3. Ensure branch is main
git branch -M main

# 4. Push to GitHub
Write-Host ""
Write-Host "[*] Pushing 'main' branch to GitHub..." -ForegroundColor Cyan
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "==========================================================" -ForegroundColor Green
    Write-Host " [SUCCESS] MemoryMirror AI successfully pushed to GitHub! " -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Green
    Write-Host ""
    
    # 5. Instructions / Steps to Add Friend as Collaborator
    if (-not $CollaboratorUsername) {
        $CollaboratorUsername = Read-Host "Enter your friend's GitHub username to add as collaborator (press Enter to skip)"
    }
    
    Write-Host ""
    Write-Host "--- ADDING YOUR FRIEND AS COLLABORATOR ---" -ForegroundColor Yellow
    Write-Host "To invite your friend (e.g. Gauri Dwivedi) to collaborate on your repository:"
    Write-Host "1. Open your repository on GitHub in your browser:"
    Write-Host "   $RepoUrl" -ForegroundColor Cyan
    Write-Host "2. Click on 'Settings' (top navigation tab of your repository)."
    Write-Host "3. In the left sidebar, click 'Collaborators' (under Access)."
    Write-Host "4. Click the green 'Add people' button."
    if ($CollaboratorUsername) {
        Write-Host "5. Type '$CollaboratorUsername' and select their profile, then click 'Add to this repository'." -ForegroundColor Green
    } else {
        Write-Host "5. Type your friend's GitHub username or email and click 'Add to this repository'."
    }
    Write-Host "6. GitHub will send an invitation email / notification to your friend to join!"
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "[!] Push encountered an issue. Ensure your repository exists and you have write permissions." -ForegroundColor Red
}
