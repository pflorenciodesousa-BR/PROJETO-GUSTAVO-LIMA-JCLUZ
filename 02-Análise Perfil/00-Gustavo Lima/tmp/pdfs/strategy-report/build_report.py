from __future__ import annotations

import os
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(r"C:\Users\Jcluz\chatGPT-Codex\02-Análise Perfil\00-Gustavo Lima")
OUTPUT = ROOT / "output" / "pdf" / "Relatorio_Estrategico_Gustavo_Lima_Agosto_2026.pdf"

PAGE_W, PAGE_H = A4
LEFT = 19 * mm
RIGHT = 19 * mm
TOP = 22 * mm
BOTTOM = 18 * mm
CONTENT_W = PAGE_W - LEFT - RIGHT

NAVY = colors.HexColor("#153A5B")
BLUE = colors.HexColor("#3D8DFF")
LIGHT_BLUE = colors.HexColor("#DDF3FC")
GREEN = colors.HexColor("#2F9E67")
PALE_GREEN = colors.HexColor("#E4F5EC")
GOLD = colors.HexColor("#F4B740")
PALE_GOLD = colors.HexColor("#FFF3D2")
RED = colors.HexColor("#D94C4C")
PALE_RED = colors.HexColor("#FCEAEA")
INK = colors.HexColor("#202124")
MUTED = colors.HexColor("#60666D")
RULE = colors.HexColor("#C8CCD1")
GRAY = colors.HexColor("#F2F3F5")
WHITE = colors.white


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Italic", r"C:\Windows\Fonts\ariali.ttf"))
    pdfmetrics.registerFontFamily(
        "Arial",
        normal="Arial",
        bold="Arial-Bold",
        italic="Arial-Italic",
        boldItalic="Arial-Bold",
    )


register_fonts()

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="CoverKicker",
        fontName="Arial-Bold",
        fontSize=9.5,
        leading=12,
        textColor=BLUE,
        spaceAfter=12,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverTitle",
        fontName="Arial-Bold",
        fontSize=32,
        leading=36,
        textColor=NAVY,
        spaceAfter=18,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverSubtitle",
        fontName="Arial",
        fontSize=16,
        leading=22,
        textColor=INK,
        spaceAfter=22,
    )
)
styles.add(
    ParagraphStyle(
        name="H1x",
        fontName="Arial-Bold",
        fontSize=21,
        leading=25,
        textColor=NAVY,
        spaceBefore=2,
        spaceAfter=9,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        name="H2x",
        fontName="Arial-Bold",
        fontSize=13.5,
        leading=17,
        textColor=BLUE,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        name="Bodyx",
        fontName="Arial",
        fontSize=10.5,
        leading=15.2,
        textColor=INK,
        spaceAfter=7,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyBold",
        parent=styles["Bodyx"],
        fontName="Arial-Bold",
    )
)
styles.add(
    ParagraphStyle(
        name="Smallx",
        fontName="Arial",
        fontSize=8.4,
        leading=11.3,
        textColor=MUTED,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="TableHeader",
        fontName="Arial-Bold",
        fontSize=8.8,
        leading=11,
        textColor=WHITE,
        alignment=TA_LEFT,
    )
)
styles.add(
    ParagraphStyle(
        name="TableBody",
        fontName="Arial",
        fontSize=8.7,
        leading=11.2,
        textColor=INK,
    )
)
styles.add(
    ParagraphStyle(
        name="TableBodyBold",
        parent=styles["TableBody"],
        fontName="Arial-Bold",
    )
)
styles.add(
    ParagraphStyle(
        name="CalloutTitle",
        fontName="Arial-Bold",
        fontSize=12,
        leading=15,
        textColor=NAVY,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="CalloutBody",
        fontName="Arial",
        fontSize=10.2,
        leading=14.2,
        textColor=INK,
    )
)
styles.add(
    ParagraphStyle(
        name="Quote",
        fontName="Arial-Bold",
        fontSize=15,
        leading=20,
        textColor=NAVY,
        alignment=TA_CENTER,
    )
)
styles.add(
    ParagraphStyle(
        name="Bulletx",
        parent=styles["Bodyx"],
        leftIndent=0,
        firstLineIndent=0,
        spaceAfter=2,
    )
)


