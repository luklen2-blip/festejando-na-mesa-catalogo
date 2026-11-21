const express = require('express');
const path = require('path');
const fs = require('fs');
const { gerarPixCopiaECola } = require('./pix');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// Resolução universal e resiliente de estáticos (public/ e raiz)
const candidateDirs = [
  path.join(__dirname, 'public'),
  __dirname,
  path.join(process.cwd(), 'public'),
  process.cwd()
];

for (const dir of candidateDirs) {
  if (fs.existsSync(dir)) {
    app.use(express.static(dir));
  }
}

// Carregar dados estruturados do catálogo
const cardapioPath = path.join(__dirname, 'data', 'cardapio.json');
function getCardapio() {
  try {
    const raw = fs.readFileSync(cardapioPath, 'utf8');
    return JSON.parse(raw);
  } catch (err) {
    console.error('Erro ao ler cardapio.json:', err.message);
    return { loja: { nome: 'Festejando na Mesa' }, categorias: [] };
  }
}

// 1. Endpoint Obrigatório de Monitoramento 24/7 (/api/health)
app.get('/api/health', (req, res) => {
  res.status(200).json({
    status: 'ok',
    app: 'Festejando na Mesa - Catálogo Digital',
    version: '2.0.0',
    uptime_seconds: Math.floor(process.uptime()),
    timestamp: new Date().toISOString()
  });
});

// 2. Rota da API do Catálogo
app.get('/api/cardapio', (req, res) => {
  res.json(getCardapio());
});

// 3. Rota de Geração de PIX Nativo (EMV Banco Central)
app.post('/api/pix', (req, res) => {
  try {
    const { valor, txid } = req.body;
    const cardapio = getCardapio();
    const pixData = gerarPixCopiaECola({
      chave: cardapio.loja.chave_pix || '21969579835',
      nome: cardapio.loja.titular_pix || 'Festejando na Mesa',
      cidade: cardapio.loja.cidade_pix || 'RIO DE JANEIRO',
      valor: valor || 0,
      txid: txid || 'FESTA'
    });
    res.json({ ok: true, ...pixData });
  } catch (err) {
    res.status(400).json({ ok: false, error: err.message });
  }
});

// 4. Rotas Legais & Conformidade (LGPD, Termos e Privacidade)
app.get('/termos', (req, res) => {
  const file = path.join(__dirname, 'public', 'termos.html');
  if (fs.existsSync(file)) return res.sendFile(file);
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/privacidade', (req, res) => {
  const file = path.join(__dirname, 'public', 'privacidade.html');
  if (fs.existsSync(file)) return res.sendFile(file);
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// 5. SPA Fallback Universal
app.get('*', (req, res) => {
  const indexPath = path.join(__dirname, 'public', 'index.html');
  if (fs.existsSync(indexPath)) {
    return res.sendFile(indexPath);
  }
  res.status(404).send('Festejando na Mesa - Catálogo Digital em Inicialização');
});

if (require.main === module) {
  app.listen(PORT, '0.0.0.0', () => {
    console.log(`🎂 [FESTEJANDO NA MESA] Servidor 24/7 rodando na porta ${PORT}`);
    console.log(`📊 Health Check: http://localhost:${PORT}/api/health`);
    console.log(`📱 Catálogo Digital: http://localhost:${PORT}`);
  });
}

module.exports = app;