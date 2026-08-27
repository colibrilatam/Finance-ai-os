import csv, os, xmlrpc.client
from datetime import date, datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Finance AI OS CUSTOMER #001", version="2.4.0")
DATA_DIR = os.getenv("DEMO_DATA_DIR", "/app/demo_data")


def load_csv(name):
    path = os.path.join(DATA_DIR, name)
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def as_float(v):
    try: return float(v)
    except: return 0.0


def demo_metrics():
    inv = load_csv("invoices.csv")
    today = date(2026,8,27)
    open_rows = [r for r in inv if r["status"] != "paid"]
    ar = sum(as_float(r["open_amount"]) for r in open_rows)
    overdue_rows=[]
    for r in open_rows:
        due=datetime.strptime(r["due_date"], "%Y-%m-%d").date()
        if due < today: overdue_rows.append(r)
    overdue=sum(as_float(r["open_amount"]) for r in overdue_rows)
    disputes=sum(as_float(r["open_amount"]) for r in open_rows if r["dispute"]=="yes")
    sales_12m=8_000_000  # baseline comercial explícito del escenario demo
    dso=round((ar / sales_12m)*365,1) if sales_12m else 0
    at_risk=sum(as_float(r["open_amount"]) for r in overdue_rows if (today-datetime.strptime(r["due_date"], "%Y-%m-%d").date()).days >= 60)
    recoverable_14=sum(as_float(r["open_amount"]) for r in overdue_rows if r["promise_14d"]=="yes")
    return {
      "dso_days": dso,
      "ar_open": round(ar,2),
      "overdue": round(overdue,2),
      "disputes": round(disputes,2),
      "risk_60_plus": round(at_risk,2),
      "recoverable_14d": round(recoverable_14,2),
      "manual_hours_week": 12,
      "cash_13w": 1240000,
      "source": "synthetic-demo"
    }


def odoo_status():
    url=os.getenv("ODOO_URL","http://odoo:8069")
    db=os.getenv("ODOO_DB","finance_demo")
    user=os.getenv("ODOO_USER","admin")
    pwd=os.getenv("ODOO_PASSWORD","admin")
    try:
        common=xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
        uid=common.authenticate(db,user,pwd,{})
        if not uid:
            return {"connected":False,"detail":"Odoo reachable, authentication pending"}
        models=xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
        partners=models.execute_kw(db,uid,pwd,"res.partner","search_count",[[["customer_rank",">",0]]])
        moves=models.execute_kw(db,uid,pwd,"account.move","search_count",[[["move_type","=","out_invoice"]]])
        return {"connected":True,"customers":partners,"invoices":moves,"api":"xmlrpc/2 (demo adapter)"}
    except Exception as e:
        return {"connected":False,"detail":str(e)[:160]}

@app.get("/health")
def health():
    return {"ok":True,"service":"finance-ai-os-demo","odoo":odoo_status()}

@app.get("/api/metrics")
def metrics():
    m=demo_metrics(); m["odoo"]=odoo_status(); return m

@app.get("/api/alerts")
def alerts():
    return [
      {"severity":"critical","title":"Cliente Atlas excede límite de crédito","impact":92000,"action":"Bloquear nueva exposición y revisar promesa de pago"},
      {"severity":"high","title":"Factura INV-0241 vencida 65 días","impact":41800,"action":"Escalar a responsable comercial"},
      {"severity":"medium","title":"3 disputas administrativas bloquean cobros","impact":63000,"action":"Resolver PO/recepción/precio"},
      {"severity":"medium","title":"Caja proyectada cae bajo umbral en semana 11","impact":-74000,"action":"Acelerar cobros recuperables a 14 días"}
    ]

@app.get("/api/roi")
def roi(annual_credit_sales: float=8_000_000, dso_reduction_days: float=4, hours_week_saved: float=12, hourly_cost: float=35):
    working_capital=annual_credit_sales*dso_reduction_days/365
    labor=hours_week_saved*hourly_cost*52
    return {"working_capital_released":round(working_capital,2),"annual_productivity_value":round(labor,2),"combined_value_indicator":round(working_capital+labor,2)}



