$ErrorActionPreference='Stop'
$urls=@('http://localhost:8088/health','http://localhost:8088/api/customer','http://localhost:8088/api/metrics')
foreach($u in $urls){ Write-Host "Checking $u"; Invoke-RestMethod $u | ConvertTo-Json -Depth 5 }
Write-Host 'MCP endpoint: http://localhost:8090/mcp'
