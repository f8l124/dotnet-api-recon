Install Guide for dotnet-api-recon

This guide walks you through installing all dependencies needed to run dotnet-api-recon on Linux, macOS, or Windows.

🔧 Requirements

Python 3.8 or newer

Git (for cloning this repo)

Internet connection (to pull dependencies and optional tools)

📦 Step-by-Step Installation

1. Clone the Repository

git clone https://github.com/yourhandle/dotnet-api-recon.git
cd dotnet-api-recon

2. Install Python Dependencies

pip install -r requirements.txt

Or manually:

pip install requests

3. (Optional) Install Nuclei

If you’d like automated vulnerability scanning:

curl -s https://api.github.com/repos/projectdiscovery/nuclei/releases/latest \
  | grep browser_download_url | grep linux | grep nuclei | cut -d '"' -f 4 \
  | wget -qi - && chmod +x nuclei && sudo mv nuclei /usr/local/bin/

Verify:

nuclei -version

4. (Optional) Proxy Configuration

If you want to inspect traffic in BurpSuite or ZAP:

Set proxy when prompted (e.g., http://127.0.0.1:8080)

Use Allow insecure SSL option (handled by script’s -k / verify=False)

✅ Ready to Go

Now you can run:

python3 blazor_recon.py

And follow the prompts.

