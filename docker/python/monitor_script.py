import time
import requests
from docker import from_env
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# Configura o cliente Docker
client = from_env()

# URL do endpoint onde os dados serão enviados
ENDPOINT = "http://localhost:8085/metrics"

def collect_containers():
    metrics = []
    for container in client.containers.list(all=True):
        # Verifica o status do container
        status = 1 if container.status == "running" else 0
        # Formata os dados no formato Prometheus
        metrics.append(
            f'# HELP container_status Container status (1 = running, 0 = exited)\n'
            f'# TYPE container_status gauge\n'
            f'container_status{{name="{container.name}",image="{container.image.tags[0] if container.image.tags else "unknown"}",status="{container.status}"}} {status}'
        )
    return "\n".join(metrics)

# Classe para o servidor HTTP
class MetricsReceiverHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Lê os dados enviados no corpo da requisição
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        print("Métricas recebidas no servidor:\n")
        print(post_data)

        # Retorna uma resposta ao cliente
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Métricas recebidas com sucesso.")

# Função para iniciar o servidor HTTP
def start_server():
    server = HTTPServer(('0.0.0.0', 8000), MetricsReceiverHandler)
    print("Servidor HTTP rodando na porta 8000...")
    server.serve_forever()

# Iniciar o servidor em uma thread separada
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# Loop principal para coletar e enviar métricas
while True:
    print("Coletando dados dos containers...")
    metrics = collect_containers()
    
    try:
        # Envia os dados para o endpoint
        response = requests.post(ENDPOINT, data=metrics, headers={"Content-Type": "text/plain"})
        print(f"Status do envio: {response.status_code}")
    except Exception as e:
        print(f"Erro ao enviar métricas: {e}")
    
    time.sleep(60)
