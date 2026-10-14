from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3

DB_PATH = "evidence/ad_astra_local.db"
API_SECRET_TOKEN = "ad-astra-secure-token-123"

class DistributedAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        auth_header = self.headers.get("Authorization")
        if auth_header != f"Bearer {API_SECRET_TOKEN}":
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "Unauthorized: Invalid or missing API Token"}')
            return
            
        if self.path == "/cluster/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM worker_leases;")
                active_leases = cursor.fetchone()[0]
                conn.close()
                
                response = {
                    "cluster_status": "healthy",
                    "node_mode": "distributed-master",
                    "active_leases": active_leases
                }
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.wfile.write(json.dumps({"error": str.format("{}", e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def run_distributed_server(port=9090):
    server = HTTPServer(('127.0.0.1', port), DistributedAPIHandler)
    print(f"[DISTRIBUTED API] Secure node running on http://127.0.0.1:{port}/cluster/status")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[DISTRIBUTED API] Server stopped.")

if __name__ == "__main__":
    run_distributed_server()
