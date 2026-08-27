#!/usr/bin/env bash
set -e
[ -f .env ] || cp .env.example .env
echo "Starting Finance AI OS demo..."
docker compose up -d --build
echo
echo "Demo URLs:"
echo "  Finance AI OS: http://localhost:8088"
echo "  Odoo:          http://localhost:8069"
echo "  n8n:           http://localhost:5678"
echo
echo "Health: http://localhost:8088/health"
