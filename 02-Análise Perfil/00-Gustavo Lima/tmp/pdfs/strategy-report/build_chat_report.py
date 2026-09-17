from pathlib import Path

from reportlab.graphics.shapes import Circle, Drawing, Line, Rect, String
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, Frame, PageBreak, PageTemplate, Spacer, Table, TableStyle

import build_report as base


OUTPUT = base.OUTPUT

TECH = colors.HexColor("#3D8DFF")
AUTHORITY = colors.HexColor("#2F9E67")
PERSONAL = colors.HexColor("#F4B740")
CHART_GRID = colors.HexColor("#D9DDE2")
CHART_DARK = colors.HexColor("#4D535A")

base.styles.add(
    ParagraphStyle(
        name="ChatBody",
        fontName="Arial",
        fontSize=11.2,
        leading=16.8,
        textColor=base.INK,
        spaceAfter=8,
    )
)
base.styles.add(
    ParagraphStyle(
        name="ChatBullet",
        fontName="Arial",
        fontSize=11.2,
        leading=16.8,
        textColor=base.INK,
        spaceAfter=0,
    )
)
base.styles.add(
    ParagraphStyle(
        name="ChatLead",
        fontName="Arial-Bold",
        fontSize=13.4,
        leading=18.5,
        textColor=base.NAVY,
        spaceAfter=10,
    )
)
base.styles.add(
    ParagraphStyle(
        name="ChatSmall",
        fontName="Arial",
        fontSize=9,
        leading=12.8,
        textColor=base.MUTED,
        spaceAfter=5,
    )
)


def T(text: str, style: str = "ChatBody"):
    return base.P(text, style)


def page_title(title: str, kicker: str):
    return base.section(title, kicker)


def chat_bullets(items: list[str]):
    rows = [[T("•", "ChatBullet"), T(item, "ChatBullet")] for item in items]
    table = Table(
        rows,
        colWidths=[5 * mm, base.CONTENT_W - 5 * mm],
        hAlign="LEFT",
        splitByRow=1,
    )
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def chart_label(
    drawing: Drawing,
    x: float,
    y: float,
    value: str,
    *,
    size: float = 8,
    color=base.INK,
    anchor: str = "start",
    bold: bool = False,
):
    drawing.add(
        String(
            x,
            y,
            value,
            fontName="Arial-Bold" if bold else "Arial",
            fontSize=size,
            fillColor=color,
            textAnchor=anchor,
        )
    )


def chart_legend(drawing: Drawing, items: list[tuple[str, colors.Color]], y: float):
    x = 0
    for label, color in items:
        drawing.add(Rect(x, y - 1.5 * mm, 3.5 * mm, 3.5 * mm, fillColor=color, strokeColor=None))
        chart_label(drawing, x + 5 * mm, y - 0.4 * mm, label, size=7.6, color=base.MUTED)
        x += 36 * mm


def mix_chart() -> Drawing:
    drawing = Drawing(base.CONTENT_W, 43 * mm)
    chart_legend(
        drawing,
        [("Técnico", TECH), ("Autoridade", AUTHORITY), ("Pessoal", PERSONAL)],
        39 * mm,
    )
    rows = [
        ("Agosto", [58.6, 34.5, 6.9]),
        ("Recomendado", [40, 30, 30]),
    ]
    x0 = 29 * mm
    bar_w = base.CONTENT_W - x0
    for index, (label, values) in enumerate(rows):
        y = (23 - index * 15) * mm
        chart_label(drawing, 0, y + 3 * mm, label, size=8.2, bold=True)
        x = x0
        for value, color in zip(values, [TECH, AUTHORITY, PERSONAL]):
            width = bar_w * value / 100
            drawing.add(Rect(x, y, width, 9 * mm, fillColor=color, strokeColor=base.WHITE, strokeWidth=0.5))
            chart_label(
                drawing,
                x + width / 2,
                y + 3.2 * mm,
                f"{value:.0f}%",
                size=8.2,
                color=base.WHITE if color != PERSONAL else base.INK,
                anchor="middle",
                bold=True,
            )
            x += width
    return drawing


