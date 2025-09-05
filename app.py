# app.py
# -*- coding: utf-8 -*-
# Aplicação Flask que entrega páginas HTML, renderiza blog em Markdown,
# carrega produtos de um JSON, e recebe pedidos de checkout.
#
# Como rodar localmente:
# 1) python -m venv .venv && source .venv/bin/activate  (Linux/Mac)
#    No Windows: py -m venv .venv && .venv\\Scripts\\activate
# 2) pip install -r requirements.txt
# 3) export FLASK_APP=app.py && flask run  (Windows PowerShell: $env:FLASK_APP = "app.py"; flask run)
# 4) Abrir http://127.0.0.1:5000

import json
import os
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from markdown import markdown
from slugify import slugify

# Cria a aplicação Flask
app = Flask(__name__)

# Caminhos base do projeto (para facilitar quando o app roda em outro diretório)
BASE_DIR = Path(__file__).parent
CONTENT_DIR = BASE_DIR / "content" / "blog"
DATA_DIR = BASE_DIR / "data"

# ------------------------------
# Utilitários do Blog
# ------------------------------

def load_posts():
    """Lê todos os arquivos .md em content/blog e devolve uma lista de posts.
    Cada post possui: title, date, slug, html, summary, tags (opcional).
    O formato esperado do arquivo .md é:

    ---
    title: Meu Título
    date: 2025-09-01
    tags: estudo, enem
    ---

    Conteúdo em Markdown do post...
    """
    posts = []

    for md_file in sorted(CONTENT_DIR.glob("*.md"), reverse=True):
        raw = md_file.read_text(encoding="utf-8")

        # Separar metadados do corpo. Metadados simples entre linhas ---
        meta = {}
        body = raw
        if raw.strip().startswith("---"):
            try:
                # Divide somente uma vez: bloco de meta e resto (corpo)
                _, meta_block, body = raw.split("---", 2)
                # Parse simplificado dos metadados (chave: valor por linha)
                for line in meta_block.strip().splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        meta[k.strip().lower()] = v.strip()
            except ValueError:
                # Se não houver formatação correta, segue com corpo inteiro
                body = raw

        title = meta.get("title") or md_file.stem.replace("-", " ").title()
        date_str = meta.get("date") or "1970-01-01"
        tags_str = meta.get("tags") or ""
        tags = [t.strip() for t in tags_str.split(",") if t.strip()]

        # Cria um slug amigável para URL (/blog/<slug>)
        slug = slugify(f"{date_str}-{title}")

        # Converte Markdown -> HTML
        html_content = markdown(body)

        # Gera um resumo simples: primeiras 160 palavras do corpo sem HTML
        summary = " ".join(body.strip().split()[:40]) + ("..." if len(body.split()) > 40 else "")

        # Converte a data em objeto para ordenação/exibição
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            date = datetime(1970, 1, 1).date()

        posts.append({
            "title": title,
            "date": date,
            "slug": slug,
            "html": html_content,
            "summary": summary,
            "tags": tags,
        })

    # Ordena por data desc
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def get_post_by_slug(slug):
    """Busca um post pelo slug."""
    for post in load_posts():
        if post["slug"] == slug:
            return post
    return None

# ------------------------------
# Utilitários de dados (produtos e redes sociais)
# ------------------------------

def load_products():
    """Carrega lista de produtos/serviços a partir de data/products.json"""
    products_path = DATA_DIR / "products.json"
    if not products_path.exists():
        return []
    return json.loads(products_path.read_text(encoding="utf-8"))


def load_social():
    """Carrega redes sociais de data/social.json"""
    social_path = DATA_DIR / "social.json"
    if not social_path.exists():
        return {}
    return json.loads(social_path.read_text(encoding="utf-8"))

# ------------------------------
# Rotas públicas
# ------------------------------

@app.route("/")
def home():
    # Página inicial: destaca serviços e últimos posts
    posts = load_posts()[:3]  # últimos 3
    return render_template("index.html", posts=posts, social=load_social())


@app.route("/services")
def services():
    # Página de serviços: aulas, marketing digital, trabalhos acadêmicos, etc.
    return render_template("services.html", social=load_social())


@app.route("/resume")
def resume():
    # Histórico profissional (você pode editar o HTML em templates/resume.html)
    return render_template("resume.html", social=load_social())


@app.route("/blog")
def blog():
    # Lista todos os posts
    posts = load_posts()
    return render_template("blog.html", posts=posts, social=load_social())


@app.route("/blog/<slug>")
def blog_post(slug):
    # Página individual de post
    post = get_post_by_slug(slug)
    if not post:
        abort(404)
    return render_template("post.html", post=post, social=load_social())


@app.route("/shop")
def shop():
    # Lista de produtos/serviços
    products = load_products()
    return render_template("shop.html", products=products, social=load_social())


@app.route("/cart")
def cart():
    # Carrinho é gerenciado no front-end (localStorage), mas renderizamos a página
    return render_template("cart.html", social=load_social())


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    # Página e endpoint de checkout
    # GET: mostra formulário de dados do cliente + resumo do carrinho (via JS)
    # POST: recebe os dados do pedido que vêm do front-end (fetch AJAX)
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        # Estrutura esperada:
        # {
        #   "customer": {"name": "...", "email": "...", "phone": "..."},
        #   "items": [{"id": "prod1", "title": "Aula particular", "qty": 2, "price": 120.0}],
        #   "total": 240.0
        # }

        # Validação simples
        customer = data.get("customer", {})
        items = data.get("items", [])
        total = data.get("total", 0)

        if not customer.get("name") or not customer.get("email") or not items:
            return jsonify({"ok": False, "message": "Dados incompletos."}), 400

        # Salva o pedido em um arquivo .json (demo). Em produção: banco de dados e pagamento.
        orders_dir = BASE_DIR / "data" / "orders"
        orders_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        order_path = orders_dir / f"order-{ts}.json"
        order_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

        # Aqui você poderia:
        # - Enviar e-mail de confirmação
        # - Integrar com um gateway (Stripe, Mercado Pago, PagSeguro)
        # - Registrar em um banco de dados

        return jsonify({"ok": True, "message": "Pedido recebido! Entraremos em contato por e-mail."})

    # GET -> renderiza o template
    return render_template("checkout.html", social=load_social())


@app.route("/api/rss.xml")
def rss():
    # Gera um RSS simples do blog para integrar com redes/leitores
    posts = load_posts()
    site_url = request.url_root.rstrip("/")

    items_xml = []
    for p in posts[:20]:  # últimos 20
        post_url = f"{site_url}{url_for('blog_post', slug=p['slug'])}"
        items_xml.append(f"""
        <item>
            <title><![CDATA[{p['title']}]]></title>
            <link>{post_url}</link>
            <pubDate>{p['date'].strftime('%a, %d %b %Y 00:00:00 +0000')}</pubDate>
            <description><![CDATA[{p['summary']}]]></description>
            <guid>{post_url}</guid>
        </item>
        """)

    rss_xml = f"""
    <?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
      <channel>
        <title>Blog da Isabela</title>
        <link>{site_url}</link>
        <description>Artigos sobre ensino, ENEM, Física, Matemática e marketing educacional.</description>
        <language>pt-br</language>
        {''.join(items_xml)}
      </channel>
    </rss>
    """

    return app.response_class(rss_xml, mimetype="application/rss+xml")


# Rota simples de saúde (útil em deploy)
@app.route("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat() + "Z"}


if __name__ == "__main__":
    # Em produção, use um servidor WSGI (gunicorn/uwsgi). Isto aqui é só p/ dev.
    app.run(debug=True)
