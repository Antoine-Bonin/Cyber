# 🛡️ Cybersecurity Portfolio — Piscine & Practical Projects

[![Security](https://img.shields.io/badge/Focus-Cybersecurity%20%7C%20Red%20%26%20Blue%20Team-red.svg)](#)
[![Environment](https://img.shields.io/badge/Platform-Linux%20%2F%20Docker-blue.svg)](#)
[![Standards](https://img.shields.io/badge/Standards-RFC%204226%20%7C%20OWASP%20Top%2010%20%7C%20MITRE%20ATT%26CK-green.svg)](#)
[![Status](https://img.shields.io/badge/Status-In%20Active%20Development-orange.svg)](#)

This repository brings together a **suite of 8 practical cybersecurity projects**, covering **Offensive (Red Team)**, **Defensive (Blue Team)**, **Reverse Engineering**, **Applied Cryptography**, and **Network/System Security** skills.

Designed to validate and demonstrate a concrete mastery of real-world attack vectors and detection mechanisms, this portfolio synthesizes the fundamentals required for roles such as **SOC / Blue Team Intern**, **Junior Pentester**, **Cybersecurity Consultant**, or **DevSecOps Engineer**.

---

## 📑 Table of Contents

1. [Skills Matrix & Overview](#-skills-matrix--overview)
2. [Details of the 8 Projects](#-details-of-the-8-projects)
   - [01. 1-arachnida web — OSINT & Forensic Image Extraction](#01-1-arachnida-web--osint--forensic-image-extraction)
   - [02. 2-ft_otp — Strong Authentication Engine (HOTP/TOTP RFC 4226)](#02-2-ft_otp--strong-authentication-engine-hotptotp-rfc-4226)
   - [03. 3-ft_onion — Secure Deployment & Tor Hidden Service](#03-3-ft_onion--secure-deployment--tor-hidden-service)
   - [04. 4-reverse me — Reverse Engineering & Binary Analysis](#04-4-reverse-me--reverse-engineering--binary-analysis)
   - [05. 5-stockholm malware — Ransomware Simulation & Encryption](#05-5-stockholm-malware--ransomware-simulation--encryption)
   - [06. 6-cyber iron dome — HIDS & Real-Time Attack Detection](#06-6-cyber-iron-dome--hids--real-time-attack-detection)
   - [07. 7-inquisitor network — Man-in-the-Middle (ARP Spoofing) & Sniffing](#07-7-inquisitor-network--man-in-the-middle-arp-spoofing--sniffing)
   - [08. 8-vaccine web — Automated SQL Injection Exploitation Engine](#08-8-vaccine-web--automated-sql-injection-exploitation-engine)
3. [Methodology & Best Practices](#-methodology--best-practices)
4. [Legal Disclaimer](#-legal-disclaimer)

---

## 📊 Skills Matrix & Overview

| Repository | Project | Domain | Role / Field | Key Technologies & Concepts |
| :--- | :--- | :--- | :--- | :--- |
| [`1-arachnida web`](./1-arachnida%20web/) | **Spider & Scorpion** | Web Scraping / Forensics | OSINT & Recon | Python, HTML Parsing, EXIF Metadata, Pillow, Requests |
| [`2-ft_otp`](./2-ft_otp/) | **ft_otp** | Cryptography / IAM | Auth Security | HMAC-SHA1, RFC 4226 (HOTP), Time-based OTP, Symmetric Encryption |
| [`3-ft_onion`](./3-ft_onion/) | **ft_onion** | Network / Anonymity | Infra Hardening | Tor Hidden Services (.onion v3), Nginx, SSH Hardening (Port 4242) |
| [`4-reverse me`](./4-reverse%20me/) | **Reverse Me** | Reverse Engineering | Malware / AppSec | GDB, x86/x64 Decompilation, Assembly Analysis, C Reconstruction |
| [`5-stockholm malware`](./5-stockholm%20malware/) | **Stockholm** | Malware Analysis | Threat Analysis | Ransomware Simulation (WannaCry extensions), AES-256, Key Management |
| [`6-cyber iron dome`](./6-cyber%20iron%20dome/) | **Iron Dome** | Blue Team / HIDS | SOC / Endpoint Def | Linux Daemon, Shannon Entropy, I/O Monitoring, `/var/log` Alerting |
| [`7-inquisitor network`](./7-inquisitor%20network/) | **Inquisitor** | Network Security | Red Team / NetSec | Raw Sockets, Full-Duplex ARP Poisoning, Libpcap Sniffing, FTP Parsing |
| [`8-vaccine web`](./8-vaccine%20web/) | **Vaccine** | Web Pentest | Red Team / AppSec | SQL Injection (Union, Error, Boolean/Blind), Payload Crafting, DB Dumping |

---

## 🔍 Details of the 8 Projects

---

### 01. `1-arachnida web` — OSINT & Forensic Image Extraction

> **Objective:** Perform the reconnaissance and information gathering (OSINT) phase using a targeted scraper coupled with a forensic metadata analyzer.

The project is split into two complementary utilities:
- **Spider (`./spider [-rlp] URL`):**
  - Recursively scrapes media hosted on a target website.
  - Fine-grained management of recursion depth (`-l [N]`, default: 5) and destination directory (`-p [PATH]`).
  - Filters standard image formats: `.jpg`/`.jpeg`, `.png`, `.gif`, `.bmp`.
- **Scorpion (`./scorpion FILE1 [FILE2 ...]`):**
  - Forensic analysis tool that extracts hidden metadata from images (creation/modification dates, GPS coordinates, camera model, dimensions, color profile, EXIF tags).

---

### 02. `2-ft_otp` — Strong Authentication Engine (HOTP/TOTP RFC 4226)

> **Objective:** Implement a multi-factor authentication (MFA/2FA) system from scratch, strictly complying with the **RFC 4226 (HOTP)** cryptographic standard and its time-based derivative (TOTP).

- **Secure Storage (`ft_otp -g <key.hex>`):**
  - Strict validation of cryptographic randomness (minimum 64-character hexadecimal key).
  - Symmetric encryption of the master key before writing to disk (`ft_otp.key`) to prevent direct extraction in case of file system compromise.
- **OTP Generation (`ft_otp -k ft_otp.key`):**
  - Dynamic derivation based on HMAC-SHA1 and Dynamic Truncation to produce a random 6-digit code.
  - Time synchronization (system clock access) for direct compatibility with standard industrial validators (e.g., `oathtool --totp`).

---

### 03. `3-ft_onion` — Secure Deployment & Tor Hidden Service

> **Objective:** Deploy a resilient and anonymized infrastructure on the decentralized **Tor** network, while hardening all exposed services.

- **Tor Hidden Service:**
  - Onion routing via native `torrc` configuration.
  - Publishing a static service with a `.onion` domain name (v3).
- **Hardening Nginx & SSH:**
  - Exclusive exposure of the static webpage on HTTP port 80 via a lightweight Nginx, configured following the principle of least privilege.
  - Isolated administrative SSH access shifted to the non-standard port **4242** (`sshd_config`).
  - Complete absence of direct exposure to the public Internet (zero open ports directly / no unmanaged port-forwarding).
- **Containerization:**
  - Orchestrated environment using Docker to ensure reproducibility and process isolation.

---

### 04. `4-reverse me` — Reverse Engineering & Binary Analysis

> **Objective:** Analyze the internal behavior of compiled and protected ELF binaries using reverse engineering tools (GDB, Objdump, Decompilers) to understand their validation algorithms and extract the secret password.

- **Static and Dynamic Analysis:**
  - Inspection of symbol tables, character strings (`strings`), `.text` sections, and control flow of x86/x64 assembly instructions.
  - Step-by-step debugging under **GDB** with breakpoints, register analysis (`eax`, `rdi`, `rsp`), and dynamic memory inspection.
- **Source Code Reconstruction (`source.c`):**
  - Faithful reverse engineering translating low-level instructions into structured and functional C source code.
  - Documentation of the validation password for each difficulty level (`level1`, `level2`, ...).

---

### 05. `5-stockholm malware` — Ransomware Simulation & Encryption

> **Objective:** Design a program in a secure and airtight environment that simulates the behavior of modern ransomware (inspired by **WannaCry**), while implementing the corresponding remediation/decryption mechanism.

> [!CAUTION]
> This project is designed purely for educational purposes within a confined environment (VM/Docker). No malicious payload is propagated.

- **Targeting & Encryption:**
  - Targeted scanning restricted to the secure `~/infection/` directory.
  - Exclusive filtering for file extensions historically vulnerable and targeted by WannaCry (`.docx`, `.xlsx`, `.pdf`, `.zip`, etc.).
  - Strong symmetric encryption (AES / Libsodium / OpenSSL) with a key of at least 16 characters and file renaming with the `.ft` extension.
- **Reversibility (`stockholm -r <key>`):**
  - Full restoration mechanism validating the key and restoring the initial integrity of the data and their original extensions.
- **Options & Robustness:**
  - Execution flags: `-h` (help), `-v` (version), `-s` (silent mode).
  - Systematic handling of I/O errors to prevent any unexpected crashes.

---

### 06. `6-cyber iron dome` — HIDS & Real-Time Attack Detection

> **Objective:** Develop a Host-based Intrusion Detection System (**HIDS**) running under Linux as a background daemon, dedicated to the early detection of suspicious activities (e.g., beginning of ransomware encryption).

- **Strict System Constraints:**
  - Execution restricted to the superuser (`root`).
  - Capped memory footprint (RAM consumption strictly under **100 MB**).
  - Resilient operation as a background daemon (POSIX daemonization).
- **Heuristic Detection Vectors:**
  - **Disk Read/Write Abuse:** Detection of massive scans or unusual I/O bursts.
  - **Intensive Cryptographic Activity:** Correlating CPU load with heavy mathematical processing loops.
  - **Shannon Entropy Calculation:** Analyzing entropy variations of files in the monitored folder (the entropy of an encrypted file approaches 8, signaling a critical anomaly compared to plaintext).
- **Centralized Logging:**
  - Real-time logging of all security alerts in `/var/log/irondome/irondome.log`.

---

### 07. `7-inquisitor network` — Man-in-the-Middle (ARP Spoofing) & Sniffing

> **Objective:** Design a low-level network interceptor capable of hijacking traffic between two local targets via bidirectional ARP cache poisoning, and analyzing the application packets in transit.

- **Full-Duplex ARP Poisoning Attack:**
  - Emitting forged ARP frames via raw sockets to associate the attacker's MAC address with the source and target IP addresses (`<IP-src>`, `<MAC-src>`, `<IP-target>`, `<MAC-target>`).
  - Exclusive support for IPv4 with routing/forwarding management.
- **Clean Network Restoration:**
  - Intercepting shutdown signals (`SIGINT` / `CTRL+C`) with immediate re-emission of legitimate ARP frames to sanitize the victims' ARP tables (anti-Denial of Service).
- **Sniffing and Application Analysis (FTP Sniffer):**
  - Passive packet capture via **Libpcap**.
  - On-the-fly decoding of the unencrypted FTP protocol: real-time extraction of exchanged credentials and filenames.
- **Automated Test Lab:**
  - Deployment via Docker Compose simulating a client, an FTP server, and the attacker.

---

### 08. `8-vaccine web` — Automated SQL Injection Exploitation Engine

> **Objective:** Develop an autonomous audit and exploitation tool for **SQL Injection (SQLi)** vulnerabilities — similar to an engine like `sqlmap`, but developed without relying on pre-existing automation libraries.

- **HTTP Versatility & Targeting (`./vaccine [-oX] URL`):**
  - Native support for `GET` and `POST` HTTP methods (`-X`).
  - Structured saving of results in an audit archive file (`-o`).
- **Multi-Engine Detection & Fingerprinting:**
  - Identification of the target DBMS architecture (e.g., MySQL, SQLite, PostgreSQL, Oracle).
- **Payload Battery & Injection Techniques:**
  - **Union-based SQLi:** Data schema reconstruction via `UNION SELECT` queries.
  - **Error-based SQLi:** Exploitation of detailed error messages returned by the database.
  - **Boolean / Blind SQLi:** Bit-by-bit inference based on conditional responses (True/False).
  - **Time-based SQLi:** Deduction through time induction (`SLEEP()`, `benchmark()`).
- **Total Database Extraction:**
  - Automatic enumeration of database names, tables, columns, and comprehensive dumping of sensitive tables.

---

## 🛠️ Methodology & Best Practices

The projects in this repository were structured according to cybersecurity industry standards:

1. **Strict Environment Isolation:**
   - All attack simulations (MITM, Ransomware, SQLi) are confined within isolated virtual private networks (`docker-compose`, dedicated virtual machines).
2. **Code Hygiene & Performance:**
   - Rigorous management of memory and file descriptors (avoiding memory leaks, respecting resource limits).
   - Comprehensive handling of all exceptions and signals (`SIGINT`, `SIGTERM`) to leave targets and the host in an integral state.
3. **Compliance with Official Standards:**
   - Explicit references to RFCs (e.g., RFC 4226) and recognized frameworks (OWASP, MITRE ATT&CK).

---

## ⚖️ Legal Disclaimer

> [!WARNING]
> The source codes, scripts, and methodologies documented in this repository are designed and developed for **strictly educational and professional purposes**, as part of technical training for cybersecurity careers.
>
> Any use of these tools or techniques on third-party systems, networks, or applications without prior, explicit written authorization from the legal owner is illegal and punishable by law (notably under Articles 323-1 and following of the French Penal Code relating to offenses against automated data processing systems, and equivalent international laws).

---

## 📬 Contact & Profile

- **Author:** Antonin Bonin
- **Education:** Ecole 42 (Piscine & Cybersecurity Curriculum)
- **Objective:** Seeking an **Internship in Cybersecurity** (SOC Analyst, Pentester, Cyber Consultant, Application Security)
- **LinkedIn / GitHub:** *(insert links here)*