import http.server
import socketserver
import subprocess
import html

SOURCE = "The start.c"
BINARY = "/tmp/start"


def compile_and_run():
    """Compile the C source, run it, and return HTML showing the output."""
    compile_result = subprocess.run(
        ["gcc", "-std=gnu89", "-Wno-implicit-int", "-Wno-implicit-function-declaration", SOURCE, "-o", BINARY], capture_output=True, text=True
    )
    if compile_result.returncode != 0:
        body = f"<h2>Compilation Error</h2><pre>{html.escape(compile_result.stderr)}</pre>"
    else:
        run_result = subprocess.run([BINARY], capture_output=True, text=True)
        output = run_result.stdout + run_result.stderr
        body = f"<pre class=\"output\">{html.escape(output)}</pre>"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>smtg</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    min-height: 100vh; background: #0d1117; color: #c9d1d9;
  }}
  h1 {{ font-size: 1.6rem; margin-bottom: 1.5rem; color: #58a6ff; font-weight: 600; }}
  pre {{
    background: #161b22; padding: 2rem 3rem; border-radius: 12px;
    border: 1px solid #30363d; font-size: 1.1rem; line-height: 1.6;
    white-space: pre-wrap; max-width: 90vw; overflow-x: auto;
  }}
  .meta {{ margin-top: 1.5rem; font-size: 0.8rem; color: #484f58; }}
</style>
</head>
<body>
  <h1>smtg</h1>
  {body}
  <p class="meta">Compiled from <code>{html.escape(SOURCE)}</code> on each request</p>
</body>
</html>"""


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        content = compile_and_run()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode())

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    with socketserver.TCPServer(("0.0.0.0", 3000), Handler) as httpd:
        print("Dev server running on http://0.0.0.0:3000")
        httpd.serve_forever()