@app.get("/api/customer")
def customer_profile():
    return {
      "code": os.getenv("CUSTOMER_CODE","CUSTOMER-001"),
      "name": os.getenv("CUSTOMER_NAME","Mi Primer Cliente"),
      "mode": os.getenv("FINANCE_MODE","SHADOW"),
      "erp": os.getenv("ERP_PROVIDER","odoo"),
      "read_only": os.getenv("READ_ONLY","true").lower()=="true",
      "approval_required": True
    }

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """<!doctype html><html lang='es'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width'><title>Finance AI OS Demo</title><style>
body{font-family:Inter,Arial,sans-serif;background:#f5f7fb;color:#0b1f3a;margin:0}.wrap{max-width:1200px;margin:auto;padding:28px}.top{display:flex;justify-content:space-between;align-items:center}.badge{background:#dff7f6;color:#087f8c;padding:8px 12px;border-radius:999px;font-weight:700}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.card{background:white;border-radius:16px;padding:18px;box-shadow:0 5px 18px #14213d12}.big{font-size:30px;font-weight:800}.muted{color:#637083}.two{display:grid;grid-template-columns:1.2fr .8fr;gap:14px;margin-top:14px}.alert{border-left:5px solid #ffb703;padding:12px;background:#fff8e6;margin:9px 0;border-radius:8px}.crit{border-left-color:#e63946}.ok{color:#16865b;font-weight:700}.footer{margin-top:18px;font-size:13px;color:#637083}@media(max-width:800px){.grid,.two{grid-template-columns:1fr}.top{align-items:flex-start;gap:10px;flex-direction:column}}
</style></head><body><div class='wrap'><div class='top'><div><h1>Finance AI OS <span style='color:#1597a5'>v2.4 CUSTOMER #001</span></h1><p class='muted'>CUSTOMER #001 · CFO Command Center</p></div><div class='badge'>SHADOW MODE · Human-in-the-loop</div></div><div id='kpis' class='grid'></div><div class='two'><div class='card'><h2>Alertas prioritarias</h2><div id='alerts'></div></div><div class='card'><h2>Impacto potencial</h2><div id='roi'></div><hr><p><b>Objetivo del piloto:</b> demostrar caja liberada, menos trabajo manual y mejor priorización en 30 días.</p><p class='ok' id='odoo'>Comprobando Odoo…</p></div></div><div class='footer'>Datos de demo sintéticos. Finance AI OS separa hechos, cálculos, hipótesis e inferencias y no ejecuta acciones críticas sin aprobación.</div></div><script>
const euro=n=>new Intl.NumberFormat('es-ES',{style:'currency',currency:'EUR',maximumFractionDigits:0}).format(n);
fetch('/api/metrics').then(r=>r.json()).then(m=>{let data=[['DSO actual',m.dso_days+' días'],['AR abierto',euro(m.ar_open)],['Vencido',euro(m.overdue)],['Disputas',euro(m.disputes)]];document.getElementById('kpis').innerHTML=data.map(x=>`<div class='card'><div class='muted'>${x[0]}</div><div class='big'>${x[1]}</div></div>`).join('');document.getElementById('odoo').textContent=m.odoo.connected?`✓ Odoo conectado · ${m.odoo.customers} clientes · ${m.odoo.invoices} facturas`:'Odoo iniciando · el dashboard sigue operativo con dataset demo';});
fetch('/api/alerts').then(r=>r.json()).then(a=>document.getElementById('alerts').innerHTML=a.map(x=>`<div class='alert ${x.severity==='critical'?'crit':''}'><b>${x.title}</b><br><span class='muted'>Impacto ${euro(x.impact)} · ${x.action}</span></div>`).join(''));
fetch('/api/roi').then(r=>r.json()).then(x=>document.getElementById('roi').innerHTML=`<p><span class='big'>${euro(x.working_capital_released)}</span><br><span class='muted'>working capital potencial con -4 días DSO</span></p><p><b>${euro(x.annual_productivity_value)}/año</b><br><span class='muted'>productividad estimada</span></p>`);
</script></body></html>"""