def P(text: str, style: str = "Bodyx") -> Paragraph:
    return Paragraph(text, styles[style])


def bullets(items: list[str], level: int = 0) -> ListFlowable:
    return ListFlowable(
        [ListItem(P(item, "Bodyx"), leftIndent=10) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=14 + level * 10,
        bulletFontName="Arial",
        bulletFontSize=7,
        spaceAfter=5,
    )


def section(title: str, kicker: str | None = None) -> list:
    out = []
    if kicker:
        out.append(P(kicker.upper(), "CoverKicker"))
    out.append(P(title, "H1x"))
    out.append(HRFlowable(width="100%", thickness=1.2, color=NAVY, spaceAfter=10))
    return out


def callout(title: str, body: str, fill=PALE_GREEN, stripe=GREEN) -> KeepTogether:
    inner = Table(
        [[P(title, "CalloutTitle")], [P(body, "CalloutBody")]],
        colWidths=[CONTENT_W - 18 * mm],
    )
    inner.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), fill),
                ("BOX", (0, 0), (-1, -1), 0, fill),
                ("LINEBEFORE", (0, 0), (0, -1), 4, stripe),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, 0), 9),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 9),
            ]
        )
    )
    return KeepTogether([inner, Spacer(1, 7)])


def data_table(rows: list[list], widths: list[float], header=True) -> Table:
    cooked = []
    for row_index, row in enumerate(rows):
        cooked.append(
            [
                cell
                if isinstance(cell, Paragraph)
                else P(str(cell), "TableHeader" if header and row_index == 0 else "TableBody")
                for cell in row
            ]
        )
    table = Table(cooked, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.45, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    if header:
        commands += [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ]
        if len(rows) > 1:
            commands.append(("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, GRAY]))
    else:
        commands.append(("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, GRAY]))
    table.setStyle(TableStyle(commands))
    return table


def decision_cards(items: list[tuple[str, str, colors.Color]]) -> Table:
    cells = []
    for title, body, accent in items:
        block = Table(
            [[P(title, "CalloutTitle")], [P(body, "CalloutBody")]],
            colWidths=[(CONTENT_W - 12) / len(items) - 10],
        )
        block.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), GRAY),
                    ("LINEABOVE", (0, 0), (-1, 0), 4, accent),
                    ("LEFTPADDING", (0, 0), (-1, -1), 9),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                    ("TOPPADDING", (0, 0), (-1, -1), 9),
                    ("BOTTOMPADDING", (0, -1), (-1, -1), 9),
                ]
            )
        )
        cells.append(block)
    outer = Table([cells], colWidths=[CONTENT_W / len(items)] * len(items), hAlign="LEFT")
    outer.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]))
    return outer


