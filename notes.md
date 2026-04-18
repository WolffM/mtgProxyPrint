## Steps to reproduce
1. Open a shell in `/home/runner/work/mtgProxyPrint/mtgProxyPrint`.
2. Run `python -m py_compile main.py` to confirm the script parses.
3. Run `~/.local/bin/bandit -r main.py`.
4. Inspect Bandit findings for `B113: request_without_timeout` in `main.py`.

## Observed
Bandit reports multiple medium-severity security findings for HTTP calls made with `requests.get(...)` and no explicit timeout. The trace shows several locations in `main.py` where requests are performed without timeout control, meaning calls can potentially hang indefinitely on slow or unresponsive endpoints.

## Expected
All outbound HTTP requests in `main.py` should include an explicit timeout value so the script fails fast when remote services are slow or unavailable. After fixing, a Bandit scan should no longer report `B113` findings in this file.
