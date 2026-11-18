#!/usr/bin/env python3
"""Local web UI for the file-based tracker.

The markdown files in tickets/ remain the single source of truth. This server
only reads and rewrites them, and regenerates BOARD.md after every write.
Ticket parsing, validation and board generation are shared with board.py.

Stdlib only - no pip install, no node_modules.

    python3 platform/tracker/serve.py
    open http://127.0.0.1:7777
"""

from __future__ import annotations

import errno
import io
import json
import re
import sys
from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from board import (EDITABLE, ENUMS, EPICS, STATUSES, TICKETS_DIR, TYPES,
                   regenerate, split_ticket, ticket_path, write_ticket)

UI_FILE = Path(__file__).resolve().parent / "ui.html"
HOST, PORT = "127.0.0.1", 7777

CHECKBOX = re.compile(r"^(\s*[-*]\s+\[)([ xX])(\]\s)", re.MULTILINE)
NOTES_HEADING = "## Notes"


def load_all() -> list[dict]:
    out = []
    for path in sorted(TICKETS_DIR.glob("*.md")):
        try:
            meta, body = split_ticket(path)
        except ValueError as exc:
            out.append({"id": path.stem, "title": path.stem, "_error": str(exc),
                        "status": "backlog", "body": ""})
            continue
        meta["body"] = body
        out.append(meta)
    return out


def toggle_checkbox(body: str, index: int) -> str:
    """Flip the index-th checkbox (0-based) in document order."""
    matches = list(CHECKBOX.finditer(body))
    if not 0 <= index < len(matches):
        raise IndexError(f"no checkbox at index {index}")
    m = matches[index]
    return body[:m.start(2)] + (" " if m.group(2) in "xX" else "x") + body[m.end(2):]


def set_notes(body: str, notes: str) -> str:
    """Replace (or append) a trailing '## Notes' section."""
    notes = notes.strip()
    index = body.find(NOTES_HEADING)
    base = (body[:index] if index != -1 else body).rstrip("\n")
    return f"{base}\n\n{NOTES_HEADING}\n\n{notes}\n" if notes else base + "\n"


def regen_quietly() -> str:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        regenerate()
    return buffer.getvalue().strip()


class Handler(BaseHTTPRequestHandler):
    server_version = "fm-tracker"

    def log_message(self, *_args):
        pass  # the console belongs to the user, not to request noise

    def _json(self, code: int, payload) -> None:
        self._raw(code, json.dumps(payload).encode(), "application/json")

    def _raw(self, code: int, data: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            if not UI_FILE.is_file():
                return self._json(500, {"error": "ui.html missing"})
            return self._raw(200, UI_FILE.read_bytes(), "text/html; charset=utf-8")
        if path == "/api/tickets":
            return self._json(200, {"tickets": load_all(), "statuses": STATUSES,
                                    "types": TYPES, "epics": EPICS})
        self._json(404, {"error": "not found"})

    def do_POST(self):
        match = re.fullmatch(r"/api/tickets/([^/]+)", urlparse(self.path).path)
        if not match:
            return self._json(404, {"error": "not found"})
        try:
            length = int(self.headers.get("Content-Length") or 0)
            payload = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            return self._json(400, {"error": "invalid JSON"})

        try:
            file = ticket_path(match.group(1))
            meta, body = split_ticket(file)
        except (ValueError, FileNotFoundError) as exc:
            return self._json(400, {"error": str(exc)})

        fields = payload.get("fields") or {}
        unknown = set(fields) - EDITABLE
        if unknown:
            return self._json(400, {"error": f"not editable: {sorted(unknown)}"})
        for key, allowed in ENUMS.items():
            if key in fields and fields[key] not in allowed:
                return self._json(400, {"error": f"invalid {key} {fields[key]!r}"})
        for key, value in fields.items():
            meta[key] = str(value).strip() or "-"

        if "toggle" in payload:
            try:
                body = toggle_checkbox(body, int(payload["toggle"]))
            except (IndexError, ValueError) as exc:
                return self._json(400, {"error": str(exc)})

        if isinstance(payload.get("notes"), str):
            body = set_notes(body, payload["notes"])

        write_ticket(file, meta, body)
        meta["body"] = body
        self._json(200, {"ticket": meta, "board": regen_quietly()})


def main() -> int:
    if not TICKETS_DIR.is_dir():
        print(f"no tickets directory at {TICKETS_DIR}", file=sys.stderr)
        return 1
    try:
        server = ThreadingHTTPServer((HOST, PORT), Handler)
    except OSError as exc:
        if exc.errno != errno.EADDRINUSE:
            raise
        print(f"port {PORT} is already in use - the tracker may already be running.",
              file=sys.stderr)
        print(f"  open it:  http://{HOST}:{PORT}", file=sys.stderr)
        print(f"  or stop the old one:  pkill -f 'serv[e].py'", file=sys.stderr)
        return 1

    print(f"tracker UI  →  http://{HOST}:{PORT}")
    print(f"tickets     →  {TICKETS_DIR}")
    print("ctrl-c to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
