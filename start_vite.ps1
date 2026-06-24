$nodePath = "C:\Users\Timor\.workbuddy\binaries\node\versions\22.22.2\node.exe"
$workingDir = "e:\linewell\program\qgb1151521\XHS_ALL_IN_ONE"
$vitePath = Join-Path $workingDir "frontend\node_modules\vite\bin\vite.js"

Set-Location $workingDir

$process = Start-Process -FilePath $nodePath `
    -ArgumentList "`"$vitePath`"", "--host", "127.0.0.1", "--port", "5173", "--strictPort" `
    -WorkingDirectory $workingDir `
    -WindowStyle Hidden `
    -PassThru `
    -RedirectStandardOutput "vite_out.log" `
    -RedirectStandardError "vite_err.log"

Write-Output "Vite started with PID: $($process.Id)"
Write-Output "Log files: vite_out.log, vite_err.log"

Start-Sleep -Seconds 5

# 验证服务
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:5173/" -UseBasicParsing -TimeoutSec 5
    Write-Output "Service status: $($response.StatusCode)"
    Write-Output "Content preview: $($response.Content.Substring(0, [Math]::Min(200, $response.Content.Length)))"
} catch {
    Write-Output "Service check failed: $_"
    Write-Output "=== vite_err.log ==="
    if (Test-Path "vite_err.log") { Get-Content "vite_err.log" }
    Write-Output "=== vite_out.log ==="
    if (Test-Path "vite_out.log") { Get-Content "vite_out.log" }
}