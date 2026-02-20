# Discord Media RPC

A Discord Rich Presence client that shows what you're watching on Jellyfin or listening to on Audiobookshelf - with cover art, timestamps, and chapter tracking.

<p align="center">
  <img src="screenshots/preview.png" width="90%" alt="RPC Preview Video">
</p>
<p align="center">
  <img src="screenshots/preview2.png" width="90%" alt="RPC Preview Audio">
</p>

<div align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge&logo=python&logoColor=ffffff&labelColor=000000&color=333446"/>
  <a href="https://github.com/MakD/media-rpc/releases"><img src="https://img.shields.io/github/downloads/MakD/media-rpc/total?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgLTk2MCA5NjAgOTYwIiBmaWxsPSJ3aGl0ZSI+PHBhdGggZD0iTTIwMC0xNjBoNTYwcTE3IDAgMjguNSAxMS41VDgwMC0xMjBxMCAxNy0xMS41IDI4LjVUNzYwLTgwSDIwMHEtMTcgMC0yOC41LTExLjVUMTYwLTEyMHEwLTE3IDExLjUtMjguNVQyMDAtMTYwWm0yODAtMTA1cS05IDAtMTcuNS00VDQ0OC0yODFMMjUwLTUzNXEtMTUtMjAtNC00Mi41dDM2LTIyLjVoNzh2LTI0MHEwLTE3IDExLjUtMjguNVQ0MDAtODgwaDE2MHExNyAwIDI4LjUgMTEuNVQ2MDAtODQwdjI0MGg3OHEyNSAwIDM2IDIyLjV0LTQgNDIuNUw1MTItMjgxcS02IDgtMTQuNSAxMnQtMTcuNSA0WiIvPjwvc3ZnPg==&logoColor=ffffff&labelColor=000000&color=333446"/></a>
</div>

---

## Features

- Jellyfin support - movies and TV shows with cover art (falls back to TMDB)
- Audiobookshelf support - audiobooks and podcasts with chapter tracking
- **Privacy-focused** - filters by your specific User ID so your friends' streams don't show on your profile
- **Secure Configuration** - uses a `.env` file to keep your API tokens and IDs safe
- Cover art fetched directly from your media servers
- Elapsed and remaining time timestamps
- Library blacklist to hide specific Jellyfin libraries (cached for performance)
- Auto-reconnect if Discord connection drops
- Local cover cache to avoid redundant requests

---

## Requirements

