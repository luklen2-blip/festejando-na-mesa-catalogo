/**
 * Suíte Formal de Testes Locais de Integridade - Festejando na Mesa
 * Validação de dados, PIX EMV BACEN, CRC16, Endpoints e Servidor HTTP.
 */

const assert = require('assert');
const http = require('http');
const fs = require('fs');
const path = require('path');
const app = require('../server');
const { gerarPixCopiaECola, calculateCRC16 } = require('../pix');

console.log('🧁 [TESTES LOCAIS] Iniciando validação do projeto Festejando na Mesa...\n');

let passedTests = 0;
function test(name, fn) {
  try {
    fn();
    console.log(`  ✅ [PASS] ${name}`);
    passedTests++;
  } catch (err) {
    console.error(`  ❌ [FAIL] ${name}: ${err.message}`);
    process.exit(1);
  }
}

// 1. Integridade do Catálogo de Produtos
test('Validação de integridade do catálogo data/cardapio.json', () => {
  const filePath = path.join(__dirname, '..', 'data', 'cardapio.json');
  assert(fs.existsSync(filePath), 'cardapio.json deve existir');
  const cardapio = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  
  assert.strictEqual(cardapio.loja.nome, 'Festejando na Mesa');
  assert.strictEqual(cardapio.loja.whatsapp, '5521969579835');
  assert(cardapio.categorias.length >= 5, 'Deve conter pelo menos 5 categorias');

  const catIds = cardapio.categorias.map(c => c.id);
  assert(catIds.includes('combos'), 'Deve conter categoria combos');
  assert(catIds.includes('bolos'), 'Deve conter categoria bolos');
  assert(catIds.includes('docinhos'), 'Deve conter categoria docinhos');
  assert(catIds.includes('trufas'), 'Deve conter categoria trufas');
  assert(catIds.includes('decoracao'), 'Deve conter categoria decoracao');

  // Validar opções de massas e recheios
  assert(cardapio.opcoes_bolos.massas.length >= 2, 'Deve ter opções de massas');
  assert(cardapio.opcoes_bolos.recheios.length >= 5, 'Deve ter opções de recheios');
});

// 2. Validação do Módulo Oficial de PIX EMV e CRC16
test('Geração de PIX EMV com cálculo de redundância cíclica CRC16 oficial', () => {
  const pix = gerarPixCopiaECola({
    chave: '21969579835',
    nome: 'FESTEJANDO MESA',
    cidade: 'RIO DE JANEIRO',
    valor: 110.00,
    txid: 'PEDIDO123'
  });

  assert(pix.payload.startsWith('000201'), 'Payload deve iniciar com padrão 000201');
  assert(pix.payload.includes('br.gov.bcb.pix'), 'Payload deve conter o identificador br.gov.bcb.pix');
  assert(pix.payload.includes('21969579835'), 'Payload deve conter a chave PIX');
  assert.strictEqual(pix.valor, '110.00');

  // Validação do cálculo de CRC16
  const payloadSemCRC = pix.payload.substring(0, pix.payload.length - 4);
  const crcCalculado = calculateCRC16(payloadSemCRC);
  const crcOriginal = pix.payload.substring(pix.payload.length - 4);
  assert.strictEqual(crcCalculado, crcOriginal, 'CRC16 calculado deve bater exatamente com o payload');
});

// 3. Validação dos Assets das Imagens Fornecidas
test('Presença e validação das 10 imagens reais dos panfletos', () => {
  const assetsDir = path.join(__dirname, '..', 'public', 'assets');
  assert(fs.existsSync(assetsDir), 'Pasta assets deve existir');

  const requiredImages = [
    'bolinho_festa_100.jpg',
    'bolos_decorados_doce_lembranca.jpg',
    'docinhos_tradicionais_gourmet.jpg',
    'kit_festa_borboleta_azul.jpg',
    'kit_festa_mulher_maravilha.jpg',
    'kit_festa_princesas_lilas.jpg',
    'kit_festa_sonic.jpg',
    'mini_festa_partir_40.jpg',
    'mini_trufas_recheadas.jpg',
    'promocao_mini_festa_mesa.jpg'
  ];

  for (const img of requiredImages) {
    const full = path.join(assetsDir, img);
    assert(fs.existsSync(full), `Imagem ${img} deve estar presente`);
    assert(fs.statSync(full).size > 10000, `Imagem ${img} deve ter tamanho válido`);
  }

  // Validação do Vídeo Promocional Vertical
  const videoPath = path.join(assetsDir, 'video_promo.mp4');
  assert(fs.existsSync(videoPath), 'Vídeo promocional video_promo.mp4 deve existir');
  assert(fs.statSync(videoPath).size > 500000, 'Vídeo promocional deve ter mais de 500KB');
  console.log('  ✅ [PASS] Vídeo promocional vertical video_promo.mp4 validado');
});

// 4. Validação dos Endpoints HTTP
const server = app.listen(0, async () => {
  const port = server.address().port;
  const baseUrl = `http://localhost:${port}`;

  function request(urlPath, method = 'GET', postData = null) {
    return new Promise((resolve, reject) => {
      const u = new URL(urlPath, baseUrl);
      const options = {
        hostname: u.hostname,
        port: u.port,
        path: u.pathname,
        method: method,
        headers: {}
      };

      if (postData) {
        options.headers['Content-Type'] = 'application/json';
      }

      const req = http.request(options, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => resolve({ status: res.statusCode, body }));
      });

      req.on('error', reject);
      if (postData) req.write(JSON.stringify(postData));
      req.end();
    });
  }

  try {
    // 4.1 Health Check (/api/health)
    const resHealth = await request('/api/health');
    assert.strictEqual(resHealth.status, 200, 'Health check deve responder 200');
    const healthJson = JSON.parse(resHealth.body);
    assert.strictEqual(healthJson.status, 'ok');
    assert(healthJson.app.includes('Festejando na Mesa'));
    assert.strictEqual(healthJson.version, '2.0.0');
    console.log('  ✅ [PASS] Endpoint GET /api/health operacional com status 200');

    // 4.2 Endpoint /api/cardapio
    const resCardapio = await request('/api/cardapio');
    assert.strictEqual(resCardapio.status, 200, '/api/cardapio deve responder 200');
    const cardapioJson = JSON.parse(resCardapio.body);
    assert(cardapioJson.categorias.length >= 5);
    console.log('  ✅ [PASS] Endpoint GET /api/cardapio retornando catálogo completo');

    // 4.3 Endpoint /api/pix
    const resPix = await request('/api/pix', 'POST', { valor: 80.00 });
    assert.strictEqual(resPix.status, 200, '/api/pix deve responder 200');
    const pixData = JSON.parse(resPix.body);
    assert.strictEqual(pixData.ok, true);
    assert(pixData.payload.includes('br.gov.bcb.pix'));
    console.log('  ✅ [PASS] Endpoint POST /api/pix gerando payload oficial BACEN');

    server.close(() => {
      console.log(`\n🎉 [SUCESSO TOTAL] Todos os testes passaram com perfeição!`);
      process.exit(0);
    });
  } catch (err) {
    server.close();
    console.error(`\n❌ [FALHA]: ${err.message}`);
    process.exit(1);
  }
});
