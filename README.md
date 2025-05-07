# ☠️ Certbot Reaper

**Certbot Reaper** is a Python utility that finds, revokes, and deletes unused Let's Encrypt certificates from your system – so you stay clean and secure. It compares existing certificates with active NGINX configurations and safely removes those that are no longer in use.

---

## 🚀 Features

- 🔍 Scans `/etc/letsencrypt/live` for all installed certificates
- 🧠 Checks if domain names are referenced in NGINX configs under `/etc/nginx/`
- 🗑️ Offers interactive or forced cleanup of unused certificates
- 🔁 Can be run manually or scheduled with `systemd` timers
- ⚙️ Supports `--force` and `--help` via `argparse`

---

## 📦 Installation

Install using **Kevin's Package Manager** [`pkgmgr`](https://github.com/kevinveenbirkenbach/package-manager):

```bash
pkgmgr install certreap
````

---

## 🛠️ Usage

```bash
certreap               # Interactive mode (asks before deleting)
certreap --force       # Deletes unused certificates without confirmation
certreap --help        # Shows help message
```

---

## 👤 Author

Developed by [Kevin Veen-Birkenbach](https://www.veen.world) 🧠
Feedback and contributions welcome!

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
Feel free to use, modify, and share it as you wish.
