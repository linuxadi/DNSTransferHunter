<h1>DNSTransferHunter</h1>
<p><b>Smart AXFR Zone Transfer Misconfiguration Scanner</b></p>

<div class="box">
    <p>
        <b>DNSTransferHunter</b> is a professional-grade security tool for detecting DNS Zone Transfer (AXFR)
        misconfigurations. It is designed for bug bounty hunters and security engineers to efficiently
        find exposed DNS zones in large recon datasets.
    </p>
    <p>
        <b>Tagline:</b> Hunt exposed DNS zone transfers before attackers do.
    </p>
</div>

<h2>🚀 Features</h2>
<ul>
    <li>Scan single domain or bulk lists</li>
    <li>Accepts full URLs or domains (auto-normalization)</li>
    <li>Smart parent zone discovery (walks up subdomains)</li>
    <li>Skips managed DNS providers (Cloudflare, AWS, Azure, Akamai, Google, etc.)</li>
    <li>Only-vulnerable output mode for large scans</li>
    <li>Automatic saving of successful AXFR results</li>
    <li>Timeout handling and stable error handling</li>
</ul>

<h2>🧠 Why AXFR Is Dangerous</h2>
<p>
    If a DNS server allows zone transfer (AXFR), an attacker can dump the entire DNS zone including:
</p>
<ul>
    <li>All subdomains</li>
    <li>Internal hostnames</li>
    <li>Development / staging systems</li>
    <li>Private infrastructure records</li>
</ul>
<p>
    This is a <b>critical misconfiguration</b> and often leads to further compromise.
</p>

<h2>⚙️ Requirements</h2>
<pre>
- Python 3
- dig command (dnsutils / bind9-dnsutils)
</pre>

<h3>Install dig on Kali / Debian / Ubuntu</h3>
<pre>
apt update
apt install dnsutils
</pre>

<h2>📦 Installation</h2>
<pre>
git clone https://github.com/yourusername/DNSTransferHunter
cd DNSTransferHunter
chmod +x zone_transfer_check.py
</pre>

<h2>🧪 Usage</h2>

<h3>Scan single domain</h3>
<pre>
python3 zone_transfer_check.py -u example.com
</pre>

<h3>Scan list of domains / URLs</h3>
<pre>
python3 zone_transfer_check.py -f targets.txt
</pre>

<h3>Show only vulnerable results (recommended for big lists)</h3>
<pre>
python3 zone_transfer_check.py -f targets.txt -v
</pre>

<h3>Save successful AXFR output to directory</h3>
<pre>
python3 zone_transfer_check.py -f targets.txt -o results/
</pre>

<h3>Set custom timeout</h3>
<pre>
python3 zone_transfer_check.py -f targets.txt -t 20
</pre>

<h2>🧩 How It Works</h2>
<ul>
    <li>Normalizes input (URL → domain)</li>
    <li>Walks up the domain tree to find real DNS zones</li>
    <li>Fetches NS records for each zone candidate</li>
    <li>Skips known cloud and managed DNS providers</li>
    <li>Attempts AXFR only on realistic targets</li>
    <li>Saves any successful zone transfers for proof</li>
</ul>

<h2>🛡️ When This Tool Is Useful</h2>
<ul>
    <li>Bug bounty recon</li>
    <li>Internal security assessments</li>
    <li>University / government domain audits</li>
    <li>Legacy infrastructure testing</li>
    <li>Acquired company asset testing</li>
</ul>

<h2>⚠️ Disclaimer</h2>
<p>
    This tool is for <b>educational and authorized security testing only</b>.
    Do NOT use it against systems you do not own or do not have explicit permission to test.
</p>
<p>
    The author is not responsible for any misuse or damage caused by this tool.
</p>

<h2>👨‍💻 Author</h2>
<p>
    Built for security research and bug bounty hunting.
</p>

<h2>⭐ Project Name</h2>
<p>
    <b>DNSTransferHunter</b> — because it hunts exposed DNS zone transfers.
</p>

</body>
</html>
