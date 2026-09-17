from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


ROOT = Path(r"C:\Users\Jcluz\chatGPT-Codex\02-Análise Perfil\00-Gustavo Lima")
OUT = ROOT / "output" / "pdf" / "Linha_Editorial_Gustavo_Lima_Setembro_2026.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

NAVY = HexColor("#11243D")
BLUE = HexColor("#2563EB")
SKY = HexColor("#EAF2FF")
GREEN = HexColor("#0F766E")
MINT = HexColor("#E6F5F1")
AMBER = HexColor("#B45309")
SAND = HexColor("#FFF2D9")
INK = HexColor("#1F2937")
MUTED = HexColor("#5B6471")
LINE = HexColor("#D9E0E8")
LIGHT = HexColor("#F6F8FB")

TECH = (BLUE, SKY)
AUTH = (GREEN, MINT)
PERSONAL = (AMBER, SAND)


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for state in self.pages:
            self.__dict__.update(state)
            self.setStrokeColor(LINE)
            self.setLineWidth(0.4)
            self.line(18 * mm, 13 * mm, 192 * mm, 13 * mm)
            self.setFont("Helvetica", 8)
            self.setFillColor(MUTED)
            self.drawString(18 * mm, 8.5 * mm, "Gustavo Lima | Linha editorial - Setembro de 2026")
            self.drawRightString(192 * mm, 8.5 * mm, f"{self._pageNumber} / {page_count}")
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)


styles = {
    "eyebrow": ParagraphStyle("eyebrow", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=BLUE, spaceAfter=7),
    "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=28, leading=32, textColor=NAVY, spaceAfter=9),
    "subtitle": ParagraphStyle("subtitle", fontName="Helvetica", fontSize=12, leading=17, textColor=MUTED),
    "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=NAVY, spaceAfter=9),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=NAVY, spaceAfter=5),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9.4, leading=13.2, textColor=INK),
    "small": ParagraphStyle("small", fontName="Helvetica", fontSize=8.1, leading=10.3, textColor=INK),
    "tiny": ParagraphStyle("tiny", fontName="Helvetica", fontSize=7.2, leading=8.8, textColor=MUTED),
    "label": ParagraphStyle("label", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=white, alignment=TA_CENTER),
    "center": ParagraphStyle("center", fontName="Helvetica", fontSize=9, leading=12, textColor=MUTED, alignment=TA_CENTER),
}


def p(text, style="body"):
    return Paragraph(text, styles[style])


def pill(text, fill, width=35 * mm):
    t = Table([[p(text, "label")]], colWidths=[width], rowHeights=[7 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), fill),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def card(title, body, accent, fill, width):
    data = [[p(title, "h2")], [p(body, "small")]]
    t = Table(data, colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), fill),
        ("LINEBEFORE", (0, 0), (0, -1), 3, accent),
        ("BOX", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 8),
    ]))
    return t


def section_heading(kicker, heading, desc=None):
    flow = [p(kicker.upper(), "eyebrow"), p(heading, "h1")]
    if desc:
        flow.append(p(desc, "subtitle"))
    flow.append(Spacer(1, 6 * mm))
    return flow


def calendar_tile(item):
    date, weekday, form, pillar, topic, note = item
    accent, fill = {"Técnico": TECH, "Autoridade": AUTH, "Pessoal": PERSONAL}[pillar]
    pillar_label = {"Técnico": "TEC", "Autoridade": "AUT", "Pessoal": "PES"}[pillar]
    lines = [
        [p(f"{date}  |  {weekday}", "small"), p(pillar_label, "tiny")],
        [p(form, "h2")],
        [p(topic, "small")],
    ]
    if note:
        lines.append([p(note, "tiny")])
    table = Table(lines, colWidths=[35 * mm, 14 * mm], rowHeights=None)
    spans = [("SPAN", (0, 1), (1, 1)), ("SPAN", (0, 2), (1, 2))]
    if note:
        spans.append(("SPAN", (0, 3), (1, 3)))
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), fill),
        ("LINEABOVE", (0, 0), (-1, 0), 3, accent),
        ("BOX", (0, 0), (-1, -1), .35, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TEXTCOLOR", (1, 0), (1, 0), accent),
    ] + spans))
    return table


