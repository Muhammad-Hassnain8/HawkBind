# 🦅 HawkBind - DNS Enumeration Tool
<img width="1920" height="1045" alt="image" src="https://github.com/user-attachments/assets/045bedd9-a3e1-42e5-8aa8-bc90b43c3810" />

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0-brightgreen.svg" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.6+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <img src="https://img.shields.io/badge/Author-Muhammad%20Hassnain-red.svg" alt="Author">
</p>

<p align="center">
  <b>A powerful, fast, and colorful DNS enumeration tool for security professionals and penetration testers</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/DNS-Enumeration-purple.svg" alt="DNS Enumeration">
  <img src="https://img.shields.io/badge/Subdomain-Bruteforce-orange.svg" alt="Subdomain Bruteforce">
  <img src="https://img.shields.io/badge/Zone-Transfer-red.svg" alt="Zone Transfer">
  <img src="https://img.shields.io/badge/Multi-threaded-green.svg" alt="Multi-threaded">
</p>

---

## 📋 Table of Contents
- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Examples](#-usage-examples)
- [Command Line Options](#-command-line-options)
- [Output Formats](#-output-formats)
- [Advanced Usage](#-advanced-usage)
- [Screenshots](#-screenshots)
- [Use Cases](#-use-cases)
- [Tips & Tricks](#-tips--tricks)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## ✨ Features

### 🎯 **Core Features**
- **Comprehensive DNS Enumeration** - Queries all common DNS record types (A, AAAA, MX, NS, TXT, SOA, CNAME, PTR)
- **Fast Subdomain Discovery** - Multi-threaded brute-forcing with custom wordlists
- **Zone Transfer Testing** - Attempts zone transfers from all nameservers to detect misconfigurations
- **Recursive Scanning** - Automatically enumerates discovered subdomains
- **Custom DNS Resolver** - Use specific DNS servers for queries

### 🎨 **Visual Features**
- **Beautiful Colored Output** - Syntax highlighting with Colorama
- **Real-time Progress Bars** - Visual feedback during scanning
- **Live Results** - Found subdomains appear instantly
- **Structured Display** - Tables and boxes for better readability

### 📊 **Output Options**
- **Multiple Formats** - TXT, JSON, CSV
- **Save to File** - Store results for later analysis
- **Customizable** - Choose which records to display

### ⚡ **Performance**
- **Multi-threaded** - Configurable thread count for speed
- **Timeout Control** - Adjustable DNS timeouts
- **Optimized Queries** - Efficient DNS resolution

---

## 🚀 Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package manager)

### Step-by-Step Installation

```bash
# Clone the repository
git clone https://github.com/muhammad-hassnain/hawkbind.git
cd hawkbind

# Create virtual environment (recommended)
python3 -m venv hawkbind-env
source hawkbind-env/bin/activate  # On Windows: hawkbind-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Make the script executable
chmod +x main.py
```

### Quick Install Script
```bash
# One-liner installation
curl -sSL https://raw.githubusercontent.com/muhammad-hassnain/hawkbind/main/install.sh | bash
```

---

## 🏃 Quick Start

```bash
# Basic enumeration
python3 main.py -d example.com

# Full scan with wordlist
python3 main.py -d example.com -w wordlists/subdomains.txt

# Save results to file
python3 main.py -d example.com -w wordlists/subdomains.txt --output json -o results.json
```

---

## 📚 Usage Examples

### **1. Basic DNS Enumeration**
```bash
python3 main.py -d example.com
```
![Basic Scan](https://via.placeholder.com/800x400?text=Basic+Scan+Screenshot)

### **2. Subdomain Discovery**
```bash
python3 main.py -d example.com -w wordlists/subdomains.txt -t 50
```
![Subdomain Scan](https://via.placeholder.com/800x400?text=Subdomain+Scan+Screenshot)

### **3. Zone Transfer Test**
```bash
python3 main.py -d example.com --no-bruteforce --dns-records NS
```
![Zone Transfer](https://via.placeholder.com/800x400?text=Zone+Transfer+Screenshot)

### **4. Custom Resolver**
```bash
python3 main.py -d example.com --resolver 8.8.8.8
```

### **5. Recursive Enumeration**
```bash
python3 main.py -d example.com -w wordlists/subdomains.txt --recursive
```

### **6. Save as JSON**
```bash
python3 main.py -d example.com -w wordlists/subdomains.txt --output json -o scan_results.json
```

### **7. Minimal Output (No Colors)**
```bash
python3 main.py -d example.com --no-color
```

---

## 🛠️ Command Line Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `-d, --domain` | Target domain (required) | - | `-d example.com` |
| `-w, --wordlist` | Path to subdomain wordlist | None | `-w wordlists/subdomains.txt` |
| `-t, --threads` | Number of threads | 20 | `-t 100` |
| `--timeout` | DNS timeout in seconds | 3 | `--timeout 5` |
| `--dns-records` | Comma-separated DNS records | All | `--dns-records A,MX,TXT` |
| `--no-zone-transfer` | Skip zone transfer | False | `--no-zone-transfer` |
| `--no-bruteforce` | Skip subdomain brute-forcing | False | `--no-bruteforce` |
| `--output` | Output format (txt, json, csv) | None | `--output json` |
| `-o, --output-file` | Save results to file | None | `-o results.json` |
| `--resolver` | Custom DNS resolver IP | System default | `--resolver 8.8.8.8` |
| `--recursive` | Enable recursive enumeration | False | `--recursive` |
| `--no-color` | Disable colored output | False | `--no-color` |

---

## 📄 Output Formats

### **JSON Format**
```json
{
    "domain": "example.com",
    "timestamp": "2024-01-01 12:00:00",
    "basic_records": {
        "A": ["93.184.216.34"],
        "AAAA": ["2606:2800:220:1:248:1893:25c8:1946"],
        "MX": ["mail.example.com (Priority: 10)"],
        "NS": ["ns1.example.com", "ns2.example.com"],
        "TXT": ["v=spf1 include:_spf.example.com ~all"],
        "SOA": ["Primary NS: ns1.example.com, Hostmaster: admin.example.com"]
    },
    "subdomains": [
        "www.example.com",
        "mail.example.com",
        "api.example.com",
        "blog.example.com"
    ],
    "zone_transfer": {
        "ns1.example.com": {
            "success": false,
            "error": "Zone transfer failed"
        }
    }
}
```

### **CSV Format**
```csv
Type,Value
A,93.184.216.34
AAAA,2606:2800:220:1:248:1893:25c8:1946
MX,mail.example.com (Priority: 10)
NS,ns1.example.com
NS,ns2.example.com
TXT,"v=spf1 include:_spf.example.com ~all"
SUBDOMAIN,www.example.com
SUBDOMAIN,mail.example.com
SUBDOMAIN,api.example.com
```

### **TXT Format**
```
╔══════════════════════════════════════════════════════════════╗
║ HawkBind Results for example.com                             ║
║ Timestamp: 2024-01-01 12:00:00                              ║
╚══════════════════════════════════════════════════════════════╝

BASIC DNS RECORDS:
──────────────────────────────────────────────────

A Records:
  ├─ 93.184.216.34

MX Records:
  ├─ mail.example.com (Priority: 10)

NS Records:
  ├─ ns1.example.com
  └─ ns2.example.com

SUBDOMAINS FOUND:
──────────────────────────────────────────────────
  ├─ www.example.com
  ├─ mail.example.com
  ├─ api.example.com
  └─ blog.example.com
```

---

## 🔥 Advanced Usage

### **1. Integration with Other Tools**

#### **Extract IPs for Nmap scanning**
```bash
python3 main.py -d example.com --output json -o - | jq -r '.basic_records.A[]' > ips.txt
nmap -iL ips.txt -sV
```

#### **Create target list for ffuf**
```bash
python3 main.py -d example.com -w wordlists/subdomains.txt --output csv -o subdomains.csv
cat subdomains.csv | grep "SUBDOMAIN" | cut -d, -f2 | sed 's/$/\/FUZZ/' > ffuf_targets.txt
```

#### **Monitor for new subdomains**
```bash
#!/bin/bash
while true; do
    python3 main.py -d example.com -w wordlists/subdomains.txt --output json -o "scan_$(date +%Y%m%d).json"
    sleep 86400  # Run daily
done
```

### **2. Performance Optimization**

#### **Maximum Speed**
```bash
python3 main.py -d example.com -w wordlists/subdomains.txt -t 200 --timeout 1
```

#### **Stealth Mode (Avoid Detection)**
```bash
python3 main.py -d example.com -w wordlists/subdomains.txt -t 5 --timeout 10 --resolver 1.1.1.1
```

### **3. Targeted Enumeration**

#### **Check specific subdomains only**
```bash
# Create custom wordlist
echo -e "admin\ndev\nstaging\n" > custom.txt
python3 main.py -d example.com -w custom.txt
```

#### **Enumerate specific record types**
```bash
python3 main.py -d example.com --dns-records A,MX,TXT --no-bruteforce
```

---

## 📸 Screenshots

### **Main Banner**
```
╔══════════════════════════════════════════════════════════════╗
║  ██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗██████╗ ██╗███╗   ██╗██████╗  ║
║  ██║  ██║██╔══██╗██║    ██║██║ ██╔╝██╔══██╗██║████╗  ██║██╔══██╗ ║
║  ███████║███████║██║ █╗ ██║█████╔╝ ██████╔╝██║██╔██╗ ██║██║  ██║ ║
║  ██╔══██║██╔══██║██║███╗██║██╔═██╗ ██╔══██╗██║██║╚██╗██║██║  ██║ ║
║  ██║  ██║██║  ██║╚███╔███╔╝██║  ██╗██████╔╝██║██║ ╚████║██████╔╝ ║
║  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═══╝╚═════╝  ║
╠══════════════════════════════════════════════════════════════╣
║              DNS ENUMERATION TOOL v1.0                      ║
║                 Created by: Muhammad Hassnain               ║
╚══════════════════════════════════════════════════════════════╝
```

### **Scan in Progress**
```
[*] Enumerating basic DNS records...
    └─ Querying A records... Found 2
    └─ Querying MX records... Found 1
    └─ Querying NS records... Found 2

[*] Starting subdomain brute-forcing...
    └─ Loaded 1000 subdomains from wordlist
    └─ Starting bruteforce with 20 threads...

    Progress: ████████████████████████████████████████░ 98.5%
    
    ✓ Found: www.example.com
    ✓ Found: mail.example.com
    ✓ Found: api.example.com
```

### **Results Display**
```
[+] Found 15 subdomains:
    ╔════════════════════════════════════════════════════╗
    ║ ├─ www.example.com                                 ║
    ║ ├─ mail.example.com                                ║
    ║ ├─ api.example.com                                 ║
    ║ ├─ blog.example.com                                ║
    ║ └─ admin.example.com                               ║
    ║     ... and 10 more                                ║
    ╚════════════════════════════════════════════════════╝
```

---

## 🎯 Use Cases

### **1. Penetration Testing**
- Discover attack surface through subdomain enumeration
- Test for zone transfer vulnerabilities
- Identify misconfigured DNS records

### **2. Bug Bounty Hunting**
- Find hidden subdomains for bounty programs
- Map out target infrastructure
- Discover takeover opportunities

### **3. Security Auditing**
- Verify DNS configurations
- Check for information leakage
- Ensure proper DNS security posture

### **4. Red Teaming**
- Reconnaissance phase
- Infrastructure mapping
- Entry point discovery

### **5. Research & Analysis**
- Study DNS patterns
- Analyze domain structures
- Track DNS changes over time

---

## 💡 Tips & Tricks

### **Pro Tips**

1. **Start with a good wordlist**
   ```bash
   # Combine multiple wordlists for better coverage
   cat wordlist1.txt wordlist2.txt | sort -u > combined.txt
   ```

2. **Use multiple resolvers**
   ```bash
   # Rotate through resolvers to avoid rate limiting
   for resolver in 8.8.8.8 1.1.1.1 9.9.9.9; do
       python3 main.py -d example.com --resolver $resolver --no-bruteforce
   done
   ```

3. **Parse JSON results**
   ```bash
   # Extract all subdomains
   jq -r '.subdomains[]' results.json
   
   # Get all A records
   jq -r '.basic_records.A[]' results.json
   ```

4. **Create custom wordlists**
   ```bash
   # Generate wordlist from common patterns
   echo -e "dev\ntest\nstage\nprod\n" > custom.txt
   ```

5. **Monitor for changes**
   ```bash
   # Compare scans over time
   diff scan_yesterday.json scan_today.json | grep "subdomain"
   ```

### **Wordlist Resources**
- [SecLists](https://github.com/danielmiessler/SecLists)
- [Assetnote Wordlists](https://wordlists.assetnote.io/)
- [CommonSpeak](https://github.com/assetnote/commonspeak2)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### **Ways to Contribute**
- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit pull requests
- 🌐 Add translations

### **Development Setup**
```bash
# Fork and clone
git clone https://github.com/yourusername/hawkbind.git
cd hawkbind

# Create feature branch
git checkout -b feature/amazing-feature

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Commit changes
git commit -m "Add amazing feature"
git push origin feature/amazing-feature
```

### **Coding Standards**
- Follow PEP 8 guidelines
- Add docstrings for functions
- Include type hints
- Write unit tests for new features

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Muhammad Hassnain

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## ⚠️ Disclaimer

**IMPORTANT**: This tool is for educational and authorized security testing purposes only. Unauthorized scanning of domains may be:

- 🚫 Illegal in many jurisdictions
- 🚫 Against terms of service
- 🚫 Considered hostile activity

**Always ensure you have proper written authorization before testing any domain or system.**

---

## 👨‍💻 Author

### **Muhammad Hassnain**
Security Researcher & Penetration Tester

- 📧 Email: [muhammad.hassnain@example.com](mailto:muhammad.hassnain@example.com)
- 🐦 Twitter: [@mhassnain](https://twitter.com/mhassnain)
- 💼 LinkedIn: [muhammad-hassnain](https://linkedin.com/in/muhammad-hassnain)
- 🐙 GitHub: [muhammad-hassnain](https://github.com/muhammad-hassnain)
- 🌐 Website: [https://muhammadhassnain.com](https://muhammadhassnain.com)

---

## 🙏 Acknowledgments

Special thanks to:
- The dnspython team for their excellent library
- The security community for continuous inspiration
- All contributors and users of HawkBind

---

## 📊 Project Stats

<p align="center">
  <img src="https://img.shields.io/github/stars/muhammad-hassnain/hawkbind?style=social" alt="Stars">
  <img src="https://img.shields.io/github/forks/muhammad-hassnain/hawkbind?style=social" alt="Forks">
  <img src="https://img.shields.io/github/watchers/muhammad-hassnain/hawkbind?style=social" alt="Watchers">
  <img src="https://img.shields.io/github/contributors/muhammad-hassnain/hawkbind" alt="Contributors">
  <img src="https://img.shields.io/github/last-commit/muhammad-hassnain/hawkbind" alt="Last Commit">
  <img src="https://img.shields.io/github/issues/muhammad-hassnain/hawkbind" alt="Issues">
</p>

---

<p align="center">
  <b>Made with ❤️ by Muhammad Hassnain</b><br>
  <i>Keep learning, keep hacking, stay ethical!</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Stay-Secure-brightgreen.svg" alt="Stay Secure">
  <img src="https://img.shields.io/badge/Hack-Ethically-blue.svg" alt="Hack Ethically">
  <img src="https://img.shields.io/badge/Keep-Learning-orange.svg" alt="Keep Learning">
</p>

---

**⭐ Star this repository if you find it useful!**
