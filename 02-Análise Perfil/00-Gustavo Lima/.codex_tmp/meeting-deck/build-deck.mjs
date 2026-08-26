import fs from "node:fs/promises";
import path from "node:path";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const OUT = process.env.FINAL_PPTX;
const TMP = process.env.TMP_DIR;

if (!OUT || !TMP) {
  throw new Error("FINAL_PPTX e TMP_DIR precisam estar definidos.");
}

const W = 1280;
const H = 720;
const M = 52;
const FONT = "Arial";

const C = {
  white: "#FFFFFF",
  black: "#111111",
  ink: "#202124",
  gray: "#F2F2F2",
  gray2: "#E7E9EC",
  rule: "#B8BCC4",
  muted: "#626870",
  lightBlue: "#6DCBF4",
  blue: "#3D8DFF",
  navy: "#123454",
  gold: "#F4B740",
  paleGold: "#FFF3D2",
  green: "#2F9E67",
  paleGreen: "#E3F5EB",
  red: "#D94C4C",
  paleRed: "#FCE8E8",
};

const SOURCES = {
  sheet: "Google Sheets - Analise de Crescimento de Autoridade - Gustavo Lima / Postagens 2026 / agosto de 2026",
  instagram: "Instagram Insights - @gustavojcluz - publicacoes de 03 a 18/08/2026",
  screenshot: "file:///C:/Users/Jcluz/Pictures/Screenshots/Captura%20de%20tela%202026-08-20%20095021.png",
  dossier: "file:///C:/Users/Jcluz/Antigravity/00-Arquitetura-de-Informacoes/02%20Informa%C3%A7%C3%B5es%20Mercado/Dossie%20do%20Mercado.pdf",
  persona: "file:///C:/Users/Jcluz/Antigravity/00-Arquitetura-de-Informacoes/02%20Informa%C3%A7%C3%B5es%20Mercado/Persona%202025%20%E2%80%94%20Lannister%20(CNPJ%20familiar)%20Estudo.pdf",
  awareness: "https://www.facebook.com/business/ads/ad-objectives/awareness",
  objectives: "https://www.facebook.com/business/ads/ad-objectives?locale=en_GB",
  leads: "https://www.facebook.com/business/ads/ad-objectives/lead-generation?locale=en_GB",
  messages: "https://www.facebook.com/business/ads/click-to-message-ads",
  retargeting: "https://www.facebook.com/business/goals/retargeting",
};

const PT_WORDS = {
  acoes: "ações",
  aderencia: "aderência",
  alguem: "alguém",
  analise: "análise",
  anuncio: "anúncio",
  anuncios: "anúncios",
  aprovacao: "aprovação",
  atribuicao: "atribuição",
  atribuido: "atribuído",
  atencao: "atenção",
  ate: "até",
  atraves: "através",
  audiencia: "audiência",
  automatico: "automático",
  automatica: "automática",
  avanca: "avança",
  carencia: "carência",
  clausula: "cláusula",
  comeca: "começa",
  comparacao: "comparação",
  competencia: "competência",
  confianca: "confiança",
  conteudo: "conteúdo",
  conteudos: "conteúdos",
  constroi: "constrói",
  cotacao: "cotação",
  cotacoes: "cotações",
  crencas: "crenças",
  decisao: "decisão",
  direcao: "direção",
  distancia: "distância",
  distribuicao: "distribuição",
  divisao: "divisão",
  dominio: "domínio",
  disposicao: "disposição",
  duvida: "dúvida",
  duvidas: "dúvidas",
  duracao: "duração",
  educacao: "educação",
  empresario: "empresário",
  espontaneo: "espontâneo",
  estrategia: "estratégia",
  estrategica: "estratégica",
  evolucao: "evolução",
  explicacao: "explicação",
  faca: "faça",
  familia: "família",
  frequencia: "frequência",
  funcao: "função",
  funcoes: "funções",
  generica: "genérica",
  ha: "há",
  hipotese: "hipótese",
  identificacao: "identificação",
  interacoes: "interações",
  intencao: "intenção",
  licao: "lição",
  lancar: "lançar",
  logica: "lógica",
  manha: "manhã",
  media: "média",
  medias: "médias",
  mes: "mês",
  metrica: "métrica",
  metricas: "métricas",
  midia: "mídia",
  nao: "não",
  negocio: "negócio",
  ninguem: "ninguém",
  objecao: "objeção",
  objecoes: "objeções",
  organico: "orgânico",
  orientacao: "orientação",
  pagina: "página",
  plantao: "plantão",
  presenca: "presença",
  pratica: "prática",
  proprio: "próprio",
  proxima: "próxima",
  proximo: "próximo",
  proximos: "próximos",
  publico: "público",
  publicos: "públicos",
  publicacoes: "publicações",
  qualificacao: "qualificação",
  rapida: "rápida",
  rapido: "rápido",
  reflexao: "reflexão",
  regua: "régua",
  reforcar: "reforçar",
  retencao: "retenção",
  responsavel: "responsável",
  saude: "saúde",
  selecao: "seleção",
  sequencia: "sequência",
  seguranca: "segurança",
  so: "só",
  sintese: "síntese",
  solicitacao: "solicitação",
  trafego: "tráfego",
  util: "útil",
  video: "vídeo",
  videos: "vídeos",
  visao: "visão",
  visualizacao: "visualização",
  visualizacoes: "visualizações",
  angulos: "ângulos",
  decisoes: "decisões",
  desperdicio: "desperdício",
};

function portuguese(value) {
  return String(value).replace(/[A-Za-zÀ-ÖØ-öø-ÿ]+/g, (word) => {
    const replacement = PT_WORDS[word.toLowerCase()];
    if (!replacement) return word;
    if (word === word.toUpperCase()) return replacement.toUpperCase();
    if (word[0] === word[0].toUpperCase()) {
      return replacement[0].toUpperCase() + replacement.slice(1);
    }
    return replacement;
  });
}