calendar = [
    ("01/09", "TER", "Reels Frase", "Técnico", "A terça-feira comum", "Ele também tem que funcionar em uma terça-feira comum."),
    ("02/09", "QUA", "Cotação", "Técnico", "Cotação para lutadores", "Gravado"),
    ("03/09", "QUI", "Estático Pessoal", "Pessoal", "Foto com Claudia saindo tarde da corretora", "Legenda: palco x bastidor e fazer o que precisa ser feito. Sem CTA."),
    ("04/09", "SEX", "Ponto de Vista", "Autoridade", "Entrevista com Bianca ou Peterson", ""),
    ("05/09", "SÁB", "Carrossel", "Autoridade", "React do conteúdo mais visualizado", ""),
    ("06/09", "DOM", "TH", "Pessoal", "Roteiro com Gustavo", "Sem CTA"),
    ("07/09", "SEG", "Reels Frase", "Técnico", "Uma cotação correta", "Não entendo por que todo mundo corre atrás de tantas, se você só precisa de uma."),
    ("08/09", "TER", "Estático Pessoal", "Pessoal", "Homenagem de 2 anos de relacionamento", "Sem CTA"),
    ("09/09", "QUA", "Cotação", "Técnico", "Empresário com família de quatro pessoas", "Cotação jogador - gravado"),
    ("10/09", "QUI", "Lista", "Técnico", "X momentos em que a coparticipação faz sentido", "No seu plano de saúde."),
    ("11/09", "SEX", "Ponto de Vista", "Autoridade", "Sextou (ponto de atenção)", "Gravar e publicar na própria sexta-feira."),
    ("12/09", "SÁB", "Carrossel", "Técnico", "Pauta a definir", ""),
    ("13/09", "DOM", "TH", "Pessoal", "Roteiro com Gustavo", "Sem CTA"),
    ("14/09", "SEG", "Lista", "Técnico", "Top X planos de saúde mais caros", ""),
    ("15/09", "TER", "Reels Frase", "Técnico", "Não se distraia", "A saúde da sua família e a sua precisam de você."),
    ("16/09", "QUA", "Lista", "Técnico", "X momentos em que a coparticipação não faz sentido nenhum", "No seu plano de saúde."),
    ("17/09", "QUI", "Estático Pessoal", "Pessoal", "Malhando ou jogando tênis", "Sem CTA"),
    ("18/09", "SEX", "Ponto de Vista", "Autoridade", "Entrevista com Giselle Tavares", ""),
    ("19/09", "SÁB", "Carrossel", "Autoridade", "Carrossel sobre a assessoria", ""),
    ("20/09", "DOM", "TH", "Pessoal", "Pauta a definir", "Sem CTA"),
    ("21/09", "SEG", "Cotação", "Técnico", "Perfil da cotação a definir", ""),
    ("22/09", "TER", "Ponto de Vista", "Autoridade", "POV com óculos na Escola de Vendas", ""),
    ("23/09", "QUA", "Ponto de Vista", "Autoridade", "Entrevista com Augusto Lima", ""),
    ("24/09", "QUI", "Carrossel", "Pessoal", "TBT com fotos de festa da empresa", "Sem CTA"),
    ("25/09", "SEX", "Ponto de Vista", "Autoridade", "POV do plantão de leads", "Registrar fotos para o Dump do dia 27."),
    ("26/09", "SÁB", "Lista", "Técnico", "Top X benefícios mais procurados", ""),
    ("27/09", "DOM", "Dump", "Pessoal", "Dump com as fotos reunidas no dia 25", "Sem CTA"),
    ("28/09", "SEG", "Cotação", "Técnico", "Perfil da cotação a definir", ""),
    ("29/09", "TER", "TH", "Autoridade", "Falar sobre o salão de vendas", ""),
    ("30/09", "QUA", "TH", "Pessoal", "Pauta a definir", "Sem CTA"),
]


