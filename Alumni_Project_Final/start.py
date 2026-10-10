import os
import sys
import traceback

port = int(os.environ.get("PORT", 10000))

try:
    print(f"[BOOT] Python version: {sys.version}")
    print(f"[BOOT] Directory: {os.getcwd()}")
    print(f"[BOOT] Target Port: {port}")
    
    import uvicorn
    from app.main import app
    
    print("[BOOT] App imported successfully, starting uvicorn...")
    uvicorn.run(app, host="0.0.0.0", port=port)

except Exception as exc:
    err_msg = traceback.format_exc()
    print("[FATAL STARTUP ERROR]", err_msg, file=sys.stderr)
    
    # Run a fallback emergency HTTP server so the exact error can be read in the browser
    from http.server import HTTPServer, BaseHTTPRequestHandler
    
    class ErrorHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(500)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(f"STARTUP ERROR:\n\n{err_msg}".encode())
            
    print(f"[BOOT] Fallback error server listening on port {port}...")
    server = HTTPServer(("0.0.0.0", port), ErrorHandler)
    server.serve_forever()
