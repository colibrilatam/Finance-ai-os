# Arquitectura CUSTOMER #001

```text
                    CFO / Equipo financiero
                             │
                    OpenClaw o Hermes
                             │
                       Finance MCP :8090
                             │
                     Finance Core :8088
                      /      |       \
                 Metrics   Alerts    ROI
                    │
             Canonical Finance Model
              /                    \
      Odoo AR Connector       Holded Connector
              │                    │
         Odoo / Postgres        Holded API

        n8n = automatización aprobada / notificaciones
        SHADOW = ningún write financiero durante baseline
```

La regla central es desacoplar **runtime**, **motor financiero** y **ERP**. El agente interpreta; Finance Core calcula; el conector lee; la aprobación humana gobierna cualquier write futuro.