def on_page(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setFont("Arial-Bold", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(LEFT, PAGE_H - 13 * mm, "GUSTAVO LIMA | ESTRATÉGIA DE CONTEÚDO E TRÁFEGO PAGO")
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.5)
        canvas.line(LEFT, PAGE_H - 15 * mm, PAGE_W - RIGHT, PAGE_H - 15 * mm)
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.4)
    canvas.line(LEFT, 12 * mm, PAGE_W - RIGHT, 12 * mm)
    canvas.setFont("Arial", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(LEFT, 8.5 * mm, "Agosto de 2026")
    canvas.drawRightString(PAGE_W - RIGHT, 8.5 * mm, f"Página {doc.page}")
    canvas.restoreState()


def build() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=LEFT,
        rightMargin=RIGHT,
        topMargin=TOP,
        bottomMargin=BOTTOM,
        title="Relatório Estratégico - Gustavo Lima - Agosto de 2026",
        author="Equipe de estratégia",
        subject="Conteúdo, tráfego pago, persona e plano de ação",
    )
    frame = Frame(LEFT, BOTTOM, CONTENT_W, PAGE_H - TOP - BOTTOM, id="normal")
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=on_page)])

    story = []

    # Cover
    story += [Spacer(1, 35 * mm), P("ANÁLISE DE AGOSTO + PRÓXIMA FASE", "CoverKicker")]
    story += [P("Gustavo Lima", "CoverTitle")]
    story += [P("Conteúdo que constrói confiança.<br/>Tráfego que gera conversa.", "CoverSubtitle")]
    story.append(
        callout(
            "Nossa régua",
            "A gente não quer plateia por vaidade. Quer o cliente certo chegando com confiança suficiente para conversar, receber uma proposta e comprar.",
            fill=PALE_GREEN,
            stripe=GREEN,
        )
    )
    story += [Spacer(1, 10 * mm), P("Relatório estratégico para reunião de equipe", "BodyBold")]
    story += [P("Base analisada: publicações e Insights de agosto de 2026, planilha interna, leitura do perfil e estudos de mercado/persona.", "Smallx")]
    story.append(PageBreak())

    # 1 Executive summary
    story += section("Resumo executivo", "As decisões que importam")
    story.append(P("Vou começar pelo fim, porque é isso que precisamos aprovar na reunião:", "Bodyx"))
    story.append(
        decision_cards(
            [
                ("Conteúdo pago", "Na descoberta: <b>80% profissional e 20% pessoal em teste</b>. Na captação: <b>100% profissional</b>.", BLUE),
                ("R$ 1.000 por mês", "<b>30% reconhecimento</b> e <b>70% captação</b>. Sem remarketing por enquanto.", GREEN),
                ("Perfil vivo", "Destaques com vídeo, Stories diários e resposta no mesmo dia para quem demonstra interesse.", GOLD),
            ]
        )
    )
    story += [Spacer(1, 10)]
    story.append(P("O mês de agosto não fracassou. Pelo contrário: mostrou que a equipe consegue sustentar ritmo. Foram 29 posts para uma meta de 30. O desvio aconteceu na composição: publicamos só 5 das 15 cotações previstas e terminamos perto de 90% profissional / 10% pessoal, em vez do desenho 70/30.", "Bodyx"))
    story.append(P("O perfil também mostrou capacidade de descoberta. Aproximadamente 57,5% das visualizações vieram de não seguidores. Ao mesmo tempo, essa atenção quase não deixou rastro comercial mensurável. É aí que entra a próxima fase: mídia paga com objetivo separado, atendimento mais presente e rastreio de ponta a ponta.", "Bodyx"))
    story.append(
        callout(
            "A síntese em uma frase",
            "O conteúdo abre a porta. O perfil confirma a confiança. O WhatsApp conduz a decisão. E o nosso painel precisa dizer quanto disso virou proposta e venda.",
            fill=LIGHT_BLUE,
            stripe=BLUE,
        )
    )
    story.append(PageBreak())

    # 2 Gustavo and persona
    story += section("Gustavo, o perfil e a pessoa do outro lado", "Posicionamento")
    story.append(P("Gustavo não precisa parecer um influenciador generalista. Precisa parecer a escolha segura para uma decisão que custa caro, mexe com a família e costuma vir acompanhada de medo de errar.", "Bodyx"))
    story += [P("O papel de cada camada do perfil", "H2x")]
    story.append(
        data_table(
            [
                ["Camada", "O que mostra", "Para que serve"],
                ["Profissional - 70%", "Cotação, rede, carência, reajuste, comparativos, mercado, prova e estrutura.", "Provar competência e reduzir risco percebido."],
                ["Pessoal - 30%", "Família, esporte, rotina, valores, crenças e bastidores reais.", "Humanizar, reduzir distância e tornar a confiança mais fácil."],
                ["Comercial - todos os dias", "Resposta, Direct, WhatsApp, perguntas e acompanhamento.", "Transformar atenção em conversa e conversa em venda."],
            ],
            [38 * mm, 67 * mm, 67 * mm],
        )
    )
    story += [Spacer(1, 8), P("Resumo da persona", "H2x")]
    story.append(P("A persona mais importante é o empresário ou profissional com CNPJ/MEI ativo, geralmente entre 35 e 54 anos, casado ou em família, com 3 a 5 pessoas e capacidade provável de investir de R$ 3 mil a R$ 5 mil por mês em proteção de saúde.", "Bodyx"))
    story.append(
        bullets(
            [
                "Ela quer rede hospitalar coerente, previsibilidade de custo e segurança na escolha.",
                "Ela teme reajuste, carência, rede ruim, cláusula escondida e contratar o plano errado.",
                "Ela pode assistir em silêncio, sem curtir ou comentar, mas isso é uma hipótese estratégica, não uma desculpa para ignorar sinais de intenção.",
                "Instagram aquece e constrói autoridade. A decisão tende a amadurecer em indicação, busca, Direct ou WhatsApp.",
            ]
        )
    )
    story.append(callout("Mensagem-mãe", "Nós não vendemos o plano mais barato. Ajudamos a família a tomar a decisão mais segura e coerente para a realidade dela.", fill=PALE_GOLD, stripe=GOLD))
    story.append(PageBreak())

    # 3 August performance
    story += section("O que agosto realmente mostrou", "Plano x execução")
    story.append(
        data_table(
            [
                ["Indicador", "Resultado", "Leitura"],
                ["Volume", "29 de 30 posts - 96,7%", "A disciplina de publicação existiu."],
                ["Cotação", "5 de 15 previstas - 33,3%", "A repetição diária de uma pauta de alta intenção não aconteceu."],
                ["Mix editorial", "Aproximadamente 90% profissional / 10% pessoal", "A camada humana ficou abaixo do 70/30 planejado."],
                ["Janela", "Duas semanas de execução", "Base útil para hipóteses, ainda curta para decretar regras definitivas."],
            ],
            [42 * mm, 50 * mm, 80 * mm],
        )
    )
    story += [Spacer(1, 9), P("Leitura acumulada das publicações de 3 a 18 de agosto", "H2x")]
    story.append(
        data_table(
            [
                ["Métrica", "Total / média", "Observação"],
                ["Visualizações", "15.357", "Soma dos Insights por publicação; não representa pessoas únicas."],
                ["Interações", "996", "Inclui 787 curtidas, 50 comentários, 42 salvamentos e 49 compartilhamentos."],
                ["Origem", "57,5% de não seguidores", "O perfil já consegue atravessar a base atual."],
                ["Seguidores atribuídos", "13", "Crescimento direto registrado nos posts."],
                ["Ações de perfil", "29 ações; 16 visitas", "Existe curiosidade, mas ainda pouca passagem mensurável para o comercial."],
                ["Toques no link externo", "0 atribuídos", "Sem rastreio de venda, não dá para provar impacto financeiro."],
            ],
            [46 * mm, 47 * mm, 79 * mm],
        )
    )
    story += [Spacer(1, 8)]
    story.append(callout("O diagnóstico", "O problema de agosto não foi falta de trabalho. Foi aderência ao desenho: mantivemos o ritmo, mas perdemos a cotação diária e a camada pessoal que sustentaria o 70/30.", fill=PALE_RED, stripe=RED))
    story.append(PageBreak())

    # 4 Counterfactual and format sequence
    story += section("O que aconteceu versus o que provavelmente aconteceria", "Contrafactual responsável")
    story.append(P("Não existe como calcular exatamente o cenário que não foi executado. Sem publicar 15 cotações e sem rastrear leads e vendas por conteúdo, qualquer número de vendas seria invenção. O que conseguimos fazer é comparar a lógica dos dois cenários.", "Bodyx"))
    story.append(
        data_table(
            [
                ["Cenário executado", "Cenário planejado", "Efeito mais provável"],
                ["29 posts, com só 5 cotações.", "15 cotações matinais + 15 posts de linha editorial.", "Mais repetição da oferta, mais pontos de entrada de alta intenção e aprendizado melhor sobre preço, praça e perfil de comprador."],
                ["Mix perto de 90/10.", "Mix de 70/30.", "Mais humanidade e confiança sem abandonar autoridade."],
                ["Formatos alternados sem regra comprovada.", "Cada formato com função explícita.", "Menos chute e mais capacidade de comparar semanas."],
            ],
            [55 * mm, 55 * mm, 62 * mm],
        )
    )
    story += [Spacer(1, 8), P("Dá para decidir qual formato vai em qual dia?", "H2x")]
    story.append(P("Ainda não com segurança estatística. Duas semanas não permitem dizer que carrossel funciona melhor na quarta ou que vídeo pessoal deve sair na quinta. A estratégia mais madura agora é escolher o dia pelo papel do conteúdo e manter esse desenho por 4 a 6 semanas. Depois, comparamos o mesmo tipo de pauta em dias e horários diferentes.", "Bodyx"))
    story.append(
        callout(
            "A regra provisória",
            "Não escolhemos o formato porque 'terça é dia de Reel'. Escolhemos porque naquela posição da semana precisamos gerar uma função: oferta, educação, prova ou proximidade.",
            fill=LIGHT_BLUE,
            stripe=BLUE,
        )
    )
    story.append(PageBreak())

    # 5 Scaling and quote video metrics
    story += section("Quanto tempo o conteúdo continua escalando", "Curva orgânica")
    story.append(
        data_table(
            [
                ["Formato", "24h para 7 dias", "7 para 14 dias", "Leitura prática"],
                ["Carrossel", "+62,6%", "+22,2%", "Melhor cauda observada; amostra ainda pequena."],
                ["Cotação", "+28,8%", "+6,3%", "A maior parte da entrega acontece na primeira semana."],
                ["Espontâneo", "+34,5%", "+5,5%", "Descoberta inicial e pouca cauda depois da primeira semana."],
                ["Frase", "+28,4%", "+22,1%", "Sinal de cauda, mas o dado de 14 dias vem de apenas uma amostra."],
                ["Foto", "+30,5%", "Sem amostra", "Não há base suficiente para falar em duas semanas."],
            ],
            [37 * mm, 38 * mm, 38 * mm, 59 * mm],
        )
    )
    story += [Spacer(1, 8)]
    story.append(P("Nossa régua de leitura pode ser simples: 24 horas para avaliar o gancho inicial; 7 dias para julgar a maior parte da distribuição; 14 dias para observar a cauda. Ainda não existe amostra de 3 semanas suficiente para sustentar uma conclusão.", "Bodyx"))
    story += [P("Vídeos de cotação - linha de base das primeiras 24 horas", "H2x")]
    story.append(
        decision_cards(
            [
                ("14,2 segundos", "Retenção média. Mediana de 13 segundos.", BLUE),
                ("46,2%", "Gancho médio. Mediana de 49%.", GOLD),
                ("268 views", "Média de visualizações. Alcance médio de 166.", GREEN),
            ]
        )
    )
    story += [Spacer(1, 8)]
    story.append(P("Esses números são uma linha de base interna, não um benchmark universal. O próximo ciclo deve testar abertura, duração, clareza da oferta e CTA, sempre conectando o vídeo a conversas qualificadas e vendas.", "Bodyx"))
    story.append(callout("Cuidado com cotação no pago", "Preço e condição podem envelhecer rápido. Para anúncio contínuo, prefiro criativos perenes e uma chamada como 'receba uma simulação atualizada' em vez de transformar uma cotação antiga em promessa permanente.", fill=PALE_GOLD, stripe=GOLD))
    story.append(PageBreak())

    # 6 Paid content roles
    story += section("Profissional ou pessoal: o que entra no tráfego pago?", "Resposta direta")
    story.append(P("Eu não dividiria a verba meio a meio. O pessoal pode ser uma ótima porta de entrada, mas o dinheiro precisa ficar majoritariamente onde a mensagem encontra o problema de saúde, o risco percebido e a proposta comercial.", "Bodyx"))
    story.append(
        data_table(
            [
                ["Uso", "Profissional", "Pessoal"],
                ["Reconhecimento", "80% da verba. Comparativos, rede, carência, reajuste, prova, bastidor de atendimento e visão de mercado.", "20% em teste. Só quando carrega valor, identidade e uma ponte explícita para a promessa profissional."],
                ["Captação", "100% da verba. Problema claro, prova, oferta e convite para conversar.", "0%. Conteúdo genérico de família, viagem ou rotina fica no orgânico."],
                ["Orgânico", "70% do calendário.", "30% do calendário."],
            ],
            [38 * mm, 67 * mm, 67 * mm],
        )
    )
    story += [Spacer(1, 8), P("O caso 'Pense menos, faça mais'", "H2x")]
    story.append(P("Esse Reel foi o ponto fora da curva: 3.713 visualizações, 353 interações e 86,9% de não seguidores. Ele provou que a camada pessoal consegue furar a bolha. Mas gerou apenas 1 seguidor atribuído e não mostrou passagem para venda. Minha leitura: excelente conteúdo para descoberta, insuficiente para justificar metade da verba.", "Bodyx"))
    story.append(
        callout(
            "Regra de seleção para reconhecimento",
            "O vencedor precisa combinar quatro sinais: não seguidores, gancho/retenção, salvamentos/compartilhamentos e ações de perfil. Alcance ou curtida isolados não bastam.",
            fill=LIGHT_BLUE,
            stripe=BLUE,
        )
    )
    story.append(PageBreak())

    # 7 R$1,000 and future budgets
    story += section("Como eu dividiria a verba", "Agora e depois")
    story.append(P("Premissa: R$ 1.000 por mês. Com esse tamanho de orçamento, precisamos de duas campanhas simples e poucos criativos. Pulverizar a verba cria movimento no painel e pouco aprendizado de verdade.", "Bodyx"))
    story.append(
        data_table(
            [
                ["Campanha", "Percentual", "Valor", "Objetivo e execução"],
                ["Reconhecimento / descoberta", "30%", "R$ 300", "Objetivo de reconhecimento ou engajamento com visualização de vídeo. Usar 2 a 3 criativos, com 80% profissional e 20% pessoal em teste."],
                ["Captação", "70%", "R$ 700", "Objetivo de leads por mensagem, levando para WhatsApp ou Direct. Usar 2 a 3 criativos profissionais."],
                ["Remarketing", "0%", "R$ 0", "Ainda não. O público quente e a verba são pequenos; forçar uma terceira campanha diluiria o aprendizado."],
            ],
            [45 * mm, 25 * mm, 25 * mm, 77 * mm],
        )
    )
    story += [Spacer(1, 8)]
    story.append(P("Na prática, eu não usaria o botão de impulsionar como centro da estratégia. Usaria os conteúdos vencedores como anúncios dentro do Gerenciador de Anúncios, com objetivo, público, mensagem e rastreio separados.", "Bodyx"))
    story += [P("Qualificação curta no WhatsApp", "H2x")]
    story.append(P("A conversa precisa começar leve, mas terminar com informação suficiente para o comercial decidir prioridade. Sugestão de até seis perguntas: cidade, idades, CNPJ/MEI, plano atual, urgência e faixa de investimento.", "Bodyx"))
    story.append(callout("Métrica principal da captação", "Custo por conversa qualificada. Clique barato sem perfil, necessidade ou condição de compra não é vitória.", fill=PALE_GREEN, stripe=GREEN))
    story.append(PageBreak())

    # 8 Future + remarketing
    story += section("Quando a verba subir, entra o remarketing", "Evolução do funil")
    story.append(
        data_table(
            [
                ["Verba mensal", "Reconhecimento", "Captação", "Remarketing"],
                ["R$ 1 mil", "30%", "70%", "0%"],
                ["R$ 3 mil", "25%", "55%", "20%"],
                ["R$ 5 mil ou mais", "20%", "55%", "25%"],
            ],
            [48 * mm, 42 * mm, 42 * mm, 40 * mm],
        )
    )
    story += [Spacer(1, 9)]
    story.append(P("Essas faixas são ponto de partida, não lei. Remarketing não é um percentual que somos obrigados a gastar; é uma capacidade que depende do tamanho do público quente e da frequência de exposição.", "Bodyx"))
    story += [P("Quem entra no remarketing", "H2x")]
    story.append(
        bullets(
            [
                "Pessoas que engajaram com o Instagram ou visitaram o perfil.",
                "Quem assistiu uma parte relevante dos vídeos.",
                "Leads que iniciaram conversa, mas não fecharam.",
                "Visitantes de site e contatos do CRM quando a estrutura de rastreio estiver pronta.",
            ]
        )
    )
    story += [P("O que mostrar para esse público", "H2x")]
    story.append(P("Prova social, comparativos, explicação de objeções, casos, rede hospitalar, carência, reajuste e uma chamada mais direta para simulação. A audiência já conhece Gustavo; agora precisa de segurança para agir.", "Bodyx"))
    story.append(callout("Regra de proteção", "Se o público for pequeno e a frequência subir, reduzimos remarketing em vez de perseguir a pessoa até cansar.", fill=PALE_RED, stripe=RED))
    story.append(PageBreak())

    # 9 Organic calendar
    story += section("Calendário semanal com função clara", "Orgânico 70/30")
    story.append(P("A proposta abaixo mantém dois posts por dia e troca o chute por uma lógica repetível. A cotação matinal cria hábito e presença comercial; a segunda postagem alterna autoridade, educação, prova e humanidade.", "Bodyx"))
    story.append(
        data_table(
            [
                ["Dia", "Manhã", "Segunda postagem", "Função"],
                ["Segunda", "Cotação", "Pessoal: rotina / família", "Oferta + proximidade"],
                ["Terça", "Cotação", "Autoridade / prova", "Oferta + confiança"],
                ["Quarta", "Cotação", "Carrossel comparativo", "Oferta + educação"],
                ["Quinta", "Cotação", "Pessoal: esporte / valores", "Oferta + identidade"],
                ["Sexta", "Cotação", "Mercado / caso", "Oferta + repertório"],
                ["Sábado", "Checklist CNPJ", "Pessoal: bastidores", "Utilidade + humanidade"],
                ["Domingo", "FAQ de risco", "Pessoal: reflexão", "Objeção + vínculo"],
            ],
            [25 * mm, 38 * mm, 65 * mm, 44 * mm],
        )
    )
    story += [Spacer(1, 8)]
    story.append(P("Esse calendário precisa rodar por pelo menos 4 a 6 semanas com pauta, hora e resultado registrados. Depois, analisamos por objetivo e formato. Não vamos condenar uma terça-feira inteira porque um único carrossel foi fraco.", "Bodyx"))
    story.append(callout("Contagem semanal", "10 conteúdos profissionais e 4 pessoais. O 70/30 volta a ser uma escolha operacional, não apenas uma intenção no planejamento.", fill=LIGHT_BLUE, stripe=BLUE))
    story.append(PageBreak())

    # 10 Profile operations
    story += section("O perfil precisa trabalhar mesmo quando ninguém posta", "Operação diária")
    story += [P("Destaques com vídeo", "H2x")]
    story.append(P("Se o destaque existe, ele precisa explicar. Não basta uma capa bonita e três artes soltas. Cada destaque começa com um vídeo curto do próprio Gustavo dizendo o que a pessoa vai encontrar e para quem aquilo serve.", "Bodyx"))
    story.append(
        data_table(
            [
                ["Destaque", "Papel"],
                ["Comece aqui", "Quem é Gustavo, para quem ele trabalha e como pedir ajuda."],
                ["Plano CNPJ", "Quem pode contratar e quais informações precisa separar."],
                ["Rede e hospitais", "Como comparar rede sem cair em lista bonita e vazia."],
                ["Carência / CPT", "Explicar sem juridiquês e sem prometer o que não controla."],
                ["Reajustes", "Como funciona e o que observar antes de contratar."],
                ["Cotações", "Exemplos e convite para simulação atualizada."],
                ["Clientes e provas", "Depoimentos, casos e processo de atendimento."],
                ["Bastidores", "Rotina, equipe, estudo e acompanhamento pós-venda."],
                ["Fale comigo", "WhatsApp, Direct e orientação do próximo passo."],
            ],
            [45 * mm, 127 * mm],
        )
    )
    story += [Spacer(1, 8), P("Stories e resposta", "H2x")]
    story.append(P("A rotina ideal é pequena o suficiente para acontecer: 3 a 5 quadros por dia. Um momento humano, uma cotação ou bastidor, uma dúvida ou insight, uma prova/contexto e um convite para responder.", "Bodyx"))
    story.append(P("Comentário não é fim de funil. A equipe responde, faz uma pergunta e, quando existe contexto, conduz para Direct ou WhatsApp. Sem spam e sem texto automático fingindo intimidade. Com presença e resposta no mesmo dia.", "Bodyx"))
    story.append(callout("A regra de ouro", "Se existe destaque, ele precisa explicar. Se existe engajamento, alguém precisa responder.", fill=PALE_GREEN, stripe=GREEN))
    story.append(PageBreak())

    # 11 Measurement and 90 days
    story += section("Como saber se está funcionando", "Métrica até a venda")
    story.append(
        data_table(
            [
                ["Etapa", "Métricas", "Pergunta que responde"],
                ["Atenção", "Alcance em não seguidores, CPM, gancho, retenção e visualização qualificada.", "A mensagem chegou e segurou a pessoa certa?"],
                ["Intenção", "Visita ao perfil, salvamento, compartilhamento, mensagem e conversa qualificada.", "Ela quis saber mais ou pedir ajuda?"],
                ["Negócio", "Proposta, taxa de proposta, venda, taxa de fechamento, CAC, receita e ROAS.", "Isso gerou dinheiro com eficiência?"],
            ],
            [34 * mm, 83 * mm, 55 * mm],
        )
    )
    story += [Spacer(1, 8)]
    story.append(P("A planilha comercial precisa registrar, no mínimo: data, contato, campanha, criativo, pauta, qualificação, proposta, venda, ticket e receita. Sem isso, o Instagram continua parecendo uma vitrine e a gente continua discutindo curtida porque é o único número fácil.", "Bodyx"))
    story += [P("Plano de 90 dias", "H2x")]
    story.append(
        data_table(
            [
                ["Período", "Prioridade", "Entregas"],
                ["0 a 30 dias", "Arrumar a casa", "Configurar estrutura de anúncios e rastreio, gravar destaques, criar rotina de Stories, lançar campanhas 30/70 e responder engajamentos."],
                ["31 a 60 dias", "Aprender rápido", "Testar três ângulos de mensagem, cortar desperdício, qualificar leads e transformar objeções do comercial em conteúdo."],
                ["61 a 90 dias", "Escalar o que vende", "Aumentar criativos vencedores, revisar o mix, abrir remarketing se houver público e recalcular verba pelo CAC e pelas vendas."],
            ],
            [34 * mm, 43 * mm, 95 * mm],
        )
    )
    story += [Spacer(1, 10)]
    story.append(callout("O fechamento da reunião", "A meta não é viralizar. É fazer o cliente certo pensar: 'é com ele que eu vou falar'.", fill=LIGHT_BLUE, stripe=BLUE))
    story.append(PageBreak())

    # 12 Methodology and sources
    story += section("Metodologia, limites e fontes", "Para ler os números do jeito certo")
    story.append(P("Esta análise combina três camadas: planilha de postagens, leitura manual dos Insights visíveis do perfil e documentos de persona/mercado. Os dados de Instagram cobrem as publicações observadas entre 3 e 18 de agosto de 2026.", "Bodyx"))
    story.append(P("Limites que precisam ficar claros:", "H2x"))
    story.append(
        bullets(
            [
                "A execução cobre aproximadamente duas semanas. Dia da semana, horário e formato ainda têm amostras pequenas.",
                "Os totais por post são acumulados e não equivalem a usuários únicos.",
                "Não havia atribuição completa entre conteúdo, conversa, proposta e venda. Por isso não afirmamos retorno financeiro de agosto.",
                "As divisões de verba são hipóteses iniciais e devem ser revisadas pelo custo por conversa qualificada, taxa de proposta, venda e CAC.",
                "A hipótese de ICP silencioso é plausível, mas precisa ser validada com Direct, WhatsApp, pesquisa de origem e CRM.",
            ]
        )
    )
    story += [P("Fontes internas", "H2x")]
    story.append(
        bullets(
            [
                "Planilha 'Análise de Crescimento de Autoridade - Gustavo Lima', página 'Postagens 2026', agosto de 2026.",
                "Instagram Insights do perfil @gustavojcluz, publicações de 3 a 18 de agosto de 2026.",
                "Dossiê do Mercado.",
                "Persona 2025 - Lannister (CNPJ familiar) - Estudo e Infográfico.",
                "Direção estratégica fornecida pelo responsável: 70% profissional / 30% pessoal e venda acima de métricas de vaidade.",
            ]
        )
    )
    story += [P("Referências oficiais da Meta", "H2x")]
    links = [
        ("Objetivos de anúncios", "https://www.facebook.com/business/ads/ad-objectives?locale=en_GB"),
        ("Reconhecimento", "https://www.facebook.com/business/ads/ad-objectives/awareness"),
        ("Geração de leads", "https://www.facebook.com/business/ads/ad-objectives/lead-generation?locale=en_GB"),
        ("Anúncios de clique para mensagem", "https://www.facebook.com/business/ads/click-to-message-ads"),
        ("Remarketing", "https://www.facebook.com/business/goals/retargeting"),
    ]
    for label, url in links:
        story.append(P(f'<link href="{url}" color="#3D8DFF">{label}</link>', "Bodyx"))
    story += [Spacer(1, 14), P("Documento preparado para discussão e decisão em equipe.", "Smallx")]

    doc.build(story)
    print(f"PDF criado em: {OUTPUT}")


if __name__ == "__main__":
    build()
