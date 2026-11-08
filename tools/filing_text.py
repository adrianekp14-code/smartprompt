"""Fetch an SEC filing (HTML) and print text windows around keywords.
python3 tools/filing_text.py URL kw1 kw2 ...  (window=700 chars, max 3 hits per keyword)"""
import sys, re, html, urllib.request, os, hashlib
UA = {"User-Agent": "EquityResearchAgent/1.0 research-bot"}
url = sys.argv[1]; kws = sys.argv[2:]
cache = os.path.join(os.path.dirname(__file__), "..", "data_cache", "filings"); os.makedirs(cache, exist_ok=True)
fn = os.path.join(cache, hashlib.md5(url.encode()).hexdigest() + ".txt")
if os.path.exists(fn): txt = open(fn).read()
else:
    raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read().decode("utf-8", "ignore")
    raw = re.sub(r"(?is)<(script|style|ix:header).*?</\1>", " ", raw)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw)); txt = re.sub(r"\s+", " ", txt)
    open(fn, "w").write(txt)
print("chars:", len(txt))
W = int(os.environ.get("W", 700)); N = int(os.environ.get("N", 3))
for k in kws:
    hits = [m.start() for m in re.finditer(re.escape(k), txt, re.I)][:N]
    for h in hits: print(f"\n[{k} @ {h}] ...{txt[max(0, h - 150):h + W]}...")
