# Odoo AR Connector

Modo recomendado para CUSTOMER #001: **read-only**.

- Demo local: el starter mantiene XML-RPC para comprobar conectividad.
- Producción Odoo 19 Custom/API: configurar `ODOO_API_KEY` y usar JSON-2.
- Datos objetivo: `account.move`, `account.payment`, `res.partner` y vencimientos.
- Nunca se publican, cancelan ni concilian asientos durante SHADOW.
