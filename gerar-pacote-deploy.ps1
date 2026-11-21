# Script Gerador de Pacote Limpo para Deploy na Nuvem (Render / GitHub)
# Gera um arquivo .zip higienizado diretamente na Area de Trabalho

$ErrorActionPreference = "Stop"
$projectName = "festejando-na-mesa-catalogo"
$sourceDir = $PSScriptRoot

$desktopPath = [System.IO.Path]::Combine($env:USERPROFILE, "OneDrive", "Desktop")
if (-not (Test-Path $desktopPath)) {
    $desktopPath = [System.IO.Path]::Combine($env:USERPROFILE, "Desktop")
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$zipPath = Join-Path $desktopPath "$projectName-DEPLOY-PRODUCAO.zip"

Write-Host "Gerando pacote de deploy para $projectName..." -ForegroundColor Cyan

# 1. Rodar os testes de integridade antes do empacotamento
Write-Host "Executando suite de testes locais..." -ForegroundColor Yellow
& node "$sourceDir\tests\run_all.js"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Testes falharam. Empacotamento cancelado."
    exit 1
}

# 2. Criar diretorio temporario para selecao de arquivos limpos
$tempDir = Join-Path ([System.IO.Path]::GetTempPath()) "$projectName-$timestamp"
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null

# Lista de pastas e arquivos a copiar
$itemsToCopy = @(
    "package.json",
    "package-lock.json",
    "server.js",
    "pix.js",
    "render.yaml",
    "Dockerfile",
    ".dockerignore",
    ".gitignore",
    "README.md",
    "public",
    "data",
    "tests"
)

foreach ($item in $itemsToCopy) {
    $srcPath = Join-Path $sourceDir $item
    if (Test-Path $srcPath) {
        $destPath = Join-Path $tempDir $item
        Copy-Item -Path $srcPath -Destination $destPath -Recurse -Force
    }
}

# 3. Remover lixo e diretorios proibidos caso tenham entrado
$forbidden = @("node_modules", ".git", ".system_generated", "scratch", "*.log")
foreach ($forb in $forbidden) {
    Get-ChildItem -Path $tempDir -Recurse -Include $forb -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
}

# 4. Comprimir em arquivo ZIP
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}

Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory($tempDir, $zipPath)

# Limpar temporario
Remove-Item $tempDir -Recurse -Force

$zipSizeMB = [Math]::Round(((Get-Item $zipPath).Length / 1MB), 2)
Write-Host "Pacote ZIP pronto na Area de Trabalho!" -ForegroundColor Green
Write-Host "Local: $zipPath" -ForegroundColor White
Write-Host "Tamanho: $zipSizeMB MB" -ForegroundColor White
Write-Host "Pronto para upload no Render, Railway ou GitHub!" -ForegroundColor Yellow