def category_performance_chart() -> Drawing:
    drawing = Drawing(base.CONTENT_W, 59 * mm)
    categories = [
        ("Técnico", 232.3, 9.8, TECH),
        ("Autoridade", 412.6, 20.7, AUTHORITY),
        ("Pessoal*", 456.0, 28.5, PERSONAL),
    ]
    chart_label(drawing, 31 * mm, 53 * mm, "Visualizações médias", size=8.4, bold=True)
    chart_label(drawing, 108 * mm, 53 * mm, "Interações médias", size=8.4, bold=True)
    for index, (label, views, interactions, color) in enumerate(categories):
        y = (38 - index * 15) * mm
        chart_label(drawing, 0, y + 2.3 * mm, label, size=8.2, bold=True)
        view_width = 54 * mm * views / 500
        interaction_width = 48 * mm * interactions / 30
        drawing.add(Rect(31 * mm, y, 54 * mm, 7 * mm, fillColor=base.GRAY, strokeColor=None))
        drawing.add(Rect(31 * mm, y, view_width, 7 * mm, fillColor=color, strokeColor=None))
        chart_label(drawing, 87 * mm, y + 2.1 * mm, f"{views:.0f}", size=8.2, bold=True)
        drawing.add(Rect(108 * mm, y, 48 * mm, 7 * mm, fillColor=base.GRAY, strokeColor=None))
        drawing.add(Rect(108 * mm, y, interaction_width, 7 * mm, fillColor=color, strokeColor=None))
        chart_label(drawing, 158 * mm, y + 2.1 * mm, f"{interactions:.1f}", size=8.2, bold=True)
    chart_label(drawing, 0, 1 * mm, "* Pessoal tem apenas 2 posts nesta comparação; a média é puxada pela foto com Riam.", size=7.4, color=base.MUTED)
    return drawing


def daypart_chart() -> Drawing:
    drawing = Drawing(base.CONTENT_W, 42 * mm)
    metrics = [
        ("Views médias", 338.5, 279.2, 360),
        ("Alcance médio", 205.1, 157.9, 220),
        ("Retenção", 12.7, 10.1, 14),
    ]
    panel_w = base.CONTENT_W / 3
    for index, (label, day, night, maximum) in enumerate(metrics):
        x = index * panel_w
        chart_label(drawing, x + panel_w / 2, 37 * mm, label, size=8, anchor="middle", bold=True)
        baseline = 8 * mm
        max_h = 23 * mm
        for offset, value, color, slot in [
            (panel_w * 0.31, day, TECH, "Dia"),
            (panel_w * 0.61, night, CHART_GRID, "Noite"),
        ]:
            height = max_h * value / maximum
            drawing.add(Rect(x + offset - 5 * mm, baseline, 10 * mm, height, fillColor=color, strokeColor=None))
            value_text = f"{value:.1f}s" if label == "Retenção" else f"{value:.0f}"
            chart_label(drawing, x + offset, baseline + height + 2 * mm, value_text, size=7.6, anchor="middle", bold=True)
            chart_label(drawing, x + offset, 3 * mm, slot, size=7.4, color=base.MUTED, anchor="middle")
        if index < 2:
            drawing.add(Line(x + panel_w, 3 * mm, x + panel_w, 37 * mm, strokeColor=CHART_GRID, strokeWidth=0.7))
    return drawing


def weekday_chart() -> Drawing:
    drawing = Drawing(base.CONTENT_W, 60 * mm)
    labels = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    views = [186.0, 441.3, 286.8, 230.3, 314.3, 379.0, 362.8]
    hooks = [0.393, 0.5425, 0.6333, 0.46, 0.51, 0.42, 0.50]
    x0 = 16 * mm
    plot_w = base.CONTENT_W - 29 * mm
    y0 = 10 * mm
    plot_h = 37 * mm
    chart_label(drawing, 0, 55 * mm, "Barras: visualizações médias", size=7.8, color=TECH, bold=True)
    chart_label(drawing, 69 * mm, 55 * mm, "Linha: gancho médio dos vídeos", size=7.8, color=PERSONAL, bold=True)
    for fraction in [0, 0.5, 1]:
        y = y0 + plot_h * fraction
        drawing.add(Line(x0, y, x0 + plot_w, y, strokeColor=CHART_GRID, strokeWidth=0.6))
        chart_label(drawing, x0 - 2 * mm, y - 1.5 * mm, f"{int(450*fraction)}", size=6.8, color=base.MUTED, anchor="end")
        chart_label(drawing, x0 + plot_w + 2 * mm, y - 1.5 * mm, f"{int(70*fraction)}%", size=6.8, color=base.MUTED)
    step = plot_w / len(labels)
    hook_points = []
    for index, (label, view, hook) in enumerate(zip(labels, views, hooks)):
        center = x0 + step * (index + 0.5)
        bar_h = plot_h * view / 450
        bar_color = AUTHORITY if index == 1 else TECH
        drawing.add(Rect(center - 4.2 * mm, y0, 8.4 * mm, bar_h, fillColor=bar_color, strokeColor=None))
        chart_label(drawing, center, 4 * mm, label, size=7.2, color=base.MUTED, anchor="middle", bold=index in (1, 2))
        hook_y = y0 + plot_h * hook / 0.70
        hook_points.append((center, hook_y))
    for first, second in zip(hook_points, hook_points[1:]):
        drawing.add(Line(first[0], first[1], second[0], second[1], strokeColor=PERSONAL, strokeWidth=1.8))
    for index, (x, y) in enumerate(hook_points):
        drawing.add(Circle(x, y, 2.1 * mm, fillColor=base.RED if index == 2 else PERSONAL, strokeColor=base.WHITE, strokeWidth=0.8))
    chart_label(drawing, hook_points[1][0], y0 + plot_h * views[1] / 450 + 2 * mm, "441", size=7.4, color=AUTHORITY, anchor="middle", bold=True)
    chart_label(drawing, hook_points[2][0], hook_points[2][1] + 3 * mm, "63%", size=7.4, color=base.RED, anchor="middle", bold=True)
    return drawing


