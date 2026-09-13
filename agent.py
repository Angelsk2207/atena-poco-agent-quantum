#!/usr/bin/env python3
"""Poco C85 diagnostic relay: lightweight, read-only, Hermes-connected."""
import json, os, subprocess, time, urllib.request

BASE = os.environ.get('HERMES_BASE_URL', 'https://atena-hermes-quantum-b81f56b01.onrunxbuild.com').rstrip('/')
KEY = os.environ.get('HERMES_API_KEY', '')
INTERVAL = int(os.environ.get('POCO_AGENT_INTERVAL', '60'))

def local_snapshot():
    data = {'agent':'poco-c85','mode':'diagnostic-read-only','ts':int(time.time())}
    try:
        p = subprocess.run(['termux-battery-status'], capture_output=True, text=True, timeout=8)
        data['battery'] = json.loads(p.stdout) if p.returncode == 0 else {'error':'unavailable'}
    except Exception:
        data['battery'] = {'error':'termux-api-unavailable'}
    data['paths'] = {p: os.path.exists(os.path.expanduser(p)) for p in ['~/storage/shared/Download','~/storage/shared/Movies']}
    return data

def heartbeat(snapshot):
    if not KEY: return
    payload = json.dumps({'command':'poco.heartbeat','payload':snapshot}).encode()
    req = urllib.request.Request(BASE+'/v1/command', data=payload, method='POST', headers={'content-type':'application/json','x-api-key':KEY})
    with urllib.request.urlopen(req, timeout=15) as r: return r.status

while True:
    try: heartbeat(local_snapshot())
    except Exception: pass
    time.sleep(INTERVAL)
