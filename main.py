import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST, PORT = "127.0.0.1", 2610

HTML = r'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Homelab — свой сервер, свои правила</title>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500;700;800&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{--bg:#000;--fg:#f2f2f2;--mut:#8a8a8a;--line:#1f1f1f;--acc:#7cc4ff}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--fg);font:18px/1.65 'Inter',system-ui,sans-serif;-webkit-font-smoothing:antialiased}
::selection{background:var(--acc);color:#000}
a{color:inherit;text-decoration:none}
:focus-visible{outline:2px solid var(--acc);outline-offset:3px}
.glow{position:fixed;inset:0;pointer-events:none;background:radial-gradient(500px circle at var(--x,50%) var(--y,30%),#7cc4ff14,transparent 70%)}
.wrap{max-width:1080px;margin:0 auto;padding:0 28px;position:relative}
header{position:sticky;top:0;z-index:10;background:#000c;backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
header .wrap{display:flex;align-items:center;height:60px;gap:28px}
header b{font:800 18px 'Inter Tight';margin-right:auto;letter-spacing:-.02em}
header a{color:var(--mut);font-size:15px;transition:color .2s}
header a:hover{color:#fff}
@media(max-width:700px){header a{display:none}}
.hero{padding:15vh 0 12vh}
h1{font:800 clamp(48px,10.5vw,148px)/.94 'Inter Tight';letter-spacing:-.045em}
h1 span{display:block;overflow:hidden}
h1 span i{display:block;font-style:normal;transform:translateY(105%);animation:up .9s cubic-bezier(.2,.8,.2,1) forwards}
h1 span:nth-child(2) i{animation-delay:.12s;color:#4a4a4a}
@keyframes up{to{transform:none}}
.hero p{max-width:560px;margin-top:40px;color:var(--mut);font-size:21px}
.cta{display:inline-block;margin-top:36px;padding:14px 26px;background:#fff;color:#000;font:600 16px 'Inter Tight';border-radius:99px;transition:.2s}
.cta:hover{background:var(--acc)}
.cta2{margin-left:18px;color:var(--mut);font-size:16px}
.cta2:hover{color:#fff}
section{padding:110px 0;border-top:1px solid var(--line)}
h2{font:700 clamp(30px,5vw,54px)/1.05 'Inter Tight';letter-spacing:-.03em;margin-bottom:22px;max-width:14em}
.lead{color:var(--mut);max-width:560px;font-size:20px}
.cols{display:grid;grid-template-columns:repeat(3,1fr);gap:48px;margin-top:60px}
.cols h3{font:600 20px 'Inter Tight';margin-bottom:10px}
.cols p{color:var(--mut);font-size:17px}
@media(max-width:800px){.cols{grid-template-columns:1fr;gap:34px}}
/* hardware */
.hw{margin-top:56px;border-top:1px solid var(--line)}
.row{display:grid;grid-template-columns:1.1fr 2fr .7fr .7fr;gap:20px;padding:26px 0;border-bottom:1px solid var(--line);align-items:baseline;transition:padding .25s,background .25s}
.row:hover{background:#0a0a0a;padding-left:14px}
.row b{font:600 22px 'Inter Tight'}
.row span{color:var(--mut);font-size:16px}
.row em{font-style:normal;text-align:right;font-size:16px}
.head{color:#555;font-size:13px;padding:14px 0}
.head:hover{background:none;padding-left:0}
@media(max-width:760px){.row{grid-template-columns:1fr 1fr}.row span{grid-column:1/-1;order:3}.head{display:none}.row em{text-align:left}}
/* stack */
.stack{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:1px;background:var(--line);border:1px solid var(--line);margin-top:56px}
.stack div{background:#000;padding:26px 22px;min-height:150px;transition:background .25s}
.stack div:hover{background:#0c1218}
.stack b{display:block;font:600 21px 'Inter Tight';margin-bottom:6px}
.stack span{color:var(--mut);font-size:15px;line-height:1.5;display:block}
/* diagram */
.diag{margin-top:56px;border:1px solid var(--line);padding:28px;overflow-x:auto}
.diag svg{display:block;min-width:720px;width:100%;height:auto}
.diag text{fill:#d8d8d8;font:500 15px 'Inter Tight'}
.diag .s{fill:#777;font-size:12px}
.diag rect{fill:#050505;stroke:#3a3a3a}
.diag .h{stroke:var(--acc)}
.diag line{stroke:#333}
.diag .pulse{stroke:var(--acc);stroke-dasharray:6 10;animation:dash 1.2s linear infinite}
@keyframes dash{to{stroke-dashoffset:-32}}
/* rules + steps */
.steps{margin-top:56px;counter-reset:s}
.st{display:grid;grid-template-columns:90px 1fr;gap:24px;padding:30px 0;border-top:1px solid var(--line)}
.st:before{counter-increment:s;content:counter(s);font:800 54px/1 'Inter Tight';color:#2a2a2a}
.st h3{font:600 24px 'Inter Tight';margin-bottom:6px}
.st p{color:var(--mut);max-width:620px}
code{font:15px ui-monospace,Consolas,monospace;background:#111;border:1px solid #222;padding:2px 7px;border-radius:5px;color:var(--acc)}
.big{font:700 clamp(34px,6vw,76px)/1.05 'Inter Tight';letter-spacing:-.035em;max-width:13em}
footer{padding:60px 0 80px;border-top:1px solid var(--line);color:#555;font-size:15px}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}h1 span i{transform:none}}
</style>
</head>
<body>
<div class="glow" id="glow"></div>
<header><div class="wrap">
  <b>homelab</b><a href="#why">Зачем</a><a href="#hw">Железо</a><a href="#stack">Софт</a><a href="#net">Сеть</a><a href="#start">Старт</a>
</div></header>

<main>
<div class="wrap hero">
  <h1><span><i>Свой сервер.</i></span><span><i>Свои правила.</i></span></h1>
  <p>Домашняя лаборатория: как перестать платить подпискам, забрать свои данные и научиться тому, чему не учат в облаке.</p>
  <a class="cta" href="#start">Как начать</a><a class="cta2" href="#hw">Что купить</a>
</div>

<section id="why"><div class="wrap">
  <h2>Почему это вообще стоит делать</h2>
  <p class="lead">Один небольшой компьютер в углу заменяет десяток сервисов и учит больше любого курса.</p>
  <div class="cols">
    <div><h3>Данные у тебя</h3><p>Фото, документы и пароли лежат на твоём диске, а не у компании, которая завтра может поднять цену или закрыться.</p></div>
    <div><h3>Деньги остаются</h3><p>Облачное хранилище, VPN, менеджер паролей, медиатека: всё это можно запустить дома на одной машине за один раз.</p></div>
    <div><h3>Ты учишься</h3><p>Сети, Linux, контейнеры, резервные копии. Сломал, починил, понял. Это лучший полигон для будущей работы.</p></div>
  </div>
</div></section>

<section id="hw"><div class="wrap">
  <h2>С чего собирать</h2>
  <p class="lead">Мощный сервер не нужен. Начни с того, что уже валяется дома, и растёшь по мере надобности.</p>
  <div class="hw">
    <div class="row head"><span>Вариант</span><span>Кому подходит</span><em>Потребление</em><em>Цена</em></div>
    <div class="row"><b>Raspberry Pi</b><span>Для первого шага: DNS-фильтр, Home Assistant, пара лёгких сервисов.</span><em>3–7 Вт</em><em>низкая</em></div>
    <div class="row"><b>Мини-ПК</b><span>Золотая середина. Тянет Docker, виртуалки и медиасервер на одном корпусе.</span><em>10–25 Вт</em><em>средняя</em></div>
    <div class="row"><b>Б/у ПК или сервер</b><span>Много ядер и памяти за небольшие деньги, но шумит и ест электричество.</span><em>60–200 Вт</em><em>низкая</em></div>
    <div class="row"><b>NAS</b><span>Когда главное хранение: фото, архивы, бэкапы, несколько дисков с резервированием.</span><em>15–40 Вт</em><em>высокая</em></div>
  </div>
</div></section>

<section id="stack"><div class="wrap">
  <h2>Что на нём крутить</h2>
  <p class="lead">Всё это работает в контейнерах и ставится за вечер.</p>
  <div class="stack">
    <div><b>Proxmox</b><span>Виртуализация. Хозяин, который делит железо на отдельные машины.</span></div>
    <div><b>Docker</b><span>Каждый сервис в своей коробке: ставится и удаляется без следов.</span></div>
    <div><b>Nextcloud</b><span>Свой диск с синхронизацией, календарём и контактами.</span></div>
    <div><b>Immich</b><span>Замена облачным фото. Распознаёт лица и места.</span></div>
    <div><b>Jellyfin</b><span>Своя медиатека с фильмами и музыкой без рекламы.</span></div>
    <div><b>AdGuard Home</b><span>Режет рекламу и трекеры для всей сети сразу.</span></div>
    <div><b>Vaultwarden</b><span>Менеджер паролей, совместимый с клиентами Bitwarden.</span></div>
    <div><b>WireGuard</b><span>Быстрый VPN, чтобы заходить домой из любой точки мира.</span></div>
    <div><b>Home Assistant</b><span>Умный дом без облаков: свет, датчики, автоматизации.</span></div>
    <div><b>Uptime Kuma</b><span>Следит за сервисами и пишет, если что-то упало.</span></div>
  </div>
</div></section>

<section id="net"><div class="wrap">
  <h2>Как это соединено</h2>
  <p class="lead">Наружу открыт только VPN. Всё остальное живёт внутри домашней сети.</p>
  <div class="diag">
    <svg viewBox="0 0 760 260" role="img" aria-label="Схема сети">
      <line class="pulse" x1="140" y1="130" x2="210" y2="130"/><line class="pulse" x1="350" y1="130" x2="420" y2="130"/>
      <line x1="560" y1="130" x2="600" y2="60"/><line x1="560" y1="130" x2="600" y2="130"/><line x1="560" y1="130" x2="600" y2="200"/>
      <rect x="20" y="100" width="120" height="60" rx="8"/><text x="80" y="136" text-anchor="middle">Интернет</text>
      <rect class="h" x="210" y="100" width="140" height="60" rx="8"/><text x="280" y="126" text-anchor="middle">Роутер</text><text class="s" x="280" y="144" text-anchor="middle">firewall + WireGuard</text>
      <rect x="420" y="100" width="140" height="60" rx="8"/><text x="490" y="136" text-anchor="middle">Свитч</text>
      <rect x="600" y="30" width="140" height="60" rx="8"/><text x="670" y="66" text-anchor="middle">Сервер</text>
      <rect x="600" y="100" width="140" height="60" rx="8"/><text x="670" y="136" text-anchor="middle">NAS</text>
      <rect x="600" y="170" width="140" height="60" rx="8"/><text x="670" y="206" text-anchor="middle">Умный дом</text>
    </svg>
  </div>
</div></section>

<section id="start"><div class="wrap">
  <h2>Как начать за выходные</h2>
  <div class="steps">
    <div class="st"><div><h3>Выбери машину</h3><p>Возьми что есть: старый ноутбук, мини-ПК или Raspberry Pi. Для первых сервисов хватит двух ядер и 4 ГБ памяти.</p></div></div>
    <div class="st"><div><h3>Поставь систему</h3><p>Debian или Ubuntu Server. Включи SSH, обнови пакеты и закрепи за машиной постоянный адрес в роутере.</p></div></div>
    <div class="st"><div><h3>Запусти Docker</h3><p>Установи его и разверни первый сервис, например <code>docker compose up -d</code> для AdGuard Home. Дальше всё по аналогии.</p></div></div>
    <div class="st"><div><h3>Закрой доступ</h3><p>Не открывай порты наружу. Подними WireGuard и заходи только через него. Включи ключи вместо паролей для SSH.</p></div></div>
    <div class="st"><div><h3>Сделай бэкапы</h3><p>Правило 3-2-1: три копии, на двух разных носителях, одна из них за пределами дома. Без бэкапа это не сервер, а лотерея.</p></div></div>
  </div>
</div></section>

<section><div class="wrap">
  <p class="big">Сломать сервер дома — это не катастрофа. Это урок.</p>
</div></section>
</main>

<footer><div class="wrap">Homelab — учебная страница. Сделано в одном файле, работает локально.</div></footer>

<script>
const g=document.getElementById('glow');
addEventListener('pointermove',e=>{g.style.setProperty('--x',e.clientX+'px');g.style.setProperty('--y',e.clientY+'px')},{passive:true});
</script>
</body>
</html>
'''.encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?")[0] in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(HTML)))
            self.end_headers()
            self.wfile.write(HTML)
        elif self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
        else:
            self.send_error(404)

    def log_message(self, *args):
        pass  # silent, no console in windowed build


URL = f"http://{HOST}:{PORT}"


def open_site(*_):
    webbrowser.open(URL)


def make_icon():
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (64, 64), "#000000")
    d = ImageDraw.Draw(img)
    d.rectangle((8, 8, 55, 55), outline="#7cc4ff", width=4)
    d.rectangle((24, 24, 39, 39), fill="#7cc4ff")
    return img


def main():
    try:
        srv = ThreadingHTTPServer((HOST, PORT), Handler)
    except OSError:
        open_site()  # already running, just open it
        return

    threading.Thread(target=srv.serve_forever, daemon=True).start()
    open_site()

    try:
        import pystray
    except ImportError:
        threading.Event().wait()  # no tray lib: keep running hidden
        return

    def quit_app(icon, _item):
        icon.stop()
        srv.shutdown()

    menu = pystray.Menu(
        pystray.MenuItem("Open", open_site, default=True),
        pystray.MenuItem("Quit", quit_app),
    )
    pystray.Icon("site", make_icon(), f"Site :{PORT}", menu).run()


if __name__ == "__main__":
    main()
