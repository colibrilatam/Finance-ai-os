# CUSTOMER #001 — Runbook de instalación

## Fase 0 — 30 minutos
- Identificar ERP real: Odoo o Holded.
- Confirmar responsable financiero y aprobador.
- Obtener baseline: ventas crédito 12m, AR abierto, vencido, DSO si existe, horas manuales/semana.
- Firmar alcance del piloto: **solo lectura / SHADOW**.

## Fase 1 — Instalación
```bash
cp .env.example .env
docker compose up -d --build
```
Validar:
- Dashboard: `http://HOST:8088`
- API: `http://HOST:8088/docs`
- MCP: `http://HOST:8090/mcp`
- Odoo demo: `http://HOST:8069`
- n8n: `http://HOST:5678`

## Fase 2 — Conectar ERP
### Odoo
1. Para demo, usar Odoo local incluido.
2. Para Odoo real, crear credencial/API dedicada read-only cuando el plan/API lo permita.
3. Mapear clientes, facturas, residual, vencimiento, pagos y moneda.
4. Reconciliar totales contra informe AR del ERP antes de mostrar resultados.

### Holded
1. Crear token dedicado.
2. Mantener únicamente GET durante SHADOW.
3. Probar contactos/facturas/cobros según endpoints disponibles en la cuenta.
4. Reconciliar AR total y muestra de 10 facturas.

## Fase 3 — Agente
Elegir **uno** al inicio:
- OpenClaw: instalar `runtimes/openclaw` como bundle.
- Hermes: fusionar `runtimes/hermes/config.yaml` y cargar `SYSTEM.md` como instrucciones.

## Fase 4 — Baseline (días 1–7)
No medir éxito todavía. Medir calidad:
- cobertura de facturas ≥ 98%
- diferencia AR Finance OS vs ERP < 0,5%
- fechas de vencimiento correctas ≥ 99%
- 0 acciones externas

## Fase 5 — Piloto asistido (días 8–30)
Daily: alertas y caja. Weekly: DSO/aging/disputas. Todo envío/acción requiere aprobación humana.

## Gate de éxito
El cliente debe poder responder sí a tres preguntas:
1. ¿Detectamos antes problemas de cobro/caja?
2. ¿El equipo ahorra tiempo medible?
3. ¿Las recomendaciones son suficientemente fiables para incorporarlas a su ritual financiero?
