import os, httpx
from fastmcp import FastMCP
mcp=FastMCP("Finance AI OS")
CORE=os.getenv("FINANCE_CORE_URL","http://finance-core:8088")

def get(path, params=None):
    with httpx.Client(timeout=20) as c:
        r=c.get(CORE+path,params=params); r.raise_for_status(); return r.json()

@mcp.tool()
def finance_health():
    """Estado del Finance Core y ERP. Solo lectura."""
    return get('/health')

@mcp.tool()
def finance_metrics():
    """KPIs financieros principales del piloto."""
    return get('/api/metrics')

@mcp.tool()
def finance_alerts():
    """Alertas financieras priorizadas. No ejecuta acciones."""
    return get('/api/alerts')

@mcp.tool()
def finance_roi(annual_credit_sales: float, dso_reduction_days: float=4, hours_week_saved: float=12, hourly_cost: float=35):
    """Calcula impacto potencial del piloto con fórmulas deterministas."""
    return get('/api/roi',locals())

@mcp.tool()
def finance_customer_profile():
    """Devuelve el perfil de cliente y modo de operación del piloto."""
    return get('/api/customer')

if __name__=='__main__':
    mcp.run(transport='http',host='0.0.0.0',port=int(os.getenv('MCP_PORT','8090')))
