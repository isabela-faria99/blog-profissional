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
