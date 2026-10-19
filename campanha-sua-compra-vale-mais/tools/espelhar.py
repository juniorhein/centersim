"""Espelha a LP do Felipe (fernaci.com.br) como pagina estatica autocontida.

Baixa HTML + CSS/JS/imagens/fontes do fernaci.com.br, reescreve tudo pra
caminho relativo e grava em ../site. Fontes do Google ficam remotas.
"""
import os, re, sys, urllib.request, urllib.parse, hashlib

ORIGEM = "https://fernaci.com.br/"
HOST = "fernaci.com.br"
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/141 Safari/537.36"}
baixados = {}

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()

def local(url):
    """caminho local (relativo a RAIZ) pra uma URL do fernaci"""
    p = urllib.parse.urlparse(url)
    caminho = urllib.parse.unquote(p.path).lstrip("/")
    return "assets/" + caminho

def baixar(url):
    url = url.replace("&#038;", "&").replace("&amp;", "&")
    sem_q = url.split("#")[0].split("?")[0]
    if sem_q in baixados:
        return baixados[sem_q]
    rel = local(sem_q)
    baixados[sem_q] = rel
    destino = os.path.join(RAIZ, rel)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    try:
        dados = get(url)
    except Exception as e:
        print("FALHOU", url, e); return rel
    if sem_q.endswith(".css"):
        txt = dados.decode("utf-8", "replace")
        txt = reescrever_css(txt, sem_q)
        dados = txt.encode("utf-8")
    open(destino, "wb").write(dados)
    print("ok", rel)
    return rel

def reescrever_css(txt, base):
    def troca(m):
        u = m.group(2).strip()
        if u.startswith("data:") or u.startswith("#"):
            return m.group(0)
        absu = urllib.parse.urljoin(base, u)
        if urllib.parse.urlparse(absu).netloc != HOST:
            return m.group(0)
        rel_alvo = baixar(absu)
        rel_css = os.path.dirname(local(base))
        return "url(%s%s%s)" % (m.group(1), os.path.relpath(rel_alvo, rel_css).replace("\\", "/"), m.group(1))
    return re.sub(r"url\(\s*(['\"]?)([^)'\"]+)\1\s*\)", troca, txt)

def main():
    html = get(ORIGEM).decode("utf-8")
    pad = re.compile(r"https?:(?:\/\/|//)" + re.escape(HOST) + r"(?:\/|/)[^\s'\"<>),]+")
    def troca(m):
        u = m.group(0)
        escapado = "\/" in u
        limpo = u.replace("\/", "/")
        if "/wp-json" in limpo or "xmlrpc" in limpo or "/feed" in limpo or "admin-ajax" in limpo:
            return u
        caminho = urllib.parse.urlparse(limpo.replace("&#038;", "&")).path
        if not re.search(r"\.(css|js|png|jpe?g|webp|gif|svg|woff2?|ttf|eot|otf|ico|pdf)$", caminho, re.I):
            return u
        rel = baixar(limpo)
        return rel.replace("/", "\/") if escapado else rel
    html = pad.sub(troca, html)
    open(os.path.join(RAIZ, "index.html"), "w", encoding="utf-8").write(html)
    print("index.html gravado; %d arquivos" % len(baixados))

if __name__ == "__main__":
    os.makedirs(RAIZ, exist_ok=True)
    main()