- Python 3.8+
- A running [Jellyfin](https://jellyfin.org/) and/or [Audiobookshelf](https://www.audiobookshelf.org/) instance
- A [Discord application](https://discord.com/developers/applications) with a Client ID
- A reverse proxy (Caddy, Nginx, Apache, Traefik) with a public domain for ABS cover art - see [Cover Art Setup](#cover-art-setup)

---

## Installation

**1. Clone the repository:**
```bash
git clone https://github.com/MakD/media-rpc.git
cd media-rpc
```

**2. Install dependencies:**
```bash
pip install requests python-dotenv
# Note: On newer Debian/Ubuntu systems, use `sudo apt install python3-requests python3-dotenv` instead.
```

**3. Configure the script:** Create a new file named `.env` in the same directory as the script and fill in your details:

```env
DISCORD_CLIENT_ID=YOUR_DISCORD_APPLICATION_ID

# Jellyfin
JELLYFIN_SERVER=https://jellyfin.example.com/Sessions
JELLYFIN_API_KEY=YOUR_JELLYFIN_API_KEY
JELLYFIN_USER_ID=YOUR_JELLYFIN_USER_ID
TMDB_API_KEY=YOUR_TMDB_API_KEY

# Audiobookshelf
ABS_SERVER=https://abs.example.com
ABS_API_TOKEN=YOUR_ABS_API_TOKEN
```

**4. Run manually to test:**
```bash
python3 media_rpc.py
```

---

## Configuration

### Discord Application ID
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Copy the **Application ID** (not a bot token) into `DISCORD_CLIENT_ID`

### Jellyfin API Key
1. In Jellyfin, go to **Dashboard → API Keys**
2. Create a new key and paste it into `JELLYFIN_API_KEY`

### Jellyfin User ID (Required for Privacy)
To ensure Discord only shows what *you* are watching and ignores other users on your server:
1. Open your Jellyfin web dashboard.
2. Go to **Dashboard → Users** and click on your user profile.
3. Look at the URL in your browser. Copy the long string of letters and numbers after `userId=`. 
4. Paste it into `JELLYFIN_USER_ID` in your `.env` file.

### Audiobookshelf API Token
1. In Audiobookshelf, go to **Settings → Users**
2. Click your user and copy the **API Token**

### TMDB API Key (optional, Jellyfin cover fallback)
1. Create an account at [themoviedb.org](https://www.themoviedb.org/)
2. Go to **Settings → API** and request a key

### Library Blacklist (optional)
To hide specific Jellyfin libraries from showing in RPC, edit the list directly in `media_rpc.py`:
```python
JELLYFIN_IGNORE_LIBRARIES = ["Bollywood", "Kids"]
```

---

## Cover Art Setup

Discord fetches cover images directly from the URL you provide, which means your media server needs to be publicly accessible. Since Audiobookshelf requires authentication, you need to set up an **authenticated proxy route** in your reverse proxy. This lets Discord access cover art via a short, clean URL, while your token stays on the server and is never exposed.

This only makes cover artwork publicly accessible - not your audio files or any other data.

### Caddy
```caddy
your-abs-domain.com {
    handle /cover/* {
        rewrite * /api/items/{http.request.uri.path.1}/cover
        reverse_proxy localhost:13378 {
            header_up Authorization "Bearer YOUR_ABS_TOKEN"
        }
    }

    reverse_proxy localhost:13378
}
```

### Nginx
```nginx
location /cover/ {
    rewrite ^/cover/(.*)$ /api/items/$1/cover break;
    proxy_pass http://localhost:13378;
    proxy_set_header Authorization "Bearer YOUR_ABS_TOKEN";
}
```

### Apache
```apache
RewriteRule ^/cover/(.*)$ /api/items/$1/cover [PT]
RequestHeader set Authorization "Bearer YOUR_ABS_TOKEN"
ProxyPass /cover/ http://localhost:13378/api/items/
```

After setup, test it by opening this in your browser (no login required):
```
[https://your-abs-domain.com/cover/ANY_LIBRARY_ITEM_ID](https://your-abs-domain.com/cover/ANY_LIBRARY_ITEM_ID)
```

For Jellyfin, no extra proxy setup is needed - cover art is fetched using your API key directly.

---

## Running as a Background Service (Linux)

Because Discord runs under your personal user account, this must be set up as a **User Service**, not a system-wide root service. Do not use `sudo` for these steps.

**1. Create the user systemd directory:**
```bash
mkdir -p ~/.config/systemd/user
```

**2. Create the service file:**
```bash
nano ~/.config/systemd/user/media-rpc.service
```

**3. Paste the following configuration:**
*(Make sure to replace `/home/YOUR_USERNAME/path/to/` with the actual absolute path to your cloned folder!)*
```ini
[Unit]
Description=Media Discord RPC
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/YOUR_USERNAME/path/to/media-rpc/media_rpc.py
WorkingDirectory=/home/YOUR_USERNAME/path/to/media-rpc/
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
```

**4. Enable and start the service:**
```bash
systemctl --user daemon-reload
systemctl --user enable --now media-rpc.service
```

**5. Check the live logs:**
```bash
journalctl --user -u media-rpc.service -f
```

---

## How It Works

Every 15 seconds, the script polls your media servers for active sessions. If something is playing, it constructs a Rich Presence payload with the title, state, timestamps, and cover art, then sends it to Discord over a local Unix socket. Cover URLs are cached in `cover_cache.json` so they are only fetched once per item. If nothing is playing, the presence is cleared.

---

## Troubleshooting

**RPC not showing**
- Make sure Discord is running, and your status is not set to invisible
- Confirm `DISCORD_CLIENT_ID` is the Application ID, not a bot token

**Cover art showing a dice/placeholder icon**
- Your image URL is likely not publicly accessible, or exceeds Discord's 256-character URL limit
- Follow the [Cover Art Setup](#cover-art-setup) instructions for your reverse proxy

**Audiobookshelf not showing**
- The script detects playback by comparing the position between polls - it needs two cycles to confirm something is playing, so there may be a brief delay on startup
- Make sure `ABS_SERVER` has no trailing slash

**Jellyfin not showing**
- Paused sessions are intentionally ignored
- Check that your `JELLYFIN_API_KEY` is valid and your server is reachable
