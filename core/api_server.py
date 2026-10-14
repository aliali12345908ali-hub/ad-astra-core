from http.server import HTTPServer, BaseHTTPRequestHandler
import sqlite3
import json

DB_PATH = "evidence/ad_astra_local.db"

class SimpleAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM tasks;")
                task_count = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM projects;")
                project_count = cursor.fetchone()[0]
                conn.close()
                
                response_data = {
                    "status": "online",
                    "architecture": "Autonomous Core v0.3",
                    "projects_count": project_count,
                    "tasks_count": task_count
                }
                self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                error_data = {"status": "error", "message": str(e)}
                self.wfile.write(json.dumps(error_data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "Endpoint Not Found"}')

def run_server(port=8080):
    server = HTTPServer(('127.0.0.1', port), SimpleAPIHandler)
    print(f"[API SERVER] Running locally on http://127.0.0.1:{port}/status")
    print("[API SERVER] Press Ctrl+C to stop the server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[API SERVER] Server stopped.")

if __name__ == "__main__":
    run_server()
