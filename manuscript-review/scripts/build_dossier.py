#!/usr/bin/env python3
"""Build a self-contained HTML review dossier from a findings JSON file.

Pure standard library — runs in the claude.ai / Cowork code sandbox and any Python 3 env.
No external dependencies, no network, no external asset loads. The output opens offline.

Usage:
    python3 build_dossier.py findings.json -o manuscript-review-dossier.html

The findings JSON schema is documented in ../SKILL.md (Step 3). Every section is optional;
missing/empty sections are simply omitted from the dossier.
"""
import argparse
import html
import json
import sys

REC_CLASS = {
    "strong accept": "rec-accept", "weak accept": "rec-accept",
    "major revision": "rec-revise", "minor revision": "rec-revise",
    "weak reject": "rec-reject", "strong reject": "rec-reject",
}
SEV_CLASS = {"critical": "sev-critical", "major": "sev-major", "minor": "sev-minor"}
STATUS_BADGE = {
    "verified": ("✓", "st-ok"), "resolved": ("✓", "st-ok"),
    "misleading": ("⚠", "st-warn"), "partial": ("⚠", "st-warn"),
    "unverified": ("?", "st-unk"), "unchecked": ("?", "st-unk"),
    "false": ("✗", "st-bad"), "open": ("●", "st-bad"),
}


def e(x):
    """HTML-escape any value as text."""
    return html.escape("" if x is None else str(x))


def section(title, body):
    if not body:
        return ""
    return f'<section><h2>{e(title)}</h2>{body}</section>'


