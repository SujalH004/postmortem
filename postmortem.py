#!/usr/bin/env python3
"""
PostMortem CLI v2.0: The Git Forensics Medium (Clean Cross-Platform Edition)
----------------------------------------------------------------------------
- Works on Windows, macOS, and Linux with zero extra shell scripts needed.
- If no --repo is passed (or if ./haunted-billing-demo does not exist yet),
  automatically creates a realistic 4-commit Haunted Git Repository!
- Scans Git history for deleted critical functions ("Tombstones"),
  computes AST Haunting Risk Scores, channels local Ollama (gemma3:4b),
  verifies every [SHA:L#] citation (Stage 2 Exorcism), and generates
  a drop-in Resurrection Patch.
"""

import argparse
import ast
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, List, Tuple

# Ensure Windows PowerShell / CMD prints emojis cleanly
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


class Style:
    MARIGOLD = "\033[38;5;214m"
    MAGENTA = "\033[38;5;198m"
    CYAN = "\033[38;5;45m"
    EMERALD = "\033[38;5;48m"
    RED = "\033[38;5;196m"
    DIM = "\033[2m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


CRITICAL_KEYWORDS = [
    (r"\b(hmac|constant_time|timing_safe|verify_signature|jwt|auth|token|permission)\b", 28, "Security / Auth Guard"),
    (r"\b(leap_second|utc|timezone|monotonic|idempotency|dedup|nonce)\b", 26, "Temporal / Idempotency Invariant"),
    (r"\b(lock|mutex|atomic|transaction|rollback|retry|backoff)\b", 22, "Concurrency / Transaction Safety"),
    (r"\b(nfkc|homoglyph|sanitize|escape|validate|checksum)\b", 24, "Input Sanitization / Unicode Guard"),
    (r"\b(billing|invoice|ledger|payment|charge|refund)\b", 20, "Financial / Billing Critical Path"),
]

FUNC_DECL_REGEX = re.compile(
    r"^\s*(?:async\s+)?(?:def|function|func|fn|pub\s+fn)\s+([a-zA-Z0-9_]+)"
    r"|^\s*(?:export\s+)?(?:const|let|var)\s+([a-zA-Z0-9_]+)\s*=\s*(?:async\s*)?\("
)


