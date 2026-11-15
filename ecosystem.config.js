module.exports = {
  apps: [
    {
      name: 'gemma-bot',
      script: './gemma_bot.py',
      interpreter: 'python3',
      instances: 1,
      exec_mode: 'fork',
      
      // Environment variables - load from .env file
      env: {
        NODE_ENV: 'production',
      },
      
      // Auto-restart on crash
      autorestart: true,
      watch: false, // Set to true if you want hot-reload on file changes (not recommended for bots)
      
      // Logging
      error_file: './logs/gemma_bot.error.log',
      out_file: './logs/gemma_bot.out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      
      // Resource limits (optional - adjust based on your VPS)
      max_memory_restart: '500M',
      
      // Graceful shutdown timeout
      kill_timeout: 5000,
      
      // Listen for uncaught exceptions
      listen_timeout: 3000,
      shutdown_with_message: true,
    }
  ]
};
