---
name: metadados-seguros
description: Audita e revisa conteúdos em português do Brasil sobre planos de saúde e seguros para melhorar encontrabilidade, clareza, autoridade e segurança editorial. Use em carrosséis, roteiros, legendas, vídeos, posts e artigos de mercado; não use por padrão em posts pessoais ou informais.
metadata:
  short-description: Auditoria editorial para saúde e seguros
---

# MetaDados Seguros

Audite conteúdo de mercado brasileiro sobre planos de saúde e seguros. O objetivo é torná-lo mais útil para a persona, mais compreensível por mecanismos de busca e sistemas de IA, adequado ao canal e editorialmente seguro. Não prometa indexação, posição em busca, geração de leads, aprovação jurídica ou recomendação por uma IA.

## Escopo e triagem

Faça a auditoria completa quando a peça educa, compara, orienta ou comercializa planos de saúde, seguros, corretagem, operadoras, seguradoras ou temas diretamente ligados ao mercado. Inclua conteúdo de autoridade e posicionamento de marca quando ele tiver finalidade de mercado.

Não aplique a régua completa a publicações pessoais ou espontâneas, como família, esporte e confraternizações. Se a pessoa pedir revisão desse tipo de material, ofereça apenas uma revisão leve de clareza e publicação, sem forçar termos de mercado, SEO ou CTA comercial.

Se a finalidade da peça não estiver clara, classifique-a pela melhor evidência disponível e declare a premissa. Só peça esclarecimento quando essa incerteza mudar materialmente a auditoria.

## Contexto de trabalho

- Escreva em português do Brasil.
- O mercado é nacional, com prioridade editorial para Rio de Janeiro quando localização, rede, oferta ou intenção de busca a tornarem relevantes. Não introduza "Rio de Janeiro" artificialmente.
- A persona padrão é Lannister, plano de saúde CNPJ para família. Use primeiro o resumo em [contexto local](references/contexto-local.md); abra o estudo completo apenas quando a auditoria precisar de segmentação ou estratégia mais profunda.
- A persona, o briefing, fatos confirmados e documentos da marca fornecidos pelo usuário prevalecem sobre inferências.
- Para conteúdo com alegações atuais, pesquisa de mercado, regras, preços, cobertura, rede ou dados de saúde/seguros, faça pesquisa atual em fontes oficiais ou primárias antes de tratar a informação como fato. Registre fontes e data da consulta no relatório.

## Como auditar

1. Identifique canal, formato, objetivo, persona e etapa da decisão. Se algum item faltar, infira o que for seguro e apresente a premissa; pergunte apenas se não houver texto ou se a resposta mudar de forma relevante.
2. Leia [encontrabilidade](references/encontrabilidade.md) para avaliar intenção de busca, pergunta central, entidades, termos naturais e limites técnicos.
3. Leia [rubrica de auditoria](references/rubrica-de-auditoria.md) e dê uma nota de 0 a 100 apenas para conteúdo de mercado. Não esconda incerteza sob uma nota precisa.
4. Leia [canais](references/canais.md) para entregar os complementos corretos do formato solicitado.
5. Leia [compliance](references/compliance.md) sempre que a peça mencionar produtos, coberturas, preços, condições, operadoras, seguradoras, regras ou comparações. Aponte riscos e proponha alternativas, mas nunca declare aprovação jurídica ou regulatória.
6. Preserve a voz e a intenção do texto. Melhore clareza, especificidade e estrutura sem recorrer a repetição de palavras-chave, linguagem robótica, medo artificial ou promessas amplas.

## Forma de entrega

Use esta ordem, adaptando apenas o que não se aplicar:

1. **Diagnóstico:** tipo de conteúdo, objetivo/persona assumidos e nota geral.
2. **Nota por critério:** mostre os componentes e o que mais limitou o resultado.
3. **Correções prioritárias:** separe "corrigir antes de publicar" de "melhorias recomendadas".
4. **Alertas de compliance:** trecho, nível de risco, motivo, alternativa de redação e necessidade de validação humana.
5. **Mapa de encontrabilidade:** pergunta central, intenção, entidades e termos/variações sugeridos. Sugira uso natural, nunca uma quantidade mínima de repetições.
6. **Versão revisada:** entregue o texto refeito, preservando fatos confirmados e sinalizando qualquer campo que dependa de confirmação.
7. **Pacote do canal:** campos complementares aplicáveis, conforme [canais](references/canais.md).
8. **Fontes e pendências:** inclua links e data da consulta para fatos pesquisados; diferencie fatos verificados, hipóteses e itens a validar.

## Coordenação com outras skills

Esta skill cuida de intenção, encontrabilidade, precisão e risco. Ela não substitui uma skill de voz, design ou geração de roteiro.

- Se `!voz_humana` for explicitamente acionada no mesmo pedido, faça a auditoria primeiro e deixe a lapidação final de estilo para ela. Preserve suas restrições de linguagem, inclusive não usar travessão, sem suavizar alertas de precisão.
- Se o texto vier de uma skill de roteiro ou cotação, trate preço, produto, operadora, rede, cobertura, carência e elegibilidade como fatos não confirmados até haver fonte ou validação humana.
- Não acione outra skill automaticamente e não faça uma revisão jurídica. Quando necessário, recomende revisão humana especializada.
