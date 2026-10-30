# 🎃 PostMortem User Manual & Developer Field Guide

> **Cyber-Halloween Edition — Local Gemma Code Forensics & Anti-Hallucination Repair Studio**

## 1. What Is PostMortem?

In fast-moving software teams, developers frequently delete "unused" helper functions during cleanup commits—only to trigger a critical production bug weeks later. **PostMortem** is a local-first diagnostic system that lets you drop in any broken file or `git diff`, performs a deep **Gemma 3** forensic autopsy, blocks AI hallucinations with a 2-stage **Exorcism Shield**, and generates a verified, copy-ready fix patch.

## 2. Who Should Use It?

* **Software Engineers & Full-Stack Developers**: Quickly diagnose why a deleted or refactored function broke an edge case (billing, auth, concurrency) and get the exact restoration patch.
* **Pull Request Reviewers & Security Auditors**: Upload a `.diff` file before merging a PR to check if any critical safety guards were accidentally removed.
* **Privacy-Strict Engineering Teams**: Analyze proprietary code 100% locally in your browser or via local **Ollama (`gemma3:4b`)** with zero cloud API data leaks.

## 3. Step-by-Step: How to Use the Web Studio (`index.html`)

1. **Open `index.html`**: Double-click `index.html` to launch the studio in Chrome, Edge, or Firefox. Notice the workspace starts completely clean with zero preloaded clutter.
2. **Step 01 — Drop Your Code**:
   * Click the **📂 Upload Your File** dropzone to select any `.py`, `.js`, `.ts`, `.diff`, `.patch`, or `.go` file from your computer (or paste code into the editor).
   * *Want a 1-click test?* Click one of the optional pills (`⚡ Leap-Year Billing Bug`, `⚡ Auth HMAC Bypass`, or `⚡ Checkout Race Condition`).
   * Click **`🎃 Run Deep Forensic Autopsy ➔`**.
3. **Step 02 — Review the Deep Gemma Autopsy**:
   * **Indexed Ground-Truth Ledger (Left)**: Every line of your file is locked with an immutable `[TAG:L#]` coordinate.
   * **Forensic Diagnosis Report (Right)**: Shows the Target Symbol, Severity Score (`0–100`), Root Vulnerability, and Gemma's Root-Cause Analysis with clickable green `✓ [TAG:L#]` badges.
4. **Step 03 — Apply the Verified Fix & Ask Follow-Ups**:
   * Compare **❌ BEFORE (Vulnerable)** vs. **✅ AFTER (Hardened Solution Patch)** side by side.
   * Click **`▶ Verify Fix (Run 3 Checks)`** to validate the patch, then click **`📋 Copy Fix Patch`** or **`📄 Export (.md)`**.
   * Switch to **`💬 2. Ask Gemma About Your Code`** to ask custom follow-up questions with 100% verified line citations.

## 4. How the Anti-Hallucination "Exorcism Shield" Works

Small LLMs often guess wrong line numbers when reading code diffs. PostMortem eliminates hallucinations in two stages:

1. **Stage 1 (Deterministic AST Pre-Locking)**: Before Gemma sees your prompt, our parser numbers every real line (`[SHA:L1]`, `[SHA:L2]`) and formats the prompt using Gemma's native `<start_of_turn>user` instruction tokens.
2. **Stage 2 (Post-Generation Citation Verifier)**: Every `[SHA:L#]` tag in the response is cross-checked against the Ground-Truth Ledger. Any fabricated line number (e.g., `[SHA:L999]`) is immediately quarantined in neon red.
