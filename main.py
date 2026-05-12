#!/usr/bin/env python3
import argparse
import os
import subprocess
import shutil

# Paths
CERT_DIR = "/etc/letsencrypt/live"
NGINX_CONF_DIR = "/etc/nginx"

def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Remove and revoke unused Let's Encrypt certificates."
    )
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Force deletion without confirmation"
    )
    return parser.parse_args()

def get_all_domains_from_nginx_configs():
    """
    Reads all nginx configuration files and extracts domain mentions.
    Returns a set of found domain strings.
    """
    domains = set()
    for root, _, files in os.walk(NGINX_CONF_DIR):
        for file in files:
            if file.endswith(".conf"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        domains.update(find_domains_in_text(content))
                except Exception as e:
                    print(f"Warning: Failed to read {filepath}: {e}")
    return domains

def find_domains_in_text(text):
    """
    Returns a set of domain-like strings found in the text.
    """
    import re
    return set(re.findall(r'\b(?:[a-z0-9-]+\.)+[a-z]{2,}\b', text, flags=re.IGNORECASE))

def get_cert_domains(cert_path):
    """
    Uses openssl to extract domain names from the certificate.
    Returns a list of domain names.
    """
    try:
        output = subprocess.check_output(
            ["openssl", "x509", "-in", os.path.join(cert_path, "cert.pem"), "-noout", "-text"],
            stderr=subprocess.DEVNULL
        ).decode("utf-8")
    except subprocess.CalledProcessError:
        return []

    import re
    matches = re.findall(r'DNS:([a-zA-Z0-9.-]+)', output)
    return matches

def revoke_and_delete_certificate(cert_name):
    """
    Revokes and deletes the given certificate.
    """
    cert_path = os.path.join(CERT_DIR, cert_name)
    print(f"Revoking certificate for {cert_name}...")
    try:
        subprocess.run(
            ["certbot", "revoke", "--cert-path", os.path.join(cert_path, "cert.pem"), "--non-interactive", "--quiet", "--delete-after-revoke"],
            check=True
        )
        print(f"Revoked certificate: {cert_name}")
    except subprocess.CalledProcessError:
        print(f"Failed to revoke certificate: {cert_name}")

    print(f"Deleting directory {cert_path}...")
    try:
        shutil.rmtree(cert_path)
        print(f"Deleted certificate directory: {cert_path}")
    except Exception as e:
        print(f"Failed to delete {cert_path}: {e}")

def main():
    args = parse_arguments()
    used_domains = get_all_domains_from_nginx_configs()

    for cert_name in os.listdir(CERT_DIR):
        cert_path = os.path.join(CERT_DIR, cert_name)
        if not os.path.isdir(cert_path):
            continue

        domains = get_cert_domains(cert_path)
        if not domains:
            continue

        if any(domain in used_domains for domain in domains):
            continue  # Certificate is still in use

        print(f"Unused certificate: {cert_name} ({', '.join(domains)})")
        if args.force:
            revoke_and_delete_certificate(cert_name)
        else:
            answer = input(f"Do you want to revoke and delete this certificate? [y/N]: ").strip().lower()
            if answer == 'y':
                revoke_and_delete_certificate(cert_name)
            else:
                print("Skipped.")

if __name__ == "__main__":
    main()
