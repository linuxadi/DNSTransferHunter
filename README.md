# DNSTransferHunter
DNSTransferHunter scans for DNS AXFR zone transfer misconfigurations. Supports bulk targets, subdomain-to-zone discovery, managed DNS filtering, and automatic proof saving. Built for security testing and bug bounty workflows.

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AXFR Zone Transfer Scanner</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: #e5e7eb;
            padding: 40px;
            line-height: 1.6;
        }
        h1, h2, h3 {
            color: #38bdf8;
        }
        code, pre {
            background: #020617;
            padding: 10px;
            border-radius: 6px;
            display: block;
            overflow-x: auto;
            color: #a5f3fc;
        }
        .box {
            background: #020617;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        ul li {
            margin-bottom: 6px;
        }
    </style>
</head>
<body>

<h1>AXFR Zone Transfer Scanner</h1>

<div class="box">
    <p>
        A professional-grade DNS Zone Transfer (AXFR) misconfiguration scanner designed for
        bug bounty hunters and security engineers.
    </p>
</div>

<h2>🚀 Features</h2>
<ul>
    <li>Single domain and bulk file scanning</li>
    <li>Automatic URL to domain normalization</li>
    <li>Smart parent zone discovery (walks up subdomains)</li>
    <li>Skips Cloudflare, AWS, Azure, Akamai, Google DNS, etc.</li>
    <li>Only-vulnerable output mode for large scans</li>
    <li>Automatic saving of successful AXFR results</li>
    <li>Timeout handling and error-safe execution</li>
</ul>

<h2>🧠 Why AXFR Matters</h2>
<p>
    A successful zone transfer can leak:
</p>
<ul>
    <li>All subdomains</li>
    <li>Internal hostnames</li>
    <li>Private infrastructure details</li>
</ul>
<p>
    This is a critical misconfiguration, but rare in modern infrastructure.
</p>

<h2>⚙️ Installation</h2>
<pre>
git clone https://github.com/yourrepo/axfr-scanner
cd axfr-scanner
chmod +x zone_transfer_check.py
</pre>

<h2>🧪 Usage</h2>

<h3>Scan single target</h3>
<pre>
python3 zone_transfer_check.py -u example.com
</pre>

<h3>Scan list of domains</h3>
<pre>
python3 zone_transfer_check.py -f domains.txt
</pre>

<h3>Only show vulnerable results</h3>
<pre>
python3 zone_transfer_check.py -f domains.txt -v
</pre>

<h3>Save results</h3>
<pre>
python3 zone_transfer_check.py -f domains.txt -o results/
</pre>

<h2>🧩 How It Works</h2>
<ul>
    <li>Normalizes URLs into domains</li>
    <li>Walks up the domain tree to find real DNS zones</li>
    <li>Fetches NS records</li>
    <li>Skips known managed DNS providers</li>
    <li>Attempts AXFR on realistic targets only</li>
</ul>

<h2>⚠️ Disclaimer</h2>
<p>
    This tool is for educational and authorized security testing only.
    Do not use against systems you do not own or have permission to test.
</p>

<h2>👨‍💻 Author</h2>
<p>
    Built for bug bounty and security research.
</p>

</body>
</html>
