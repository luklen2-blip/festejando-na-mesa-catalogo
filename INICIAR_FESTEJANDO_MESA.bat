@echo off
title FESTEJANDO NA MESA - CATALOGO DIGITAL 24/7
color 0D
chcp 65001 >nul

echo ===================================================================
echo   🎂 FESTEJANDO NA MESA - CATÁLOGO DIGITAL & PEDIDOS WHATSAPP
echo   Bolos Decorados • Doces Gourmet • Decoração Pegue e Monte
echo   Senador Vasconcelos - RJ • WhatsApp: (21) 96957-9835
echo ===================================================================
echo.

:: 1. Entrar diretamente na pasta do projeto
cd /d "c:\Users\luciano\.gemini\antigravity\scratch\festejando-na-mesa-catalogo"

:: 2. Validar arquivos vitais
if not exist "server.js" (
  echo [ERRO] Arquivo server.js nao encontrado!
  pause
  exit /b 1
)

:: 3. Abrir o navegador no catálogo local
echo [1/2] Abrindo Catálogo Digital no seu navegador...
timeout /t 2 /nobreak >nul
start "" http://localhost:3000

echo [2/2] Servidor 24/7 ativo com monitoramento de saúde!
echo.
echo ===================================================================
echo   Acesso Local: http://localhost:3000
echo   Health Check: http://localhost:3000/api/health
echo   API Cardápio: http://localhost:3000/api/cardapio
echo   Termos & LGPD: http://localhost:3000/termos
echo.
echo   Para encerrar o catálogo, basta fechar esta janela.
echo ===================================================================
echo.
node server.js
