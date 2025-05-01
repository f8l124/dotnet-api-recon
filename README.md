dotnet-api-recon

dotnet-api-recon is a Blazor- and .NET-aware API reconnaissance and fuzzing toolkit for black-box penetration testing. It identifies exposed endpoints, misconfigured API paths, SSRF risks, SignalR negotiation interfaces, and authentication bypass surfaces commonly found in .NET and Blazor WebAssembly deployments.

🔍 Features

✅ Probes for .NET-specific paths and extensions (.dll, .cshtml, _framework/, etc.)

✅ SignalR WebSocket handshake testing via /_blazor/negotiate

✅ WAF bypass fuzzing with trusted IP headers

✅ Brute-forces login portals with common credentials

✅ SSRF vector testing with render?url= injection

✅ Subdomain brute-forcing with DNS resolution check

✅ JSON, CSV, and HTML reporting

✅ BurpSuite-style request export

✅ Auto-invokes Nuclei if installed

📦 Requirements

Python 3.8+

requests module (pip install -r requirements.txt)

Optional: nuclei in your $PATH

🚀 Installation

git clone https://github.com/yourhandle/dotnet-api-recon.git
cd dotnet-api-recon
pip install -r requirements.txt

🔧 Usage

python3 blazor_recon.py

You’ll be prompted for:

Target URL (e.g., https://api.example.com)

Host header (e.g., api.example.com)

Optional upstream proxy (e.g., http://127.0.0.1:8080)

📄 Output Files

recon_<timestamp>.json — full result set

recon_<timestamp>.csv — simplified CSV report

recon_<timestamp>.html — browsable HTML table

recon_<timestamp>.burp-requests.txt — ready for BurpSuite import

recon_<timestamp>.nuclei.txt — if Nuclei scan enabled

📚 Documentation

Install Guide

Usage & Examples

Output File Formats

Wordlist Expansion Tips

🙌 Contributing

PRs, feature ideas, and bug reports welcome. Wordlist improvements and .NET-specific endpoint suggestions are especially appreciated!

📄 License

This project is licensed under the MIT License — see the LICENSE file for details.

🛡️ Disclaimer

This tool is provided for educational and authorized penetration testing purposes only. Unauthorized scanning or probing of systems you do not own is strictly forbidden.