def paid_content_chart() -> Drawing:
    drawing = Drawing(base.CONTENT_W, 43 * mm)
    chart_legend(
        drawing,
        [("Técnico", TECH), ("Autoridade", AUTHORITY), ("Pessoal", PERSONAL)],
        39 * mm,
    )
    x0 = 34 * mm
    bar_w = base.CONTENT_W - x0
    y = 23 * mm
    chart_label(drawing, 0, y + 3 * mm, "Reconhecimento", size=8.1, bold=True)
    x = x0
    for value, color in zip([35, 50, 15], [TECH, AUTHORITY, PERSONAL]):
        width = bar_w * value / 100
        drawing.add(Rect(x, y, width, 9 * mm, fillColor=color, strokeColor=base.WHITE, strokeWidth=0.5))
        chart_label(drawing, x + width / 2, y + 3.2 * mm, f"{value}%", size=8.2, color=base.WHITE if color != PERSONAL else base.INK, anchor="middle", bold=True)
        x += width
    y = 8 * mm
    chart_label(drawing, 0, y + 3 * mm, "Captação", size=8.1, bold=True)
    drawing.add(Rect(x0, y, bar_w, 9 * mm, fillColor=base.NAVY, strokeColor=None))
    chart_label(drawing, x0 + bar_w / 2, y + 3.2 * mm, "Formatos validados: Direto + Conversa", size=8.2, color=base.WHITE, anchor="middle", bold=True)
    return drawing


