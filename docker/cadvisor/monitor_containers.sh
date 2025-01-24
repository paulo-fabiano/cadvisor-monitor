#!/bin/bash

# URL do endpoint onde os dados serão enviados
ENDPOINT="http://localhost:8000/metrics"

# Função para coletar informações de containers
collect_containers() {
  docker ps -a --format '{{.Names}},{{.Status}},{{.Image}}' | while IFS=, read -r name status image; do
    # Cria os dados no formato Prometheus para cada container
    cat <<EOF
# HELP container_status Container status (1 = running, 0 = exited)
# TYPE container_status gauge
container_status{name="$name",image="$image",status="$status"} $(echo "$status" | grep -q "Up" && echo 1 || echo 0)
EOF
  done
}

# Loop infinito para coletar e enviar os dados periodicamente
while true; do
  echo "Coletando dados dos containers..."
  
  # Coleta os dados e os envia para o endpoint
  metrics=$(collect_containers)
  echo "$metrics" | curl -X POST -H "Content-Type: text/plain" --data-binary @- "$ENDPOINT"
  
  # Aguarda 60 segundos antes de repetir
  sleep 60
done
