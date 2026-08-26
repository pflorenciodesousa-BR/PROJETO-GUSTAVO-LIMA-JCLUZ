$NeutroPath = "C:\Users\Jcluz\Antigravity IDE\Estrutura Carrossel\Playbook_Carrosseis_v3_Neutro.md"
$GustavoPath = "C:\Users\Jcluz\Antigravity IDE\Estrutura Carrossel\informacoes Gustavo Lima\playbook_carrosseis_gustavo_lima.md"

$NeutroRules = @"

---

## 🛡️ 5. Travas de Segurança e Engenharia (Anti-Bug)

**Estas regras são absolutas e não podem ser violadas durante a construção de um HTML:**

1. **A Regra das Legendas (Web-App):**
   - Se o usuário escolher "Uma Legenda por Imagem", a IA está **PROIBIDA** de criar uma caixa de texto global no fim da página.
   - O código HTML deve gerar uma `<textarea>` independente **abaixo de cada slide** dentro da grade (`.slides-grid`), contendo o texto da "camada adicional" específica daquele slide, seguido de um botão para "Copiar Legenda".

2. **A Física da Sobreposição (Z-Index):**
   - Imagens de fundo e *Sketches* desenhados (divs com `background-image`) **NUNCA** podem ultrapassar o `z-index: 0`.
   - Todos os textos de um slide devem estar envelopados em um container com `position: relative; z-index: 2;` para garantir que o desenho de fundo jamais atrapalhe a leitura.

3. **CSS das Ilustrações (A Moldura Quadrada):**
   - Ao aplicar uma ilustração (como os Business Sketches) sobre um slide de fundo sólido, **nunca use `transform: scale()`** no container da imagem, pois isso revela as bordas "quadradas" da imagem gerada por IA.
   - O container da imagem deve ter `width: 100%; height: 100%;` e o tamanho do desenho deve ser controlado via `background-size` (ex: `65%`) e `background-position`.
   - **OBRIGATÓRIO:** Para apagar as quinas e fundir perfeitamente o fundo do sketch com o fundo do slide, aplique o seguinte CSS no div da imagem:
     `mix-blend-mode: darken; filter: brightness(1.05); opacity: 0.25;`
"@

$GustavoRules = @"

---

## 🛡️ 5. Travas de Segurança Visuais (Anti-Bug)

**Estas regras são absolutas e não podem ser violadas durante a direção de arte do Gustavo Lima:**

1. **Proibição de Clones (Sketches):**
   - É **EXTREMAMENTE PROIBIDO** repetir a mesma imagem de *Business Sketch* em dois slides diferentes.
   - Cada slide que exigir uma ilustração de fundo deve ter o seu próprio arquivo de imagem gerado de forma exclusiva.

2. **Rodízio de Ancoragem:**
   - As ilustrações não podem ficar ancoradas sempre no mesmo canto (ex: sempre no bottom-right).
   - A IA deve planejar um **Rodízio de Posições** (Top-Right, Bottom-Left, Top-Left) de acordo com o alinhamento do texto para gerar dinamismo visual e evitar que o carrossel pareça engessado ou colado de forma genérica.
"@

[System.IO.File]::AppendAllText($NeutroPath, $NeutroRules, [System.Text.Encoding]::UTF8)
[System.IO.File]::AppendAllText($GustavoPath, $GustavoRules, [System.Text.Encoding]::UTF8)

Write-Host "Playbooks atualizados com sucesso com as novas travas de seguranca."
