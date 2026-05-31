"""Build read.html and per-entry HTML pages from books/ and writings/.

Source of truth is the .md files in books/ and writings/. Writings are only
listed on the index when their front-matter has `publish: true`; book entries
honor a `status:` field (read / reading / abandoned).
"""

import html
import re
import sys
from pathlib import Path

import yaml


LEGO = Path(__file__).parent
BOOKS = LEGO / "books"
WRITINGS = LEGO / "writings"
TEMPLATES = LEGO / "templates"
GITHUB_BASE = "https://jd2504.github.io/lego/"




def read_entry(path: Path) -> tuple[dict, str]:
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not m:
        raise ValueError(f"{path}: missing front-matter")
    meta = yaml.safe_load(m.group(1)) or {}
    body = m.group(2).strip()
    return meta, body


def render_markdown(text: str) -> str:
    """Minimal markdown: paragraphs, blockquotes (> ...), bullet lists (- ...),
    inline links [t](u). Blockquote contents are rendered recursively so they
    can contain paragraphs and lists."""
    if not text.strip():
        return ""
    blocks = re.split(r"\n\s*\n", text.strip())
    out = []
    for block in blocks:
        lines = block.splitlines()
        if all(ln.startswith(">") or not ln.strip() for ln in lines):
            inner = "\n".join(re.sub(r"^>\s?", "", ln) for ln in lines)
            out.append(f"<blockquote>\n{render_markdown(inner)}\n</blockquote>")
        elif all(re.match(r"^\s*-\s", ln) for ln in lines if ln.strip()):
            items = [re.sub(r"^\s*-\s+", "", ln) for ln in lines if ln.strip()]
            li = "\n".join(f"  <li>{inline(it)}</li>" for it in items)
            out.append(f"<ul>\n{li}\n</ul>")
        else:
            out.append(f"<p>{inline(block.strip())}</p>")
    return "\n".join(out)


def inline(s: str) -> str:
    # escape, then re-introduce [text](url) links
    s = html.escape(s)
    s = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>',
        s,
    )
    # preserve paragraph breaks within a block as <br> only if explicit; otherwise
    # collapse single newlines into spaces
    s = re.sub(r"\n", " ", s)
    return s


def load_template(name: str) -> str:
    return (TEMPLATES / name).read_text()


def fill(template: str, **vars) -> str:
    out = template
    for k, v in vars.items():
        out = out.replace("{{" + k + "}}", v)
    return out


# book/index rendering

def book_link(meta: dict, slug: str, has_body: bool) -> str:
    """Return the cell content for the leftmost column in the index table."""
    label = meta.get("legacy_id") or slug
    if meta.get("pdf"):
        return f'<a href="{meta["pdf"]}">{html.escape(label)}</a>'
    if has_body:
        return f'<a href="{slug}.html">{html.escape(label)}</a>'
    return html.escape(label)


def render_book_page(slug: str, meta: dict, body_md: str) -> str:
    title = meta["title"]
    bits = [
        html.escape(meta.get("author", "")),
        str(meta.get("published", "")),
    ]
    read = meta.get("read")
    if read:
        bits.append(f"read {read}")
    if meta.get("legacy_id"):
        bits.append(meta["legacy_id"])
    meta_line = " &middot; ".join(b for b in bits if b)
    return fill(
        load_template("page.html"),
        title=html.escape(title),
        meta=meta_line,
        body=render_markdown(body_md),
    )


def render_writing_page(slug: str, meta: dict, body_md: str) -> str:
    title = meta["title"]
    bits = []
    if meta.get("subtitle"):
        bits.append(html.escape(meta["subtitle"]))
    if meta.get("date"):
        bits.append(str(meta["date"]))
    meta_line = " &middot; ".join(bits)
    return fill(
        load_template("page.html"),
        title=html.escape(title),
        meta=meta_line,
        body=render_markdown(body_md),
    )


