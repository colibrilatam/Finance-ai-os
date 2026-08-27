# Finance AI OS v2.4 — CUSTOMER #001

Este paquete **sí contiene la cadena completa del piloto**:

```text
v2.2 Demo Starter
   ↓
v2.2.1 Odoo AR Connector
   ↓
v2.2.2 Holded Connector
   ↓
v2.3 Finance MCP
   ↓
OpenClaw / Hermes
   ↓
v2.4 CFO Dashboard
   ↓
CUSTOMER #001
```

## Arranque
### Windows
```powershell
Copy-Item .env.example .env
# cambia passwords + CUSTOMER_NAME
docker compose up -d --build
.\scripts\verify-customer.ps1
```

### Linux/macOS
```bash
cp .env.example .env
# cambia passwords + CUSTOMER_NAME
docker compose up -d --build
./scripts/verify-customer.sh
```

## Puertos
- CFO Dashboard/API: `8088`
- Finance MCP: `8090`
- Odoo: `8069`
- n8n: `5678`

## Orden para el cliente real
1. Arrancar con dataset demo y enseñar el flujo.
2. Configurar el perfil en `.env` y `customer/customer.example.yaml`.
3. Conectar el ERP real **read-only**.
4. Reconciliar Finance AI OS contra AR del ERP.
5. Elegir OpenClaw o Hermes, no ambos durante la primera semana.
6. Ejecutar 7 días de baseline SHADOW.
7. Pasar a ASSISTED solo cuando reconciliación y calidad estén dentro del gate.

Lee `docs/CUSTOMER001_RUNBOOK.md` antes de tocar datos reales.
