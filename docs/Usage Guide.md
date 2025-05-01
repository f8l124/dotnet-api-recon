Usage Guide: dotnet-api-recon

This guide describes how to use the tool for maximum effect during reconnaissance or penetration tests.

🏁 Quickstart

Run the tool directly:

python3 blazor_recon.py

You'll be prompted for:

Base target URL (e.g., https://170.249.88.215)

Host header (e.g., api.grote.com)

Optional: HTTP proxy

Optional: JWT, Bearer, or Basic authentication header

🧰 Recon Features

🔍 Endpoint Brute-Force

/api, /api/v1, /_framework/, .well-known/, and more

Fuzzing via FFUF with multiple wordlists

📡 SignalR/WebSocket Testing

Checks /negotiate, /_blazor/negotiate, and known hubs

🔐 Auth Portal Testing

Brute-forces login pages with common paths and credentials

🔗 SSRF Vector Testing

Probes for endpoints like render?url=, proxy?uri=, etc.

📛 Subdomain Discovery

Uses DNS brute-force to find subdomains from SecLists

🧪 Nuclei Scanner (Optional)

Automatically scans found endpoints if Nuclei is installed

🔄 Example Prompt Responses

Target base URL: https://170.249.88.215
Host header: api.grote.com
Use upstream proxy (or leave blank): http://127.0.0.1:8080
Authorization header (optional): Bearer test

🪪 Output Files

Outputs are timestamped, e.g. recon_2025-05-01_1530.*

.json — Full response metadata

.csv — One row per endpoint

.html — Browser viewable table

.burp-requests.txt — BurpSuite-ready import

.nuclei.txt — Nuclei output

⚠️ Tip: Use VPNs or Proxies

This tool is aggressive. Use through a VPN or proxy during engagements.

