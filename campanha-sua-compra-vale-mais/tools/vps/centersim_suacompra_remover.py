#!/usr/bin/env python3
"""Center SIM - campanha SUA COMPRA VALE MAIS: tira do ar em 31/12/2026 23:55 (repescagem 01/01 00:15 e 06:00).
Remove o slide da home (pagina 3207) e troca a LP centersim.com.br/campanhasuacompravalemais por redirecionamento pra home.
Pedido da Tatiana (Mantra) por e-mail em 14/10/2026. Avisa no grupo da Torre."""
import json, os, subprocess, sys, urllib.request, datetime
BASE = "/opt/hq/campanhas"
FEITO = f"{BASE}/centersim-suacompra-remocao.feito"
LOG = f"{BASE}/centersim-suacompra.log"
ENV = dict(l.strip().split("=", 1) for l in open("/opt/torre/.env") if "=" in l and not l.startswith("#"))
SSH = ["ssh", "-i", "/root/.ssh/grupo-sim-vigia-ssh", "-p", "65002", "-o", "StrictHostKeyChecking=accept-new",
       "-o", "ConnectTimeout=20", "u817473585@82.180.158.248"]

def log(msg):
    with open(LOG, "a") as f: f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {msg}\n")

def whatsapp(text):
    body = json.dumps({"number": ENV.get("AVISO_DESTINO") or ENV["GRUPO_COMANDO_JID"], "text": text}).encode()
    req = urllib.request.Request(f"http://127.0.0.1:8080/message/sendText/{ENV.get('AVISO_INSTANCIA', 'torre')}",
                                 data=body, headers={"Content-Type": "application/json", "apikey": ENV["EVOLUTION_API_KEY"]})
    urllib.request.urlopen(req, timeout=30)

def fora_do_ar():
    req = urllib.request.Request("https://centersim.com.br/?nc=" + datetime.datetime.now().strftime("%s"),
                                 headers={"User-Agent": "Mozilla/5.0 HQ-check", "Cache-Control": "no-cache"})
    home = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
    class NoRedir(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k): return None
    try:
        r = urllib.request.build_opener(NoRedir).open("https://centersim.com.br/campanhasuacompravalemais/", timeout=30); lp = r.status
    except urllib.error.HTTPError as e: lp = e.code
    return "campanha-suacompravalemais" not in home and lp in (301, 302, 404)

if os.path.exists(FEITO): sys.exit(0)
teste = "--teste" in sys.argv
agora = datetime.datetime.now()
if not teste and agora < datetime.datetime(2026, 12, 31, 23, 50): sys.exit(0)
try:
    cmd = ("php -l ~/campanhas/sua-compra-vale-mais/remover.php" if teste else
           "cd ~/domains/centersim.com.br/public_html && wp eval-file ~/campanhas/sua-compra-vale-mais/remover.php && wp cache flush")
    out = subprocess.run(SSH + [cmd], capture_output=True, text=True, timeout=180)
    log(f"remover rc={out.returncode} out={out.stdout.strip()} err={out.stderr.strip()[-300:]}")
    if teste:
        print(out.stdout, out.stderr[-300:]); sys.exit(0)
    if out.returncode != 0:
        raise RuntimeError(f"script no servidor falhou: {out.stdout.strip()[:200]} {out.stderr.strip()[-200:]}")
    if not fora_do_ar():
        raise RuntimeError("rodou, mas a home ainda mostra o banner ou a LP ainda abre (cache?)")
    open(FEITO, "w").write(agora.isoformat())
    log("FORA DO AR confirmado")
    whatsapp("✅ Center SIM: campanha SUA COMPRA VALE MAIS saiu do ar (banner da home removido; LP redireciona pra home). LP arquivada em ~/campanhas/sua-compra-vale-mais/lp-arquivada no servidor.")
except Exception as e:
    log(f"FALHA {e}")
    try: whatsapp(f"⚠️ Center SIM: retirada da campanha SUA COMPRA VALE MAIS falhou nesta tentativa ({e}). Tento de novo no próximo horário; se for a última (01/01 06:00), precisa de mão.")
    except Exception as e2: log(f"whatsapp falhou {e2}")
    sys.exit(1)
