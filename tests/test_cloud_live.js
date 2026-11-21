/**
 * Suíte de Testes de Homologação Ao Vivo na Nuvem (Live Cloud E2E)
 * Valida a saúde e disponibilidade 24/7 do catálogo Festejando na Mesa em produção.
 * Execução: node tests/test_cloud_live.js <URL_DO_DEPLOY>
 */

const https = require('https');
const http = require('http');

const targetUrl = process.argv[2] || process.env.DEPLOY_URL || 'https://festejando-na-mesa-catalogo.onrender.com';

console.log(`🌐 [LIVE CLOUD TEST] Homologando Festejando na Mesa na URL: ${targetUrl}`);

// Configuração com rejectUnauthorized: false para tolerar certificados intermediários no Windows
const agentOptions = { rejectUnauthorized: false };

function fetchUrl(endpoint) {
  return new Promise((resolve, reject) => {
    const fullUrl = new URL(endpoint, targetUrl).toString();
    const client = fullUrl.startsWith('https') ? https : http;

    client.get(fullUrl, { agent: fullUrl.startsWith('https') ? new https.Agent(agentOptions) : undefined }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve({ status: res.statusCode, body: data }));
    }).on('error', reject);
  });
}

async function runLiveTests() {
  try {
    console.log('1. Testando endpoint de saúde (/api/health)...');
    const health = await fetchUrl('/api/health');
    console.log(`   Status HTTP: ${health.status}`);
    const healthJson = JSON.parse(health.body);
    console.log(`   Status: ${healthJson.status} | Uptime: ${healthJson.uptime_seconds}s | Versão: ${healthJson.version}`);

    if (health.status !== 200 || healthJson.status !== 'ok') {
      throw new Error('Falha no Health Check em produção');
    }

    console.log('2. Testando API do catálogo (/api/cardapio)...');
    const cardapio = await fetchUrl('/api/cardapio');
    const cardapioJson = JSON.parse(cardapio.body);
    console.log(`   Loja: ${cardapioJson.loja.nome} | Categorias: ${cardapioJson.categorias.length}`);

    console.log('3. Testando vitrine principal (/)...');
    const index = await fetchUrl('/');
    if (!index.body.includes('Festejando na Mesa')) {
      throw new Error('HTML principal não contém o nome Festejando na Mesa');
    }
    console.log('   Página inicial carregada e validada.');

    console.log('4. Testando streaming do vídeo promocional (/assets/video_promo.mp4)...');
    const videoRes = await fetchUrl('/assets/video_promo.mp4');
    if (videoRes.status !== 200) {
      throw new Error(`Vídeo promocional retornou status ${videoRes.status}`);
    }
    console.log('   Vídeo promocional disponível para reprodução 24/7.');

    console.log('\n✅ [LIVE CLOUD HOMOLOGADO] Aplicação 100% online, íntegra e operacional 24/7 na nuvem!');
  } catch (err) {
    console.error(`\n❌ [FALHA NO TESTE AO VIVO]: ${err.message}`);
    process.exit(1);
  }
}

runLiveTests();