async function imageBytes(imagePath) {
  const bytes = await fs.readFile(imagePath);
  return bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
}

function box(slide, left, top, width, height, fill = C.gray, opts = {}) {
  return slide.shapes.add({
    geometry: opts.geometry || "rect",
    position: { left, top, width, height },
    fill,
    line: {
      style: "solid",
      fill: opts.lineFill || "none",
      width: opts.lineWidth ?? 0,
    },
    ...(opts.borderRadius ? { borderRadius: opts.borderRadius } : {}),
  });
}

function textBox(slide, text, left, top, width, height, opts = {}) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    position: { left, top, width, height },
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text = portuguese(text);
  shape.text.style = {
    fontSize: opts.fontSize ?? 20,
    typeface: opts.typeface || FONT,
    color: opts.color || C.black,
    bold: opts.bold || false,
    alignment: opts.align || "left",
    verticalAlignment: opts.valign || "top",
    autoFit: opts.autoFit || "shrinkText",
    wrap: "square",
    insets: opts.insets || { top: 0, right: 0, bottom: 0, left: 0 },
  };
  return shape;
}

function rule(slide, left, top, width, color = C.rule, height = 2) {
  return box(slide, left, top, width, height, color);
}

function title(slide, heading, kicker = "") {
  if (kicker) {
    textBox(slide, kicker.toUpperCase(), M, 30, 850, 24, {
      fontSize: 13,
      bold: true,
      color: C.blue,
    });
  }
  textBox(slide, heading, M, kicker ? 58 : 36, 1160, 70, {
    fontSize: 44,
    bold: true,
    color: C.black,
  });
  rule(slide, M, kicker ? 128 : 105, 1176, C.black, 2);
}

function footer(slide, number, label = "GUSTAVO LIMA | ESTRATEGIA 2026") {
  textBox(slide, label, M, 682, 520, 20, {
    fontSize: 11,
    bold: true,
    color: C.muted,
    valign: "bottom",
  });
  textBox(slide, String(number).padStart(2, "0"), 1180, 682, 48, 20, {
    fontSize: 12,
    color: C.muted,
    align: "right",
    valign: "bottom",
  });
}

function notes(slide, body, sources = []) {
  const block = [
    body,
    "",
    "[Sources]",
    ...sources.map((source) => `- ${source}`),
    "[/Sources]",
  ].join("\n");
  slide.speakerNotes.textFrame.setText(block);
  slide.speakerNotes.setVisible(true);
}

function metricCard(slide, left, top, width, number, label, color = C.blue, note = "") {
  box(slide, left, top, width, 202, C.gray);
  box(slide, left, top, 8, 202, color);
  textBox(slide, number, left + 28, top + 24, width - 52, 68, {
    fontSize: 52,
    bold: true,
    color,
  });
  textBox(slide, label, left + 28, top + 101, width - 52, 50, {
    fontSize: 22,
    bold: true,
    color: C.ink,
  });
  if (note) {
    textBox(slide, note, left + 28, top + 157, width - 52, 28, {
      fontSize: 15,
      color: C.muted,
    });
  }
}

function labelBlock(slide, left, top, width, height, index, heading, body, color = C.blue) {
  const indexWidth = String(index).length > 4 ? 104 : String(index).length > 2 ? 72 : 42;
  box(slide, left, top, width, height, C.gray);
  textBox(slide, index, left + 18, top + 16, indexWidth, 32, {
    fontSize: 16,
    bold: true,
    color,
  });
  textBox(slide, heading, left + 28 + indexWidth, top + 14, width - 48 - indexWidth, 34, {
    fontSize: 22,
    bold: true,
  });
  textBox(slide, body, left + 28 + indexWidth, top + 52, width - 50 - indexWidth, height - 66, {
    fontSize: 17,
    color: C.muted,
  });
}

function addImage(slide, blob, contentType, left, top, width, height, alt, fit = "cover") {
  return slide.images.add({
    blob,
    contentType,
    alt,
    fit,
    position: { left, top, width, height },
    geometry: "rect",
  });
}

function addSlide(presentation, number, heading, kicker = "") {
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  title(slide, heading, kicker);
  footer(slide, number);
  return slide;
}

