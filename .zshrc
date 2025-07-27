# === pyenv Initialization ===
# This part is essential for pyenv to manage Python versions.
# It should be at the end of your .bashrc
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"

# === Environment Variables for asyncpg / PostgreSQL (libpq) ===
# These tell pip where to find the PostgreSQL development libraries on macOS (Homebrew)
# These paths are typical for Apple Silicon Macs. For Intel Macs, it might be /usr/local/opt/libpq
export LDFLAGS="-L/opt/homebrew/opt/libpq/lib"
export CPPFLAGS="-I/opt/homebrew/opt/libpq/include"

# Optional: Add /opt/homebrew/bin to your PATH if it's not already there,
# especially if you installed Python directly with Homebrew and not pyenv
# export PATH="/opt/homebrew/bin:$PATH"

# === Prefect API URL (for convenience in new terminals) ===
# This sets the default Prefect API URL for any new terminal session.
# Useful if you're consistently connecting to a local server.
# Only uncomment and use if you're running Prefect Server directly (not via Docker for Prefect Server).
# export PREFECT_API_URL="http://127.0.0.1:4200/api"