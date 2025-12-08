import http.server
import socketserver
import json
import base64
import uuid
import os

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/pix-create.php':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # QR Code fake SIMPLES
            txid = f'fake_{uuid.uuid4().hex[:8]}'
            
            # QR Code fake em SVG
            svg_qr = '''<svg width="200" height="200">
                <rect width="200" height="200" fill="#f0f0f0"/>
                <text x="100" y="50" text-anchor="middle" font-size="14">QR CODE FAKE</text>
                <text x="100" y="100" text-anchor="middle" font-size="16">💰</text>
                <text x="100" y="130" text-anchor="middle" font-size="12">PIX DEMO</text>
                <text x="100" y="150" text-anchor="middle" font-size="10">R$ 5,00</text>
                <text x="100" y="170" text-anchor="middle" font-size="8">NÃO PAGA</text>
            </svg>'''
            
            response = {
                'success': True,
                'txid': txid,
                'qrcode': f'data:image/svg+xml;base64,{base64.b64encode(svg_qr.encode()).decode()}',
                'pixCopiaECola': '00020101021226890014br.gov.bcb.pix0136123e4567-e12b-12d1-a456-426614174000520400005303986540510.005802BR5909DEMO FAKE6008BRASILIA62070503***6304ABCD'
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/api/pix-check.php':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # SEMPRE confirma pagamento fake
            response = {
                'success': True,
                'paid': True,
                'status': 'CONCLUIDA',
                'message': 'Pagamento fake confirmado'
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        else:
            super().do_GET()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"✅ Servidor fake rodando em http://localhost:{PORT}")
        print("📱 QR Code 100% falso - Nenhuma API real")
        httpd.serve_forever()
