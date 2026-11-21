# 🎂 Festejando na Mesa — Catálogo Digital Interativo 24/7

> **Bolos Decorados • Doces Gourmet • Decoração Pegue & Monte**  
> *"Doces momentos, lembranças que ficam!"* • Senador Vasconcelos – Rio de Janeiro / RJ

---

## 🌟 Visão Geral

Catálogo digital de alta conversão desenvolvido para **Festejando na Mesa**, integrando vitrine de produtos, seletor interativo de massas/recheios, cálculo dinâmico de sinal (50%) ou valor integral, checkout com **PIX Banco Central Oficial (EMV QR Code + Copia-e-Cola)** e envio estruturado de pedidos diretamente para o WhatsApp oficial **(21) 96957-9835**.

---

## 🚀 Arquitetura & Recursos

1. **Monitoramento 24/7 de Saúde (`/api/health`):**
   - Retorna status HTTP 200, versão, tempo de atividade e timestamp para monitoramento contínuo em nuvem (Render, Railway, UptimeRobot).
2. **API Estruturada do Cardápio (`/api/cardapio`):**
   - Dados completos de categorias:
     - 🌟 **Combos Mini Festa na Mesa:** Opção 1 (R$ 220), Opção 2 (R$ 150) e Básica (R$ 40).
     - 🎂 **Bolos Decorados "Doce Lembrança":** 15cm (R$ 150), 20cm (R$ 180), 25cm (R$ 220) e 30cm (R$ 260) com personalização de massas amanteigada/chocolate e 7 opções de recheios.
     - 🍰 **Bolinho de Festa Econômico:** R$ 100 (30 fatias, 2 camadas de recheio fartas).
     - 🍬 **Docinhos Tradicionais & Gourmet:** Cento a R$ 110 e R$ 165, docinhos avulsos e pirulitos de chocolate.
     - 🍫 **Mini Trufas Recheadas:** Cento a R$ 140 (até 4 sabores) ou a partir de 50 un a R$ 2,00 cada.
     - 🎈 **Kits Pegue e Monte:** Princesas, Mulher Maravilha, Sonic e Borboleta Azul.
3. **Módulo Oficial de PIX Banco Central (`/api/pix`):**
   - Geração de BR Code EMV padrão oficial Bacen com cálculo de redundância cíclica **CRC-16/CCITT-FALSE**.
   - Geração dinâmica de QR Code e Copia-e-Cola em tempo real.
4. **Fechamento Ágil no WhatsApp:**
   - Botão "Enviar Pedido" que gera texto formatado com nome do cliente, data da festa, tema, itens com personalizações, subtotal, sinal e endereço de retirada.
5. **Conformidade Legal & LGPD:**
   - Termos de Uso e Condições de Encomenda (`/termos`).
   - Política de Privacidade com foco na LGPD e proteção de menores (`/privacidade`).
   - Alerta destacado de alérgenos e orientações de transporte (desencorajando uso de Uber Entregas para bolos artesanais).

---

## 🛠️ Comandos Rápidos

```bash
# Instalar dependências
npm install

# Executar suíte de testes locais de integridade
npm test

# Iniciar servidor localmente
npm start

# Teste ao vivo na nuvem (Live Cloud E2E)
node tests/test_cloud_live.js <URL_DO_DEPLOY>
```

---

## ☁️ Deploy Contínuo no Render.com

1. Crie um novo Web Service apontando para este repositório ou faça upload do arquivo `festejando-na-mesa-catalogo-DEPLOY-PRODUCAO.zip`.
2. O arquivo `render.yaml` configura automaticamente:
   - **Ambiente:** Node.js 20
   - **Comando de Build:** `npm test`
   - **Comando de Início:** `node server.js`
   - **Health Check Path:** `/api/health`
   - **Porta:** 3000