def build():
    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm, topMargin=18 * mm, bottomMargin=18 * mm,
        title="Linha Editorial - Gustavo Lima - Setembro de 2026",
        author="JCLuz",
    )
    story = []

    # Cover
    story += [Spacer(1, 20 * mm), p("PLANEJAMENTO DE CONTEÚDO", "eyebrow"), p("Linha editorial", "title")]
    story += [p("Setembro de 2026", "title"), Spacer(1, 4 * mm)]
    story += [p("Gustavo Lima | JCLuz", "subtitle"), Spacer(1, 20 * mm)]
    cover_box = Table([[p("Um post por dia, com ritmo que a equipe consegue sustentar. A linha combina conteúdo técnico, prova de autoridade e proximidade pessoal para transformar presença em confiança.", "body")]], colWidths=[156 * mm])
    cover_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("LINEBEFORE", (0, 0), (0, -1), 4, BLUE),
        ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 14), ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
    ]))
    story += [cover_box, Spacer(1, 16 * mm)]
    story += [Table([[pill("40% TÉCNICO", BLUE), pill("30% AUTORIDADE", GREEN), pill("30% PESSOAL", AMBER)]], colWidths=[52 * mm, 52 * mm, 52 * mm], style=[("VALIGN", (0,0), (-1,-1), "MIDDLE")])]
    story += [Spacer(1, 8 * mm), p("O conteúdo técnico reduz dúvida. A autoridade reduz insegurança. O pessoal dá contexto humano para a relação existir antes da conversa comercial.", "subtitle")]
    story.append(PageBreak())

    # Strategy
    story += section_heading("Visão do mês", "O ritmo que vamos sustentar", "Setembro é o mês de colocar a equipe no mesmo compasso. Por isso, a estratégia trabalha com uma publicação diária e com funções claras para cada formato.")
    rhythm = [
        ("SEG", "Cotação", "Fundo de funil: perfil do cliente, raciocínio e resultado da cotação."),
        ("TER", "Distribuição", "Lista ou Ponto de Vista com potencial de alcance e salvamento."),
        ("QUA", "Gancho", "Reels Frase ou TH que abre uma conversa forte."),
        ("QUI", "Pessoal", "Família, esporte, rotina e proximidade sem CTA."),
        ("SEX", "Autoridade", "Ponto de Vista dentro da empresa: pessoas, processo e bastidor."),
        ("SÁB", "Aprofundamento", "Lista ou Carrossel: conteúdo que a pessoa guarda e revisita."),
        ("DOM", "Proximidade", "Crença, reflexão, família ou um Dump do mês. Sem CTA."),
    ]
    rhythm_rows = [[p("DIA", "tiny"), p("FUNÇÃO", "tiny"), p("O QUE ENTRA", "tiny")]]
    for d, f, x in rhythm:
        rhythm_rows.append([p(d, "small"), p(f, "small"), p(x, "small")])
    rt = Table(rhythm_rows, colWidths=[20 * mm, 36 * mm, 100 * mm])
    rt.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY), ("TEXTCOLOR", (0,0), (-1,0), white),
        ("GRID", (0,0), (-1,-1), .35, LINE), ("BACKGROUND", (0,1), (-1,-1), white),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story += [rt, Spacer(1, 10 * mm)]
    story += [p("A distribuição", "h2"), Spacer(1, 2 * mm)]
    mix = Table([[p("12<br/><font size=8>TÉCNICO</font>", "center"), p("9<br/><font size=8>AUTORIDADE</font>", "center"), p("9<br/><font size=8>PESSOAL</font>", "center")]], colWidths=[52*mm]*3, rowHeights=[21*mm])
    mix.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), SKY), ("BACKGROUND", (1,0), (1,0), MINT), ("BACKGROUND", (2,0), (2,0), SAND),
        ("BOX", (0,0), (-1,-1), .35, LINE), ("INNERGRID", (0,0), (-1,-1), .35, LINE), ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    story += [mix, Spacer(1, 7 * mm)]
    story += [p("Técnico: 4 Cotações, 4 Listas, 3 Reels Frase e 1 Carrossel. Autoridade: 6 Pontos de Vista, 2 Carrosséis e 1 TH. Pessoal: 3 Estáticos Pessoais, 4 TH, 1 Carrossel e 1 Dump.", "body")]
    story.append(PageBreak())

    # Format dictionary
    story += section_heading("Formatos", "O nome e a função de cada conteúdo", "A equipe trabalha com um vocabulário único. Isso deixa briefing, gravação, edição e aprovação mais rápidos.")
    format_cards = [
        ("Cotação", "Reels de fundo de funil. Parte de um perfil real, explica o raciocínio e apresenta a cotação. Fecha chamando para o <b>link da bio</b>.", TECH),
        ("Reels Frase", "Reels curto, com uma frase provocadora na tela. A legenda aprofunda o ponto e conduz para uma conversa técnica relacionada.", TECH),
        ("Lista", "Conteúdo informativo de meio de funil. O Gustavo revela os itens no quadro, um a um. Busca salvamento, compartilhamento e visita ao perfil.", TECH),
        ("Carrossel", "Formato para reaproveitar e aprofundar uma ideia que já funciona. Pode ser técnico, de autoridade ou pessoal, sempre com leitura simples e útil.", TECH),
        ("Ponto de Vista", "Reels espontâneo dentro da empresa: entrevistas, rotina, pessoas, processos e bastidores. Constrói autoridade sem parecer anúncio.", AUTH),
        ("TH", "Talking Head: Gustavo falando diretamente para a câmera. Pode servir a uma crença pessoal, a um ponto técnico ou a um princípio de autoridade.", AUTH),
        ("Estático Pessoal", "Foto de família, esposa, esporte ou rotina. Serve para gerar familiaridade. <b>Nunca leva CTA.</b>", PERSONAL),
        ("Dump", "Resumo visual de momentos reais do mês: família, esporte, equipe e bastidores. Pessoal, simples e sem CTA.", PERSONAL),
    ]
    pairs = []
    for i in range(0, len(format_cards), 2):
        row = []
        for title, body, colors in format_cards[i:i+2]:
            row.append(card(title, body, colors[0], colors[1], 76 * mm))
        pairs.append(row)
    ft = Table(pairs, colWidths=[76 * mm, 76 * mm], hAlign="LEFT")
    ft.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 0), ("RIGHTPADDING", (0,0), (-1,-1), 4), ("TOPPADDING", (0,0), (-1,-1), 0), ("BOTTOMPADDING", (0,0), (-1,-1), 5)]))
    story += [ft]
    story.append(PageBreak())

    # Calendar 1
    story += section_heading("Calendário", "Setembro em ação | 01 a 15", "Cada data já traz formato, pilar e direção de pauta. As escolhas técnicas de Lista e Reels Frase foram atualizadas com os temas definidos para setembro.")
    rows = []
    for i in range(0, 15, 3):
        rows.append([calendar_tile(x) for x in calendar[i:i+3]])
    cal1 = Table(rows, colWidths=[52*mm, 52*mm, 52*mm])
    cal1.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 0), ("RIGHTPADDING", (0,0), (-1,-1), 4), ("TOPPADDING", (0,0), (-1,-1), 0), ("BOTTOMPADDING", (0,0), (-1,-1), 5)]))
    story += [cal1]
    story.append(PageBreak())

    # Calendar 2
    story += section_heading("Calendário", "Setembro em ação | 16 a 30", "A segunda quinzena reforça a sequência: alcance e educação no meio da semana, autoridade na sexta e profundidade no sábado.")
    rows = []
    for i in range(15, 30, 3):
        rows.append([calendar_tile(x) for x in calendar[i:i+3]])
    cal2 = Table(rows, colWidths=[52*mm, 52*mm, 52*mm])
    cal2.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 0), ("RIGHTPADDING", (0,0), (-1,-1), 4), ("TOPPADDING", (0,0), (-1,-1), 0), ("BOTTOMPADDING", (0,0), (-1,-1), 5)]))
    story += [cal2]
    story.append(PageBreak())

    # List production page
    story += section_heading("Série Lista", "Quatro espaços de Lista no mês", "A dinâmica é simples: os pontos começam cobertos; a cada explicação, o Gustavo revela um item. O número é o que a pauta precisar, sem forçar cinco por obrigação.")
    list_cards = [
        ("10/09", "X momentos em que a coparticipação faz sentido", "Situações em que essa modalidade pode combinar com o uso e o planejamento do cliente."),
        ("14/09", "Top X planos de saúde mais caros", "A quantidade e os planos entram na etapa de roteiro."),
        ("16/09", "X momentos em que a coparticipação não faz sentido nenhum", "Situações em que essa modalidade não combina com o uso ou a necessidade de previsibilidade do cliente."),
        ("26/09", "Top X benefícios mais procurados", "Os benefícios serão organizados por procura e valor percebido pelo cliente."),
    ]
    list_table_rows = []
    for date, title, desc in list_cards:
        list_table_rows.append([pill(date, NAVY, 18*mm), card(title, desc, BLUE, SKY, 133*mm)])
    lt = Table(list_table_rows, colWidths=[22*mm, 134*mm])
    lt.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 0), ("RIGHTPADDING", (0,0), (-1,-1), 0), ("TOPPADDING", (0,0), (-1,-1), 0), ("BOTTOMPADDING", (0,0), (-1,-1), 7)]))
    story += [lt, Spacer(1, 6*mm)]
    cta = Table([[p("REGRA DE CTA", "label")], [p("Cotação: convite direto para o link da bio. Lista e Carrossel técnico: CTA leve para salvar, compartilhar ou visitar o perfil. Conteúdo pessoal: sem CTA.", "body")]], colWidths=[156*mm])
    cta.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY), ("BACKGROUND", (0,1), (-1,1), LIGHT),
        ("BOX", (0,0), (-1,-1), .4, LINE), ("LEFTPADDING", (0,0), (-1,-1), 11), ("RIGHTPADDING", (0,0), (-1,-1), 11),
        ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    story += [cta]

    doc.build(story, canvasmaker=NumberedCanvas)
    print(OUT)


if __name__ == "__main__":
    build()
