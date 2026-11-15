# Gemma Bot - VPS Deployment Guide

## Prerequisites

- Python 3.8+
- Node.js (for PM2)
- PM2 installed globally: `npm install -g pm2`

## Step-by-Step Setup

### 1. Clone the repo and navigate to it
```bash
git clone https://github.com/your-username/gemma-bot
cd gemma-bot
```

### 2. Create Python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your tokens/keys
nano .env
```

You'll need:
- **DISCORD_TOKEN**: From [Discord Developer Portal](https://discord.com/developers/applications)
  - Create a new application → Bot → Copy token
  - Enable "Message Content Intent" under Privileged Gateway Intents
  - Invite bot to your server with OAuth2: `https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot`

- **GOOGLE_API_KEY**: From [Google AI Studio](https://ai.google.dev)
  - Create a new API key
  - Ensure Gemini API is enabled

### 5. Create logs directory
```bash
mkdir -p logs
```

### 6. Start the bot with PM2
```bash
pm2 start ecosystem.config.js
```

### 7. Save PM2 startup on reboot
```bash
pm2 startup
# Run the command that PM2 outputs
pm2 save
```

## Commands

### Check bot status
```bash
pm2 status
pm2 logs gemma-bot
pm2 logs gemma-bot --err  # Error logs only
```

### Restart bot
```bash
pm2 restart gemma-bot
```

### Stop bot
```bash
pm2 stop gemma-bot
```

### Delete from PM2
```bash
pm2 delete gemma-bot
```

### Monitor in real-time
```bash
pm2 monit
```

## Troubleshooting

### Bot won't start
1. Check logs: `pm2 logs gemma-bot --err`
2. Verify `.env` file exists and has valid tokens
3. Test Python directly: `python3 gemma_bot.py`

### Bot crashes frequently
1. Check memory usage: `pm2 monit`
2. Check for API rate limits in logs
3. Verify Google API key is still valid
4. Check Discord bot permissions on the server

### Bot not responding to mentions
1. Make sure "Message Content Intent" is enabled in Discord Developer Portal
2. Verify bot has permission to read messages and send messages
3. Check bot role is high enough in server hierarchy

## Updating the bot

```bash
git pull
# Restart with PM2
pm2 restart gemma-bot
```

## Production Notes

- **Memory limit**: Set to 500MB by default in ecosystem.config.js (adjust as needed)
- **Auto-restart**: Enabled. Bot will automatically restart on crashes
- **Logging**: Logs are saved in `logs/` directory
- **Graceful shutdown**: Bot has 5 seconds to clean up before hard kill
- **No hot-reload**: File changes require manual restart with `pm2 restart gemma-bot`

## Monitoring

### Long-term resource monitoring
```bash
pm2 web  # Opens PM2 web dashboard on http://localhost:9615
```

### Check system resources
```bash
# From your earlier VPS performance snippet
top -b -n 1 | head -20
free -h
df -h
```

## Useful PM2 commands

```bash
pm2 list              # List all processes
pm2 describe gemma-bot # Detailed info about bot
pm2 flush             # Clear logs
pm2 kill              # Stop all processes and exit PM2 daemon
pm2 update            # Update PM2
```