async function main() {
  await fs.mkdir(TMP, { recursive: true });
  const presentation = Presentation.create({ slideSize: { width: W, height: H } });

  const profileScreenshot = await imageBytes("C:/Users/Jcluz/Pictures/Screenshots/Captura de tela 2026-08-20 095021.png");
  const personaPreview = await imageBytes("C:/Users/Jcluz/chatGPT-Codex/02-Análise Perfil/00-Gustavo Lima/tmp/pdfs/dossie/late-14.png");

  // 01 - Cover
  {
    const slide = presentation.slides.add();
    slide.background.fill = C.white;
    box(slide, 0, 0, 12, H, C.blue);
    textBox(slide, "ESTRATEGIA DE CONTEUDO + TRAFEGO PAGO", 58, 62, 620, 28, {
      fontSize: 14,
      bold: true,
      color: C.blue,
    });
    textBox(slide, "Gustavo Lima", 58, 128, 620, 82, {
      fontSize: 66,
      bold: true,
    });
    textBox(slide, "Conteudo que constroi confianca.\nTrafego que gera conversa.", 58, 236, 620, 150, {
      fontSize: 36,
      bold: true,
      color: C.ink,
    });
    textBox(slide, "Leitura de agosto de 2026 + plano de midia para a proxima fase", 58, 420, 560, 76, {
      fontSize: 21,
      color: C.muted,
    });
    rule(slide, 58, 570, 590, C.black, 2);
    textBox(slide, "NOSSA REGUA: CONVERSA QUALIFICADA, PROPOSTA E VENDA", 58, 588, 590, 34, {
      fontSize: 14,
      bold: true,
      color: C.green,
    });
    box(slide, 748, 36, 480, 648, C.gray);
    addImage(slide, profileScreenshot, "image/png", 760, 48, 456, 624, "Captura do perfil @gustavojcluz no Instagram", "cover");
    notes(slide, "Abrir a reuniao alinhando que o plano nasce dos dados de agosto, mas tem venda como destino.", [SOURCES.screenshot, SOURCES.sheet, SOURCES.instagram]);
  }

  // 02 - Philosophy
  {
    const slide = addSlide(presentation, 2, "A gente nao quer plateia. Quer venda.", "Nossa filosofia");
    textBox(slide, "View e alcance mostram que a mensagem circulou. Mas o resultado comeca quando a pessoa certa confia, chama e avanca.", M, 160, 590, 160, {
      fontSize: 28,
      color: C.ink,
    });
    box(slide, M, 378, 590, 170, C.paleGreen);
    textBox(slide, "A pergunta central", M + 28, 402, 530, 28, { fontSize: 16, bold: true, color: C.green });
    textBox(slide, "Este conteudo aproxima o cliente certo de uma conversa comercial?", M + 28, 442, 530, 72, {
      fontSize: 26,
      bold: true,
    });
    labelBlock(slide, 710, 156, 518, 128, "01", "Atencao", "Nao seguidores, gancho, retencao e alcance util.", C.lightBlue);
    labelBlock(slide, 710, 306, 518, 128, "02", "Intencao", "Visita ao perfil, salvamento, compartilhamento e mensagem.", C.blue);
    labelBlock(slide, 710, 456, 518, 128, "03", "Negocio", "Lead qualificado, proposta, venda, CAC e receita.", C.green);
    notes(slide, "A equipe pode olhar metricas de atencao, desde que elas estejam ligadas a intencao e negocio.", [SOURCES.dossier, SOURCES.leads]);
  }

  // 03 - Gustavo
  {
    const slide = addSlide(presentation, 3, "O papel do perfil do Gustavo", "Posicionamento");
    textBox(slide, "Gustavo nao precisa parecer influenciador. Precisa parecer a escolha segura.", M, 160, 610, 180, {
      fontSize: 40,
      bold: true,
      color: C.navy,
    });
    textBox(slide, "O perfil deve unir dominio de plano de saude, presenca humana e resposta comercial rapida.", M, 370, 580, 86, {
      fontSize: 23,
      color: C.muted,
    });
    labelBlock(slide, 710, 160, 518, 126, "70%", "Profissional", "Cotacao, comparacao, mercado, prova, estrutura e orientacao.", C.blue);
    labelBlock(slide, 710, 308, 518, 126, "30%", "Pessoal", "Familia, esporte, rotina, valores e crencas que humanizam.", C.gold);
    labelBlock(slide, 710, 456, 518, 126, "100%", "Coerente", "Todo conteudo deve reforcar confianca, clareza e responsabilidade.", C.green);
    notes(slide, "Defender o 70/30 como arquitetura de confianca: profissional prova competencia; pessoal reduz distancia.", ["Direcao estrategica fornecida pelo responsavel do perfil", SOURCES.screenshot]);
  }

  // 04 - Persona
  {
    const slide = addSlide(presentation, 4, "Quem precisa confiar na gente", "Persona essencial");
    textBox(slide, "CNPJ familiar", M, 158, 480, 56, { fontSize: 38, bold: true, color: C.navy });
    textBox(slide, "Empresario ou profissional, geralmente entre 35 e 54 anos, com familia de 3 a 5 pessoas e disposicao para investir R$ 3 mil a R$ 5 mil por mes.", M, 228, 480, 140, {
      fontSize: 22,
      color: C.ink,
    });
    box(slide, M, 394, 480, 168, C.paleGold);
    textBox(slide, "Ele nao busca o plano mais barato.", M + 24, 416, 432, 34, { fontSize: 23, bold: true });
    textBox(slide, "Busca rede, previsibilidade e seguranca para nao escolher errado.", M + 24, 460, 432, 72, { fontSize: 21, color: C.ink });
    box(slide, 570, 154, 658, 430, C.gray);
    addImage(slide, personaPreview, "image/png", 584, 168, 630, 402, "Trecho visual da matriz final da persona CNPJ familiar", "contain");
    textBox(slide, "Medos que movem a decisao: reajuste, carencia, rede ruim e clausula escondida.", 570, 602, 658, 44, { fontSize: 18, bold: true, color: C.red });
    notes(slide, "Apresentar a persona sem transformar hipotese em certeza absoluta. O ponto forte e a necessidade de seguranca na decisao.", [SOURCES.dossier, SOURCES.persona]);
  }

  // 05 - August plan vs execution
  {
    const slide = addSlide(presentation, 5, "Agosto: volume quase cheio, estrategia incompleta", "Postado x planejado");
    metricCard(slide, M, 166, 360, "96,7%", "do volume planejado", "#3D8DFF", "29 posts realizados de 30 previstos");
    metricCard(slide, 460, 166, 360, "5 / 15", "cotacoes realizadas", C.red, "apenas 33,3% da meta de cotacao");
    metricCard(slide, 868, 166, 360, "90 / 10", "mix profissional / pessoal", C.gold, "o desenho desejado era 70 / 30");
    box(slide, M, 414, 1176, 168, C.navy);
    textBox(slide, "O problema nao foi falta de trabalho.", M + 30, 442, 520, 40, { fontSize: 27, bold: true, color: C.white });
    textBox(slide, "Foi aderencia ao plano: mantivemos dois posts por dia, mas perdemos a repeticao da cotacao e a camada humana do perfil.", M + 30, 492, 1110, 64, { fontSize: 22, color: C.white });
    notes(slide, "Usar este slide para separar disciplina de execucao e fidelidade estrategica.", [SOURCES.sheet]);
  }

  // 06 - Format performance
  {
    const slide = addSlide(presentation, 6, "O formato abre a porta. A pauta decide quem entra.", "Desempenho de agosto");
    slide.charts.add("bar", {
      position: { left: M, top: 168, width: 610, height: 420 },
      categories: ["Reels", "Posts"],
      series: [{
        name: "Media de visualizacoes",
        values: [550, 361],
        fill: C.blue,
        points: [{ idx: 0, fill: C.blue }, { idx: 1, fill: C.gold }],
      }],
      hasLegend: false,
      dataLabels: { showValue: true, position: "outEnd", textStyle: { fontSize: 16, bold: true, fill: C.black } },
      chartFill: C.white,
      chartLine: { style: "solid", width: 0, fill: C.white },
      plotAreaFill: { type: "none" },
      plotAreaLine: { style: "solid", width: 0, fill: C.white },
      xAxis: {
        visible: true,
        line: { style: "solid", width: 1, fill: C.rule },
        textStyle: { typeface: FONT, fontSize: 15, color: C.black },
      },
      yAxis: {
        visible: true,
        max: 650,
        majorUnit: 100,
        majorGridlines: { style: "solid", width: 1, fill: C.gray2 },
        line: { style: "solid", width: 0, fill: C.white },
        textStyle: { typeface: FONT, fontSize: 12, color: C.muted },
      },
      barOptions: { direction: "column", grouping: "clustered", gapWidth: 90 },
    });
    labelBlock(slide, 712, 168, 516, 112, "15.357", "visualizacoes", "Soma dos Insights das publicacoes lidas.", C.blue);
    labelBlock(slide, 712, 300, 516, 112, "57,5%", "nao seguidores", "Descoberta existe: mais da metade veio de fora da base.", C.lightBlue);
    labelBlock(slide, 712, 432, 516, 112, "13", "novos seguidores", "Crescimento atribuido diretamente aos posts.", C.green);
    textBox(slide, "Sem o Reel fora da curva, a media de Reels cai para aproximadamente 412: apenas 14% acima dos posts.", 712, 566, 516, 60, { fontSize: 17, color: C.muted });
    notes(slide, "A conclusao nao e 'fazer so Reels'. A conclusao e usar video para distribuicao e pauta certa para atrair o ICP.", [SOURCES.instagram]);
  }

  // 07 - Outlier
  {
    const slide = addSlide(presentation, 7, "Alcance alto nao e sinal verde automatico", "O video fora da curva");
    box(slide, M, 160, 440, 420, C.navy);
    textBox(slide, "3.713", M + 32, 194, 370, 88, { fontSize: 70, bold: true, color: C.white });
    textBox(slide, "visualizacoes", M + 34, 284, 350, 34, { fontSize: 20, color: C.lightBlue, bold: true });
    textBox(slide, "'Pense menos, faca mais'", M + 34, 354, 360, 76, { fontSize: 30, bold: true, color: C.white });
    textBox(slide, "Excelente porta de entrada.", M + 34, 484, 360, 34, { fontSize: 20, color: C.white });
    box(slide, 534, 160, 694, 126, C.gray);
    textBox(slide, "86,9%", 560, 180, 180, 46, { fontSize: 36, bold: true, color: C.blue });
    textBox(slide, "nao seguidores", 560, 230, 190, 30, { fontSize: 17, bold: true });
    textBox(slide, "353", 790, 180, 150, 46, { fontSize: 36, bold: true, color: C.gold });
    textBox(slide, "interacoes", 790, 230, 160, 30, { fontSize: 17, bold: true });
    textBox(slide, "1", 1018, 180, 110, 46, { fontSize: 36, bold: true, color: C.green });
    textBox(slide, "seguidor", 1018, 230, 150, 30, { fontSize: 17, bold: true });
    box(slide, 534, 316, 694, 264, C.paleGold);
    textBox(slide, "A licao", 562, 340, 610, 34, { fontSize: 18, bold: true, color: C.gold });
    textBox(slide, "O pessoal pode atrair. Mas, sem uma ponte para a promessa profissional, ele entretém e vai embora.", 562, 388, 610, 98, { fontSize: 29, bold: true });
    textBox(slide, "A ponte pode ser legenda, sequencia de Stories, destaque ou CTA para uma duvida real do cliente.", 562, 508, 610, 46, { fontSize: 17, color: C.muted });
    notes(slide, "Usar o outlier como exemplo de descoberta forte e conversao direta baixa, sem desvalorizar o conteudo pessoal.", [SOURCES.instagram]);
  }

  // 08 - Organic scaling
  {
    const slide = addSlide(presentation, 8, "Quanto tempo o conteudo escala organicamente", "Curva de agosto");
    const rows = [
      { name: "Carrossel", w1: 62.6, w2: 22.2, color: C.blue },
      { name: "Cotacao", w1: 28.8, w2: 6.3, color: C.green },
      { name: "Espontaneo", w1: 34.5, w2: 5.5, color: C.gold },
      { name: "Frase", w1: 28.4, w2: 22.1, color: C.lightBlue },
      { name: "Foto", w1: 30.5, w2: null, color: C.red },
    ];
    const x = 220;
    const maxW = 440;
    textBox(slide, "0 a 7 dias", x, 148, 230, 28, { fontSize: 15, bold: true, color: C.muted });
    textBox(slide, "7 a 14 dias", 780, 148, 230, 28, { fontSize: 15, bold: true, color: C.muted });
    rows.forEach((row, i) => {
      const y = 190 + i * 78;
      textBox(slide, row.name, M, y + 10, 150, 32, { fontSize: 20, bold: true });
      box(slide, x, y, maxW, 30, C.gray2);
      box(slide, x, y, maxW * (row.w1 / 70), 30, row.color);
      textBox(slide, `+${row.w1.toFixed(1).replace(".", ",")}%`, x + maxW + 14, y + 2, 78, 28, { fontSize: 17, bold: true, color: row.color });
      if (row.w2 !== null) {
        box(slide, 780, y, 250, 30, C.gray2);
        box(slide, 780, y, 250 * (row.w2 / 25), 30, row.color);
        textBox(slide, `+${row.w2.toFixed(1).replace(".", ",")}%`, 1048, y + 2, 96, 28, { fontSize: 17, bold: true, color: row.color });
      } else {
        textBox(slide, "sem amostra", 780, y + 3, 180, 28, { fontSize: 16, color: C.muted });
      }
    });
    box(slide, M, 586, 1176, 66, C.gray);
    textBox(slide, "Leitura pratica: 24h mede gancho, 7 dias mede a maior parte da distribuicao e 14 dias revela a cauda. Ainda nao ha base de 3 semanas.", M + 22, 598, 1132, 46, { fontSize: 18, bold: true });
    notes(slide, "As taxas sao variacoes internas observadas nas amostras disponiveis; carrossel e frase ainda possuem amostras pequenas.", [SOURCES.sheet]);
  }

  // 09 - Quotation videos
  {
    const slide = addSlide(presentation, 9, "Videos de cotacao: nosso ponto de partida", "Primeiras 24 horas");
    metricCard(slide, M, 172, 360, "14,2 s", "retencao media", C.blue, "mediana: 13 segundos");
    metricCard(slide, 460, 172, 360, "46,2%", "gancho medio", C.gold, "mediana: 49%");
    metricCard(slide, 868, 172, 360, "268", "views medias", C.green, "alcance medio: 166");
    box(slide, M, 424, 1176, 154, C.paleGreen);
    textBox(slide, "Isso e uma linha de base interna, nao um veredito.", M + 28, 448, 1110, 34, { fontSize: 25, bold: true, color: C.green });
    textBox(slide, "O proximo passo e testar abertura, duracao, oferta e CTA, sempre ligando o video a conversas qualificadas e vendas.", M + 28, 494, 1110, 56, { fontSize: 22, color: C.ink });
    notes(slide, "Nao comparar estes numeros com benchmark generico. Usar agosto como linha de base para os testes do proprio perfil.", [SOURCES.sheet]);
  }

  // 10 - Professional vs personal in paid
  {
    const slide = addSlide(presentation, 10, "Profissional e pessoal cumprem funcoes diferentes", "O que impulsionar");
    box(slide, M, 160, 560, 410, C.gray);
    box(slide, M, 160, 560, 9, C.blue);
    textBox(slide, "Conteudo profissional", M + 28, 190, 500, 44, { fontSize: 30, bold: true, color: C.blue });
    textBox(slide, "80% da verba de descoberta", M + 28, 248, 500, 36, { fontSize: 24, bold: true });
    textBox(slide, "100% da verba de captacao", M + 28, 292, 500, 36, { fontSize: 24, bold: true, color: C.green });
    rule(slide, M + 28, 344, 500, C.rule, 1);
    textBox(slide, "Cotacao, comparacao, rede, carencia, reajuste, prova, bastidor de atendimento e visao de mercado.", M + 28, 366, 500, 120, { fontSize: 21, color: C.ink });
    textBox(slide, "Objetivo: atrair e converter pela competencia.", M + 28, 516, 500, 32, { fontSize: 17, bold: true, color: C.blue });
    box(slide, 668, 160, 560, 410, C.paleGold);
    box(slide, 668, 160, 560, 9, C.gold);
    textBox(slide, "Conteudo pessoal", 696, 190, 500, 44, { fontSize: 30, bold: true, color: C.gold });
    textBox(slide, "20% da verba de descoberta", 696, 248, 500, 36, { fontSize: 24, bold: true });
    textBox(slide, "0% da verba de captacao", 696, 292, 500, 36, { fontSize: 24, bold: true, color: C.red });
    rule(slide, 696, 344, 500, C.rule, 1);
    textBox(slide, "So entra no pago quando carrega valor, identidade e uma ponte para a promessa profissional. Foto generica de familia fica no organico.", 696, 366, 500, 120, { fontSize: 21, color: C.ink });
    textBox(slide, "Objetivo: reduzir distancia e aumentar confianca.", 696, 516, 500, 32, { fontSize: 17, bold: true, color: C.gold });
    textBox(slide, "No organico, mantemos o desenho 70% profissional / 30% pessoal.", M, 604, 1176, 32, { fontSize: 20, bold: true, align: "center" });
    notes(slide, "A divisao 80/20 em descoberta e uma recomendacao de teste. Nao escolher anuncios apenas por alcance ou curtidas.", [SOURCES.awareness, SOURCES.objectives, "Analise estrategica a partir dos dados de agosto"]);
  }

  // 11 - R$ 1,000 budget
  {
    const slide = addSlide(presentation, 11, "Com R$ 1.000, a verba precisa ter foco", "Plano mensal inicial");
    textBox(slide, "R$ 1.000", M, 154, 340, 72, { fontSize: 58, bold: true, color: C.navy });
    textBox(slide, "sem remarketing nesta fase", M, 230, 380, 32, { fontSize: 19, color: C.muted });
    const barX = M;
    const barY = 308;
    const barW = 700;
    box(slide, barX, barY, barW * 0.3, 74, C.lightBlue);
    box(slide, barX + barW * 0.3, barY, barW * 0.7, 74, C.green);
    textBox(slide, "30%", barX + 20, barY + 19, 130, 36, { fontSize: 26, bold: true, color: C.navy });
    textBox(slide, "70%", barX + barW * 0.3 + 20, barY + 19, 130, 36, { fontSize: 26, bold: true, color: C.white });
    textBox(slide, "Reconhecimento", barX, 394, 210, 32, { fontSize: 19, bold: true, color: C.blue });
    textBox(slide, "Captacao", barX + barW * 0.3, 394, 190, 32, { fontSize: 19, bold: true, color: C.green });
    box(slide, M, 470, 700, 110, C.gray);
    textBox(slide, "Estrutura enxuta", M + 22, 490, 240, 28, { fontSize: 18, bold: true });
    textBox(slide, "2 campanhas, com 2 a 3 criativos em cada. Sem pulverizar R$ 33 por dia em dezenas de conjuntos.", M + 22, 528, 648, 44, { fontSize: 18, color: C.ink });
    box(slide, 808, 160, 420, 180, C.gray);
    textBox(slide, "R$ 300", 836, 188, 360, 52, { fontSize: 40, bold: true, color: C.blue });
    textBox(slide, "Descoberta e visualizacao qualificada", 836, 250, 348, 60, { fontSize: 21, bold: true });
    box(slide, 808, 364, 420, 216, C.paleGreen);
    textBox(slide, "R$ 700", 836, 392, 360, 52, { fontSize: 40, bold: true, color: C.green });
    textBox(slide, "Leads por mensagem", 836, 454, 348, 34, { fontSize: 21, bold: true });
    textBox(slide, "WhatsApp ou Direct, com qualificacao curta.", 836, 502, 348, 52, { fontSize: 18, color: C.ink });
    notes(slide, "Tratar R$ 1.000 como verba mensal. A Meta entrega conforme o objetivo escolhido; por isso descoberta e leads ficam separados.", [SOURCES.awareness, SOURCES.leads, SOURCES.messages]);
  }

  // 12 - Recognition selection
  {
    const slide = addSlide(presentation, 12, "O que merece verba de reconhecimento", "Regra de selecao");
    const criteria = [
      ["01", "Nao seguidores", "O conteudo atravessou a bolha atual."],
      ["02", "Gancho + retencao", "A pessoa parou e permaneceu."],
      ["03", "Salvos + compartilhados", "Houve utilidade ou identificacao."],
      ["04", "Acoes de perfil", "O interesse continuou depois do post."],
    ];
    criteria.forEach((item, i) => {
      const col = i % 2;
      const row = Math.floor(i / 2);
      labelBlock(slide, M + col * 592, 162 + row * 166, 560, 138, item[0], item[1], item[2], i === 1 ? C.gold : C.blue);
    });
    box(slide, M, 522, 1176, 90, C.paleRed);
    textBox(slide, "Nao impulsionar porque 'foi o que mais deu view'.", M + 26, 540, 580, 32, { fontSize: 23, bold: true, color: C.red });
    textBox(slide, "O vencedor precisa combinar distribuicao, aderencia ao ICP e uma ponte para o comercial.", M + 626, 540, 520, 48, { fontSize: 20, bold: true, color: C.ink });
    notes(slide, "Os sinais de selecao sao uma regra interna de teste. A campanha deve otimizar para alcance ou visualizacao, conforme o criativo.", [SOURCES.awareness, SOURCES.objectives, SOURCES.instagram]);
  }

  // 13 - Lead capture
  {
    const slide = addSlide(presentation, 13, "Captacao: anuncio que comeca uma conversa", "WhatsApp como ponte");
    const steps = [
      ["1", "Dor", "Rede, carencia, reajuste ou escolha errada"],
      ["2", "Clareza", "Explicacao simples e comparacao"],
      ["3", "Prova", "Caso, estrutura ou resultado real"],
      ["4", "Convite", "Simule ou compare sem compromisso"],
      ["5", "Conversa", "WhatsApp ou Instagram Direct"],
    ];
    steps.forEach((step, i) => {
      const x = M + i * 236;
      box(slide, x, 166, 196, 178, i === 4 ? C.paleGreen : C.gray);
      textBox(slide, step[0], x + 18, 182, 38, 30, { fontSize: 16, bold: true, color: i === 4 ? C.green : C.blue });
      textBox(slide, step[1], x + 18, 224, 160, 36, { fontSize: 23, bold: true });
      textBox(slide, step[2], x + 18, 272, 160, 56, { fontSize: 16, color: C.muted });
      if (i < steps.length - 1) {
        textBox(slide, ">", x + 202, 228, 24, 40, { fontSize: 30, bold: true, color: C.rule, align: "center" });
      }
    });
    textBox(slide, "Qualificar em ate 6 perguntas", M, 384, 540, 36, { fontSize: 25, bold: true, color: C.navy });
    const qs = ["Cidade", "Idades", "CNPJ/MEI", "Plano atual", "Urgencia", "Faixa de investimento"];
    qs.forEach((q, i) => {
      const col = i % 3;
      const row = Math.floor(i / 3);
      box(slide, M + col * 202, 438 + row * 72, 182, 52, C.gray);
      textBox(slide, q, M + col * 202 + 14, 451 + row * 72, 154, 28, { fontSize: 17, bold: true, align: "center" });
    });
    box(slide, 704, 384, 524, 198, C.navy);
    textBox(slide, "A metrica principal", 732, 410, 470, 30, { fontSize: 18, bold: true, color: C.lightBlue });
    textBox(slide, "Custo por conversa qualificada", 732, 454, 470, 70, { fontSize: 32, bold: true, color: C.white });
    textBox(slide, "Nao custo por clique isolado.", 732, 536, 470, 28, { fontSize: 18, color: C.white });
    notes(slide, "O objetivo de leads por mensagem permite iniciar e qualificar conversas. O roteiro deve ser curto para nao matar a intencao.", [SOURCES.leads, SOURCES.messages, SOURCES.dossier]);
  }

  // 14 - Future budget
  {
    const slide = addSlide(presentation, 14, "Com mais verba, entra o remarketing", "Evolucao recomendada");
    const rows = [
      { label: "R$ 1 mil", rec: 30, cap: 70, ret: 0 },
      { label: "R$ 3 mil", rec: 25, cap: 55, ret: 20 },
      { label: "R$ 5 mil+", rec: 20, cap: 55, ret: 25 },
    ];
    const x = 190;
    const width = 670;
    rows.forEach((r, i) => {
      const y = 184 + i * 126;
      textBox(slide, r.label, M, y + 20, 120, 34, { fontSize: 22, bold: true });
      box(slide, x, y, width * (r.rec / 100), 72, C.lightBlue);
      box(slide, x + width * (r.rec / 100), y, width * (r.cap / 100), 72, C.green);
      if (r.ret > 0) box(slide, x + width * ((r.rec + r.cap) / 100), y, width * (r.ret / 100), 72, C.gold);
      if (r.rec >= 20) textBox(slide, `${r.rec}%`, x + 10, y + 22, width * (r.rec / 100) - 20, 30, { fontSize: 18, bold: true, color: C.navy, align: "center" });
      textBox(slide, `${r.cap}%`, x + width * (r.rec / 100) + 8, y + 22, width * (r.cap / 100) - 16, 30, { fontSize: 18, bold: true, color: C.white, align: "center" });
      if (r.ret > 0) textBox(slide, `${r.ret}%`, x + width * ((r.rec + r.cap) / 100) + 6, y + 22, width * (r.ret / 100) - 12, 30, { fontSize: 18, bold: true, color: C.navy, align: "center" });
    });
    textBox(slide, "Reconhecimento", 190, 574, 170, 28, { fontSize: 15, bold: true, color: C.blue });
    textBox(slide, "Captacao", 372, 574, 140, 28, { fontSize: 15, bold: true, color: C.green });
    textBox(slide, "Remarketing", 526, 574, 170, 28, { fontSize: 15, bold: true, color: C.gold });
    box(slide, 910, 164, 318, 418, C.gray);
    textBox(slide, "Remarketing entra quando existe publico quente suficiente.", 938, 190, 262, 84, { fontSize: 25, bold: true });
    rule(slide, 938, 292, 260, C.rule, 1);
    textBox(slide, "Publicos", 938, 316, 260, 28, { fontSize: 17, bold: true, color: C.gold });
    textBox(slide, "Engajados do Instagram\nQuem viu videos\nLeads sem fechamento\nVisitantes de site/CRM depois", 938, 354, 260, 128, { fontSize: 18, color: C.ink });
    textBox(slide, "Nao forcar 25% se a audiencia for pequena ou a frequencia subir demais.", 938, 500, 260, 58, { fontSize: 16, bold: true, color: C.red });
    notes(slide, "As faixas sao pontos de partida. O percentual de remarketing deve respeitar o tamanho do publico quente e a frequencia.", [SOURCES.retargeting, SOURCES.leads, SOURCES.awareness]);
  }

  // 15 - Weekly calendar
  {
    const slide = addSlide(presentation, 15, "Calendario semanal: 14 posts com funcao clara", "Organico 70/30");
    textBox(slide, "10 profissionais + 4 pessoais", 842, 106, 386, 22, { fontSize: 16, bold: true, color: C.green, align: "right" });
    const rows = [
      ["SEG", "Cotacao", "Pessoal: rotina / familia"],
      ["TER", "Cotacao", "Autoridade / prova"],
      ["QUA", "Cotacao", "Carrossel comparativo"],
      ["QUI", "Cotacao", "Pessoal: esporte / valores"],
      ["SEX", "Cotacao", "Mercado / caso"],
      ["SAB", "Checklist CNPJ", "Pessoal: bastidores"],
      ["DOM", "FAQ de risco", "Pessoal: reflexao"],
    ];
    const cols = [M, 188, 668];
    const widths = [118, 460, 560];
    ["DIA", "MANHA", "SEGUNDA POSTAGEM"].forEach((h, i) => {
      box(slide, cols[i], 150, widths[i], 46, C.navy);
      textBox(slide, h, cols[i] + 14, 163, widths[i] - 28, 24, { fontSize: 15, bold: true, color: C.white });
    });
    rows.forEach((r, idx) => {
      const y = 204 + idx * 58;
      const fill = idx % 2 === 0 ? C.gray : C.white;
      r.forEach((cell, col) => {
        box(slide, cols[col], y, widths[col], 52, fill, { lineFill: C.gray2, lineWidth: 1 });
        const personal = col === 2 && cell.startsWith("Pessoal");
        textBox(slide, cell, cols[col] + 14, y + 13, widths[col] - 28, 28, { fontSize: 18, bold: col === 0 || personal, color: personal ? C.gold : C.ink });
      });
    });
    textBox(slide, "A logica do dia deixa de ser chute: repetimos a cotacao para criar habito e variamos a noite para cumprir autoridade, educacao e humanidade.", M, 630, 1176, 38, { fontSize: 18, bold: true, align: "center" });
    notes(slide, "O calendario e uma estrutura inicial. A ordem deve ser recalibrada com custo por conversa, respostas de Stories e vendas por pauta.", ["Direcao estrategica fornecida pelo responsavel", SOURCES.sheet]);
  }

  // 16 - Highlights and stories
  {
    const slide = addSlide(presentation, 16, "O perfil precisa trabalhar mesmo quando ninguem posta", "Destaques, Stories e resposta");
    box(slide, M, 158, 360, 430, C.gray);
    textBox(slide, "Destaques com video", M + 24, 184, 312, 40, { fontSize: 27, bold: true, color: C.blue });
    textBox(slide, "Comece aqui\nPlano CNPJ\nRede e hospitais\nCarencia / CPT\nReajustes\nCotacoes\nClientes e provas\nBastidores\nFale comigo", M + 24, 244, 312, 304, { fontSize: 20, color: C.ink });
    box(slide, 460, 158, 360, 430, C.paleGold);
    textBox(slide, "Stories todos os dias", 484, 184, 312, 40, { fontSize: 27, bold: true, color: C.gold });
    textBox(slide, "3 a 5 quadros", 484, 244, 312, 44, { fontSize: 31, bold: true });
    textBox(slide, "1. Um momento humano\n2. Cotacao ou bastidor\n3. Duvida ou insight\n4. Prova / contexto\n5. Convite para responder", 484, 310, 312, 210, { fontSize: 20, color: C.ink });
    textBox(slide, "Pouco, real e frequente.", 484, 540, 312, 28, { fontSize: 17, bold: true, color: C.gold });
    box(slide, 868, 158, 360, 430, C.paleGreen);
    textBox(slide, "Responder e conduzir", 892, 184, 312, 40, { fontSize: 27, bold: true, color: C.green });
    textBox(slide, "Comentario nao e fim de funil.", 892, 248, 312, 58, { fontSize: 25, bold: true });
    textBox(slide, "Responder, fazer uma pergunta e, quando houver contexto, convidar para Direct ou WhatsApp.", 892, 328, 312, 118, { fontSize: 21, color: C.ink });
    textBox(slide, "Sem spam. Com presenca.", 892, 506, 312, 40, { fontSize: 20, bold: true, color: C.green });
    textBox(slide, "Se existe destaque, ele precisa explicar. Se existe engajamento, alguem precisa responder.", M, 616, 1176, 38, { fontSize: 20, bold: true, align: "center" });
    notes(slide, "Os destaques funcionam como atendimento de plantao. Videos curtos do proprio Gustavo aumentam contexto e confianca.", ["Solicitacao e observacao operacional fornecida pelo responsavel", SOURCES.dossier]);
  }

  // 17 - Measurement
  {
    const slide = addSlide(presentation, 17, "Metrica bonita nao paga boleto", "Painel de decisao");
    const stages = [
      { x: M, width: 356, color: C.lightBlue, title: "ATENCAO", items: "Alcance em nao seguidores\nCPM\nGancho\nRetencao\nVisualizacao qualificada" },
      { x: 462, width: 356, color: C.blue, title: "INTENCAO", items: "Visitas ao perfil\nSalvos e compartilhados\nMensagens\nConversas qualificadas\nCusto por lead qualificado" },
      { x: 872, width: 356, color: C.green, title: "NEGOCIO", items: "Propostas\nVendas\nLead para proposta\nCAC / custo por venda\nReceita e ROAS" },
    ];
    stages.forEach((s, i) => {
      box(slide, s.x, 162, s.width, 414, C.gray);
      box(slide, s.x, 162, s.width, 62, s.color);
      textBox(slide, s.title, s.x + 22, 180, s.width - 44, 28, { fontSize: 19, bold: true, color: i === 2 ? C.white : C.navy, align: "center" });
      textBox(slide, s.items, s.x + 28, 254, s.width - 56, 240, { fontSize: 22, color: C.ink, align: "center", valign: "middle" });
      if (i < 2) textBox(slide, ">", s.x + s.width + 12, 342, 28, 50, { fontSize: 36, bold: true, color: C.rule, align: "center" });
    });
    box(slide, M, 598, 1176, 56, C.navy);
    textBox(slide, "Nossa decisao de escala acontece no negocio. As outras metricas explicam o caminho.", M + 22, 614, 1132, 28, { fontSize: 19, bold: true, color: C.white, align: "center" });
    notes(slide, "O painel precisa ligar cada lead a pauta, criativo, campanha, proposta e venda. Sem essa trilha, nao existe aprendizado comercial.", [SOURCES.leads, SOURCES.messages, "Framework interno de medicao: atencao > intencao > negocio"]);
  }

  // 18 - 90 days and close
  {
    const slide = addSlide(presentation, 18, "O que aprovamos hoje", "Proximos 90 dias");
    labelBlock(slide, M, 158, 360, 228, "0-30", "Arrumar a casa", "Gravar destaques, criar rotina de Stories, instalar rastreio simples e lancar a divisao 30/70.", C.blue);
    labelBlock(slide, 460, 158, 360, 228, "31-60", "Aprender rapido", "Testar 3 angulos, cortar desperdicio e levar as objecoes das conversas de volta para o conteudo.", C.gold);
    labelBlock(slide, 868, 158, 360, 228, "61-90", "Escalar o que vende", "Aumentar vencedores e abrir remarketing quando houver publico quente e verba suficiente.", C.green);
    box(slide, M, 430, 1176, 184, C.navy);
    textBox(slide, "A meta não é viralizar.", M + 36, 462, 1104, 44, { fontSize: 29, bold: true, color: C.lightBlue, align: "center" });
    textBox(slide, "É fazer o cliente certo pensar: 'é com ele que eu vou falar.'", M + 36, 520, 1104, 60, { fontSize: 36, bold: true, color: C.white, align: "center" });
    notes(slide, "Fechar pedindo aprovacao das quatro decisoes: papel de cada conteudo, verba 30/70, rotina do perfil e painel comercial.", ["Sintese estrategica desta analise", SOURCES.awareness, SOURCES.leads, SOURCES.retargeting]);
  }

  // Export evidence for inspection.
  for (const [index, slide] of presentation.slides.items.entries()) {
    const stem = `slide-${String(index + 1).padStart(2, "0")}`;
    const png = await presentation.export({ slide, format: "png", scale: 1 });
    await fs.writeFile(path.join(TMP, `${stem}.png`), new Uint8Array(await png.arrayBuffer()));
    const layout = await slide.export({ format: "layout" });
    await fs.writeFile(path.join(TMP, `${stem}.layout.json`), await layout.text());
  }

  const montage = await presentation.export({ format: "webp", montage: true, scale: 1 });
  await fs.writeFile(path.join(TMP, "deck-montage.webp"), new Uint8Array(await montage.arrayBuffer()));

  const pptx = await PresentationFile.exportPptx(presentation);
  await pptx.save(OUT);
  console.log(`Deck salvo em ${OUT}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
