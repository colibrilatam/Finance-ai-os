if (!(Test-Path .env)) { Copy-Item .env.example .env }
Write-Host "Starting Finance AI OS demo..."
docker compose up -d --build
Write-Host ""
Write-Host "Finance AI OS: http://localhost:8088"
Write-Host "Odoo:          http://localhost:8069"
Write-Host "n8n:           http://localhost:5678"
Write-Host "Health:        http://localhost:8088/health"