def render_index(books: list, writings: list) -> str:
    # books: list of (slug, meta, has_body)
    finished = [b for b in books if b[1].get("status", "read") == "read"]
    reading = [b for b in books if b[1].get("status") == "reading"]
    abandoned = [b for b in books if b[1].get("status") == "abandoned"]

    finished.sort(key=lambda b: str(b[1].get("read", "")), reverse=True)
    reading.sort(key=lambda b: str(b[1].get("started", b[1].get("read", ""))), reverse=True)
    abandoned.sort(key=lambda b: str(b[1].get("read", "")), reverse=True)

    finished_table = render_finished_table(finished)

    if reading:
        items = "\n".join(
            f'    <li><strong>{html.escape(m["title"])}</strong> &mdash; '
            f'{html.escape(m.get("author", ""))}'
            + (f' ({m["published"]})' if m.get("published") else "")
            + (f' <span class="date">started {m["started"]}</span>' if m.get("started") else "")
            + "</li>"
            for _, m, _ in reading
        )
        currently = f'<h2>Currently reading ({len(reading)})</h2>\n  <ul class="reading-list">\n{items}\n  </ul>'
    else:
        currently = ""

    if abandoned:
        items = "\n".join(
            f'    <li>{html.escape(m["title"])} &mdash; {html.escape(m.get("author",""))}</li>'
            for _, m, _ in abandoned
        )
        abandoned_section = f'<h2>Abandoned ({len(abandoned)})</h2>\n  <ul class="reading-list">\n{items}\n  </ul>'
    else:
        abandoned_section = ""

    published_writings = [(s, m) for s, m in writings if m.get("publish")]
    published_writings.sort(key=lambda w: str(w[1].get("date", "")), reverse=True)
    if published_writings:
        items = []
        for slug, m in published_writings:
            href = m.get("external") or f"writings/{slug}.html"
            date = f' <span class="date">{m["date"]}</span>' if m.get("date") else ""
            items.append(f'    <li><a href="{href}">{html.escape(m["title"])}</a>{date}</li>')
        writings_section = (
            f'<h2>Writings ({len(published_writings)})</h2>\n  '
            f'<ul class="writings-list">\n' + "\n".join(items) + "\n  </ul>"
        )
    else:
        writings_section = ""

    return fill(
        load_template("index.html"),
        currently_reading_section=currently,
        finished_table=finished_table,
        abandoned_section=abandoned_section,
        writings_section=writings_section,
    )


def render_finished_table(finished: list) -> str:
    rows = []
    rows.append('<table id="finishedTable">')
    rows.append("  <thead><tr>")
    for i, label in enumerate(["title", "author", "published", "read", "keywords"]):
        rows.append(f'    <th onclick="sortTable({i})">{label}</th>')
    rows.append("  </tr></thead>")
    rows.append("  <tbody>")
    for slug, meta, has_body in finished:
        title = html.escape(meta["title"])
        if meta.get("pdf"):
            title_cell = f'<a href="{meta["pdf"]}">{title}</a>'
        elif has_body:
            title_cell = f'<a href="{slug}.html">{title}</a>'
        else:
            title_cell = title
        cells = [
            title_cell,
            html.escape(meta.get("author", "")),
            html.escape(str(meta.get("published", ""))),
            html.escape(str(meta.get("read", ""))),
            html.escape(" ".join(meta.get("keywords", []) or [])),
        ]
        rows.append("    <tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
    rows.append("  </tbody>")
    rows.append("</table>")
    return "\n".join(rows)


# legacy redirects

def render_redirect(target: str) -> str:
    return (
        '<!DOCTYPE html><html><head>'
        f'<meta http-equiv="refresh" content="0; url={target}">'
        f'<link rel="canonical" href="{target}">'
        "</head></html>\n"
    )




def main():
    books = []
    for path in sorted(BOOKS.glob("*.md")):
        slug = path.stem
        meta, body = read_entry(path)
        has_body = bool(body.strip())
        books.append((slug, meta, has_body))
        if has_body:
            (LEGO / f"{slug}.html").write_text(render_book_page(slug, meta, body))
        # legacy aaNNN redirect (if there was a legacy id, redirect to new url)
        legacy = meta.get("legacy_id")
        if legacy and has_body:
            (LEGO / f"{legacy}.html").write_text(render_redirect(f"{slug}.html"))

    writings = []
    for path in sorted(WRITINGS.glob("*.md")):
        slug = path.stem
        meta, body = read_entry(path)
        writings.append((slug, meta))
        if body.strip():
            out = WRITINGS / f"{slug}.html"
            out.write_text(render_writing_page(slug, meta, body))

    index = render_index(books, writings)
    (LEGO / "read.html").write_text(index)

    print(f"books: {len(books)}")
    print(f"  reading:   {sum(1 for _,m,_ in books if m.get('status') == 'reading')}")
    print(f"  abandoned: {sum(1 for _,m,_ in books if m.get('status') == 'abandoned')}")
    print(f"  finished:  {sum(1 for _,m,_ in books if m.get('status', 'read') == 'read')}")
    print(f"writings:  {len(writings)} ({sum(1 for _,m in writings if m.get('publish'))} published)")


if __name__ == "__main__":
    main()