def build() -> None:
    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=base.A4,
        leftMargin=base.LEFT,
        rightMargin=base.RIGHT,
        topMargin=base.TOP,
        bottomMargin=base.BOTTOM,
        title="Análise Estratégica do Perfil de Gustavo Lima - Agosto de 2026",
        author="Equipe de estratégia",
        subject="Texto para reunião: conteúdo, tráfego pago, persona e vendas",
    )
    frame = Frame(
        base.LEFT,
        base.BOTTOM,
        base.CONTENT_W,
        base.PAGE_H - base.TOP - base.BOTTOM,
        id="normal",
    )
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=base.on_page)])

    story = []

    # Capa
    story += [Spacer(1, 34 * mm)]
    story += [T("TEXTO PARA REUNIÃO | AGOSTO DE 2026", "CoverKicker")]
    story += [T("Alinhamento estratégico do perfil Gustavo Lima", "CoverTitle")]
    story += [T("Visão geral da estratégia, do perfil e do público desejado. O que agosto ensinou, como vamos usar o tráfego pago e o que precisa acontecer para o perfil ajudar a vender.", "CoverSubtitle")]
    story.append(
        base.callout(
            "A ideia central",
            "A gente não está construindo um perfil para colecionar aplauso. Estamos construindo confiança para fazer o cliente certo conversar, receber uma proposta e comprar.",
            fill=base.PALE_GREEN,
            stripe=base.GREEN,
        )
    )
    story.append(PageBreak())

    # Abertura
    story += page_title("Antes de falar de número, quero alinhar a nossa régua", "Por que esse perfil existe")
    story.append(T("Plano de saúde não é um mercado de desejo. Ninguém acorda animado porque decidiu comprar um plano. A pessoa procura quando a necessidade aperta, quando a família muda, quando o plano atual decepciona ou quando o medo de ficar desprotegido passa a incomodar."))
    story.append(T("Por isso eu não espero que esse perfil tenha os mesmos números de entretenimento, moda ou humor. E, sinceramente, eu também não quero usar view, curtida e seguidor como troféu. Esses números são úteis, mas só quando ajudam a responder uma pergunta maior: <b>o conteúdo aproximou o cliente certo de uma conversa comercial?</b>"))
    story.append(T("A nossa régua fica assim:"))
    story.append(
        chat_bullets(
            [
                "Primeiro vem a atenção: alcance em não seguidores, gancho e retenção.",
            ]
        )
    )
    story.append(T("Então eu não quero abandonar as métricas de conteúdo. Quero colocar cada uma no lugar certo. View mostra circulação. Venda mostra resultado."))
    story.append(
        base.callout(
            "A frase que resume tudo",
            "O Instagram aquece e constrói confiança. O WhatsApp conduz a decisão. O nosso painel precisa ligar uma coisa à outra.",
            fill=base.LIGHT_BLUE,
            stripe=base.BLUE,
        )
    )
    story.append(PageBreak())

    # Gustavo e persona
    story += page_title("Quem é o Gustavo dentro dessa estratégia", "Posicionamento")
    story.append(T("Gustavo não precisa parecer um influenciador generalista. Ele precisa parecer a escolha segura para uma decisão cara, sensível e cheia de detalhes. O cliente precisa bater o olho no perfil e pensar duas coisas: <b>ele entende do assunto</b> e <b>eu me sentiria confortável falando com ele</b>."))
    story.append(T("É daí que vem a lógica de 70% profissional e 30% pessoal."))
    story.append(
        chat_bullets(
            [
                "Técnico reduz o risco da decisão: cotação, produto, rede, carência, CPT, reajuste, comparativo, contrato e dúvidas de contratação.",
                "Autoridade torna a promessa crível: estrutura da empresa, prêmios, entrevistas com corretores, cultura, bastidores profissionais e prova social.",
                "Pessoal reduz distância: família, esporte, esposa, rotina, crenças, disciplina, procrastinação e interesses reais.",
            ]
        )
    )
    story.append(T("Minha recomendação editorial passa a ser <b>40% técnico, 30% autoridade e 30% pessoal</b>. Assim, o profissional continua em 70%, mas deixa de ser uma caixa única. O técnico aproxima da cotação; a autoridade diminui a dúvida sobre com quem comprar; o pessoal faz o público parar e conhecer a pessoa."))
    story += [T("E quem é a pessoa do outro lado?", "H2x")]
    story.append(T("A persona mais importante é o empresário ou profissional com CNPJ ou MEI, geralmente entre 35 e 54 anos, com família de 3 a 5 pessoas e capacidade provável de investir de R$ 3 mil a R$ 5 mil por mês."))
    story.append(T("Ela não está procurando simplesmente o plano mais barato. Ela quer rede coerente, previsibilidade e a sensação de que não vai descobrir uma pegadinha depois. O medo central é escolher errado: errar na rede, na carência, no reajuste ou no contrato."))
    story.append(T("A hipótese de que esse ICP assiste em silêncio faz sentido. Ele pode não curtir, comentar ou compartilhar. Mas eu trataria isso como hipótese, não como desculpa. Se ele realmente é silencioso, precisamos enxergar o rastro em visitas, mensagens, pedidos de cotação, propostas e vendas."))
    story.append(
        base.callout(
            "A mensagem-mãe",
            "40% técnico + 30% autoridade + 30% pessoal. Nós não vendemos só um produto: reduzimos o risco da escolha, provamos que sabemos executar e criamos proximidade para a conversa começar.",
            fill=base.PALE_GOLD,
            stripe=base.GOLD,
        )
    )
    story.append(PageBreak())

    # Agosto
    story += page_title("O que agosto realmente mostrou", "O plano versus o que foi executado")
    story.append(T("Vou começar reconhecendo o que funcionou: a equipe manteve ritmo. A meta era fazer 30 posts em duas semanas e fizemos 29. Isso representa 96,7% do volume planejado. Então o problema de agosto não foi falta de trabalho."))
    story.append(T("O desvio aconteceu na composição. A estratégia previa uma cotação todas as manhãs e outro conteúdo da linha editorial. Isso significaria 15 cotações. Foram publicadas 5. Ou seja, entregamos apenas 33,3% da meta de cotação, mesmo mantendo quase todo o volume de posts."))
    story.append(T("Com a classificação corrigida, os 29 posts ficaram assim: <b>17 técnicos, 10 de autoridade e 2 pessoais</b>. Em percentual, isso dá 58,6% técnico, 34,5% autoridade e 6,9% pessoal. Ou seja: o profissional ficou em 93,1%. O carrossel do Bitcoin entra no técnico porque usa o risco financeiro de uma internação para falar da necessidade de plano de saúde."))
    story.append(mix_chart())
    story.append(T("Para comparar desempenho de forma justa, usei a primeira leitura de 24 horas dos 29 posts, incluindo o CPT."))
    story.append(category_performance_chart())
    story.append(T("O conteúdo de <b>autoridade foi o sinal mais consistente</b>: média de 413 visualizações, alcance de 264 e 20,7 interações. O técnico ficou em 232 visualizações, alcance de 134 e 9,8 interações. Mesmo com menos posts, autoridade teve 78% mais visualizações, 97% mais alcance e 112% mais interações por publicação."))
    story.append(T("O pessoal teve média de 456 visualizações e 28,5 interações, mas são só dois posts: a foto com Riam e o dump de Roma. A média foi puxada pela foto com Riam, que fez 702 visualizações nas primeiras 24 horas. Então existe potencial de descoberta, mas ainda não existe consistência nem prova de venda."))
    story.append(T("Na leitura acumulada do perfil em <b>20 de agosto</b>, somando as visualizações que apareciam nas publicações de <b>3 a 18 de agosto de 2026</b>, foram 15.357 visualizações e 996 interações, com 57,5% das views vindas de não seguidores. Ao mesmo tempo, apareceram 29 ações de perfil, 16 visitas e <b>4 toques no link da bio</b>. A mensagem circulou; a passagem para o comercial ainda precisa de rastreio melhor."))
    story.append(T("Minha leitura é simples: <b>agosto não provou que a estratégia estava errada; mostrou que executamos volume, concentramos demais no profissional e ainda não demos a cada tipo de conteúdo uma função comercial clara</b>."))
    story.append(
        base.callout(
            "O diagnóstico de agosto",
            "Autoridade merece mais peso na descoberta. Técnico continua sendo a ponte principal para a cotação. Pessoal precisa crescer de 6,9% para 30%, mas com conexão de marca e rastreio até a conversa.",
            fill=base.PALE_RED,
            stripe=base.RED,
        )
    )

    # Contrafactual e formato
    story += page_title("O que teria acontecido se seguíssemos o plano inteiro?", "A resposta honesta")
    story.append(T("Não dá para calcular exatamente um cenário que não aconteceu. Sem publicar as 15 cotações e sem rastrear leads por conteúdo, qualquer promessa de 'teríamos vendido X a mais' seria chute com roupa de relatório."))
    story.append(T("Agora existe uma correção importante: 15 cotações em 30 posts já ocupariam 50% da grade com conteúdo técnico. Se mantivéssemos 30% pessoal, sobrariam só 20% para autoridade. Portanto, o plano antigo completo viraria <b>50% técnico, 20% autoridade e 30% pessoal</b>. É executável, mas não aproveita o fato de que autoridade foi a categoria profissional mais forte no topo do funil."))
    story.append(T("Mas dá para dizer o que provavelmente mudaria:"))
    story.append(
        chat_bullets(
            [
                "Teríamos muito mais repetição de uma pauta de alta intenção. A cotação diária colocaria a oferta na frente do público todos os dias.",
                "Teríamos mais oportunidades de descobrir qual abertura, faixa de preço, praça e perfil de família geram conversa.",
                "Com 30% pessoal executado, o perfil provavelmente ficaria mais humano e teria mais tentativas de descoberta.",
                "A comparação entre semanas seria mais justa, porque estaríamos testando uma rotina fixa e não uma sequência improvisada.",
            ]
        )
    )
    story.append(T("Mesmo assim, eu ajustaria o próximo ciclo para <b>40% técnico, 30% autoridade e 30% pessoal</b>. Como vamos operar com um post diário durante a integração da equipe, a tradução prática da semana é 3 técnicos, 2 de autoridade e 2 pessoais. A cotação deixa de ser sete dias por semana e passa a ser uma presença forte nos dias úteis, abrindo espaço para a prova de autoridade que agosto mostrou funcionar."))
    story += [T("É possível definir o formato de cada dia?", "H2x")]
    story.append(T("Ainda não com segurança estatística. Duas semanas não são suficientes para decretar que carrossel funciona na quarta, foto na terça e vídeo na quinta. O que dá para fazer agora é sair do chute usando <b>função</b>."))
    story.append(T("Em vez de falar 'terça é dia de Reel', eu prefiro falar: 'terça à noite é dia de prova e autoridade'. O formato vem depois. Pode ser Reel, carrossel ou foto, desde que cumpra a função."))
    story.append(T("Eu manteria um calendário fixo por 4 a 6 semanas. Aí sim compararíamos o mesmo tipo de pauta em dias e horários diferentes. Um único post fraco não condena um formato nem um dia da semana."))
    story.append(
        base.callout(
            "A regra provisória",
            "A gente não escolhe o formato porque o algoritmo supostamente gosta dele naquele dia. Escolhe porque naquela posição da semana precisa gerar oferta, educação, prova ou proximidade.",
            fill=base.LIGHT_BLUE,
            stripe=base.BLUE,
        )
    )

    # Sinais de dia e horário
    story += page_title("Há sinais de dia e horário que valem um teste sério", "Diurno, terça e quarta")
    story.append(T("Aqui está a leitura que não pode ficar de fora: nas primeiras 24 horas, os <b>15 conteúdos diurnos</b> tiveram média de 339 visualizações, alcance de 205 e retenção de 12,7 segundos. Os <b>14 noturnos</b> ficaram em 279 visualizações, alcance de 158 e retenção de 10,1 segundos."))
    story.append(daypart_chart())
    story.append(T("Isso representa uma vantagem diurna de 21% em visualizações, 30% em alcance e 26% em retenção. As interações também foram 14% maiores durante o dia: 15,7 contra 13,9 por post."))
    story.append(T("Quando abrimos por dia da semana, a <b>terça teve a maior média de visualizações: 441 por post</b>, além de 27,5 interações médias. A <b>quarta teve o melhor gancho médio dos vídeos: 63,3%</b>."))
    story.append(weekday_chart())
    story.append(T("Eu usaria esses sinais assim: terça recebe uma pauta com potencial de distribuição; quarta recebe um vídeo que depende de uma abertura forte; e os slots diurnos ficam com os conteúdos prioritários de técnico e autoridade."))
    story.append(T("Mas eu não chamaria isso de regra ainda. Segunda tem cinco posts comparáveis; os demais dias, quatro, e quarta tem três vídeos com gancho medido. Além disso, terça concentrou bons conteúdos e autoridade apareceu bastante no período diurno. O efeito pode ser da pauta, não do relógio."))
    story.append(
        base.callout(
            "Como transformar sinal em decisão",
            "Rodar o mesmo desenho por 4 a 6 semanas e alternar pautas equivalentes entre dia e noite. Terça e quarta entram como hipóteses prioritárias, não como superstição de calendário.",
            fill=base.PALE_GREEN,
            stripe=base.GREEN,
        )
    )

    # Escala
    story += page_title("Quanto tempo cada conteúdo continua escalando", "A curva orgânica")
    story.append(T("Eu usaria três janelas de leitura. As primeiras 24 horas mostram se o gancho funcionou. Sete dias mostram a maior parte da distribuição. Quatorze dias mostram se existe cauda. Ainda não temos amostra de três semanas suficiente para concluir alguma coisa."))
    story.append(T("O que apareceu em agosto:"))
    story.append(
        chat_bullets(
            [
                "Carrossel: cresceu 62,6% entre 24 horas e 7 dias, e mais 22,2% entre 7 e 14 dias. Foi a melhor cauda observada, embora a amostra ainda seja pequena.",
                "Cotação: cresceu 28,8% até 7 dias e apenas 6,3% depois. A maior parte da entrega acontece na primeira semana.",
                "Conteúdo espontâneo: cresceu 34,5% até 7 dias e 5,5% depois. Tem descoberta inicial, mas pouca cauda.",
                "Frase: cresceu 28,4% até 7 dias e 22,1% até 14 dias. É um sinal interessante, mas a segunda janela vem de uma única amostra.",
                "Foto: cresceu 30,5% até 7 dias. Não existe amostra suficiente de 14 dias.",
            ]
        )
    )
    story.append(T("Na prática, eu não escolheria conteúdo para impulsionar olhando só as primeiras 24 horas. Deixaria o orgânico respirar por 7 dias, exceto quando o conteúdo for muito datado."))
    story += [T("E os vídeos de cotação?", "H2x")]
    story.append(T("A linha de base das primeiras 24 horas ficou em <b>14,2 segundos de retenção média</b>, com mediana de 13 segundos; <b>46,2% de gancho médio</b>, com mediana de 49%; e <b>268 visualizações médias</b>, com alcance médio de 166."))
    story.append(T("Eu trataria isso como nosso ponto de partida, não como benchmark universal. O próximo ciclo precisa testar abertura, duração, clareza da oferta e CTA. E precisa medir conversa, porque um vídeo pode reter bem e continuar vendendo nada."))
    story.append(
        base.callout(
            "Um cuidado importante",
            "Cotação envelhece. Para anúncio contínuo, prefiro uma promessa perene como 'receba uma simulação atualizada' em vez de manter preço antigo rodando como se ainda fosse atual.",
            fill=base.PALE_GOLD,
            stripe=base.GOLD,
        )
    )
    story.append(PageBreak())

    # Pago
    story += page_title("Agora entra o tráfego pago", "O papel de técnico, autoridade e pessoal")
    story.append(T("Eu não dividiria a verba igualmente entre as três categorias. Cada campanha pede uma função diferente. Reconhecimento precisa fazer a pessoa parar e confiar; captação precisa transformar essa confiança em uma conversa comercial."))
    story.append(T("Na campanha de <b>reconhecimento</b>, minha recomendação é <b>50% autoridade, 35% técnico e 15% pessoal</b>. Autoridade recebe a maior fatia porque foi a categoria mais consistente em alcance e interação. Técnico mantém a conexão com o problema. Pessoal entra como teste controlado de descoberta, sempre com uma ponte para a marca."))
    story.append(T("Na campanha de <b>captação</b>, a gente não vai copiar o mix editorial nem reaproveitar o post orgânico como regra. Já existe um formato validado de venda, separado do feed: <b>Direto</b> e <b>Conversa</b>. Ele deve ser medido por conversa qualificada, proposta e venda."))
    story.append(paid_content_chart())
    story += [T("O caso do vídeo 'Pense menos, faça mais'", "H2x")]
    story.append(T("Esse Reel foi o ponto fora da curva: 3.713 visualizações, 353 interações e 86,9% de não seguidores. Ele mostrou que a camada pessoal consegue furar a bolha. Só que gerou apenas 1 seguidor atribuído e não mostrou passagem para venda."))
    story.append(T("Minha leitura não é 'conteúdo pessoal não serve'. É o contrário: ele pode servir muito bem para descoberta. Mas precisa de uma ponte. Essa ponte pode ser uma legenda, uma sequência de Stories, um destaque ou uma chamada que conecte o valor pessoal ao jeito como Gustavo cuida do cliente."))
    story += [T("O que merece verba de reconhecimento", "H2x")]
    story.append(
        chat_bullets(
            [
                "Chegou a não seguidores.",
                "Teve gancho e retenção.",
                "Gerou salvamento ou compartilhamento.",
                "Provocou visita ou ação de perfil.",
                "Fala com o ICP e permite uma ponte para o comercial.",
            ]
        )
    )
    story.append(base.callout("O que eu não faria", "Não impulsionaria um post só porque foi o que mais deu view. Alcance alto sozinho não é sinal verde automático.", fill=base.PALE_RED, stripe=base.RED))

    # Verba
    story += page_title("Como eu dividiria os R$ 1.000", "Duas campanhas e foco")
    story.append(T("Estou tratando os R$ 1.000 como verba mensal. Com esse tamanho de orçamento, eu faria só duas campanhas, com 2 ou 3 criativos em cada. Mais do que isso seria pulverizar R$ 33 por dia até o aprendizado virar poeira."))
    story.append(T("A divisão seria:"))
    story.append(
        chat_bullets(
            [
                "R$ 300, ou 30%, para reconhecimento: R$ 150 em autoridade, R$ 105 em técnico e R$ 45 em pessoal.",
                "R$ 700, ou 70%, para captação nos formatos Direto e Conversa, ajustando a divisão entre eles pelo custo por conversa qualificada, proposta e venda.",
                "R$ 0 para remarketing nesta primeira fase.",
            ]
        )
    )
    story.append(T("Na descoberta, o objetivo é apresentar Gustavo para pessoas novas e observar quem realmente para, assiste e demonstra interesse. Na captação, o anúncio precisa começar uma conversa no WhatsApp ou no Direct."))
    story.append(T("Eu não usaria o botão de impulsionar como centro da estratégia. No reconhecimento, usaria os conteúdos vencedores como anúncios dentro do Gerenciador de Anúncios. Na captação, entrariam os criativos Direto e Conversa, em campanhas separadas, com objetivo, público e rastreio próprios."))
    story += [T("A captação precisa qualificar sem assustar", "H2x")]
    story.append(T("A conversa pode começar leve, mas precisa chegar em até seis informações: cidade, idades, CNPJ ou MEI, plano atual, urgência e faixa de investimento. O nosso indicador principal deixa de ser custo por clique e passa a ser <b>custo por conversa qualificada</b>."))
    story += [T("Quando a verba subir", "H2x")]
    story.append(
        chat_bullets(
            [
                "Com R$ 3 mil: 25% reconhecimento, 55% captação e 20% remarketing.",
                "Com R$ 5 mil ou mais: 20% reconhecimento, 55% captação e 25% remarketing.",
            ]
        )
    )
    story.append(T("Remarketing entra quando houver público quente suficiente: quem engajou, viu vídeos, visitou o perfil, iniciou conversa ou chegou ao site sem fechar. Aí mostramos prova social, comparativos e objeções; se a frequência subir demais, reduzimos a verba."))
    story.append(PageBreak())

    # Calendário e perfil
    story += page_title("Como eu organizaria a rotina do perfil", "Conteúdo e presença")
    story.append(T("Neste momento de integração da equipe, eu começaria com <b>um post por dia</b>. Não é recuo: é a forma de criar rotina, clareza de função e consistência sem falhar. O conteúdo prioritário fica no período diurno; terça aproveita o sinal de distribuição e quarta recebe uma abertura especialmente forte:"))
    story.append(
        chat_bullets(
            [
                "Segunda: cotação ou dúvida técnica de alta intenção.",
                "Terça: autoridade ou prova com potencial de distribuição.",
                "Quarta: vídeo técnico com o melhor gancho da semana.",
                "Quinta: pessoal, com esporte, família, rotina ou valores.",
                "Sexta: autoridade, como mercado, prêmio, entrevista ou caso.",
                "Sábado: técnico, como FAQ de risco, rede, CPT, carência ou reajuste.",
                "Domingo: pessoal, com reflexão, família ou crença que aproxime sem fugir da marca.",
            ]
        )
    )
    story.append(T("Isso gera <b>3 conteúdos técnicos, 2 de autoridade e 2 pessoais</b> por semana: 42,9%, 28,6% e 28,6%, a tradução prática mais próxima do 40/30/30 em uma grade de 7 posts. Também preserva presença de cotação sem deixar a cotação engolir a autoridade."))
    story += [T("O perfil também precisa trabalhar quando não tem post novo", "H2x")]
    story.append(T("Os destaques já estão criados: <b>Prêmios, Inspirações, Família, Corretora e Assessoria</b>. O que falta agora são os conteúdos próprios dentro deles. Se o destaque está lá, ele precisa explicar."))
    story.append(T("Cada destaque começa com um vídeo curto do Gustavo explicando o assunto e para quem aquilo serve. Não precisa de produção cinematográfica. Precisa de presença, clareza e atualização."))
    story.append(T("No período analisado, a interação do Gustavo com o público foi baixa: pouco movimento de Stories e, principalmente, pouca resposta aos comentários. Isso enfraquece a relação justamente onde o perfil pode transformar atenção silenciosa em conversa."))
    story.append(T("Nos Stories, eu prefiro uma rotina pequena que aconteça: 2 ou 3 quadros em quatro dias por semana. Um momento humano, uma cotação ou bastidor e uma dúvida ou convite para responder."))
    story.append(T("E tem uma parte que não pode continuar esquecida: responder as pessoas. Comentário não é fim de funil. A equipe responde em até 24 horas, faz uma pergunta e, quando existe contexto, conduz para Direct ou WhatsApp. Sem spam e sem texto automático fingindo intimidade."))
    story.append(base.callout("A regra de ouro", "Se existe destaque, ele precisa explicar. Se existe engajamento, alguém precisa responder.", fill=base.PALE_GOLD, stripe=base.GOLD))
    # Medição e fechamento
    story += page_title("Como vamos saber se tudo isso está funcionando", "Da atenção até a venda")
    story.append(T("Eu montaria o painel em três níveis:"))
    story.append(
        chat_bullets(
            [
                "Atenção: não seguidores, CPM, gancho, retenção e visualização qualificada.",
                "Intenção: visita ao perfil, salvamento, compartilhamento, mensagem e conversa qualificada.",
                "Negócio: proposta, taxa de proposta, venda, taxa de fechamento, CAC, receita e ROAS.",
            ]
        )
    )
    story.append(T("A planilha comercial precisa registrar data, contato, campanha, criativo, pauta, qualificação, proposta, venda, ticket e receita. Sem essa trilha, a gente vai continuar discutindo curtida porque é o número mais fácil, não porque é o mais importante."))
    story += [T("O que eu faria nos próximos 90 dias", "H2x")]
    story.append(
        chat_bullets(
            [
                "Nos primeiros 30 dias: integrar funções, fixar um post diário, preencher os destaques, criar a rotina de Stories, lançar 30% de reconhecimento e 70% de captação e responder os engajamentos.",
                "De 31 a 60 dias: testar três ângulos de mensagem, cortar desperdício, qualificar os leads e transformar as objeções do comercial em conteúdo.",
                "De 61 a 90 dias: aumentar os criativos que geram conversa e venda, revisar o mix e abrir remarketing se já existir público suficiente.",
            ]
        )
    )
    story.append(T("A maior mudança desta próxima fase não é simplesmente colocar dinheiro. É fazer o conteúdo, o perfil, o atendimento e a planilha comercial trabalharem como uma coisa só."))
    story.append(
        base.callout(
            "Para fechar a reunião",
            "A meta não é viralizar. É fazer o cliente certo pensar: 'é com ele que eu vou falar'.",
            fill=base.LIGHT_BLUE,
            stripe=base.BLUE,
        )
    )
    story += [Spacer(1, 10)]
    story += [T("Notas sobre a análise", "H2x")]
    story.append(T("A execução analisada cobre aproximadamente duas semanas. A comparação por categoria usa 29 posts com leitura equivalente de 24 horas, incluindo o CPT. Pessoal tem apenas 2 posts nessa amostra. Dia e noite têm 15 e 14 posts; segunda tem 5 posts comparáveis e os demais dias, 4; o gancho de quarta vem de 3 vídeos. Os totais por publicação não representam usuários únicos e ainda não existe atribuição completa entre conteúdo e venda. Por isso, percentuais, verba e calendário são hipóteses de trabalho que precisam ser revisadas pelo resultado comercial.", "ChatSmall"))
    story += [T("Fontes: planilha 'Postagens 2026'; Insights @gustavojcluz (leitura em 20 de agosto, posts de 3 a 18); Dossiê do Mercado; persona Lannister; Meta.", "ChatSmall")]

    doc.build(story)
    print(f"PDF conversacional criado em: {OUTPUT}")


if __name__ == "__main__":
    build()
