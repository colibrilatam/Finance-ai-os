import os, requests
class HoldedClient:
    def __init__(self):
        self.key=os.getenv("HOLDED_API_KEY","")
        self.base=os.getenv("HOLDED_API_BASE","https://api.holded.com/api").rstrip("/")
    def _get(self,path,params=None):
        if not self.key: raise RuntimeError("HOLDED_API_KEY missing")
        r=requests.get(self.base+path,headers={"key":self.key},params=params or {},timeout=30)
        r.raise_for_status(); return r.json()
    def invoices(self): return self._get('/invoicing/v1/documents/invoice')
    def contacts(self): return self._get('/invoicing/v1/contacts')