def render(f):
    meta = f.get("meta", {}) or {}
    parts = []

    # ---- header / meta ----
    title = meta.get("title") or "Manuscript Review"
    sub = []
    if meta.get("reviewed_on"):
        sub.append(f'Reviewed {e(meta["reviewed_on"])}')
    if meta.get("field_or_venue"):
        sub.append(e(meta["field_or_venue"]))
    header = f'<h1>{e(title)}</h1>'
    if sub:
        header += f'<p class="sub">{" · ".join(sub)}</p>'

    def chips(label, items, cls):
        if not items:
            return ""
        c = "".join(f'<span class="chip {cls}">{e(i)}</span>' for i in items)
        return f'<p class="chips"><b>{e(label)}:</b> {c}</p>'
    header += chips("Inputs", meta.get("inputs"), "chip-neutral")
    header += chips("Capabilities used", meta.get("capabilities_used"), "chip-ok")
    header += chips("Not performed", meta.get("capabilities_skipped"), "chip-warn")
    parts.append(f'<div class="head">{header}</div>')

    # ---- verdict ----
    v = f.get("verdict") or {}
    if v:
        rec = v.get("recommendation", "")
        cls = REC_CLASS.get(rec.strip().lower(), "rec-revise")
        conf = f' <span class="conf">confidence: {e(v.get("confidence"))}</span>' if v.get("confidence") else ""
        parts.append(
            f'<div class="verdict {cls}">'
            f'<div class="rec">{e(rec)}{conf}</div>'
            f'<p>{e(v.get("summary"))}</p></div>'
        )

    # ---- scorecard ----
    sc = f.get("scorecard") or []
    if sc:
        rows = ""
        for d in sc:
            score = d.get("score")
            mx = d.get("max", 10)
            pct = 0
            try:
                pct = max(0, min(100, round(100 * float(score) / float(mx))))
            except (TypeError, ValueError, ZeroDivisionError):
                pass
            rows += (
                f'<tr><td class="dim">{e(d.get("dimension"))}</td>'
                f'<td class="scorenum">{e(score)}/{e(mx)}</td>'
                f'<td class="bar"><span style="width:{pct}%"></span></td>'
                f'<td class="note">{e(d.get("note"))}</td></tr>'
            )
        parts.append(section("Scorecard", f'<table class="scorecard">{rows}</table>'))

    # ---- priority fixes ----
    pf = f.get("priority_fixes") or []
    if pf:
        items = ""
        for x in pf:
            sev = (x.get("severity") or "").lower()
            sc_cls = SEV_CLASS.get(sev, "sev-minor")
            rank = x.get("rank")
            rank_html = f'<span class="rank">#{e(rank)}</span>' if rank is not None else ""
            body = ""
            if x.get("what"):
                body += f'<p><b>What:</b> {e(x["what"])}</p>'
            if x.get("why"):
                body += f'<p><b>Why it matters:</b> {e(x["why"])}</p>'
            if x.get("fix"):
                body += f'<p class="fix"><b>Suggested fix:</b> {e(x["fix"])}</p>'
            items += (
                f'<div class="fix-card {sc_cls}">'
                f'<div class="fix-head">{rank_html}<span class="sev">{e(sev or "issue")}</span>'
                f'<span class="fix-title">{e(x.get("title"))}</span></div>{body}</div>'
            )
        parts.append(section("Priority fixes (ranked)", items))

    # ---- blockers checklist ----
    bl = f.get("blockers") or []
    if bl:
        rows = ""
        for b in bl:
            sym, cls = STATUS_BADGE.get((b.get("status") or "open").lower(), ("●", "st-bad"))
            rows += f'<li><span class="badge {cls}">{sym}</span> {e(b.get("item"))}' \
                    f' <span class="stat">({e(b.get("status") or "open")})</span></li>'
        parts.append(section("Blocker checklist", f'<ul class="checklist">{rows}</ul>'))

    # ---- reviewers ----
    rv = f.get("reviewers") or []
    if rv:
        cards = ""
        for r in rv:
            cards += (
                f'<div class="reviewer"><div class="rv-head">'
                f'<span class="rv-persona">{e(r.get("persona"))}</span>'
                f'<span class="rv-score">{e(r.get("score"))}/10</span></div>'
                f'<p>{e(r.get("review"))}</p></div>'
            )
        parts.append(section("Reviewer panel", cards))

    # ---- section findings ----
    sf = f.get("section_findings") or []
    if sf:
        blocks = ""
        for s in sf:
            lis = "".join(f'<li>{e(i)}</li>' for i in (s.get("findings") or []))
            blocks += f'<div class="secfind"><h3>{e(s.get("section"))}</h3><ul>{lis}</ul></div>'
        parts.append(section("Per-section findings", blocks))

    # ---- fact check ----
    fc = f.get("fact_check") or []
    if fc:
        rows = ""
        for c in fc:
            sym, cls = STATUS_BADGE.get((c.get("status") or "unverified").lower(), ("?", "st-unk"))
            src = c.get("source")
            src_html = e(src)
            if src and str(src).startswith(("http://", "https://")):
                src_html = f'<a href="{e(src)}">link</a>'
            rows += (
                f'<tr><td>{e(c.get("claim"))}</td><td class="loc">{e(c.get("location"))}</td>'
                f'<td><span class="badge {cls}">{sym}</span> {e(c.get("status"))}</td>'
                f'<td>{e(c.get("evidence"))}</td><td>{src_html}</td></tr>'
            )
        table = ('<table class="factcheck"><thead><tr><th>Claim</th><th>Location</th>'
                 '<th>Status</th><th>Evidence</th><th>Source</th></tr></thead>'
                 f'<tbody>{rows}</tbody></table>')
        parts.append(section("Fact-check & citation audit", table))

    # ---- rewrites ----
    rw = f.get("rewrites") or []
    if rw:
        cards = ""
        for i, r in enumerate(rw):
            why = f'<p class="rw-why">{e(r["why"])}</p>' if r.get("why") else ""
            cards += (
                f'<div class="rewrite"><div class="rw-loc">{e(r.get("location"))}</div>'
                f'<div class="rw-cols">'
                f'<div class="rw-orig"><span class="rw-tag">original</span>'
                f'<pre>{e(r.get("original"))}</pre></div>'
                f'<div class="rw-sug"><span class="rw-tag">suggested</span>'
                f'<button class="copy" data-i="{i}">copy</button>'
                f'<pre id="rw{i}">{e(r.get("suggested"))}</pre></div>'
                f'</div>{why}</div>'
            )
        parts.append(section("Suggested rewrites", cards))

    # ---- venues ----
    ve = f.get("venues") or []
    if ve:
        rows = ""
        for x in ve:
            rows += (
                f'<tr><td class="vrank">{e(x.get("rank"))}</td>'
                f'<td class="vname">{e(x.get("venue"))}</td>'
                f'<td>{e(x.get("why"))}</td><td class="vwatch">{e(x.get("watch_outs"))}</td></tr>'
            )
        table = ('<table class="venues"><thead><tr><th>#</th><th>Venue</th><th>Why</th>'
                 f'<th>Watch-outs</th></tr></thead><tbody>{rows}</tbody></table>')
        parts.append(section("Recommended venues", table))

    return "\n".join(p for p in parts if p)


