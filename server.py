import http.server
import socketserver
import json
import base64
import uuid
import os
import time
from urllib.parse import urlparse, parse_qs

# ⚠️ REMOVA AS CREDENCIAIS REAIS E CERTIFICADOS!
CONFIG = {
    'valor': '0.01',  # Valor mínimo para demonstração
    'demo_mode': True,  # FORÇA modo demonstração
    'warning': '🚨 SISTEMA DE DEMONSTRAÇÃO - NÃO USA API REAL DA EFI 🚨'
}

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="./", **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'online', 
                'timestamp': time.time(),
                'app': 'Demo Portfólio',
                'demo': True,
                'warning': 'APENAS DEMONSTRAÇÃO - NÃO GERA PAGAMENTO REAL'
            }
            self.wfile.write(json.dumps(response).encode())
            return
        
        elif self.path == '/wakeup':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'status': 'awake', 'demo': True}
            self.wfile.write(json.dumps(response).encode())
            return
    
        elif self.path.startswith('/api/pix-check.php'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            txid = query_params.get('txid', [None])[0]
            
            if txid:
                # ⭐ SEMPRE retorna pagamento confirmado para demonstração
                response = {
                    'success': True,
                    'paid': True,  # Pagamento simulado
                    'status': 'CONCLUIDA',
                    'demo': True,
                    'message': 'Pagamento simulado para portfólio',
                    'warning': 'Este é um sistema de demonstração'
                }
            else:
                response = {
                    'success': False,
                    'paid': False,
                    'demo': True
                }
            
            self.wfile.write(json.dumps(response).encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/pix-create.php':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            try:
                qr_data = self.criar_pix_simulado()
                response = {
                    'success': True,
                    'txid': qr_data['txid'],
                    'qrcode': qr_data['qrcode'],
                    'pixCopiaECola': qr_data['pix_copia_cola'],
                    'demo': True,
                    'warning': 'QR Code de demonstração - Não gera pagamento real'
                }
            except Exception as e:
                response = {
                    'success': False,
                    'error': str(e),
                    'demo': True
                }
            
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def criar_pix_simulado(self):
        """Gera QR Code PIX FICTÍCIO para demonstração"""
        txid = f'demo_{uuid.uuid4().hex[:12]}'
        valor = "5.00"
        
        # QR Code estático com avisos visíveis
        svg_content = f'''<svg width="256" height="256" viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#1f2937;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#111827;stop-opacity:1" />
                </linearGradient>
            </defs>
            
            <!-- Fundo -->
            <rect width="256" height="256" fill="#f8f9fa"/>
            
            <!-- Cartão principal -->
            <rect x="10" y="10" width="236" height="236" fill="url(#grad1)" rx="12"/>
            
            <!-- Título -->
            <text x="128" y="45" text-anchor="middle" fill="white" 
                  font-family="Arial, sans-serif" font-size="16" font-weight="bold">
                PIX DEMONSTRAÇÃO
            </text>
            
            <!-- Linha divisória -->
            <line x1="30" y1="55" x2="226" y2="55" stroke="#4b5563" stroke-width="1"/>
            
            <!-- Valor -->
            <text x="128" y="85" text-anchor="middle" fill="#9ca3af" 
                  font-family="Arial, sans-serif" font-size="12">
                VALOR
            </text>
            <text x="128" y="105" text-anchor="middle" fill="white" 
                  font-family="Arial, sans-serif" font-size="20" font-weight="bold">
                R$ {valor}
            </text>
            
            <!-- Chave PIX fictícia -->
            <text x="128" y="130" text-anchor="middle" fill="#9ca3af" 
                  font-family="Arial, sans-serif" font-size="11">
                CHAVE PIX (DEMO)
            </text>
            <text x="128" y="150" text-anchor="middle" fill="#60a5fa" 
                  font-family="Arial, sans-serif" font-size="10">
                demo.portfolio@pix.com
            </text>
            
            <!-- TXID -->
            <text x="128" y="170" text-anchor="middle" fill="#9ca3af" 
                  font-family="Arial, sans-serif" font-size="10">
                ID: {txid}
            </text>
            
            <!-- Aviso de demonstração -->
            <rect x="30" y="180" width="196" height="40" fill="#f59e0b" rx="6" opacity="0.9"/>
            <text x="128" y="195" text-anchor="middle" fill="#000" 
                  font-family="Arial, sans-serif" font-size="10" font-weight="bold">
                ⚠️ APENAS DEMONSTRAÇÃO
            </text>
            <text x="128" y="210" text-anchor="middle" fill="#000" 
                  font-family="Arial, sans-serif" font-size="9">
                Não gera pagamento real
            </text>
            
            <!-- Padrões decorativos (não funcionais) -->
            <rect x="40" y="40" width="12" height="12" fill="#3b82f6" rx="2"/>
            <rect x="204" y="40" width="12" height="12" fill="#3b82f6" rx="2"/>
            <rect x="40" y="204" width="12" height="12" fill="#3b82f6" rx="2"/>
            
        </svg>'''
        
        # Código PIX fictício (não funciona)
        pix_copia_cola = f'00020126580014BR.GOV.BCB.PIX0136demo.portfolio@pix.com5204000053039865406{valor.replace(".", "")}5802BR5915DEMO-PORTFOLIO6014SAO-PAULO-SP62070503DEM6304ABCD'
        
        return {
            'txid': txid,
            'qrcode': f"data:image/svg+xml;base64,{base64.b64encode(svg_content.encode()).decode()}",
            'pix_copia_cola': pix_copia_cola
        }

def keep_alive_ping():
    """Ping automático para manter Render ativo"""
    import requests
    
    base_url = f"http://localhost:{PORT}"
    
    while True:
        try:
            requests.get(f'{base_url}/wakeup', timeout=5)
            print(f"✅ Ping - {time.strftime('%H:%M:%S')}")
        except:
            pass
        
        time.sleep(240)  # 4 minutos

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8000))
    
    # Inicia ping em background (apenas se necessário)
    try:
        ping_thread = threading.Thread(target=keep_alive_ping, daemon=True)
        ping_thread.start()
        print("🔔 Sistema de ping ativado")
    except:
        pass
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("=" * 60)
        print("🌐 DEMO PIX - PORTFÓLIO SEGURO")
        print("📍 Porta:", PORT)
        print("💰 MODO: DEMONSTRAÇÃO (100% SIMULADO)")
        print("🔒 SEGURANÇA: Sem credenciais reais")
        print("🎯 FINALIDADE: Exemplo para portfólio")
        print("=" * 60)
        print("⚠️  AVISO: Este sistema NÃO processa pagamentos reais")
        print("=" * 60)
        httpd.serve_forever()
