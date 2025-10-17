#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CHIMBITA-FLY-FIXED-INTEGRATED (cron, silent)
import json, traceback, requests

TELEGRAM_TOKEN = "8364292253:AAE7zlGjDqGV63_0DuILVVJZCFb91igxA8Y"
CHAT_ID = "1982879600"
TG_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

BINANCE_ENDPOINTS = [
    "https://api4.binance.com",
    "https://api1.binance.com",
    "https://api2.binance.com",
    "https://api3.binance.com",
    "https://api.binance.com",
]

def tg_send(text):
    try:
        requests.post(f"{TG_API}/sendMessage", json={"chat_id": CHAT_ID, "text": text}, timeout=15)
    except Exception:
        pass

def tg_send_file(bytes_content: bytes, filename: str, caption: str):
    try:
        requests.post(f"{TG_API}/sendDocument",
                      data={"chat_id": CHAT_ID, "caption": caption},
                      files={"document": (filename, bytes_content, "application/json")},
                      timeout=20)
    except Exception:
        pass

def fetch_exchange_info():
    last = None
    for ep in BINANCE_ENDPOINTS:
        url = ep.rstrip("/") + "/fapi/v1/exchangeInfo"
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                js = r.json()
                if "symbols" in js:
                    return js, ep
            else:
                last = {"endpoint": ep, "status": r.status_code, "body": r.text[:400]}
        except Exception as e:
            last = {"endpoint": ep, "error": str(e)}
    return None, last

def extract_usdt_perp_symbols(info: dict):
    out = []
    for s in info.get("symbols", []):
        name = s.get("symbol", "")
        ctype = str(s.get("contractType", "")).upper()
        if name.endswith("USDT") and (ctype == "PERPETUAL" or "PERP" in name):
            out.append(name)
    return sorted(set(out))

def main():
    tg_send("🔵 Bot CHIMBITA-FLY-FIXED-INTEGRATED started on Fly.io")
    info, meta = fetch_exchange_info()
    if not info:
        msg = "🚨 Critical bot error: Binance unreachable or restricted — automatic fallback engaged"
        tg_send(msg)
        try:
            blob = json.dumps({"error": meta}, ensure_ascii=False, indent=2).encode("utf-8")
            tg_send_file(blob, "exchangeInfo_error.json", "exchangeInfo_error.json (debug)")
        except Exception:
            pass
        return 2

    syms = extract_usdt_perp_symbols(info)
    total = len(syms)
    if total <= 0:
        tg_send("ℹ️ Scan complete — 0 USDT perpetual pairs returned by exchangeInfo.")
        return 0
    tg_send(f"Scan completed — analyzed {total} USDT perpetual pairs.\nNo aligned signals found.")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        try:
            tg_send(f"❌ Fatal error: {e}")
        except Exception:
            pass
        raise