def document(body):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Manuscript Review Dossier</title>
<style>
:root{{--bg:#fff;--fg:#1a1a1a;--muted:#666;--line:#e4e4e7;--card:#f7f7f8;--accent:#3b5bdb;
--ok:#2b8a3e;--warn:#e67700;--bad:#c92a2a;--unk:#868e96;}}
@media (prefers-color-scheme:dark){{:root{{--bg:#16181c;--fg:#e6e6e6;--muted:#9aa0a6;
--line:#2c2f36;--card:#1e2127;--accent:#748ffc;--ok:#51cf66;--warn:#ffa94d;--bad:#ff6b6b;--unk:#adb5bd;}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}}
.wrap{{max-width:960px;margin:0 auto;padding:32px 20px 80px}}
h1{{font-size:26px;margin:0 0 4px}} h2{{font-size:19px;margin:34px 0 12px;padding-bottom:6px;border-bottom:2px solid var(--line)}}
h3{{font-size:15px;margin:14px 0 6px}}
.sub{{color:var(--muted);margin:0 0 10px}}
.chips{{margin:6px 0;font-size:13px}} .chip{{display:inline-block;padding:2px 8px;border-radius:10px;margin:2px 3px;font-size:12px}}
.chip-neutral{{background:var(--card);color:var(--fg)}} .chip-ok{{background:rgba(43,138,62,.15);color:var(--ok)}}
.chip-warn{{background:rgba(230,119,0,.15);color:var(--warn)}}
.head{{border-bottom:1px solid var(--line);padding-bottom:12px}}
.verdict{{margin:18px 0;padding:16px 18px;border-radius:10px;border-left:5px solid var(--accent);background:var(--card)}}
.verdict .rec{{font-size:18px;font-weight:700}} .verdict .conf{{font-size:13px;font-weight:400;color:var(--muted)}}
.rec-accept{{border-left-color:var(--ok)}} .rec-revise{{border-left-color:var(--warn)}} .rec-reject{{border-left-color:var(--bad)}}
table{{width:100%;border-collapse:collapse;font-size:14px;margin:6px 0}}
th,td{{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}}
th{{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}}
.scorecard .dim{{font-weight:600;width:150px}} .scorecard .scorenum{{width:60px;font-variant-numeric:tabular-nums}}
.scorecard .bar{{width:160px}} .scorecard .bar span{{display:block;height:8px;border-radius:4px;background:var(--accent)}}
.fix-card{{background:var(--card);border-radius:9px;padding:12px 14px;margin:9px 0;border-left:4px solid var(--unk)}}
.sev-critical{{border-left-color:var(--bad)}} .sev-major{{border-left-color:var(--warn)}} .sev-minor{{border-left-color:var(--accent)}}
.fix-head{{display:flex;align-items:center;gap:8px;margin-bottom:4px}} .rank{{color:var(--muted);font-weight:700}}
.sev{{font-size:11px;text-transform:uppercase;letter-spacing:.05em;padding:2px 7px;border-radius:8px;background:rgba(0,0,0,.06)}}
@media (prefers-color-scheme:dark){{.sev{{background:rgba(255,255,255,.08)}}}}
.fix-title{{font-weight:600}} .fix-card p{{margin:3px 0}} .fix{{color:var(--ok)}}
.checklist{{list-style:none;padding:0}} .checklist li{{padding:4px 0}} .stat{{color:var(--muted);font-size:12px}}
.badge{{display:inline-block;width:18px;text-align:center;font-weight:700}}
.st-ok{{color:var(--ok)}} .st-warn{{color:var(--warn)}} .st-bad{{color:var(--bad)}} .st-unk{{color:var(--unk)}}
.reviewer{{background:var(--card);border-radius:9px;padding:12px 14px;margin:9px 0}}
.rv-head{{display:flex;justify-content:space-between;font-weight:600}} .rv-score{{color:var(--accent)}}
.secfind h3{{color:var(--accent)}} .loc{{color:var(--muted);white-space:nowrap}}
.rewrite{{border:1px solid var(--line);border-radius:9px;margin:10px 0;overflow:hidden}}
.rw-loc{{background:var(--card);padding:6px 12px;font-weight:600;font-size:13px}}
.rw-cols{{display:grid;grid-template-columns:1fr 1fr;gap:0}}
@media (max-width:640px){{.rw-cols{{grid-template-columns:1fr}}}}
.rw-orig,.rw-sug{{padding:10px 12px;position:relative}} .rw-orig{{border-right:1px solid var(--line)}}
.rw-tag{{font-size:11px;text-transform:uppercase;color:var(--muted)}}
.rewrite pre{{white-space:pre-wrap;margin:6px 0 0;font:13px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace}}
.copy{{position:absolute;top:8px;right:8px;font-size:11px;padding:2px 8px;border:1px solid var(--line);
border-radius:6px;background:var(--bg);color:var(--fg);cursor:pointer}}
.copy:active{{transform:scale(.96)}}
.venues .vrank{{width:32px;font-weight:700}} .vname{{font-weight:600}} .vwatch{{color:var(--muted)}}
a{{color:var(--accent)}}
footer{{margin-top:48px;padding-top:14px;border-top:1px solid var(--line);color:var(--muted);font-size:12px}}
</style></head>
<body><div class="wrap">
{body}
<footer>Generated by the <b>manuscript-review</b> skill · read-only review — the author's manuscript was not modified.</footer>
</div>
<script>
document.querySelectorAll('.copy').forEach(function(b){{
  b.addEventListener('click',function(){{
    var pre=document.getElementById('rw'+b.dataset.i); if(!pre)return;
    navigator.clipboard.writeText(pre.innerText).then(function(){{
      var t=b.textContent; b.textContent='copied'; setTimeout(function(){{b.textContent=t;}},1200);
    }});
  }});
}});
</script>
</body></html>"""


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build a self-contained HTML review dossier.")
    ap.add_argument("findings", help="Path to the findings JSON file.")
    ap.add_argument("-o", "--output", default="manuscript-review-dossier.html",
                    help="Output HTML path (default: manuscript-review-dossier.html).")
    args = ap.parse_args(argv)

    try:
        with open(args.findings, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as err:
        print(f"error: could not read findings JSON: {err}", file=sys.stderr)
        return 1

    with open(args.output, "w", encoding="utf-8") as out:
        out.write(document(render(data)))
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
