# YT2Drive - YouTube to Google Drive Automation

Python automation script that downloads YouTube videos and uploads them to Google Drive with public sharing links.

## Features

- YouTube video downloading
- Automatic Google Drive upload  
- Public link generation
- Error handling and recovery
- Automatic cleanup of temporary files

## Prerequisites

- Python 3.9 or higher
- pip package manager
- Google Cloud Console account
- Google Drive API enabled

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/andrxmedy/yt2drive.git
cd yt2drive
```

### 2. Create and activate virtual environment
```bash
# Create virtual environment
python -m venv .venv

# Activate on Linux/Mac
source .venv/bin/activate

# Activate on Windows (cmd)
.venv\Scripts\activate.bat

# Activate on Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash 
pip install -r requirements.txt
```

### 4. Google Drive API Configuration

- Step 4.1: Access Google Cloud Console:
    - Go to console.cloud.google.com
    - Sign in with your Google account

    ![Google Cloud Console](https://raw.githubusercontent.com/andrxmedy/yt2drive/main/docs/step1-console.jpg)

- Step 4.2: Create a new project
    - Click project selector at top
    - Select "New Project" 
    - Name: YT2Drive-Automation
    - Click "Create"

    ![Create New Project](https://raw.githubusercontent.com/andrxmedy/yt2drive/main/docs/step2-first-project.jpg)

- Step 4.3: Enable Google Drive API
    - Left menu → "APIs & Services" → "Library"
    - Search for "Google Drive API"
    - Click "Enable" 

    ![Enable Drive API](https://raw.githubusercontent.com/andrxmedy/yt2drive/main/docs/step3-enable-api.jpg)

- Step 4.4: Configure OAuth consent screen 
    - Left menu → "APIs & Services" → "OAuth consent screen"
    - User Type: "External"
    - Fill required information:
        - App name: Ex: YT2Drive-Automation
        - User support email: (your email)
        - Developer contact email: (your email)
    
    ![OAuth Consent Screen](https://raw.githubusercontent.com/andrxmedy/yt2drive/main/docs/step4-oauth-consent.jpg)

- Step 4.5: Create OAuth credentials 
    - Left menu → "APIs & Services" → "Credentials"
    - Click "Create Credentials" → "OAuth client ID"
    - Application type: "Desktop application"
    - Name: Ex: YT2Drive-Desktop-Client
    - Click "Create"

    ![Create OAuth Credentials](https://raw.githubusercontent.com/andrxmedy/yt2drive/main/docs/step5-create-credentials.jpg)

- Step 4.6: Download credentials
    - Click download icon next to the OAuth client
    - Rename file to "credentials.json"
    - Place in project folder

    ![Download Credentials](https://raw.githubusercontent.com/andrxmedy/yt2drive/main/docs/step6-download-credentials.jpg)

## Usage

Basic execution: 
```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Run the script
python yt2drive.py
```
Execution flow:
- Script will prompt for YouTube URL
- Video will be downloaded automatically
- Browser will open for Google authentication (first time only)
- Video will upload to Google Drive
- Public link will be generated and displayed
- Temporary files will be cleaned up

## Important notes

Processing time

Google Drive may take time to process videos after upload:
Small videos (<100MB): 1-3 minutes
Medium videos (100-500MB): 3-8 minutes
Large videos (500MB+): 5-15+ minutes

Security

NEVER share your credentials.json file
token.json is auto-generated after first authentication
Both files are included in .gitignore

## Technologies Used
- Python 3.9+
- yt-dlp - YouTube video downloading
- Google APIs Client Library - Google Drive integration
- OAuth2 - Secure authentication

## Author

Letícia Andrade de Oliveira Barros - andradeleticia456@gmail.com







