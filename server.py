import http.server
import socketserver
import json
import csv
import os
import datetime

PORT = 8000
CSV_FILE = 'yorum.csv'

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        # Handle the PHP endpoint request for compatibility
        if self.path.endswith('save_comment.php'):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                
                level = data.get('level', '')
                pages = data.get('pages', '')
                comment = data.get('comment', '')
                date_str = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
                
                file_exists = os.path.isfile(CSV_FILE)
                
                # Use utf-8-sig for Excel compatibility (BOM)
                with open(CSV_FILE, 'a', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    if not file_exists:
                        writer.writerow(['Seviye', 'Sayfa', 'Yorum', 'Tarih'])
                    writer.writerow([level, pages, comment, date_str])
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True}).encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'message': str(e)}).encode('utf-8'))
        else:
            self.send_error(404, "Not Found")

print(f"Sunucu başlatıldı: http://localhost:{PORT}")
print("Durdurmak için CTRL+C tuşlarına basınız.")

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nSunucu durduruldu.")
