"""Ajusta o espelho da LP pra rodar em centersim.com.br/campanhasuacompravalemais/.

- remove rastros do WP do Felipe (feeds, oembed, rsd, shortlink, generator)
- caminhos de asset absolutos sob /campanhasuacompravalemais/
- botao LER REGULAMENTO aponta pro PDF; rodape cita o endereco oficial do regulamento
- tag do Google (Site Kit da Center, GT-WPF6KSFV) + og basico
"""
import os, re

BASE = "/campanhasuacompravalemais/"
URL = "https://centersim.com.br" + BASE
ARQ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site", "index.html")

t = open(ARQ, encoding="utf-8").read()

# head: lixo do WP de origem
t = re.sub(r'<link rel="alternate"[^>]*fernaci[^>]*/>\n?', "", t)
t = re.sub(r'<link rel="(https://api\.w\.org/|EditURI)"[^>]*/>', "", t)
t = re.sub(r"<link rel='shortlink'[^>]*/>\n?", "", t)
t = re.sub(r'<meta name="generator"[^>]*>\n?', "", t)
t = t.replace('<link rel="canonical" href="https://fernaci.com.br/" />', '<link rel="canonical" href="%s" />' % URL)

# config do Elementor (JSON escapado)
t = t.replace(r"https:\/\/fernaci.com.br\/wp-content\/", r"\/campanhasuacompravalemais\/assets\/wp-content\/")
t = t.replace(r"https:\/\/fernaci.com.br\/wp-admin\/", r"https:\/\/centersim.com.br\/wp-admin\/")
t = t.replace(r"https:\/\/fernaci.com.br\/wp-json\/", r"https:\/\/centersim.com.br\/wp-json\/")
t = t.replace(r"https:\/\/fernaci.com.br\/", r"https:\/\/centersim.com.br\/")
t = t.replace(r'"assets\/wp-', r'"\/campanhasuacompravalemais\/assets\/wp-')

# assets relativos -> absolutos
t = re.sub(r"""(["'(\s,])assets/wp-""", r"\1" + BASE + "assets/wp-", t)

# rodape: endereco oficial (o mesmo do regulamento registrado)
t = t.replace("simnegocios.com.br/suacompravalemaiscentersim",
              '<a href="%s" style="color:inherit;text-decoration:underline">centersim.com.br/campanhasuacompravalemais</a>' % BASE)

# botao do regulamento
t = re.sub(r'(<a class="elementor-button elementor-size-sm" role="button")(>\s*<span class="elementor-button-content-wrapper">\s*<span class="elementor-button-text">LER REGULAMENTO)',
           r'\1 href="%sregulamento.pdf" target="_blank" rel="noopener"\2' % BASE, t)

# tag do Google + og
extra = """<meta name="description" content="A cada R$ 500 em compras nas lojas participantes da Rede Center SIM, você ganha 1 cupom para concorrer a R$ 65 mil em prêmios." />
<meta property="og:type" content="website" />
<meta property="og:title" content="Sua compra vale mais | Center SIM" />
<meta property="og:description" content="A cada R$ 500 em compras, 1 cupom para concorrer a R$ 65 mil em prêmios." />
<meta property="og:url" content="%s" />
<meta property="og:image" content="https://centersim.com.br%sbanner-2560x833.png" />
<script async src="https://www.googletagmanager.com/gtag/js?id=GT-WPF6KSFV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","GT-WPF6KSFV",{"page_path":"%s"});</script>
""" % (URL, BASE, BASE)
if "GT-WPF6KSFV" not in t:
    t = t.replace("</head>", extra + "</head>", 1)

open(ARQ, "w", encoding="utf-8").write(t)
print("restos fernaci:", len(re.findall("fernaci", t)))
print("botao regulamento ok:", "regulamento.pdf" in t)
print("rodape ok:", "simnegocios.com.br/suacompra" not in t)
