import os,time,xmlrpc.client,random
URL=os.getenv('ODOO_URL','http://odoo:8069'); DB=os.getenv('ODOO_DB','finance_demo'); USER=os.getenv('ODOO_USER','admin'); PWD=os.getenv('ODOO_PASSWORD','admin')

def connect():
  common=xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
  for _ in range(60):
    try:
      uid=common.authenticate(DB,USER,PWD,{})
      if uid:return uid
    except Exception: pass
    time.sleep(3)
  return None
uid=connect()
if not uid:
  print('SEED: Odoo not authenticated. Demo dashboard will use synthetic data.'); raise SystemExit(0)
models=xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
companies=['Atlas Retail SL','Nova Logistics SA','Iberia Components SL','BluePeak SaaS SL','Delta Industrial SA','Orion Consulting SL','Nexo Distribución SL','Terra Build SL','Aster Services SL','Vector Tech SL']
for i,name in enumerate(companies):
  found=models.execute_kw(DB,uid,PWD,'res.partner','search',[[['name','=',name]]],{'limit':1})
  if not found:
    try:
      models.execute_kw(DB,uid,PWD,'res.partner','create',[{'name':name,'company_type':'company','customer_rank':1,'email':f'finance{i+1}@example.com','phone':f'+34 910 000 {100+i}'}])
    except Exception as e: print('partner warning',name,str(e)[:120])
print('SEED: customer master loaded. Invoice scenario remains in Finance AI OS synthetic dataset for deterministic demo.')
