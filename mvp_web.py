import json
import argparse
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "mvp_educativo_registros.json"
HOST = "127.0.0.1"
PORT = 8000


HTML = """<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Memória Inteligente de Aprendizagem</title>
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#176b5b">
  <style>
    :root {
      color-scheme: light;
      --bg: #f7f8f4;
      --panel: #ffffff;
      --text: #17201b;
      --muted: #5f6b63;
      --line: #d8ded7;
      --primary: #176b5b;
      --primary-dark: #0f4d43;
      --accent: #d58b2f;
      --danger: #9d2d2d;
      --shadow: 0 10px 28px rgba(25, 38, 31, 0.08);
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.4;
    }

    header {
      position: sticky;
      top: 0;
      z-index: 2;
      background: rgba(247, 248, 244, 0.96);
      border-bottom: 1px solid var(--line);
      backdrop-filter: blur(10px);
    }

    .wrap {
      width: min(100%, 760px);
      margin: 0 auto;
      padding: 16px;
    }

    .topbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }

    .brand {
      display: grid;
      gap: 4px;
    }

    h1 {
      margin: 0;
      font-size: 1.6rem;
      letter-spacing: 0;
    }

    .brand-short {
      color: var(--muted);
      font-size: 0.92rem;
      font-weight: 650;
    }

    .status {
      min-height: 22px;
      color: var(--muted);
      font-size: 0.92rem;
    }

    main {
      padding: 12px 0 28px;
    }

    section {
      margin: 0 0 18px;
    }

    .home-screen {
      display: none;
    }

    .home-screen.active {
      display: block;
    }

    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
      padding: 16px;
    }

    .screen {
      display: none;
    }

    .screen.active {
      display: block;
    }

    h2 {
      margin: 0 0 12px;
      font-size: 1rem;
      letter-spacing: 0;
    }

    label {
      display: block;
      margin: 12px 0 6px;
      color: var(--muted);
      font-size: 0.94rem;
      font-weight: 650;
    }

    input,
    select,
    textarea,
    button {
      width: 100%;
      min-height: 44px;
      border-radius: 8px;
      font: inherit;
    }

    input,
    select,
    textarea {
      border: 1px solid var(--line);
      background: #fff;
      color: var(--text);
      padding: 10px 12px;
    }

    textarea {
      min-height: 104px;
      resize: vertical;
    }

    .row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }

    .actions {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-top: 14px;
    }

    button,
    .button {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border: 0;
      background: var(--primary);
      color: #fff;
      cursor: pointer;
      font-weight: 750;
      text-decoration: none;
      padding: 10px 12px;
      white-space: normal;
    }

    button:hover,
    .button:hover {
      background: var(--primary-dark);
    }

    .secondary {
      background: #ecefeb;
      color: var(--text);
    }

    .secondary:hover {
      background: #dfe5de;
    }

    .danger {
      background: #9d2d2d;
    }

    .danger:hover {
      background: #7f2222;
    }

    .intro {
      color: var(--muted);
      font-size: 1.02rem;
    }

    .hero-card {
      padding: 20px;
    }

    .hero-card h2 {
      font-size: 1.35rem;
      margin-bottom: 14px;
    }

    .hero-card .intro {
      margin: 0 0 10px;
    }

    .time-note {
      margin: 12px 0 0;
      color: var(--primary-dark);
      font-size: 0.95rem;
      font-weight: 750;
    }

    .mode-grid {
      display: grid;
      gap: 12px;
    }

    .mode-card {
      display: grid;
      gap: 12px;
      border: 1px solid var(--line);
      border-left: 4px solid var(--primary);
      border-radius: 8px;
      background: #fff;
      color: var(--text);
      padding: 14px;
    }

    .mode-card h3 {
      margin: 0 0 4px;
      font-size: 1.04rem;
      letter-spacing: 0;
    }

    .mode-card p {
      margin: 0;
      color: var(--muted);
    }

    .mode-card button {
      justify-self: start;
      width: auto;
      min-width: 180px;
    }

    .primary-cta {
      min-height: 64px;
      margin-top: 16px;
      font-size: 1.14rem;
      background: var(--primary);
      box-shadow: 0 8px 20px rgba(23, 107, 91, 0.18);
    }

    .secondary-nav {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      margin-top: 12px;
    }

    .secondary-nav button {
      min-height: 42px;
      border: 1px solid var(--line);
      background: #ecefeb;
      color: var(--text);
      font-size: 0.94rem;
    }

    .principles {
      margin: 0;
      padding-left: 22px;
    }

    .principles li {
      margin: 8px 0;
    }

    .summary {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 10px;
      color: var(--muted);
      font-size: 0.94rem;
    }

    .record-list {
      display: grid;
      gap: 10px;
    }

    .record {
      border: 1px solid var(--line);
      border-left: 4px solid var(--accent);
      border-radius: 8px;
      background: #fff;
      padding: 12px;
    }

    .record strong {
      display: block;
      margin-bottom: 4px;
      font-size: 0.98rem;
    }

    .today-list {
      display: grid;
      gap: 8px;
      margin-top: 10px;
    }

    .today-item {
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      padding: 10px;
    }

    .meta {
      color: var(--muted);
      font-size: 0.86rem;
      margin-bottom: 8px;
    }

    .empty,
    .error {
      border: 1px dashed var(--line);
      border-radius: 8px;
      color: var(--muted);
      padding: 14px;
    }

    .error {
      border-color: #e0b4b4;
      color: var(--danger);
    }

    @media (max-width: 560px) {
      .wrap {
        padding: 12px;
      }

      .topbar,
      .row,
      .actions,
      .secondary-nav {
        grid-template-columns: 1fr;
        flex-direction: column;
        align-items: stretch;
      }

      h1 {
        font-size: 1.45rem;
      }

      .hero-card {
        padding: 16px;
      }

      .mode-card button {
        width: 100%;
      }
    }
  </style>
</head>
<body>
  <header>
    <div class="wrap">
      <div class="topbar">
        <div class="brand" aria-label="Memória Inteligente de Aprendizagem">
          <h1>MIM</h1>
          <span class="brand-short">Memória Inteligente de Aprendizagem</span>
        </div>
      </div>
    </div>
  </header>

  <main class="wrap">
    <section id="inicio" class="home-screen screen active">
      <div class="panel hero-card">
        <h2>Bem-vindo ao MIM</h2>
        <p class="intro">Registre rapidamente evidências da sua aula.</p>
        <p class="intro">O MIM ajuda a transformar observações em memória pedagógica.</p>
        <p class="time-note">⏱ Menos de 1 minuto</p>
        <button class="primary-cta" type="button" data-screen="registro">+ Registrar Aula</button>
      </div>
      <div class="secondary-nav" aria-label="Navegação secundária">
        <button class="secondary" type="button" data-screen="lista">Ver Registros</button>
        <button class="secondary" type="button" data-screen="sobre">Sobre o MIM</button>
        <button class="secondary" type="button" data-screen="ferramentas">Ferramentas</button>
      </div>
    </section>

    <section id="registro" class="panel screen">
      <h2>Como você quer observar hoje?</h2>
      <div class="mode-grid" id="modo-escolha">
        <article class="mode-card">
          <div>
            <h3>Observação Essencial</h3>
            <p>Registrar uma observação principal da aula.</p>
          </div>
          <button type="button" data-mode="essencial">Escolher modo essencial</button>
        </article>
        <article class="mode-card">
          <div>
            <h3>Observação Investigativa</h3>
            <p>Registrar múltiplas evidências ao longo do dia.</p>
          </div>
          <button type="button" data-mode="investigativa">Escolher modo investigativo</button>
        </article>
      </div>

      <form id="essencial-form" hidden>
        <label for="foco">Foco de observação</label>
        <select id="foco" name="foco" required>
          <option value="">Escolha um foco</option>
          <option>Leitura</option>
          <option>Escrita</option>
          <option>Participação</option>
          <option>Comportamento</option>
          <option>Grupo A</option>
          <option>Grupo B</option>
          <option>Grupo C</option>
          <option>Outro</option>
        </select>

        <label for="observacao-essencial">O que você observou?</label>
        <textarea id="observacao-essencial" name="observacao" maxlength="900" required></textarea>

        <div class="actions">
          <button type="submit">Salvar registro essencial</button>
          <button class="secondary" type="button" data-voltar-modos>Voltar</button>
        </div>
      </form>

      <div id="investigativa-form" hidden>
        <label for="observacao-investigativa">Registrar observação</label>
        <textarea id="observacao-investigativa" maxlength="900"></textarea>

        <div class="actions">
          <button type="button" id="salvar-observacao-investigativa">+ Salvar observação</button>
          <button class="secondary" type="button" data-voltar-modos>Voltar</button>
        </div>

        <h2>Registros de hoje</h2>
        <div id="registros-hoje" class="today-list">
          <div class="empty">Nenhuma observação registrada hoje.</div>
        </div>

        <button type="button" id="finalizar-investigativa">Finalizar observações do dia</button>
      </div>
      <p class="status" id="status" aria-live="polite"></p>
    </section>

    <section class="panel screen" id="lista">
      <div class="summary">
        <h2>Registros anteriores</h2>
        <span id="contador">0 registros</span>
      </div>
      <div id="registros" class="record-list"></div>
    </section>

    <section id="sobre" class="panel screen">
      <h2>Sobre o MIM</h2>
      <p class="intro">O professor inicia sua prática observando as evidências de aprendizagem e, a partir delas, realiza mediações que favorecem o desenvolvimento dos estudantes.</p>
      <ol class="principles">
        <li>O professor inicia sua prática observando as evidências de aprendizagem e, a partir delas, realiza mediações que favorecem o desenvolvimento dos estudantes.</li>
        <li>O MIM adapta-se ao modo como o professor deseja observar: de forma essencial ou investigativa.</li>
        <li>A observação antecede a intervenção.</li>
        <li>A evidência antecede a classificação.</li>
        <li>O registro deve ser rápido, humano e significativo.</li>
        <li>A tecnologia deve reduzir burocracias e ampliar a reflexão pedagógica.</li>
        <li>O julgamento pedagógico permanece humano.</li>
      </ol>
    </section>

    <section id="ferramentas" class="panel screen">
      <h2>Ferramentas</h2>
      <div class="actions">
        <a class="button secondary" href="/export/registros.json" download>Exportar JSON</a>
        <button class="danger" type="button" id="limpar-registros">Limpar registros</button>
      </div>
    </section>
  </main>

  <script>
    const modoEscolha = document.querySelector("#modo-escolha");
    const essencialForm = document.querySelector("#essencial-form");
    const investigativaForm = document.querySelector("#investigativa-form");
    const observacaoInvestigativaEl = document.querySelector("#observacao-investigativa");
    const registrosHojeEl = document.querySelector("#registros-hoje");
    const salvarObservacaoInvestigativaBtn = document.querySelector("#salvar-observacao-investigativa");
    const finalizarInvestigativaBtn = document.querySelector("#finalizar-investigativa");
    const statusEl = document.querySelector("#status");
    const listaEl = document.querySelector("#registros");
    const contadorEl = document.querySelector("#contador");
    const limparRegistrosBtn = document.querySelector("#limpar-registros");
    const telas = document.querySelectorAll(".screen");
    const botoesTela = document.querySelectorAll("[data-screen]");
    let observacoesInvestigativas = [];

    function abrirTela(id) {
      telas.forEach((tela) => {
        tela.classList.toggle("active", tela.id === id);
      });
      document.querySelectorAll(".nav-button").forEach((botao) => {
        botao.classList.toggle("active", botao.dataset.screen === id);
      });
    }

    botoesTela.forEach((botao) => {
      botao.addEventListener("click", () => abrirTela(botao.dataset.screen));
    });

    function textoSeguro(valor) {
      return String(valor || "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }

    function mostrarEscolhaDeModo(mensagem = "") {
      modoEscolha.hidden = false;
      essencialForm.hidden = true;
      investigativaForm.hidden = true;
      statusEl.textContent = mensagem;
    }

    function horaAtual() {
      return new Date().toLocaleTimeString("pt-BR", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      });
    }

    function renderizarRegistrosHoje() {
      registrosHojeEl.innerHTML = "";
      if (!observacoesInvestigativas.length) {
        registrosHojeEl.innerHTML = '<div class="empty">Nenhuma observação registrada hoje.</div>';
        return;
      }

      observacoesInvestigativas.forEach((observacao) => {
        const item = document.createElement("div");
        item.className = "today-item";
        item.innerHTML = `
          <div class="meta">${textoSeguro(observacao.hora)}</div>
          <p>${textoSeguro(observacao.texto)}</p>
        `;
        registrosHojeEl.appendChild(item);
      });
    }

    function tituloRegistro(registro) {
      if (registro.modo === "observacao_essencial") {
        return `Observação Essencial · ${registro.foco}`;
      }
      if (registro.modo === "observacao_investigativa") {
        return "Observação Investigativa";
      }
      return registro.titulo || "Registro pedagógico";
    }

    function metaRegistro(registro) {
      if (registro.modo === "observacao_investigativa") {
        return `${registro.data} ${registro.hora_inicio} - ${registro.hora_finalizacao}`;
      }
      return `${registro.data} ${registro.hora}`;
    }

    function corpoRegistro(registro) {
      if (registro.modo === "observacao_investigativa") {
        const itens = (registro.observacoes || [])
          .map((observacao) => `<p><strong>${textoSeguro(observacao.hora)}</strong> ${textoSeguro(observacao.texto)}</p>`)
          .join("");
        return `<p>${textoSeguro(registro.sintese)}</p>${itens}`;
      }
      return `<p>${textoSeguro(registro.observacao)}</p>`;
    }

    function renderizar(registros) {
      contadorEl.textContent = `${registros.length} ${registros.length === 1 ? "registro" : "registros"}`;
      listaEl.innerHTML = "";

      if (!registros.length) {
        listaEl.innerHTML = '<div class="empty">Nenhum registro salvo ainda.</div>';
        return;
      }

      registros.slice().reverse().forEach((registro) => {
        const artigo = document.createElement("article");
        artigo.className = "record";
        const evidencias = registro.evidencias
          ? `<p><strong>Evidências:</strong> ${textoSeguro(registro.evidencias)}</p>`
          : "";
        const feedback = registro.feedback_professor
          ? `<p><strong>Feedback:</strong> ${textoSeguro(registro.feedback_professor)}</p>`
          : "";
        artigo.innerHTML = `
          <strong>${textoSeguro(tituloRegistro(registro))}</strong>
          <div class="meta">${textoSeguro(metaRegistro(registro))}</div>
          ${corpoRegistro(registro)}
          ${evidencias}
          ${feedback}
        `;
        listaEl.appendChild(artigo);
      });
    }

    async function carregarRegistros() {
      const resposta = await fetch("/api/registros");
      if (!resposta.ok) {
        throw new Error("Não foi possível carregar os registros.");
      }
      renderizar(await resposta.json());
    }

    document.querySelectorAll("[data-mode]").forEach((botao) => {
      botao.addEventListener("click", () => {
        modoEscolha.hidden = true;
        essencialForm.hidden = botao.dataset.mode !== "essencial";
        investigativaForm.hidden = botao.dataset.mode !== "investigativa";
        statusEl.textContent = "";
      });
    });

    document.querySelectorAll("[data-voltar-modos]").forEach((botao) => {
      botao.addEventListener("click", mostrarEscolhaDeModo);
    });

    essencialForm.addEventListener("submit", async (evento) => {
      evento.preventDefault();
      statusEl.textContent = "Salvando...";
      const dados = {
        modo: "observacao_essencial",
        ...Object.fromEntries(new FormData(essencialForm).entries()),
      };

      const resposta = await fetch("/api/registros", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(dados),
      });

      const corpo = await resposta.json();
      if (!resposta.ok) {
        statusEl.textContent = corpo.erro || "Erro ao salvar.";
        return;
      }

      essencialForm.reset();
      renderizar(corpo.registros);
      mostrarEscolhaDeModo("Registro salvo localmente.");
    });

    salvarObservacaoInvestigativaBtn.addEventListener("click", () => {
      const texto = observacaoInvestigativaEl.value.trim();
      if (!texto) {
        statusEl.textContent = "Informe a observação.";
        return;
      }
      observacoesInvestigativas.push({hora: horaAtual(), texto});
      observacaoInvestigativaEl.value = "";
      statusEl.textContent = "Observação adicionada.";
      renderizarRegistrosHoje();
    });

    finalizarInvestigativaBtn.addEventListener("click", async () => {
      if (!observacoesInvestigativas.length) {
        statusEl.textContent = "Salve ao menos uma observação.";
        return;
      }

      statusEl.textContent = "Finalizando...";
      const resposta = await fetch("/api/registros", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          modo: "observacao_investigativa",
          observacoes: observacoesInvestigativas,
        }),
      });

      const corpo = await resposta.json();
      if (!resposta.ok) {
        statusEl.textContent = corpo.erro || "Erro ao finalizar.";
        return;
      }

      observacoesInvestigativas = [];
      renderizarRegistrosHoje();
      renderizar(corpo.registros);
      mostrarEscolhaDeModo(corpo.registro.sintese);
    });

    limparRegistrosBtn.addEventListener("click", async () => {
      const confirmado = window.confirm("Limpar todos os registros locais?");
      if (!confirmado) {
        return;
      }

      const resposta = await fetch("/api/registros", {method: "DELETE"});
      if (!resposta.ok) {
        statusEl.textContent = "Erro ao limpar registros.";
        return;
      }
      renderizar([]);
      statusEl.textContent = "Registros limpos.";
    });

    carregarRegistros().catch((erro) => {
      listaEl.innerHTML = `<div class="error">${erro.message}</div>`;
    });

    if ("serviceWorker" in navigator) {
      navigator.serviceWorker.register("/service-worker.js").catch(() => {});
    }
  </script>
</body>
</html>
"""

