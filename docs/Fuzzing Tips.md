Fuzzing Tips: dotnet-api-recon

Optimize your endpoint discovery by customizing wordlists and request behavior.

📚 Recommended Wordlists

🔸 Blazor / .NET Specific

SecLists/Discovery/Web-Content/api/api-endpoints.txt

SecLists/Discovery/Web-Content/swagger.txt

SecLists/Discovery/Web-Content/spring-boot.txt

SecLists/Discovery/Web-Content/aspnet.txt

🔸 Login Portals / Admin Panels

SecLists/Discovery/Web-Content/burp-parameter-names.txt

SecLists/Discovery/Web-Content/Logins.fuzz.txt

SecLists/Passwords/Common-Credentials/10k-most-common.txt

🔸 Subdomain Fuzzing

SecLists/Discovery/DNS/bitquark-subdomains-top100000.txt

SecLists/Discovery/DNS/namelist.txt

🔧 FFUF Parameters That Matter

Filter By Response Size

Avoid noisy 404s:

-fs 315

Match Everything, Analyze Later

-mc all

💥 Advanced Targets

SSRF Targets

render?url=, proxy?url=, fetch?uri=, open?file=, url=...

Test internal addresses like:

http://127.0.0.1:80

http://169.254.169.254/

http://localhost/.env

SignalR Handshake

Check for:

/_blazor/negotiate

/chatHub/negotiate

⚠️ Don't Forget

Always use -H "Host: target.com" when testing IPs

Use -k or verify=False to avoid TLS issues

Use -X POST or -X OPTIONS to probe additional verbs

