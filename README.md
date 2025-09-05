# blog-profissional
Desenvolvimento de site profissional em HTML, CSS, JavaScript e Python (Flask), com blog integrado às redes sociais, portfólio, divulgação de serviços, histórico profissional e loja virtual para venda de materiais didáticos, aulas particulares, marketing digital e trabalhos acadêmicos.

Estrutura de pastas

meu_site_profissional/

├─ app.py                      # Aplicação Flask com rotas e integração do blog e checkout

├─ requirements.txt            # Dependências Python

├─ README.md                   # Passo a passo para rodar e publicar

├─ data/

│  ├─ products.json            # Base simples de produtos/serviços

│  └─ social.json              # Suas redes sociais para renderização automática

├─ content/

│  └─ blog/

│     ├─ 2025-09-01-boas-vindas.md

│     └─ 2025-09-03-dicas-de-estudo.md

├─ static/

│  ├─ css/

│  │  └─ style.css            # Estilos globais

│  ├─ js/

│  │  └─ main.js              # Lógica do front-end (menu, carrinho, etc.)

│  └─ img/

│     ├─ avatar.jpg           # Sua foto (opcional)

│     └─ og-image.png         # Imagem para compartilhamento nas redes

└─ templates/

   ├─ base.html                # Base com head, header, footer
   
   ├─ index.html               # Home
   
   ├─ services.html            # Serviços (aulas, marketing digital, trabalhos acadêmicos)
   
   ├─ blog.html                # Lista de posts do blog
   
   ├─ post.html                # Página de post individual
   
   ├─ resume.html              # Histórico profissional / currículo
   
   ├─ shop.html                # Loja (listagem de produtos)
   
   ├─ cart.html                # Carrinho (frontend)
   
   └─ checkout.html            # Checkout (envio do pedido para o backend)

# Meu Site Profissional — Flask + HTML/CSS/JS

## Rodando localmente

1. Crie e ative um ambiente virtual
   ```bash
   python -m venv .venv
   # Linux/Mac
   source .venv/bin/activate
   # Windows (PowerShell)
   .venv\\Scripts\\Activate.ps1
````

2. Instale as dependências

   ```bash
   pip install -r requirements.txt
   ```
3. Execute o servidor

   ```bash
   set FLASK_APP=app.py  # Windows (cmd)
   $env:FLASK_APP = "app.py"  # Windows (PowerShell)
   export FLASK_APP=app.py     # Linux/Mac
   flask run
   ```
4. Acesse [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Estrutura

Veja `app.py`, `templates/`, `static/`, `data/` e `content/`.

## Deploy (Render, Railway, etc.)

### Render

* Conecte seu repositório GitHub.
* Escolha *Web Service*, runtime *Python*, comando de execução:

  ```bash
  gunicorn app:app --preload --workers 2 --timeout 60
  ```
* Adicione um arquivo `Procfile` (opcional) com `web: gunicorn app:app`
* Adicione variável `PORT` se necessário (Render já injeta).

### Railway / Fly.io / Deta

* Processo semelhante: aponte para `app:app` com `gunicorn`.

## GitHub Pages

* Somente front-end (HTML/CSS/JS). Se quiser usar **somente** a parte estática, publique `templates` renderizadas como HTML puro (ou gere um build estático). O backend Flask não roda no Pages.

## Pagamentos

* Este projeto **não** integra pagamento diretamente. Para produção, conecte **Stripe, PagSeguro, Mercado Pago ou Pix**.
* Exemplo futuro: no `checkout` enviar ao seu provedor de pagamentos e registrar o pedido em um banco de dados.

## Segurança & Privacidade

* Não publique dados sensíveis no repositório.
* Se integrar e-mails, use variáveis de ambiente para chaves.