MANIFEST = {
    "name": "Memória Inteligente de Aprendizagem",
    "short_name": "MIM",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#f7f8f4",
    "theme_color": "#176b5b",
}

SERVICE_WORKER = """const CACHE = "mim-v2";

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(["/"])));
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") {
    return;
  }
  event.respondWith(fetch(event.request).catch(() => caches.match(event.request)));
});
"""


def carregar_registros(caminho=DATA_FILE):
    caminho = Path(caminho)
    if not caminho.exists():
        return []
    conteudo = caminho.read_text(encoding="utf-8").strip()
    if not conteudo:
        return []
    return json.loads(conteudo)


def salvar_registros(registros, caminho=DATA_FILE):
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(registros, ensure_ascii=False, indent=2), encoding="utf-8")


FOCOS_OBSERVACAO = (
    "Leitura",
    "Escrita",
    "Participação",
    "Comportamento",
    "Grupo A",
    "Grupo B",
    "Grupo C",
    "Outro",
)


def listar_registros(caminho=DATA_FILE):
    return carregar_registros(caminho)


def exportar_registros_json(caminho=DATA_FILE):
    return json.dumps(listar_registros(caminho), ensure_ascii=False, indent=2)


def limpar_registros(caminho=DATA_FILE):
    salvar_registros([], caminho)
    return []


