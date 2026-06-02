from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import csv
import json
import os
from pathlib import Path
import signal
import shutil
import subprocess
import sys
import time
from urllib.parse import parse_qs, urlparse


BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR
PACKAGE_DIR = BASE_DIR / "real_estate3"
FRONTEND_FILE = PACKAGE_DIR / "real_third_frontend.html"
OUTPUT_DIR = BASE_DIR / "outputs"
JSON_OUTPUT = OUTPUT_DIR / "real_third_latest.json"
CSV_OUTPUT = OUTPUT_DIR / "real_third_latest.csv"
LOG_OUTPUT = OUTPUT_DIR / "real_third_latest.log"
SPIDER_NAME = "real_third"

FIELDNAMES = [
    "title",
    "price",
    "location",
    "description",
    "link",
    "phone",
    "time_to_paste",
]

process = None
started_at = None


def ensure_output_dir():
    OUTPUT_DIR.mkdir(exist_ok=True)


def read_json_items():
    if not JSON_OUTPUT.exists():
        return []
    try:
        with JSON_OUTPUT.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return []
    return data if isinstance(data, list) else []


def write_csv(items):
    ensure_output_dir()
    with CSV_OUTPUT.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        for item in items:
            writer.writerow({key: item.get(key, "") for key in FIELDNAMES})


def refresh_csv_from_json():
    items = read_json_items()
    write_csv(items)
    return items


def is_running():
    global process
    if process is None:
        return False
    if process.poll() is None:
        return True
    process = None
    refresh_csv_from_json()
    return False


def process_status():
    running = is_running()
    items = read_json_items()
    return {
        "running": running,
        "pid": process.pid if running and process else None,
        "started_at": started_at,
        "items_count": len(items),
        "json_exists": JSON_OUTPUT.exists(),
        "csv_exists": CSV_OUTPUT.exists(),
        "log_exists": LOG_OUTPUT.exists(),
        "json_mtime": JSON_OUTPUT.stat().st_mtime if JSON_OUTPUT.exists() else None,
        "csv_mtime": CSV_OUTPUT.stat().st_mtime if CSV_OUTPUT.exists() else None,
    }


def start_spider():
    global process, started_at
    if is_running():
        return False

    ensure_output_dir()
    if JSON_OUTPUT.exists():
        JSON_OUTPUT.unlink()
    if CSV_OUTPUT.exists():
        CSV_OUTPUT.unlink()

    log_file = LOG_OUTPUT.open("w", encoding="utf-8")
    scrapy_command = os.environ.get("SCRAPY_COMMAND") or shutil.which("scrapy")
    if not scrapy_command:
        raise RuntimeError("Scrapy command was not found. Install Scrapy or set SCRAPY_COMMAND.")

    command = [
        scrapy_command,
        "crawl",
        SPIDER_NAME,
        "-O",
        str(JSON_OUTPUT),
    ]
    process = subprocess.Popen(
        command,
        cwd=PROJECT_DIR,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        text=True,
        start_new_session=True,
    )
    started_at = time.time()
    return True


def stop_spider():
    if not is_running() or process is None:
        return False

    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return False

    try:
        process.wait(timeout=8)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait(timeout=4)

    refresh_csv_from_json()
    return True


def read_log_tail(lines=80):
    if not LOG_OUTPUT.exists():
        return ""
    try:
        content = LOG_OUTPUT.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    return "\n".join(content.splitlines()[-lines:])


class DashboardHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in {"/", "/dashboard"}:
            self.send_file_headers(FRONTEND_FILE, "text/html; charset=utf-8")
        elif path == "/download/json":
            self.send_file_headers(JSON_OUTPUT, "application/json", download_name="real_third_latest.json")
        elif path == "/download/csv":
            refresh_csv_from_json()
            self.send_file_headers(CSV_OUTPUT, "text/csv; charset=utf-8", download_name="real_third_latest.csv")
        else:
            self.send_error(404, "Not found")

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in {"/", "/dashboard"}:
            self.send_file(FRONTEND_FILE, "text/html; charset=utf-8")
        elif path == "/api/status":
            self.send_json(process_status())
        elif path == "/api/data":
            items = refresh_csv_from_json()
            self.send_json(items)
        elif path == "/api/logs":
            params = parse_qs(parsed.query)
            limit = int(params.get("lines", ["80"])[0] or "80")
            self.send_json({"log": read_log_tail(limit)})
        elif path == "/download/json":
            self.send_file(JSON_OUTPUT, "application/json", download_name="real_third_latest.json")
        elif path == "/download/csv":
            refresh_csv_from_json()
            self.send_file(CSV_OUTPUT, "text/csv; charset=utf-8", download_name="real_third_latest.csv")
        else:
            self.send_error(404, "Not found")

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/start":
            try:
                started = start_spider()
            except RuntimeError as error:
                self.send_json({"started": False, "error": str(error), **process_status()}, status=500)
                return
            self.send_json({"started": started, **process_status()})
        elif parsed.path == "/api/stop":
            stopped = stop_spider()
            self.send_json({"stopped": stopped, **process_status()})
        else:
            self.send_error(404, "Not found")

    def send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, file_path, content_type, download_name=None):
        if not file_path.exists():
            self.send_error(404, "File not found")
            return

        body = file_path.read_bytes()
        self.send_file_headers(file_path, content_type, download_name=download_name, content_length=len(body))
        self.wfile.write(body)

    def send_file_headers(self, file_path, content_type, download_name=None, content_length=None):
        if not file_path.exists():
            self.send_error(404, "File not found")
            return

        if content_length is None:
            content_length = file_path.stat().st_size
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(content_length))
        self.send_header("Cache-Control", "no-store")
        if download_name:
            self.send_header("Content-Disposition", f'attachment; filename="{download_name}"')
        self.end_headers()

    def log_message(self, format, *args):
        sys.stdout.write("%s - %s\n" % (self.address_string(), format % args))


def main():
    ensure_output_dir()
    port = int(os.environ.get("CRAWLER_DASHBOARD_PORT", "8000"))
    server = ThreadingHTTPServer(("127.0.0.1", port), DashboardHandler)
    print(f"Dashboard running at http://127.0.0.1:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        if is_running():
            stop_spider()
        print("\nDashboard stopped")


if __name__ == "__main__":
    main()
