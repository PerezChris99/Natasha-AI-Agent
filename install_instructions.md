# Installation Instructions

## Setting up the Environment

1. Create a virtual environment:
   ```
   python -m venv env
   ```

2. Activate the environment:
   ```
   env\Scripts\activate
   ```

3. Upgrade pip:
   ```
   python -m pip install --upgrade pip
   ```

## Installing PyAudio

PyAudio requires special handling on Windows with Python 3.12. Follow these steps:

1. Download the unofficial wheel for your Python version from:
   https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

   For Python 3.12 on 64-bit Windows, download:
   `PyAudio‑0.2.13‑cp312‑cp312‑win_amd64.whl`

2. Install the downloaded wheel:
   ```
   pip install path\to\downloaded\PyAudio‑0.2.13‑cp312‑cp312‑win_amd64.whl
   ```

## Setting up Spotify Integration

To use the Spotify features, you need to create a Spotify Developer account and register an app:

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and log in
2. Click "Create An App"
3. Fill in the app name and description, then click "Create"
4. In your new app dashboard, note the "Client ID" and "Client Secret"
5. Click "Edit Settings" and add `http://localhost:8888/callback` to the Redirect URIs section
6. Save your changes

Next, set up your credentials using one of these methods:

### Method 1: Using config file
1. Open `config/spotify_config.py`
2. Replace the placeholder values with your actual Spotify credentials:
   ```python
   SPOTIPY_CLIENT_ID = "your_actual_client_id"
   SPOTIPY_CLIENT_SECRET = "your_actual_client_secret"
   ```

### Method 2: Using environment variables
1. Copy the `.env.example` file to a new file named `.env`:
   ```
   copy .env.example .env
   ```
2. Edit the `.env` file with your actual credentials
3. Install python-dotenv to load these variables:
   ```
   pip install python-dotenv
   ```
4. Make sure your main app loads these variables at startup:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

## Installing Other Requirements

Install the remaining packages:
```
pip install -r requirements.txt
```

## Troubleshooting

If you encounter issues with other packages:

1. For Pillow, if the version in requirements.txt still doesn't work, try:
   ```
   pip install --only-binary :all: Pillow
   ```

2. For any other packages that fail to build, search for pre-built wheels at:
   - https://www.lfd.uci.edu/~gohlke/pythonlibs/
   - https://pypi.org/

## Note on Compatibility

This project was tested with Python 3.12. Some packages may require specific versions to ensure compatibility.