def criar_registro_essencial(dados, data_hora=None):
    if data_hora is None:
        data_hora = datetime.now()

    foco = dados.get("foco", "").strip()
    if foco not in FOCOS_OBSERVACAO:
        focos = ", ".join(FOCOS_OBSERVACAO)
        raise ValueError(f"Escolha um foco de observação: {focos}.")

    observacao = dados.get("observacao", "").strip()
    if not observacao:
        raise ValueError("Informe o que você observou.")

    return {
        "modo": "observacao_essencial",
        "foco": foco,
        "observacao": observacao[:900],
        "data": data_hora.strftime("%Y-%m-%d"),
        "hora": data_hora.strftime("%H:%M:%S"),
    }


def criar_registro_investigativo(dados, data_hora=None):
    if data_hora is None:
        data_hora = datetime.now()

    observacoes = []
    for item in dados.get("observacoes", []):
        texto = str(item.get("texto", "")).strip()
        if texto:
            observacoes.append(
                {
                    "hora": str(item.get("hora") or data_hora.strftime("%H:%M:%S")).strip()[:8],
                    "texto": texto[:900],
                }
            )

    if not observacoes:
        raise ValueError("Salve ao menos uma observação.")

    quantidade = len(observacoes)
    return {
        "modo": "observacao_investigativa",
        "observacoes": observacoes,
        "quantidade_observacoes": quantidade,
        "sintese": f"Hoje foram registradas {quantidade} observações.",
        "data": data_hora.strftime("%Y-%m-%d"),
        "hora_inicio": observacoes[0]["hora"],
        "hora_finalizacao": data_hora.strftime("%H:%M:%S"),
    }


