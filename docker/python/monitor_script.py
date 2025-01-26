import time
from docker import from_env
from http.server import BaseHTTPRequestHandler, HTTPServer

# Configura o cliente Docker
client = from_env()

# Função para coletar métricas dos containers
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
    def do_GET(self):
        # Responde às requisições GET no endpoint /metrics
        if self.path == "/metrics":
            # Coleta as métricas no momento da requisição
            metrics = collect_containers()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(metrics.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

# Função para iniciar o servidor HTTP
def start_server():
    server = HTTPServer(('0.0.0.0', 8085), MetricsReceiverHandler)
    print("Servidor HTTP rodando na porta 8085...")
    server.serve_forever()

# Inicia o servidor HTTP
if __name__ == "__main__":
    start_server()
