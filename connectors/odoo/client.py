import os, requests

class OdooJSON2Client:
    def __init__(self):
        self.base=os.getenv("ODOO_URL","http://odoo:8069").rstrip("/")
        self.db=os.getenv("ODOO_DB","finance_demo")
        self.key=os.getenv("ODOO_API_KEY","")
    def call(self, model, method, payload):
        if not self.key:
            raise RuntimeError("ODOO_API_KEY missing. JSON-2 is disabled until a key is configured.")
        h={"Authorization":f"bearer {self.key}","Content-Type":"application/json","X-Odoo-Database":self.db}
        r=requests.post(f"{self.base}/json/2/{model}/{method}",headers=h,json=payload,timeout=30)
        r.raise_for_status(); return r.json()
    def open_invoices(self):
        return self.call("account.move","search_read",{
          "domain":[["move_type","=","out_invoice"],["state","=","posted"],["payment_state","!=","paid"]],
          "fields":["name","partner_id","invoice_date","invoice_date_due","amount_total","amount_residual","payment_state","currency_id"],
          "limit":1000
        })