def criar_registro_mim(dados, data_hora=None):
    modo = dados.get("modo", "").strip()
    if modo == "observacao_essencial":
        return criar_registro_essencial(dados, data_hora)
    if modo == "observacao_investigativa":
        return criar_registro_investigativo(dados, data_hora)
    raise ValueError("Escolha um modo de observação.")


def adicionar_registro_mim(dados, caminho=DATA_FILE, data_hora=None):
    registros = carregar_registros(caminho)
    registro = criar_registro_mim(dados, data_hora)
    registros.append(registro)
    salvar_registros(registros, caminho)
    return registro, registros


class MIMHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        caminho = urlparse(self.path).path
        if caminho == "/":
            self.responder(HTTPStatus.OK, HTML, "text/html; charset=utf-8")
            return
        if caminho == "/api/registros":
            self.responder_json(HTTPStatus.OK, listar_registros())
            return
        if caminho == "/api/health":
            self.responder_json(HTTPStatus.OK, {"status": "ok", "app": "mim"})
            return
        if caminho == "/manifest.json":
            self.responder_json(HTTPStatus.OK, MANIFEST)
            return
        if caminho == "/service-worker.js":
            self.responder(HTTPStatus.OK, SERVICE_WORKER, "text/javascript; charset=utf-8")
            return
        if caminho == "/export/registros.json":
            conteudo = exportar_registros_json()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Disposition", 'attachment; filename="mim-registros.json"')
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))
            return
        self.responder_json(HTTPStatus.NOT_FOUND, {"erro": "Rota não encontrada."})

    def do_POST(self):
        caminho = urlparse(self.path).path
        if caminho != "/api/registros":
            self.responder_json(HTTPStatus.NOT_FOUND, {"erro": "Rota não encontrada."})
            return

        tamanho = int(self.headers.get("Content-Length", "0"))
        try:
            dados = json.loads(self.rfile.read(tamanho).decode("utf-8"))
            registro, registros = adicionar_registro_mim(dados)
        except (json.JSONDecodeError, ValueError) as erro:
            self.responder_json(HTTPStatus.BAD_REQUEST, {"erro": str(erro)})
            return

        self.responder_json(HTTPStatus.CREATED, {"registro": registro, "registros": registros})

    def do_DELETE(self):
        caminho = urlparse(self.path).path
        if caminho != "/api/registros":
            self.responder_json(HTTPStatus.NOT_FOUND, {"erro": "Rota não encontrada."})
            return

        self.responder_json(HTTPStatus.OK, {"registros": limpar_registros()})

    def log_message(self, formato, *args):
        print("%s - %s" % (self.address_string(), formato % args))

    def responder(self, status, corpo, content_type):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(corpo.encode("utf-8"))

    def responder_json(self, status, dados):
        self.responder(
            status,
            json.dumps(dados, ensure_ascii=False),
            "application/json; charset=utf-8",
        )


def executar_servidor(host=HOST, port=PORT):
    servidor = ThreadingHTTPServer((host, port), MIMHandler)
    print(f"MIM rodando em http://{host}:{port}")
    print(f"Registros locais: {DATA_FILE}")
    servidor.serve_forever()


def parse_args():
    parser = argparse.ArgumentParser(description="Memória Inteligente de Aprendizagem")
    parser.add_argument("--host", default=HOST, help="Host do servidor. Use 0.0.0.0 para testar no celular.")
    parser.add_argument("--port", default=PORT, type=int, help="Porta do servidor.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    executar_servidor(args.host, args.port)
