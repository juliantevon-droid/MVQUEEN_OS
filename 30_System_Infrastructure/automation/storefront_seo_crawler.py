#!/usr/bin/env python3
"""Bounded, read-only SEO audit of MVQUEEN public Shopify sitemap pages.

No login, crawler signature, Shopify Admin API, or storefront mutation is used.
Findings are informational; runtime/access failures cause a nonzero exit code.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import time
from urllib import error, parse, request, robotparser
from xml.etree import ElementTree

STORE = "https://tsucu0-1i.myshopify.com"
AGENT = "MVQUEEN-Site-Audit/1.0"
MAX_BYTES = 2_000_000
MAX_SITEMAPS = 20
PAGE_PATH = re.compile(r"^/(?:products|collections|pages|blogs)/[^/]+")


def approved_url(value: str, *, sitemap: bool = False) -> str:
    parsed = parse.urlsplit(value)
    if parsed.scheme != "https" or parsed.hostname != parse.urlsplit(STORE).hostname or parsed.port is not None or parsed.username or parsed.password:
        raise ValueError("off-store or non-HTTPS URL")
    if sitemap and not parsed.path.startswith("/sitemap"):
        raise ValueError("invalid sitemap path")
    if not sitemap and not (parsed.path in ("/", "/robots.txt") or PAGE_PATH.match(parsed.path)):
        raise ValueError("not a storefront content page")
    return parse.urlunsplit(("https", parsed.netloc, parsed.path or "/", parsed.query if sitemap else "", ""))


class SameStoreRedirects(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if parse.urlsplit(newurl).hostname != parse.urlsplit(STORE).hostname or parse.urlsplit(newurl).scheme != "https":
            raise ValueError("cross-domain redirect blocked")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


OPENER = request.build_opener(SameStoreRedirects)


def download(url: str, *, sitemap: bool = False) -> tuple[int, str, bytes]:
    approved_url(url, sitemap=sitemap)
    req = request.Request(url, headers={"User-Agent": AGENT, "Accept": "text/html,application/xml,text/xml;q=0.9,*/*;q=0.5"})
    try:
        with OPENER.open(req, timeout=15) as response:
            final_url = response.geturl()
            approved_url(final_url, sitemap=sitemap)
            data = response.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                raise ValueError("response too large")
            return response.status, response.headers.get("Content-Type", ""), data
    except error.HTTPError as exc:
        return exc.code, exc.headers.get("Content-Type", ""), b""


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.title = ""
        self.description = ""
        self.robots = ""
        self.canonical = ""
        self.h1_count = 0
        self.missing_alt = 0
        self.images = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.h1_count += 1
        if tag == "img":
            self.images += 1
            if "alt" not in attrs:  # alt="" is valid for decorative images
                self.missing_alt += 1
        if tag == "meta":
            name = (attrs.get("name") or "").lower()
            if name == "description":
                self.description = attrs.get("content") or ""
            if name == "robots":
                self.robots = (attrs.get("content") or "").lower()
        if tag == "link" and "canonical" in (attrs.get("rel") or "").lower().split():
            self.canonical = attrs.get("href") or ""

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def assess(url: str, body: bytes) -> dict:
    page = Page()
    page.feed(body.decode("utf-8", errors="replace"))
    issues = []
    if not page.title.strip():
        issues.append("missing_title")
    elif len(page.title.strip()) > 65:
        issues.append("long_title")
    if not page.description.strip():
        issues.append("missing_meta_description")
    elif not 50 <= len(page.description.strip()) <= 165:
        issues.append("description_length_review")
    if page.h1_count != 1:
        issues.append("h1_count_review")
    if not page.canonical:
        issues.append("missing_canonical")
    else:
        try:
            target = approved_url(parse.urljoin(url, page.canonical))
            if target != url:
                issues.append("canonical_mismatch_review")
        except ValueError:
            issues.append("canonical_external_or_invalid")
    if "noindex" in page.robots:
        issues.append("noindex_review")
    if page.missing_alt:
        issues.append("image_alt_missing")
    return {"url": url, "status": 200, "title": page.title.strip(), "issues": issues,
            "h1_count": page.h1_count, "images": page.images, "images_missing_alt": page.missing_alt}


def sitemap_pages(robots: robotparser.RobotFileParser, *, max_pages: int) -> list[str]:
    pending = [f"{STORE}/sitemap.xml"]
    visited = set()
    pages = []
    seen_pages = set()
    while pending and len(visited) < MAX_SITEMAPS and len(pages) < max_pages:
        url = approved_url(pending.pop(0), sitemap=True)
        if url in visited:
            continue
        visited.add(url)
        if not robots.can_fetch(AGENT, url):
            raise RuntimeError("robots.txt disallows sitemap access")
        status, _, data = download(url, sitemap=True)
        if status != 200:
            raise RuntimeError(f"sitemap fetch status {status}: {url}")
        try:
            root = ElementTree.fromstring(data)
        except ElementTree.ParseError as exc:
            raise RuntimeError(f"unparseable sitemap: {url}") from exc
        children = [(node.text or "").strip() for node in root.iter() if node.tag.rsplit("}", 1)[-1] == "loc"]
        if root.tag.rsplit("}", 1)[-1] == "sitemapindex":
            for child in children:
                try:
                    sub = approved_url(child, sitemap=True)
                except ValueError:
                    continue
                if sub not in visited and sub not in pending:
                    pending.append(sub)
        elif root.tag.rsplit("}", 1)[-1] == "urlset":
            for child in children:
                try:
                    candidate = approved_url(child)
                except ValueError:
                    continue
                if candidate not in seen_pages and robots.can_fetch(AGENT, candidate):
                    seen_pages.add(candidate)
                    pages.append(candidate)
                    if len(pages) >= max_pages:
                        break
        else:
            raise RuntimeError(f"unknown sitemap root: {url}")
    if pending and len(visited) >= MAX_SITEMAPS:
        raise RuntimeError("sitemap limit reached before traversal completed")
    return pages


def run(max_pages: int, delay: float) -> dict:
    robots_url = f"{STORE}/robots.txt"
    status, _, text = download(robots_url)
    if status != 200:
        raise RuntimeError(f"robots.txt unavailable (HTTP {status}); declining to crawl")
    robots = robotparser.RobotFileParser()
    robots.set_url(robots_url)
    robots.parse(text.decode("utf-8", errors="replace").splitlines())
    if not robots.can_fetch(AGENT, f"{STORE}/sitemap.xml"):
        raise RuntimeError("robots.txt disallows sitemap access")
    urls = sitemap_pages(robots, max_pages=max_pages)
    if not urls:
        raise RuntimeError("no permitted Shopify content pages found in sitemap")
    findings = []
    for url in urls:
        try:
            status, kind, body = download(url)
            if status != 200 or "html" not in kind.lower():
                findings.append({"url": url, "status": status, "issues": ["unavailable_or_not_html"]})
            elif b'type="password"' in body[:15000] and b'name="password"' in body[:15000]:
                findings.append({"url": url, "status": 200, "issues": ["password_page_review"]})
            else:
                findings.append(assess(url, body))
        except (error.URLError, ValueError, TimeoutError) as exc:
            findings.append({"url": url, "status": None, "issues": ["fetch_failed"], "reason": str(exc)[:150]})
        time.sleep(delay)
    count = Counter(issue for page in findings for issue in page["issues"])
    return {"store": STORE, "checked_at": datetime.now(timezone.utc).isoformat(),
            "pages_checked": len(findings), "max_pages": max_pages,
            "findings_by_type": dict(sorted(count.items())), "pages": findings,
            "note": "Read-only sample capped by max-pages; SEO findings are review suggestions, not automatic content changes."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-pages", type=int, default=200)
    parser.add_argument("--delay", type=float, default=0.4)
    parser.add_argument("--output", type=Path, default=Path("seo-audit.json"))
    args = parser.parse_args()
    if not (1 <= args.max_pages <= 250) or not (0.2 <= args.delay <= 5):
        parser.error("max-pages must be 1..250 and delay 0.2..5 seconds")
    try:
        report = run(args.max_pages, args.delay)
    except (RuntimeError, error.URLError, ValueError, TimeoutError) as exc:
        print(f"MVQUEEN SEO crawler: NOT VERIFIED — {exc}")
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"MVQUEEN SEO crawler audited {report['pages_checked']} public pages")
    print(json.dumps(report["findings_by_type"], sort_keys=True))
    print(f"Saved: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