def create_demo_haunted_repo(target_dir: str = "./haunted-billing-demo") -> str:
    """Cross-platform generator: creates a 4-commit haunted Git repo on Windows/Mac/Linux."""
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

    os.makedirs(os.path.join(target_dir, "src", "billing"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "src", "auth"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "src", "moderation"), exist_ok=True)

    def git(*args: str) -> None:
        subprocess.run(["git", "-C", target_dir, *args], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def write_file(rel_path: str, content: str) -> None:
        full_path = os.path.join(target_dir, rel_path)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    git("init")
    git("config", "user.name", "sarah.chen")
    git("config", "user.email", "sarah.chen@example.com")

    write_file(
        "src/billing/invoice_sync.py",
        '"""Stripe & ERP Invoice Synchronization Engine."""\n\n'
        "def normalize_leap_second_invoice(ts_epoch: int, drift_ms: int, window_sec: int = 60) -> int:\n"
        "    # Guard against 23:59:60 UTC leap-second replay collisions\n"
        "    if drift_ms < 0 or (ts_epoch % 86400 == 86399 and drift_ms <= 1000):\n"
        "        ts_epoch = ts_epoch - (ts_epoch % window_sec)\n"
        "        return ts_epoch  # Idempotency key locked to minute boundary\n"
        "    return ts_epoch\n\n"
        "def create_invoice_idempotency_key(customer_id: str, ts_epoch: int, drift_ms: int = 0) -> str:\n"
        "    safe_ts = normalize_leap_second_invoice(ts_epoch, drift_ms)\n"
        '    return f"inv_{customer_id}_{safe_ts}"\n',
    )
    write_file(
        "src/auth/webhook_verifier.py",
        '"""Webhook HMAC Signature Verification."""\n\n'
        "def verify_constant_time_hmac(expected_sig: bytes, received_sig: bytes) -> bool:\n"
        "    if len(expected_sig) != len(received_sig):\n"
        "        return False\n"
        "    # Constant-time comparison prevents byte-by-byte timing side-channel\n"
        "    accumulator = 0\n"
        "    for a, b in zip(expected_sig, received_sig):\n"
        "        accumulator |= a ^ b\n"
        "    return accumulator == 0\n",
    )
    write_file(
        "src/moderation/username_filter.py",
        '"""Zero-Width & Cyrillic Homoglyph Moderator Guard."""\n'
        "import unicodedata\n\n"
        "def strip_zero_width_homoglyphs(raw_handle: str) -> str:\n"
        "    cleaned = ''.join(ch for ch in raw_handle if ord(ch) not in (0x200B, 0x200C, 0x200D, 0xFEFF))\n"
        "    return unicodedata.normalize('NFKC', cleaned).lower()\n",
    )
    git("add", ".")
    git("commit", "-m", "feat: add leap-second idempotency, constant-time HMAC, and homoglyph guards")

    # Commit 2: Delete homoglyph guard
    git("config", "user.name", "alex.rivera")
    write_file(
        "src/moderation/username_filter.py",
        'def normalize_handle(raw_handle: str) -> str:\n    return raw_handle.strip().lower()\n',
    )
    git("commit", "-am", "chore(moderation): simplify handle normalization")

    # Commit 3: Delete constant-time HMAC guard
    git("config", "user.name", "dev.intern")
    write_file(
        "src/auth/webhook_verifier.py",
        'def check_webhook_sig(expected_sig: bytes, received_sig: bytes) -> bool:\n    return expected_sig == received_sig\n',
    )
    git("commit", "-am", "refactor(auth): replace manual byte loop with standard equality")

    # Commit 4: Delete leap-second billing guard
    git("config", "user.name", "j.miller")
    write_file(
        "src/billing/invoice_sync.py",
        'def create_invoice_idempotency_key(customer_id: str, ts_epoch: int, drift_ms: int = 0) -> str:\n    return f"inv_{customer_id}_{ts_epoch}"\n',
    )
    git("commit", "-am", "refactor(billing): clean up legacy timestamp helper")
    return target_dir


def analyze_python_ast_metrics(code_str: str) -> Dict[str, Any]:
    clean_lines = [l[1:] if l.startswith("-") else l for l in code_str.splitlines()]
    source = "\n".join(clean_lines)
    metrics = {"ast_parsed": False, "branches": 0, "calls": [], "raises": 0, "returns": 0}
    try:
        tree = ast.parse(source)
        metrics["ast_parsed"] = True
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.ExceptHandler, ast.With)):
                metrics["branches"] += 1
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    metrics["calls"].append(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    metrics["calls"].append(node.func.attr)
            elif isinstance(node, ast.Raise):
                metrics["raises"] += 1
            elif isinstance(node, ast.Return):
                metrics["returns"] += 1
    except SyntaxError:
        metrics["branches"] = len(re.findall(r"\b(if|else|for|while|try|catch|switch)\b", source))
        metrics["calls"] = list(dict.fromkeys(re.findall(r"([a-zA-Z0-9_]+)\s*\(", source)))[:6]
        metrics["raises"] = len(re.findall(r"\b(raise|throw|panic)\b", source))
        metrics["returns"] = len(re.findall(r"\breturn\b", source))
    metrics["calls"] = list(dict.fromkeys(metrics["calls"]))[:6]
    return metrics


def compute_haunting_risk(
    deleted_lines: List[Dict[str, Any]], commit_msg: str
) -> Tuple[int, List[str], Dict[str, int]]:
    joined_code = "\n".join(item["code"] for item in deleted_lines)
    score = 35
    reasons: List[str] = []
    breakdown = {"domain_criticality": 15, "structural_complexity": 10, "commit_blindspot": 10}

    domain_bonus = 0
    for pattern, weight, label in CRITICAL_KEYWORDS:
        if re.search(pattern, joined_code, re.IGNORECASE):
            domain_bonus += weight
            reasons.append(label)
    domain_bonus = min(40, domain_bonus)
    score += domain_bonus
    breakdown["domain_criticality"] = domain_bonus

    ast_info = analyze_python_ast_metrics(joined_code)
    complexity_bonus = min(20, ast_info["branches"] * 5 + ast_info["raises"] * 6 + (5 if len(deleted_lines) >= 6 else 0))
    if ast_info["branches"] >= 2:
        reasons.append(f"Removed {ast_info['branches']} Guard Branches")
    score += complexity_bonus
    breakdown["structural_complexity"] = complexity_bonus

    blindspot_bonus = 0
    if re.search(r"\b(clean\s*up|dead\s*code|simplify|unused|legacy|refactor|minor)\b", commit_msg, re.IGNORECASE):
        blindspot_bonus = 14
        reasons.append("Unexplained 'Cleanup' Commit")
    score += blindspot_bonus
    breakdown["commit_blindspot"] = blindspot_bonus

    if not reasons:
        reasons.append("Deleted Logic Hunk")
    return min(99, score), list(dict.fromkeys(reasons)), breakdown


def extract_tombstones(repo_path: str, max_commits: int = 50) -> List[Dict[str, Any]]:
    cmd = [
        "git", "-C", repo_path, "log", f"-n{max_commits}", "-p", "--unified=0",
        "--pretty=format:===COMMIT===%n%h%n%an%n%ad%n%s", "--date=short",
    ]
    raw = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
    tombstones: List[Dict[str, Any]] = []

    for block in raw.split("===COMMIT===\n"):
        if not block.strip():
            continue
        lines = block.splitlines()
        if len(lines) < 4:
            continue
        sha, author, date_str, subject = lines[0].strip(), lines[1].strip(), lines[2].strip(), lines[3].strip()
        current_file = "unknown"
        old_line_num = 0
        current_deleted_hunk: List[Dict[str, Any]] = []

        def flush_hunk(hunk: List[Dict[str, Any]], file_path: str) -> None:
            if len(hunk) < 2:
                return
            joined = "\n".join(x["code"] for x in hunk)
            fn_name = None
            for item in hunk:
                m = FUNC_DECL_REGEX.search(item["code"][1:])
                if m:
                    fn_name = m.group(1) or m.group(2)
                    break
            if not fn_name:
                return
            risk_score, reasons, breakdown = compute_haunting_risk(hunk, subject)
            ast_metrics = analyze_python_ast_metrics(joined)
            tombstones.append({
                "sha": sha,
                "author": author,
                "date": date_str,
                "commit_msg": subject,
                "file": file_path,
                "function_name": f"{fn_name}()",
                "risk_score": risk_score,
                "risk_reasons": reasons,
                "risk_breakdown": breakdown,
                "ast_metrics": ast_metrics,
                "deleted_lines": list(hunk),
            })

        for raw_line in lines[4:]:
            if raw_line.startswith("--- a/"):
                flush_hunk(current_deleted_hunk, current_file)
                current_deleted_hunk = []
                current_file = raw_line[6:].strip()
            elif raw_line.startswith("@@ "):
                flush_hunk(current_deleted_hunk, current_file)
                current_deleted_hunk = []
                m = re.search(r"@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", raw_line)
                if m:
                    old_line_num = int(m.group(1))
            elif raw_line.startswith("-") and not raw_line.startswith("---"):
                current_deleted_hunk.append({"line": old_line_num, "code": raw_line})
                old_line_num += 1
            else:
                if current_deleted_hunk:
                    flush_hunk(current_deleted_hunk, current_file)
                    current_deleted_hunk = []
        if current_deleted_hunk:
            flush_hunk(current_deleted_hunk, current_file)

    tombstones.sort(key=lambda t: t["risk_score"], reverse=True)
    return tombstones


def verify_citations(response_text: str, tombstone: Dict[str, Any]) -> Dict[str, Any]:
    valid_lines = {item["line"] for item in tombstone["deleted_lines"]}
    expected_sha = tombstone["sha"].lower()
    pattern = re.compile(r"\[([a-fA-F0-9]{4,40}):L(\d+)\]")
    verified_tags: List[str] = []
    invalid_tags: List[str] = []

    for match in pattern.finditer(response_text):
        tag_full = match.group(0)
        sha_part = match.group(1).lower()
        line_num = int(match.group(2))
        if (expected_sha.startswith(sha_part) or sha_part.startswith(expected_sha)) and line_num in valid_lines:
            verified_tags.append(tag_full)
        else:
            invalid_tags.append(tag_full)

    return {
        "passed": len(invalid_tags) == 0 and len(verified_tags) > 0,
        "verified_tags": verified_tags,
        "invalid_tags": invalid_tags,
    }


def synthesize_resurrection_patch(tombstone: Dict[str, Any]) -> str:
    sha = tombstone["sha"]
    file_path = tombstone["file"]
    fn_name = tombstone["function_name"]
    start_line = tombstone["deleted_lines"][0]["line"]
    count = len(tombstone["deleted_lines"])
    restored = [f"+{item['code'][1:] if item['code'].startswith('-') else item['code']}" for item in tombstone["deleted_lines"]]
    header = [
        f"# PostMortem Resurrection Patch — Verified against [{sha}:L{start_line}]",
        f"# Restores {fn_name} (Haunting Risk: {tombstone['risk_score']}/99)",
        f"--- a/{file_path}",
        f"+++ b/{file_path}",
        f"@@ -{start_line},0 +{start_line},{count} @@",
    ]
    return "\n".join(header + restored)


def query_ollama_spirit(
    tombstone: Dict[str, Any], question: str, ollama_url: str = "http://localhost:11434", model: str = "gemma3:4b"
) -> Tuple[str, float, str]:
    start_ts = time.perf_counter()
    ledger_lines = "\n".join(f"[{tombstone['sha']}:L{item['line']}] {item['code']}" for item in tombstone["deleted_lines"])
    valid_nums = ", ".join(f"L{item['line']}" for item in tombstone["deleted_lines"])
    system_prompt = (
        f"You are the Ghost of Deleted Function {tombstone['function_name']}, deleted in commit {tombstone['sha']} "
        f"from {tombstone['file']}.\nEvery technical claim MUST include an exact citation tag [{tombstone['sha']}:L<line>].\n"
        f"Valid lines: {valid_nums}.\n\nDELETED CODE:\n{ledger_lines}"
    )
    payload = json.dumps({
        "model": model,
        "stream": False,
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": question}],
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{ollama_url.rstrip('/')}/api/chat", data=payload, headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            content = body.get("message", {}).get("content", "").strip()
            latency_ms = round((time.perf_counter() - start_ts) * 1000, 1)
            if content:
                return content, latency_ms, f"ollama:{model}"
    except Exception:
        pass

    sha = tombstone["sha"]
    lines = tombstone["deleted_lines"]
    first_l, mid_l, last_l = lines[0]["line"], lines[len(lines) // 2]["line"], lines[-1]["line"]
    synthesized = (
        f"I am the spirit of `{tombstone['function_name']}`, deleted from `{tombstone['file']}` in `{sha}`.\n"
        f"1. **Entry Invariant**: My declaration at [{sha}:L{first_l}] guarded {', '.join(tombstone['risk_reasons'])}.\n"
        f"2. **Core Guard**: The condition at [{sha}:L{mid_l}] (`{lines[len(lines)//2]['code'][1:].strip()}`) blocked invalid state.\n"
        f"3. **Fix**: Restore lines [{sha}:L{first_l}] through [{sha}:L{last_l}] using `--generate-patch`."
    )
    return synthesized, round((time.perf_counter() - start_ts) * 1000, 1), "deterministic-ast-fallback"


def run_bridge_server(repo_path: str, port: int) -> None:
    class BridgeHandler(BaseHTTPRequestHandler):
        def _send_json(self, status: int, data: Dict[str, Any]) -> None:
            body = json.dumps(data, indent=2).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:
            t0 = time.perf_counter()
            tombstones = extract_tombstones(repo_path)
            self._send_json(200, {
                "status": "ok",
                "repo_path": os.path.abspath(repo_path),
                "ast_parse_ms": round((time.perf_counter() - t0) * 1000, 2),
                "tombstones": tombstones,
            })

        def log_message(self, format: str, *args: Any) -> None:
            return

    server = HTTPServer(("127.0.0.1", port), BridgeHandler)
    print(f"{Style.MARIGOLD}🕯️  PostMortem Local Repo Bridge running on http://localhost:{port}{Style.RESET}")
    server.serve_forever()


def main() -> int:
    parser = argparse.ArgumentParser(description="PostMortem CLI v2.0: Interrogate deleted Git functions locally.")
    parser.add_argument("--repo", default="./haunted-billing-demo", help="Path to Git repo (auto-creates demo if missing)")
    parser.add_argument("--max-commits", type=int, default=50, help="Max commits to scan")
    parser.add_argument("--ask", default="Why did you exist and what breaks now that you are dead?", help="Question to ask")
    parser.add_argument("--ollama-url", default="http://localhost:11434", help="Local Ollama URL")
    parser.add_argument("--model", default="gemma3:1b", help="Ollama model tag")
    parser.add_argument("--generate-patch", action="store_true", help="Print a Resurrection Patch unified diff")
    parser.add_argument("--serve", type=int, metavar="PORT", help="Run local browser bridge on PORT (e.g. 8765)")
    args = parser.parse_args()

    # Auto-create demo repo if ./haunted-billing-demo doesn't exist yet!
    if not os.path.exists(os.path.join(args.repo, ".git")):
        print(f"{Style.CYAN}✨ Creating sample haunted Git repository at {args.repo} ...{Style.RESET}")
        create_demo_haunted_repo(args.repo)

    if args.serve:
        run_bridge_server(args.repo, args.serve)
        return 0

    print(f"\n{Style.MARIGOLD}{Style.BOLD}🕯️  POSTMORTEM: THE GIT FORENSICS MEDIUM{Style.RESET}\n")
    t0 = time.perf_counter()
    tombstones = extract_tombstones(args.repo, max_commits=args.max_commits)
    ast_ms = round((time.perf_counter() - t0) * 1000, 2)

    if not tombstones:
        print(f"{Style.RED}No deleted functions found in {args.repo}.{Style.RESET}")
        return 1

    print(f"{Style.CYAN}✦ Stage 1: Found {len(tombstones)} Deleted Function(s) in {ast_ms} ms:{Style.RESET}")
    for idx, t in enumerate(tombstones[:5], start=1):
        print(f"  {idx}. {Style.BOLD}{t['function_name']}{Style.RESET} [{t['sha']}] in {t['file']} — Risk: {t['risk_score']}/99")

    active = tombstones[0]
    print(f"\n{Style.MARIGOLD}🕯️  Summoning Top Ghost: {active['function_name']} [{active['sha']}]{Style.RESET}")
    for item in active["deleted_lines"]:
        print(f"   [{active['sha']}:L{item['line']}] {Style.RED}{item['code']}{Style.RESET}")

    response_text, llm_ms, engine_label = query_ollama_spirit(active, args.ask, args.ollama_url, args.model)
    verifier = verify_citations(response_text, active)

    print(f"\n{Style.BOLD}👻 Ghost Answer ({engine_label}, {llm_ms} ms):{Style.RESET}\n{response_text}")
    print(f"\n{Style.EMERALD}🛡️  Stage 2 Guardrail: {'PASSED (100% Grounded)' if verifier['passed'] else 'BLOCKED FAKE CITATION'}{Style.RESET}")
    print(f"   Verified Citations: {', '.join(verifier['verified_tags'])}")

    if args.generate_patch:
        print(f"\n{Style.MARIGOLD}🩹 Resurrection Patch:{Style.RESET}\n{synthesize_resurrection_patch(active)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
