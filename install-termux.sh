#!/data/data/com.termux/files/usr/bin/bash
set -eu
mkdir -p "$HOME/.atena-poco-agent"
cp agent.py "$HOME/.atena-poco-agent/agent.py"
mkdir -p "$HOME/.termux/boot"
cat > "$HOME/.termux/boot/start-atena-agent" <<'BOOT'
#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock 2>/dev/null || true
export HERMES_BASE_URL='https://atena-hermes-quantum-b81f56b01.onrunxbuild.com'
# Set HERMES_API_KEY in ~/.atena-poco-agent/env before starting.
[ -f "$HOME/.atena-poco-agent/env" ] && . "$HOME/.atena-poco-agent/env"
exec python "$HOME/.atena-poco-agent/agent.py" >> "$HOME/.atena-poco-agent/agent.log" 2>&1
BOOT
chmod 700 "$HOME/.termux/boot/start-atena-agent"
echo 'Agent files installed. Configure ~/.atena-poco-agent/env, then open Termux:Boot.'
