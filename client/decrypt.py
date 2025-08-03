#!/usr/bin/env python3
import argparse, base64, sys, json, os
# Импорт из соседней папки proxy
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from crypto import decrypt

def main():
    ap = argparse.ArgumentParser(description="PrivAnalyticsDB decryptor")
    ap.add_argument("--in", dest="infile", default="-", help="JSON с encrypted_data")
    ap.add_argument("--out", default="-", help="Output file (- = stdout)")
    args = ap.parse_args()

    inf = sys.stdin if args.infile == "-" else open(args.infile)
    outf = sys.stdout if args.out == "-" else open(args.out, "w")

    data = inf.read().strip()
    payload = json.loads(data)
    key_id = payload["key_id"]
    iv = base64.b64decode(payload["iv"])
    ct = base64.b64decode(payload["encrypted_data"])

    plain = decrypt(key_id, iv, ct)
    outf.write(plain.decode())
    outf.flush()

if __name__ == "__main__":
    main()
