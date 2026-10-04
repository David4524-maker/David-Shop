# ============================================================
# DAVID SHOP — v4.1 (arreglado)
# 1000 productos | Logo Canvas | Descargas reales | HTML jugables
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3, hashlib, os, csv, shutil, random, subprocess, sys
import datetime as dt
import threading, time, pathlib

DB_PATH = "david_shop.db"
DOWNLOADS_FOLDER = pathlib.Path.home() / "David_Shop_Downloads"

# ============================================================
# LOGO DIBUJADO CON CANVAS
# ============================================================
def draw_david_logo(canvas, x, y, w):
    h = w * 0.62
    S = w / 400.0
    hw = 140 * S
    hx = x + (w - hw) / 2
    hth = max(2, int(15 * S))
    canvas.create_arc(hx, y - 80*S, hx + hw, y + 30*S, start=0, extent=180,
                      style="arc", outline="#000", width=hth)
    canvas.create_line(hx, y - 40*S, hx, y + 4*S, fill="#000", width=hth, capstyle="round")
    canvas.create_line(hx + hw, y - 40*S, hx + hw, y + 4*S, fill="#000", width=hth, capstyle="round")
    canvas.create_rectangle(x, y, x + w, y + h, fill="#3aa4e0", outline="")
    canvas.create_polygon(x + 140*S, y, x + w, y, x + w, y + h, x + 100*S, y + h,
                          fill="#b3daf5", outline="")
    canvas.create_rectangle(x, y, x + w, y + h, fill="", outline="#888", width=max(1, int(5*S)))
    canvas.create_text(x + 100*S, y + 90*S, text=">", fill="#FF8C00",
                       font=("Arial", int(100*S), "bold"), anchor="c")
    canvas.create_line(x + 55*S, y + 145*S, x + 148*S, y + 145*S,
                       fill="#FF8C00", width=max(2, int(14*S)))
    dcx, dcy = x + 200*S, y + 125*S
    dsz = int(150*S)
    for dx, dy in [(-2,-2),(2,-2),(-2,2),(2,2),(-2,0),(2,0),(0,-2),(0,2)]:
        canvas.create_text(dcx + dx*S, dcy + dy*S, text="D", fill="#555",
                           font=("Arial", dsz, "bold"), anchor="c")
    canvas.create_text(dcx + 3*S, dcy + 4*S, text="D", fill="#666",
                       font=("Arial", dsz, "bold"), anchor="c")
    canvas.create_text(dcx, dcy, text="D", fill="#a0a0a0",
                       font=("Arial", dsz, "bold"), anchor="c")
    gcx, gcy = x + 200*S, y + 210*S
    gw2, gh2 = 80*S, 42*S
    canvas.create_oval(gcx-gw2/2, gcy-gh2/2, gcx-gw2/6, gcy+gh2/2, fill="#999", outline="#777")
    canvas.create_oval(gcx+gw2/6, gcy-gh2/2, gcx+gw2/2, gcy+gh2/2, fill="#999", outline="#777")
    canvas.create_rectangle(gcx-gw2/4, gcy-gh2/2, gcx+gw2/4, gcy+gh2/2, fill="#999", outline="#777")
    dp = gh2 * 0.5
    dpx = gcx - gw2 * 0.28
    canvas.create_rectangle(dpx-dp/2, gcy-dp/4, dpx+dp/2, gcy+dp/4, fill="#555", outline="")
    canvas.create_rectangle(dpx-dp/4, gcy-dp/2, dpx+dp/4, gcy+dp/2, fill="#555", outline="")
    br = gh2 * 0.16
    canvas.create_oval(gcx+gw2*0.10-br, gcy-gh2*0.28-br, gcx+gw2*0.10+br, gcy-gh2*0.28+br,
                       fill="#e74c3c", outline="")
    canvas.create_oval(gcx+gw2*0.28-br, gcy+gh2*0.10-br, gcx+gw2*0.28+br, gcy+gh2*0.10+br,
                       fill="#f1c40f", outline="")
    sq = 32 * S; gap = 12 * S
    gx = x + 285 * S; gy = y + 70 * S
    canvas.create_rectangle(gx, gy, gx+sq, gy+sq, fill="#e74c3c", outline="")
    canvas.create_rectangle(gx+sq+gap, gy, gx+2*sq+gap, gy+sq, fill="#27ae60", outline="")
    canvas.create_rectangle(gx, gy+sq+gap, gx+sq, gy+2*sq+gap, fill="#8e44ad", outline="")
    px = gx + sq + gap; py = gy + sq + gap
    canvas.create_rectangle(px, py, px+sq*0.7, py+sq*0.7, fill="#888", outline="")
    canvas.create_rectangle(px+sq*0.7, py+sq*0.22, px+sq*1.05, py+sq*0.62, fill="#888", outline="")

class LogoCanvas(tk.Canvas):
    def __init__(self, parent, width=100, bg="#2196F3", **kw):
        h = int(width * 0.88)
        super().__init__(parent, width=width, height=h, bg=bg, highlightthickness=0, bd=0, **kw)
        bw = width * 0.88; bh = bw * 0.62
        draw_david_logo(self, (width-bw)/2, h-bh-width*0.02, bw)

# ============================================================
# TEMAS
# ============================================================
THEMES = {
    "light": {"bg":"#f4f6fb","fg":"#1a1a1a","card":"#ffffff","primary":"#2196F3",
              "primary_fg":"#ffffff","accent":"#FF9800","border":"#d5d8e0","muted":"#666",
              "success":"#2e7d32","danger":"#c62828","sidebar":"#1f2a44","sidebar_fg":"#e8eaf2"},
    "dark": {"bg":"#161622","fg":"#e6e6e6","card":"#22223a","primary":"#7c4dff",
             "primary_fg":"#ffffff","accent":"#FFB74D","border":"#33334d","muted":"#aaa",
             "success":"#66bb6a","danger":"#ef5350","sidebar":"#0f0f18","sidebar_fg":"#e6e6e6"},
}

# ============================================================
# i18n
# ============================================================
I18N = {
    "ES": {"app_title":"David Shop — Tienda Legítima","login":"Iniciar sesión","register":"Registrarse",
           "logout":"Cerrar sesión","username":"Usuario","password":"Contraseña","email":"Correo",
           "confirm_password":"Confirmar contraseña","remember":"Recordarme","welcome":"¡Bienvenido",
           "invalid_login":"Usuario o contraseña incorrectos","user_exists":"El usuario o email ya existe",
           "pw_mismatch":"Las contraseñas no coinciden","email_invalid":"Correo inválido",
           "pw_short":"Contraseña muy corta (mín. 6)","search":"Buscar productos...","home":"Inicio",
           "catalog":"Catálogo","cart":"Carrito","library":"Biblioteca","orders":"Pedidos",
           "wishlist":"Favoritos","profile":"Perfil","admin":"Admin","categories":"Categorías","all":"Todas",
           "min_price":"Precio mín.","max_price":"Precio máx.","in_stock":"Solo en stock","sort":"Ordenar",
           "sort_name":"Nombre","sort_price_asc":"Precio ↑","sort_price_desc":"Precio ↓",
           "sort_sales":"Más vendidos","sort_new":"Novedades","grid":"Cuadrícula","list":"Lista",
           "add_cart":"Añadir al carrito","buy":"Comprar ahora","price":"Precio","stock":"Stock",
           "description":"Descripción","reviews":"Reseñas","write_review":"Escribir reseña","submit":"Enviar",
           "rating":"Valoración","comment":"Comentario","empty_cart":"Tu carrito está vacío",
           "subtotal":"Subtotal","tax":"Impuestos (16%)","total":"Total","checkout":"Pagar",
           "coupon":"Cupón","apply":"Aplicar","clear":"Vaciar","coupon_ok":"Cupón aplicado",
           "coupon_bad":"Cupón inválido","purchase_ok":"¡Compra realizada!","orders_empty":"Sin pedidos",
           "download":"Descargar","downloading":"Descargando","done":"Completado","save":"Guardar",
           "cancel":"Cancelar","confirm":"Confirmar","delete":"Eliminar","edit":"Editar","new":"Nuevo",
           "confirm_delete":"¿Seguro que quieres eliminar?","about":"Acerca de","back":"Volver",
           "empty":"Nada por aquí","logout_confirm":"¿Cerrar sesión?","user_deleted":"Cuenta eliminada",
           "added_cart":"Añadido al carrito","removed_cart":"Quitado del carrito","added_wish":"Añadido a favoritos",
           "removed_wish":"Quitado de favoritos","language":"Idioma","theme":"Tema","featured":"Destacados",
           "recommended":"Recomendado para ti","recent":"Vistos recientemente","admin_only":"Solo admin",
           "name":"Nombre","sales":"Ventas","actions":"Acciones","stats":"Estadísticas","users":"Usuarios",
           "products":"Productos","revenue":"Ingresos","export_csv":"Exportar CSV","backup":"Backup",
           "restore":"Restaurar","coupons":"Cupones","new_password":"Nueva contraseña","avatar":"Avatar",
           "save_changes":"Guardar cambios","delete_account":"Eliminar mi cuenta","splash_loading":"Cargando David Shop...",
           "on_sale":"OFERTA","new_badge":"NUEVO","no_results":"Sin resultados","total_products":"productos",
           "page":"Página","prev":"Anterior","next":"Siguiente","login_required":"Inicia sesión primero",
           "welcome_back":"Bienvenido de nuevo","activity":"Actividad","free":"GRATIS","get_free":"Obtener gratis",
           "owned":"En biblioteca","obtained":"¡Añadido a tu biblioteca!","already_owned":"Ya lo tienes en tu biblioteca",
           "free_no_pay":"Producto gratuito — sin carrito ni pago","saved_at":"Guardado en","open_folder":"¿Abrir la carpeta?",
           "download_error":"Error al descargar","open_folder_btn":"📂 Abrir carpeta","downloads_folder":"Carpeta de descargas",
           "play_html":"▶ Abrir juego en navegador"},
    "EN": {"app_title":"David Shop — Legit Store","login":"Sign in","register":"Sign up","logout":"Log out",
           "username":"Username","password":"Password","email":"Email","confirm_password":"Confirm password",
           "remember":"Remember me","welcome":"Welcome","invalid_login":"Invalid user or password",
           "user_exists":"User or email already exists","pw_mismatch":"Passwords do not match",
           "email_invalid":"Invalid email","pw_short":"Password too short (min 6)","search":"Search products...",
           "home":"Home","catalog":"Catalog","cart":"Cart","library":"Library","orders":"Orders",
           "wishlist":"Wishlist","profile":"Profile","admin":"Admin","categories":"Categories","all":"All",
           "min_price":"Min price","max_price":"Max price","in_stock":"In stock only","sort":"Sort",
           "sort_name":"Name","sort_price_asc":"Price ↑","sort_price_desc":"Price ↓","sort_sales":"Best sellers",
           "sort_new":"Newest","grid":"Grid","list":"List","add_cart":"Add to cart","buy":"Buy now",
           "price":"Price","stock":"Stock","description":"Description","reviews":"Reviews","write_review":"Write review",
           "submit":"Submit","rating":"Rating","comment":"Comment","empty_cart":"Your cart is empty",
           "subtotal":"Subtotal","tax":"Tax (16%)","total":"Total","checkout":"Checkout","coupon":"Coupon",
           "apply":"Apply","clear":"Clear","coupon_ok":"Coupon applied","coupon_bad":"Invalid coupon",
           "purchase_ok":"Purchase complete!","orders_empty":"No orders","download":"Download",
           "downloading":"Downloading","done":"Done","save":"Save","cancel":"Cancel","confirm":"Confirm",
           "delete":"Delete","edit":"Edit","new":"New","confirm_delete":"Are you sure you want to delete?",
           "about":"About","back":"Back","empty":"Nothing here","logout_confirm":"Log out?",
           "user_deleted":"Account deleted","added_cart":"Added to cart","removed_cart":"Removed from cart",
           "added_wish":"Added to wishlist","removed_wish":"Removed from wishlist","language":"Language",
           "theme":"Theme","featured":"Featured","recommended":"Recommended for you","recent":"Recently viewed",
           "admin_only":"Admin only","name":"Name","sales":"Sales","actions":"Actions","stats":"Stats",
           "users":"Users","products":"Products","revenue":"Revenue","export_csv":"Export CSV","backup":"Backup",
           "restore":"Restore","coupons":"Coupons","new_password":"New password","avatar":"Avatar",
           "save_changes":"Save changes","delete_account":"Delete my account","splash_loading":"Loading David Shop...",
           "on_sale":"SALE","new_badge":"NEW","no_results":"No results","total_products":"products",
           "page":"Page","prev":"Previous","next":"Next","login_required":"Please sign in first",
           "welcome_back":"Welcome back","activity":"Activity","free":"FREE","get_free":"Get for free",
           "owned":"In library","obtained":"Added to your library!","already_owned":"Already in your library",
           "free_no_pay":"Free product — no cart or payment","saved_at":"Saved at","open_folder":"Open folder?",
           "download_error":"Download error","open_folder_btn":"📂 Open folder","downloads_folder":"Downloads folder",
           "play_html":"▶ Open game in browser"},
    "PT": {"app_title":"David Shop — Loja Legítima","login":"Entrar","register":"Registrar","logout":"Sair",
           "username":"Usuário","password":"Senha","email":"Email","confirm_password":"Confirmar senha",
           "remember":"Lembrar-me","welcome":"Bem-vindo","invalid_login":"Usuário ou senha inválidos",
           "user_exists":"Usuário ou email já existe","pw_mismatch":"As senhas não coincidem",
           "email_invalid":"Email inválido","pw_short":"Senha muito curta (mín. 6)","search":"Buscar produtos...",
           "home":"Início","catalog":"Catálogo","cart":"Carrinho","library":"Biblioteca","orders":"Pedidos",
           "wishlist":"Favoritos","profile":"Perfil","admin":"Admin","categories":"Categorias","all":"Todas",
           "min_price":"Preço mín.","max_price":"Preço máx.","in_stock":"Só em estoque","sort":"Ordenar",
           "sort_name":"Nome","sort_price_asc":"Preço ↑","sort_price_desc":"Preço ↓","sort_sales":"Mais vendidos",
           "sort_new":"Novidades","grid":"Grade","list":"Lista","add_cart":"Adicionar ao carrinho","buy":"Comprar agora",
           "price":"Preço","stock":"Estoque","description":"Descrição","reviews":"Avaliações",
           "write_review":"Escrever avaliação","submit":"Enviar","rating":"Nota","comment":"Comentário",
           "empty_cart":"Seu carrinho está vazio","subtotal":"Subtotal","tax":"Impostos (16%)","total":"Total",
           "checkout":"Pagar","coupon":"Cupom","apply":"Aplicar","clear":"Limpar","coupon_ok":"Cupom aplicado",
           "coupon_bad":"Cupom inválido","purchase_ok":"Compra concluída!","orders_empty":"Sem pedidos",
           "download":"Baixar","downloading":"Baixando","done":"Concluído","save":"Salvar","cancel":"Cancelar",
           "confirm":"Confirmar","delete":"Excluir","edit":"Editar","new":"Novo",
           "confirm_delete":"Tem certeza que deseja excluir?","about":"Sobre","back":"Voltar","empty":"Nada por aqui",
           "logout_confirm":"Sair?","user_deleted":"Conta excluída","added_cart":"Adicionado ao carrinho",
           "removed_cart":"Removido do carrinho","added_wish":"Adicionado aos favoritos",
           "removed_wish":"Removido dos favoritos","language":"Idioma","theme":"Tema","featured":"Destaques",
           "recommended":"Recomendado para você","recent":"Vistos recentemente","admin_only":"Só admin",
           "name":"Nome","sales":"Vendas","actions":"Ações","stats":"Estatísticas","users":"Usuários",
           "products":"Produtos","revenue":"Receita","export_csv":"Exportar CSV","backup":"Backup",
           "restore":"Restaurar","coupons":"Cupons","new_password":"Nova senha","avatar":"Avatar",
           "save_changes":"Salvar alterações","delete_account":"Excluir minha conta","splash_loading":"Carregando David Shop...",
           "on_sale":"OFERTA","new_badge":"NOVO","no_results":"Sem resultados","total_products":"produtos",
           "page":"Página","prev":"Anterior","next":"Próximo","login_required":"Faça login primeiro",
           "welcome_back":"Bem-vindo de volta","activity":"Atividade","free":"GRÁTIS","get_free":"Obter grátis",
           "owned":"Na biblioteca","obtained":"Adicionado à sua biblioteca!","already_owned":"Já está na sua biblioteca",
           "free_no_pay":"Produto grátis — sem carrinho ou pagamento","saved_at":"Salvo em","open_folder":"Abrir pasta?",
           "download_error":"Erro ao baixar","open_folder_btn":"📂 Abrir pasta","downloads_folder":"Pasta de downloads",
           "play_html":"▶ Abrir jogo no navegador"},
}

AVATARS = ["👤","😀","😎","🦊","🐱","🐼","🐯","🦁","🐸","🐵","🤖","👑","🎮","🚀","⭐","💎"]
COUPONS = {"DAVID10":10,"LEGIT20":20,"WELCOME5":5,"VIP30":30}

# ============================================================
# POOLS DE NOMBRES
# ============================================================
STEAM_ADJ = ["Dark","Ancient","Neon","Cyber","Pixel","Mega","Ultra","Cosmic","Shadow","Crystal",
             "Iron","Star","Moon","Fire","Frost","Storm","Silent","Wild","Lost","Hidden","Eternal",
             "Broken","Rising","Fallen","Sacred","Cursed","Golden","Silver","Blood","Sky","Deep",
             "Hollow","Frozen","Burning","Endless","Final","Prime","Noble","Wicked","Brave"]
STEAM_NOUN = ["Legend","Quest","Warrior","Kingdom","Empire","Saga","Chronicle","Odyssey","Adventure",
              "Battle","Hero","Dungeon","Sword","Dragon","Titan","Ninja","Samurai","Pirate","Knight",
              "Wizard","Ranger","Hunter","Realm","World","Fortress","Castle","Village","Forest","Desert",
              "Island","Ocean","Mountain","Temple","Tower","Crypt","Cathedral","Arena","Maze","Labyrinth","Throne"]
EPIC_ADJ = ["Fort","Rocket","Battle","Mega","Super","Giga","Hyper","Neon","Crystal","Quantum","Turbo",
            "Nitro","Power","Alpha","Omega","Prime","Elite","Royal","Epic","Legendary","Cosmic","Vortex",
            "Thunder","Blazing","Shadow","Iron","Steel","Void","Astral","Radiant"]
EPIC_NOUN = ["Legends","Royale","Arena","Champions","Wars","Strike","Force","Squad","Rush","Brawl",
             "Clash","Raid","Empire","Titans","Heroes","Legion","Vanguard","Syndicate","Alliance","Front",
             "Tactics","Colony","Outpost","Rebellion","Dominion","Uprising","Surge","Crusade","Odyssey","Conquest"]
HTML_ADJ = ["Mini","Tiny","Retro","Classic","Pixel","Quick","Simple","Fun","Casual","Turbo","Neo","Lite",
            "Basic","Happy","Crazy","Wild","Flash","Old-School"]
HTML_NOUN = ["Snake","Tetris","Pacman","Breakout","Pong","2048","Flappy","Minesweeper","Solitaire","Chess",
             "Checkers","Sudoku","Mahjong","Asteroids","Invaders","Maze","Runner","Jump","Puzzle","Match",
             "Cards","Dice","Quiz","Typing","Reaction","Memory","Tower","Farm","Candy","Bubble"]
APPS_ADJ = ["Pro","Plus","Lite","Ultra","Mega","Mini","Smart","Quick","Easy","Super","Turbo","Nitro","Max",
            "Prime","Neo","Cloud","Nova","Pixel","Rapid","Swift"]
APPS_NOUN = ["Editor","Viewer","Maker","Creator","Manager","Tracker","Player","Reader","Writer","Painter",
             "Studio","Converter","Compressor","Recorder","Scanner","Sync","Backup","Cleaner","Finder",
             "Explorer","Notepad","Notes","Diary","Calendar","Reminder","Timer","Clock","Weather","Maps","Music"]
UTIL_ADJ = ["Win","Mega","Super","Ultra","Pro","Advanced","Turbo","Max","Smart","Easy","Quick","Fast",
            "Clean","System","Total","Perfect","All-in-One"]
UTIL_NOUN = ["Cleaner","Defrag","Compressor","Archiver","Antivirus","Firewall","VPN","Backup","Recovery",
             "Optimizer","Tuner","Registry","Driver","Updater","Uninstaller","Monitor","Benchmark",
             "Diagnostic","Repair","Toolkit","Utilities","Suite","Manager","Explorer","Ripper","Burner","Converter"]
SUBS_ADJ = ["Premium","Pro","Plus","Ultra","Family","Duo","Basic","Standard","Deluxe","Elite","Gold",
            "Platinum","Diamond","VIP","Unlimited"]
SUBS_NOUN = ["Streaming","Music","Cloud","Storage","Learning","Fitness","News","Sports","Gaming","Movies",
             "TV","Anime","Books","Courses","Design","Coding","AI","Video","Photo","Audio"]

ICON_STEAM = ["🎮","🕹️","👾","🎯","🎲","⚔️","🛡️","🏹","🗡️","🔥","💀","🐉","🧙","🏰","🗺️","🚀","⚡","❄️","🌟","🌌"]
ICON_EPIC = ["🏆","🚗","⚽","🎪","🎨","🎭","🎬","🏰","🗺️","💥","🌟","🚀","🎯","🎲","🎮","🎖️","🛸","🌠"]
ICON_HTML = ["🔢","🐍","🟦","🟡","🎴","🃏","♟️","🎯","🏓","🎳","🧩","🎰","🕹️","👾"]
ICON_APPS = ["📱","📝","🎵","🖼","📸","💬","📊","📈","🎨","✏️","📚","🗂","💾","📁","🖥️","📷"]
ICON_UTIL = ["🛠️","🧹","🗜️","📚","💻","🔧","⚙️","🔩","🔑","🔒","🧰","💽","📡","🖨️"]
ICON_SUBS = ["⭐","🎥","🍥","🏰","🎮","💎","📺","🎵","📰","⚽","🎬","🎞️","📡","☁️","🔓"]

# ============================================================
# PLANTILLAS HTML — AHORA CON LLAVES SIMPLES (sin .format())
# ============================================================
HTML_HEAD = '''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,sans-serif;background:#0d0d16;color:#e8e8f0;
min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;
padding:16px;user-select:none;-webkit-user-select:none;touch-action:manipulation}
h1{color:#7c4dff;margin-bottom:6px;font-size:24px;text-align:center}
.meta{color:#888;font-size:12px;margin-bottom:14px}
canvas{background:#181826;border:2px solid #7c4dff;border-radius:10px;max-width:92vw;touch-action:none}
.info{margin:12px 0;font-size:16px;text-align:center}
.info b{color:#ffb74d}
.ctrl{display:grid;grid-template-columns:repeat(3,64px);gap:8px;margin-top:14px}
.ctrl button{padding:16px;font-size:20px;background:#2a2a44;color:#eee;border:1px solid #4a4a6a;
border-radius:10px;cursor:pointer;transition:.15s}
.ctrl button:active{background:#7c4dff;transform:scale(.95)}
.ctrl .empty{visibility:hidden}
.btn{padding:12px 24px;font-size:16px;background:#7c4dff;color:#fff;border:none;border-radius:8px;
cursor:pointer;margin-top:14px;font-weight:bold}
.btn:active{transform:scale(.96)}
.hint{color:#888;margin-top:12px;font-size:13px;text-align:center;max-width:440px}
.footer{margin-top:14px;color:#555;font-size:11px}
a{color:#7c4dff}
</style></head><body>
<h1>{icon} {title}</h1>
<div class="meta">{description}</div>
'''

HTML_FOOT = '''<div class="footer">David Shop · 100% legítimo 😉</div>
</body></html>'''

HTML_SNAKE = HTML_HEAD + '''
<div class="info">Puntos: <b id="s">0</b> · Récord: <b id="b">0</b></div>
<canvas id="c" width="420" height="420"></canvas>
<div class="ctrl">
<div class="empty"></div><button data-d="u">▲</button><div class="empty"></div>
<button data-d="l">◀</button><button id="pz">⏸</button><button data-d="r">▶</button>
<div class="empty"></div><button data-d="d">▼</button><div class="empty"></div>
</div>
<div class="hint">Flechas / WASD para mover · Espacio = pausa</div>
<script>
const c=document.getElementById('c'),x=c.getContext('2d'),N=21,S=c.width/N;
let sn,dr,nd,fd,sc,bs=+localStorage.getItem('snBs')||0,pa=0,dd=0,tm,sp;
document.getElementById('b').textContent=bs;
function rs(){sn=[{x:10,y:10},{x:9,y:10},{x:8,y:10}];dr={x:1,y:0};nd={x:1,y:0};fd=rnd();
sc=0;pa=0;dd=0;sp=140;document.getElementById('s').textContent=0;clearInterval(tm);tm=setInterval(tk,sp);drw()}
function rnd(){let p;do{p={x:~~(Math.random()*N),y:~~(Math.random()*N)}}while(sn.some(s=>s.x==p.x&&s.y==p.y));return p}
function tk(){if(pa||dd)return;dr=nd;const h={x:sn[0].x+dr.x,y:sn[0].y+dr.y};
if(h.x<0||h.x>=N||h.y<0||h.y>=N||sn.some(s=>s.x==h.x&&s.y==h.y)){dd=1;clearInterval(tm);
if(sc>bs){bs=sc;localStorage.setItem('snBs',bs);document.getElementById('b').textContent=bs}drw();return}
sn.unshift(h);if(h.x==fd.x&&h.y==fd.y){sc+=10;document.getElementById('s').textContent=sc;fd=rnd();
if(sp>60){sp-=3;clearInterval(tm);tm=setInterval(tk,sp)}}else sn.pop();drw()}
function drw(){x.fillStyle='#181826';x.fillRect(0,0,c.width,c.height);
x.strokeStyle='#22223a';for(let i=1;i<N;i++){x.beginPath();x.moveTo(i*S,0);x.lineTo(i*S,c.height);x.stroke();
x.beginPath();x.moveTo(0,i*S);x.lineTo(c.width,i*S);x.stroke()}
x.fillStyle='#e74c3c';x.beginPath();x.arc(fd.x*S+S/2,fd.y*S+S/2,S/2-2,0,7);x.fill();
sn.forEach((p,i)=>{x.fillStyle=i===0?'#7cfc00':'#4caf50';x.fillRect(p.x*S+1,p.y*S+1,S-2,S-2)});
if(pa){x.fillStyle='rgba(0,0,0,.6)';x.fillRect(0,0,c.width,c.height);x.fillStyle='#fff';
x.font='bold 32px sans-serif';x.textAlign='center';x.fillText('PAUSA',c.width/2,c.height/2)}
if(dd){x.fillStyle='rgba(0,0,0,.75)';x.fillRect(0,0,c.width,c.height);x.fillStyle='#e74c3c';
x.font='bold 34px sans-serif';x.textAlign='center';x.fillText('GAME OVER',c.width/2,c.height/2-20);
x.fillStyle='#fff';x.font='18px sans-serif';x.fillText('Puntos: '+sc,c.width/2,c.height/2+20);
x.fillText('Espacio = reiniciar',c.width/2,c.height/2+50)}}
document.addEventListener('keydown',e=>{const k=e.key.toLowerCase();
if((k=='arrowup'||k=='w')&&!dr.y)nd={x:0,y:-1};if((k=='arrowdown'||k=='s')&&!dr.y)nd={x:0,y:1};
if((k=='arrowleft'||k=='a')&&!dr.x)nd={x:-1,y:0};if((k=='arrowright'||k=='d')&&!dr.x)nd={x:1,y:0};
if(k==' '){e.preventDefault();if(dd)rs();else{pa=!pa;drw()}}
if(k.startsWith('arrow'))e.preventDefault()});
document.querySelectorAll('.ctrl button[data-d]').forEach(b=>b.onclick=()=>{const d=b.dataset.d;
if(d=='u'&&!dr.y)nd={x:0,y:-1};if(d=='d'&&!dr.y)nd={x:0,y:1};
if(d=='l'&&!dr.x)nd={x:-1,y:0};if(d=='r'&&!dr.x)nd={x:1,y:0}});
document.getElementById('pz').onclick=()=>{if(dd)rs();else{pa=!pa;drw()}};
rs();
</script>''' + HTML_FOOT

HTML_PONG = HTML_HEAD + '''
<div class="info">Tú: <b id="ps">0</b> · CPU: <b id="cs">0</b></div>
<canvas id="c" width="600" height="400"></canvas>
<button class="btn" id="rs">Reiniciar</button>
<div class="hint">Mueve el ratón o las flechas ↑↓ / toca la pantalla</div>
<script>
const c=document.getElementById('c'),x=c.getContext('2d');
const W=c.width,H=c.height,PW=10,PH=80,BS=10;
let py,cy,bx,by,bvx,bvy,ps,cs;
function rs(){py=H/2-PH/2;cy=H/2-PH/2;bx=W/2;by=H/2;bvx=5;bvy=3;ps=0;cs=0;ud();loop()}
function ud(){document.getElementById('ps').textContent=ps;document.getElementById('cs').textContent=cs}
c.addEventListener('mousemove',e=>{const r=c.getBoundingClientRect();py=e.clientY-r.top-PH/2;});
c.addEventListener('touchmove',e=>{e.preventDefault();const r=c.getBoundingClientRect();py=e.touches[0].clientY-r.top-PH/2;},{passive:0});
document.addEventListener('keydown',e=>{if(e.key=='ArrowUp')py-=30;if(e.key=='ArrowDown')py+=30});
function loop(){if(bx<18&&by>cy&&by<cy+PH){bvx=-bvx+0.3;bvy+=((by-(cy+PH/2))/PH)*4}
if(bx>W-18-BS&&by>py&&by<py+PH){bvx=-bvx-0.3;bvy+=((by-(py+PH/2))/PH)*4}
const cyMid=cy+PH/2;if(by<cyMid-8)cy-=4;else if(by>cyMid+8)cy+=4;
cy=Math.max(0,Math.min(H-PH,cy));py=Math.max(0,Math.min(H-PH,py));
bx+=bvx;by+=bvy;if(by<BS/2||by>H-BS/2)bvy=-bvy;
if(bx<0){cs++;ud();bx=W/2;by=H/2;bvx=5;bvy=3}
if(bx>W){ps++;ud();bx=W/2;by=H/2;bvx=-5;bvy=3}
x.fillStyle='#181826';x.fillRect(0,0,W,H);
x.setLineDash([8,8]);x.strokeStyle='#333';x.beginPath();x.moveTo(W/2,0);x.lineTo(W/2,H);x.stroke();x.setLineDash([]);
x.fillStyle='#7c4dff';x.fillRect(10,py,PW,PH);
x.fillStyle='#e74c3c';x.fillRect(W-20,cy,PW,PH);
x.fillStyle='#fff';x.beginPath();x.arc(bx,by,BS,0,7);x.fill();
requestAnimationFrame(loop)}
document.getElementById('rs').onclick=rs;
rs();
</script>''' + HTML_FOOT

HTML_BREAKOUT = HTML_HEAD + '''
<div class="info">Puntos: <b id="s">0</b> · Vidas: <b id="l">3</b></div>
<canvas id="c" width="480" height="480"></canvas>
<button class="btn" id="rs">Reiniciar</button>
<div class="hint">Mueve con el ratón / ← → / toca la pantalla</div>
<script>
const c=document.getElementById('c'),x=c.getContext('2d');
const W=c.width,H=c.height,PW=90,PH=12,BR=16,BC=8,BW=W/BC,BH=22;
let px,bx,by,bvx,bvy,brk,sc,lv,run;
function rs(){px=W/2-PW/2;bx=W/2;by=H-40;bvx=4;bvy=-4;sc=0;lv=3;run=1;brk=[];
for(let r=0;r<BR;r++)for(let k=0;k<BC;k++)brk.push({x:k*BW,y:r*BH+40,w:BW-2,h:BH-2,alive:1,
color:['#e74c3c','#f1c40f','#2ecc71','#3498db','#9b59b6'][r%5]});
ud();loop()}
function ud(){document.getElementById('s').textContent=sc;document.getElementById('l').textContent=lv}
c.addEventListener('mousemove',e=>{const r=c.getBoundingClientRect();px=e.clientX-r.left-PW/2});
c.addEventListener('touchmove',e=>{e.preventDefault();const r=c.getBoundingClientRect();px=e.touches[0].clientX-r.left-PW/2},{passive:0});
document.addEventListener('keydown',e=>{if(e.key=='ArrowLeft')px-=30;if(e.key=='ArrowRight')px+=30});
function loop(){if(!run)return;
px=Math.max(0,Math.min(W-PW,px));
bx+=bvx;by+=bvy;if(bx<8||bx>W-8)bvx=-bvx;if(by<8)bvy=-bvy;
if(by>H-PH-8&&bx>px&&bx<px+PW&&bvy>0){bvy=-bvy;bvx+=((bx-(px+PW/2))/PW)*3;sc++;ud()}
for(const b of brk){if(!b.alive)continue;
if(bx>b.x&&bx<b.x+b.w&&by>b.y&&by<b.y+b.h){b.alive=0;bvy=-bvy;sc+=5;ud();break}}
if(by>H){lv--;ud();if(lv<=0){run=0;}else{bx=W/2;by=H-40;bvx=4;bvy=-4;px=W/2-PW/2}}
if(!brk.some(b=>b.alive)){run=0}
x.fillStyle='#181826';x.fillRect(0,0,W,H);
for(const b of brk){if(!b.alive)continue;x.fillStyle=b.color;x.fillRect(b.x,b.y,b.w,b.h)}
x.fillStyle='#7c4dff';x.fillRect(px,H-PH-4,PW,PH);
x.fillStyle='#fff';x.beginPath();x.arc(bx,by,8,0,7);x.fill();
if(!run){x.fillStyle='rgba(0,0,0,.7)';x.fillRect(0,0,W,H);x.fillStyle='#fff';
x.font='bold 32px sans-serif';x.textAlign='center';
x.fillText(lv>0?'¡GANASTE!':'GAME OVER',W/2,H/2-10);
x.font='18px sans-serif';x.fillText('Puntos: '+sc,W/2,H/2+25)}
requestAnimationFrame(loop)}
document.getElementById('rs').onclick=rs;
rs();
</script>''' + HTML_FOOT

HTML_2048 = HTML_HEAD + '''
<div class="info">Puntos: <b id="s">0</b> · Récord: <b id="b">0</b></div>
<canvas id="c" width="440" height="440"></canvas>
<button class="btn" id="rs">Nuevo juego</button>
<div class="hint">Flechas / WASD / desliza el dedo</div>
<script>
const c=document.getElementById('c'),x=c.getContext('2d'),N=4,S=c.width/N;
let g,sc,bs=+localStorage.getItem('g2048')||0,over;
document.getElementById('b').textContent=bs;
function rs(){g=Array.from({length:N},()=>Array(N).fill(0));sc=0;over=0;add();add();ud()}
function ud(){document.getElementById('s').textContent=sc;drw()}
function add(){const e=[];for(let i=0;i<N;i++)for(let j=0;j<N;j++)if(!g[i][j])e.push([i,j]);
if(!e.length)return;const[i,j]=e[~~(Math.random()*e.length)];g[i][j]=Math.random()<0.9?2:4}
function mv(d){let ch=0;
if(d=='l')for(let i=0;i<N;i++){const r=slide(g[i]);g[i]=r[0];ch+=r[1]}
if(d=='r')for(let i=0;i<N;i++){const r=slide(g[i].slice().reverse());g[i]=r[0].reverse();ch+=r[1]}
if(d=='u')for(let j=0;j<N;j++){const col=g.map(r=>r[j]);const r=slide(col);for(let i=0;i<N;i++)g[i][j]=r[0][i];ch+=r[1]}
if(d=='d')for(let j=0;j<N;j++){const col=g.map(r=>r[j]).reverse();const r=slide(col);const rc=r[0].reverse();for(let i=0;i<N;i++)g[i][j]=rc[i];ch+=r[1]}
if(ch){add();ud();chk()}}
function slide(a){a=a.filter(v=>v);let ch=0;
for(let i=0;i<a.length-1;i++)if(a[i]==a[i+1]){a[i]*=2;sc+=a[i];a.splice(i+1,1);ch=1}
while(a.length<N)a.push(0);return[a,ch]}
function chk(){for(let i=0;i<N;i++)for(let j=0;j<N;j++)if(!g[i][j])return;
for(let i=0;i<N;i++)for(let j=0;j<N;j++){if(j<N-1&&g[i][j]==g[i][j+1])return;if(i<N-1&&g[i][j]==g[i+1][j])return}
over=1;if(sc>bs){bs=sc;localStorage.setItem('g2048',bs);document.getElementById('b').textContent=bs}}
const CL={2:'#eee4da',4:'#ede0c8',8:'#f2b179',16:'#f59563',32:'#f67c5f',64:'#f65e3b',
128:'#edcf72',256:'#edcc61',512:'#edc850',1024:'#edc53f',2048:'#edc22e'};
function drw(){x.fillStyle='#181826';x.fillRect(0,0,c.width,c.height);
for(let i=0;i<N;i++)for(let j=0;j<N;j++){const v=g[i][j];
const px=j*S+6,py=i*S+6,s=S-12;
x.fillStyle=v?(CL[v]||'#3c3a32'):'#2a2a44';x.fillRect(px,py,s,s);
if(v){x.fillStyle=v<=4?'#776e65':'#fff';x.font='bold '+(v>=1024?26:v>=128?32:38)+'px sans-serif';
x.textAlign='center';x.textBaseline='middle';x.fillText(v,px+s/2,py+s/2)}}
if(over){x.fillStyle='rgba(0,0,0,.7)';x.fillRect(0,0,c.width,c.height);x.fillStyle='#fff';
x.font='bold 36px sans-serif';x.textAlign='center';x.textBaseline='middle';x.fillText('GAME OVER',c.width/2,c.height/2)}}
document.addEventListener('keydown',e=>{if(over)return;
const k=e.key.toLowerCase();if(k=='arrowleft'||k=='a')mv('l');
if(k=='arrowright'||k=='d')mv('r');if(k=='arrowup'||k=='w')mv('u');if(k=='arrowdown'||k=='s')mv('d');
if(k.startsWith('arrow'))e.preventDefault()});
let sx,sy;c.addEventListener('touchstart',e=>{sx=e.touches[0].clientX;sy=e.touches[0].clientY},{passive:1});
c.addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-sx,dy=e.changedTouches[0].clientY-sy;
if(Math.max(Math.abs(dx),Math.abs(dy))<30)return;
if(Math.abs(dx)>Math.abs(dy))mv(dx>0?'r':'l');else mv(dy>0?'d':'u')},{passive:1});
document.getElementById('rs').onclick=rs;
rs();
</script>''' + HTML_FOOT

HTML_TETRIS = HTML_HEAD + '''
<div class="info">Puntos: <b id="s">0</b> · Líneas: <b id="l">0</b> · Nivel: <b id="n">1</b></div>
<canvas id="c" width="300" height="600"></canvas>
<button class="btn" id="rs">Reiniciar</button>
<div class="hint">← → mover · ↑ rotar · ↓ bajar · Espacio = soltar</div>
<script>
const c=document.getElementById('c'),x=c.getContext('2d'),COLS=10,ROWS=20,S=30;
const SHAPES=[[[1,1,1,1]],[[1,1],[1,1]],[[1,1,1],[0,1,0]],[[1,1,1],[1,0,0]],[[1,1,1],[0,0,1]],
[[1,1,0],[0,1,1]],[[0,1,1],[1,1,0]]];
const COLORS=['#00f0f0','#f0f000','#a000f0','#0000f0','#f0a000','#00f000','#f00000'];
let bd,cur,cx,cy,sc,ln,nv,over,drp,tm;
function rs(){bd=Array.from({length:ROWS},()=>Array(COLS).fill(0));sc=0;ln=0;nv=1;over=0;drp=800;nw();tm=setInterval(tk,drp);ud()}
function nw(){const i=~~(Math.random()*SHAPES.length);cur={s:SHAPES[i],c:i+1};cx=~~((COLS-cur.s[0].length)/2);cy=0;
if(hit()){over=1;clearInterval(tm)}}
function hit(nx=cx,ny=cy,sh=cur.s){for(let i=0;i<sh.length;i++)for(let j=0;j<sh[i].length;j++)
if(sh[i][j]){const X=nx+j,Y=ny+i;if(X<0||X>=COLS||Y>=ROWS)return 1;if(Y>=0&&bd[Y][X])return 1}return 0}
function lock(){for(let i=0;i<cur.s.length;i++)for(let j=0;j<cur.s[i].length;j++)
if(cur.s[i][j]&&cy+i>=0)bd[cy+i][cx+j]=cur.c;
let cl=0;for(let i=ROWS-1;i>=0;i--)if(bd[i].every(v=>v)){bd.splice(i,1);bd.unshift(Array(COLS).fill(0));cl++;i++}
if(cl){ln+=cl;sc+=[0,100,300,500,800][cl];nv=1+~~(ln/10);drp=Math.max(100,800-ln*20);
clearInterval(tm);tm=setInterval(tk,drp)}nw();ud()}
function tk(){cy++;if(hit()){cy--;lock()}ud()}
function rot(){const s=cur.s;const n=s[0].map((_,i)=>s.map(r=>r[i]).reverse());
if(!hit(cx,cy,n))cur.s=n;ud()}
function ud(){document.getElementById('s').textContent=sc;document.getElementById('l').textContent=ln;
document.getElementById('n').textContent=nv;drw()}
function drw(){x.fillStyle='#181826';x.fillRect(0,0,c.width,c.height);
x.strokeStyle='#22223a';for(let i=0;i<=COLS;i++){x.beginPath();x.moveTo(i*S,0);x.lineTo(i*S,c.height);x.stroke()}
for(let i=0;i<=ROWS;i++){x.beginPath();x.moveTo(0,i*S);x.lineTo(c.width,i*S);x.stroke()}
for(let i=0;i<ROWS;i++)for(let j=0;j<COLS;j++)if(bd[i][j]){x.fillStyle=COLORS[bd[i][j]-1];x.fillRect(j*S+1,i*S+1,S-2,S-2)}
if(!over&&cur)for(let i=0;i<cur.s.length;i++)for(let j=0;j<cur.s[i].length;j++)
if(cur.s[i][j]&&cy+i>=0){x.fillStyle=COLORS[cur.c-1];x.fillRect((cx+j)*S+1,(cy+i)*S+1,S-2,S-2)}
if(over){x.fillStyle='rgba(0,0,0,.75)';x.fillRect(0,0,c.width,c.height);x.fillStyle='#fff';
x.font='bold 32px sans-serif';x.textAlign='center';x.fillText('GAME OVER',c.width/2,c.height/2-20);
x.font='18px sans-serif';x.fillText('Puntos: '+sc,c.width/2,c.height/2+20)}}
document.addEventListener('keydown',e=>{if(over)return;const k=e.key;
if(k=='ArrowLeft'&&!hit(cx-1))cx--;
if(k=='ArrowRight'&&!hit(cx+1))cx++;if(k=='ArrowDown'){cy++;if(hit()){cy--;lock()}}
if(k=='ArrowUp')rot();if(k==' '){while(!hit(cx,cy+1))cy++;cy--;lock()}
ud();if(k.startsWith('Arrow'))e.preventDefault()});
document.getElementById('rs').onclick=rs;
rs();
</script>''' + HTML_FOOT

HTML_FLAPPY = HTML_HEAD + '''
<div class="info">Puntos: <b id="s">0</b> · Récord: <b id="b">0</b></div>
<canvas id="c" width="400" height="560"></canvas>
<div class="hint">Clic / Espacio / Toca para volar</div>
<script>
const c=document.getElementById('c'),x=c.getContext('2d'),W=c.width,H=c.height;
let by,bv,pipes,sc,bs=+localStorage.getItem('fB')||0,over,tm,gd;
document.getElementById('b').textContent=bs;
function rs(){by=H/2;bv=0;pipes=[];sc=0;over=0;gd=0;
for(let i=0;i<3;i++)pipes.push({x:W+i*180,gy:100+Math.random()*(H-300),p:0});
document.getElementById('s').textContent=0;clearInterval(tm);tm=setInterval(tk,16)}
function fl(){if(over){rs();return}if(gd>0)return;bv=-7}
document.addEventListener('click',fl);
document.addEventListener('touchstart',e=>{e.preventDefault();fl()},{passive:0});
document.addEventListener('keydown',e=>{if(e.key==' ')fl()});
function tk(){gd++;if(gd<45){drw();return}
bv+=0.45;by+=bv;if(by<0||by>H-30){die();return}
for(const p of pipes){p.x-=2.4;if(!p.p&&p.x<60){p.p=1;sc++;document.getElementById('s').textContent=sc}
const gm=34;if(60+18>p.x&&60-18<p.x+50&&(by+15>p.gy+gm||by-15<p.gy-150)){die();return}
if(60+18>p.x+50&&60-18<p.x&&(by+15>p.gy+gm||by-15<p.gy-150)){die();return}}
pipes=pipes.filter(p=>p.x>-60);while(pipes.length<3)pipes.push({x:W+80+Math.random()*100,gy:100+Math.random()*(H-300),p:0});
drw()}
function die(){over=1;clearInterval(tm);if(sc>bs){bs=sc;localStorage.setItem('fB',bs);document.getElementById('b').textContent=bs};drw()}
function drw(){x.fillStyle='#87ceeb';x.fillRect(0,0,W,H);
x.fillStyle='#2e7d32';x.fillRect(0,H-30,W,30);
for(const p of pipes){x.fillStyle='#4caf50';x.fillRect(p.x,0,50,p.gy-150);x.fillRect(p.x,p.gy+34,50,H)}
x.fillStyle='#f1c40f';x.beginPath();x.arc(60,by,18,0,7);x.fill();
x.fillStyle='#000';x.beginPath();x.arc(66,by-4,3,0,7);x.fill();
if(gd<45){x.fillStyle='rgba(0,0,0,.5)';x.fillRect(0,0,W,H);x.fillStyle='#fff';x.font='bold 24px sans-serif';
x.textAlign='center';x.fillText('Toca para empezar',W/2,H/2)}
if(over){x.fillStyle='rgba(0,0,0,.75)';x.fillRect(0,0,W,H);x.fillStyle='#fff';x.font='bold 32px sans-serif';
x.textAlign='center';x.fillText('GAME OVER',W/2,H/2-20);x.font='18px sans-serif';
x.fillText('Puntos: '+sc,W/2,H/2+20);x.fillText('Toca para reiniciar',W/2,H/2+50)}}
rs();
</script>''' + HTML_FOOT

HTML_MEMORY = HTML_HEAD + '''
<div class="info">Movimientos: <b id="m">0</b> · Parejas: <b id="p">0</b>/8</div>
<canvas id="c" width="440" height="440"></canvas>
<button class="btn" id="rs">Nuevo</button>
<div class="hint">Encuentra todas las parejas</div>
<script>
const c=document.getElementById('c'),x=c.getContext('2d'),N=4,S=c.width/N;
const EMO=['🐶','🐱','🐭','🐹','🐰','🦊','🐻','🐼'];
let cards,flip,mv,prs,lock;
function rs(){const d=EMO.concat(EMO);d.sort(()=>Math.random()-0.5);
cards=d.map((e,i)=>({e,r:i%N,c:~~(i/N),up:0,dn:0}));flip=[];mv=0;prs=0;lock=0;ud()}
function ud(){document.getElementById('m').textContent=mv;document.getElementById('p').textContent=prs}
c.addEventListener('click',e=>{if(lock)return;const r=c.getBoundingClientRect();
const X=(e.clientX-r.left)/(c.width/N),Y=(e.clientY-r.top)/(c.height/N);
const card=cards.find(k=>k.r==~~X&&k.c==~~Y);if(!card||card.dn||card.up)return;
card.up=1;flip.push(card);drw();
if(flip.length==2){mv++;ud();lock=1;
if(flip[0].e==flip[1].e){setTimeout(()=>{flip.forEach(k=>k.dn=1);flip=[];prs++;ud();lock=0;drw();if(prs==8)win()},500)}
else setTimeout(()=>{flip.forEach(k=>k.up=0);flip=[];lock=0;drw()},800)}});
function drw(){x.fillStyle='#181826';x.fillRect(0,0,c.width,c.height);
for(const k of cards){const px=k.r*S+6,py=k.c*S+6,s=S-12;
x.fillStyle=k.dn?'#2e7d32':k.up?'#fff':'#7c4dff';x.fillRect(px,py,s,s);
x.textAlign='center';x.textBaseline='middle';
if(k.up||k.dn){x.font='44px sans-serif';x.fillStyle='#000';x.fillText(k.e,px+s/2,py+s/2)}
else{x.fillStyle='#fff';x.font='bold 30px sans-serif';x.fillText('?',px+s/2,py+s/2)}}}
function win(){x.fillStyle='rgba(0,0,0,.75)';x.fillRect(0,0,c.width,c.height);x.fillStyle='#4caf50';
x.font='bold 34px sans-serif';x.textAlign='center';x.fillText('¡GANASTE!',c.width/2,c.height/2-10);
x.fillStyle='#fff';x.font='18px sans-serif';x.fillText('Movimientos: '+mv,c.width/2,c.height/2+25)}
document.getElementById('rs').onclick=rs;
rs();
</script>''' + HTML_FOOT

HTML_MINES = HTML_HEAD + '''
<div class="info">Minas: <b id="m">10</b> · Banderas: <b id="f">0</b></div>
<canvas id="c" width="420" height="420"></canvas>
<button class="btn" id="rs">Nuevo</button>
<div class="hint">Clic = abrir · Clic derecho = bandera 🚩</div>
<script>
const c=document.getElementById('c'),x=c.getContext('2d'),N=10,S=c.width/N,MN=10;
let g,over,win,rst;
function rs(){g=Array.from({length:N},()=>Array(N).fill(null).map(()=>({m:0,o:0,f:0,n:0})));
let p=0;while(p<MN){const i=~~(Math.random()*N),j=~~(Math.random()*N);if(!g[i][j].m){g[i][j].m=1;p++}}
for(let i=0;i<N;i++)for(let j=0;j<N;j++)if(!g[i][j].m){let n=0;
for(let a=-1;a<=1;a++)for(let b=-1;b<=1;b++){const x=i+a,y=j+b;
if(x>=0&&x<N&&y>=0&&y<N&&g[x][y].m)n++}g[i][j].n=n}
over=0;win=0;rst=Date.now();ud()}
function ud(){const f=g.flat().filter(k=>k.f).length;
document.getElementById('f').textContent=f;document.getElementById('m').textContent=MN-f;drw()}
c.addEventListener('contextmenu',e=>{e.preventDefault();if(over)return;
const r=c.getBoundingClientRect();const X=~~((e.clientX-r.left)/S),Y=~~((e.clientY-r.top)/S);
const k=g[Y]&&g[Y][X];if(!k||k.o)return;k.f=!k.f;ud()});
c.addEventListener('click',e=>{if(over)return;
const r=c.getBoundingClientRect();const X=~~((e.clientX-r.left)/S),Y=~~((e.clientY-r.top)/S);
const k=g[Y]&&g[Y][X];if(!k||k.f||k.o)return;
if(k.m){k.o=1;over=1;lose();return}open(Y,X);check();ud()});
function open(i,j){if(i<0||i>=N||j<0||j>=N)return;const k=g[i][j];if(k.o||k.f)return;
k.o=1;if(k.n==0)for(let a=-1;a<=1;a++)for(let b=-1;b<=1;b++)open(i+a,j+b)}
function check(){for(let i=0;i<N;i++)for(let j=0;j<N;j++)if(!g[i][j].m&&!g[i][j].o)return;
win=1;over=1}
function lose(){for(let i=0;i<N;i++)for(let j=0;j<N;j++)if(g[i][j].m)g[i][j].o=1}
function drw(){x.fillStyle='#181826';x.fillRect(0,0,c.width,c.height);
for(let i=0;i<N;i++)for(let j=0;j<N;j++){const k=g[i][j];
let col='#2a2a44';if(k.o)col='#3a3a5a';else if(k.f)col='#f1c40f';
x.fillStyle=col;x.fillRect(j*S+1,i*S+1,S-2,S-2);
x.textAlign='center';x.textBaseline='middle';x.font='bold 20px sans-serif';
if(k.o&&k.m){x.font='22px sans-serif';x.fillText('💣',j*S+S/2,i*S+S/2)}
else if(k.o&&k.n){x.fillStyle=['','#3498db','#2ecc71','#e74c3c','#9b59b6','#e67e22','#16a085','#000','#7f8c8d'][k.n];
x.fillText(k.n,j*S+S/2,i*S+S/2)}
else if(k.f){x.font='22px sans-serif';x.fillText('🚩',j*S+S/2,i*S+S/2)}}
if(over){x.fillStyle='rgba(0,0,0,.7)';x.fillRect(0,0,c.width,c.height);x.fillStyle=win?'#4caf50':'#e74c3c';
x.font='bold 32px sans-serif';x.textAlign='center';x.fillText(win?'¡GANASTE!':'BOOM',c.width/2,c.height/2);
x.fillStyle='#fff';x.font='16px sans-serif';x.fillText('Tiempo: '+~~((Date.now()-rst)/1000)+'s',c.width/2,c.height/2+30)}}
document.getElementById('rs').onclick=rs;
rs();
</script>''' + HTML_FOOT

HTML_MAZE = HTML_HEAD + '''
<div class="info">Nivel: <b id="n">1</b> · Tiempo: <b id="t">0</b>s</div>
<canvas id="c" width="440" height="440"></canvas>
<div class="hint">Flechas / WASD para mover</div>
<script>
const c=document.getElementById('c'),x=c.getContext('2d'),N=15,S=c.width/N;
let g,px,py,ex,ey,lv,t0,tm,win;
function gen(){g=Array.from({length:N},()=>Array(N).fill(1));
function cw(i,j){if(i<0||i>=N||j<0||j>=N||!g[i][j])return;g[i][j]=0;
const d=[[0,2],[0,-2],[2,0],[-2,0]].sort(()=>Math.random()-0.5);
for(const[a,b]of d){const ni=i+a,nj=j+b;if(ni>0&&ni<N-1&&nj>0&&nj<N-1&&g[ni][nj]){g[i+a/2][j+b/2]=0;cw(ni,nj)}}}
cw(1,1);px=1;py=1;ex=N-2;ey=N-2;g[px][py]=0;g[ex][ey]=0}
function rs(){lv=1;t0=Date.now();gen();clearInterval(tm);tm=setInterval(()=>{document.getElementById('t').textContent=~~((Date.now()-t0)/1000)},200);ud()}
function ud(){document.getElementById('n').textContent=lv;drw()}
function mv(dx,dy){const nx=px+dx,ny=py+dy;if(g[ny]&&g[ny][nx]==0){px=nx;py=ny;
if(px==ex&&py==ey){lv++;gen();t0=Date.now()}ud()}}
document.addEventListener('keydown',e=>{const k=e.key.toLowerCase();
if(k=='arrowup'||k=='w')mv(0,-1);if(k=='arrowdown'||k=='s')mv(0,1);
if(k=='arrowleft'||k=='a')mv(-1,0);if(k=='arrowright'||k=='d')mv(1,0);
if(k.startsWith('arrow'))e.preventDefault()});
function drw(){x.fillStyle='#181826';x.fillRect(0,0,c.width,c.height);
for(let i=0;i<N;i++)for(let j=0;j<N;j++){if(g[i][j]){x.fillStyle='#7c4dff';x.fillRect(j*S,i*S,S,S)}};
x.fillStyle='#f1c40f';x.fillRect(ex*S+S/4,ey*S+S/4,S/2,S/2);
x.fillStyle='#4caf50';x.beginPath();x.arc(px*S+S/2,py*S+S/2,S/3,0,7);x.fill()}
rs();
</script>''' + HTML_FOOT

HTML_TYPING = HTML_HEAD + '''
<div class="info">Puntos: <b id="s">0</b> · Tiempo: <b id="t">30</b>s · Récord: <b id="b">0</b></div>
<div style="background:#181826;border:2px solid #7c4dff;border-radius:10px;padding:24px;max-width:520px;text-align:center;font-size:22px;min-width:300px">
<div style="color:#888;font-size:14px;margin-bottom:8px">Palabra actual:</div>
<div id="w" style="color:#ffb74d;font-weight:bold;font-size:34px">—</div>
<input id="i" autocomplete="off" autocapitalize="off" style="margin-top:16px;padding:12px;font-size:20px;width:100%;text-align:center;border:2px solid #7c4dff;border-radius:8px;background:#0d0d16;color:#fff" placeholder="Escribe aquí...">
</div>
<button class="btn" id="rs">Empezar</button>
<script>
const WS=['gato','perro','casa','árbol','libro','sol','luna','agua','fuego','tierra','cielo','mar','viento','nube','flor','pájaro','ratón','elefante','tigre','león','naranja','manzana','plátano','uva','sandía','mesa','silla','ventana','puerta','reloj','espejo','lápiz','papel','teléfono','computadora','teclado','pantalla','paraguas','cuchara'];
let s,t,r=30,act,cur_word=+localStorage.getItem('tB')||0;
document.getElementById('b').textContent=cur_word;
function nw(){cur_word=WS[~~(Math.random()*WS.length)];document.getElementById('w').textContent=cur_word;document.getElementById('i').value=''}
function st(){s=0;t=30;act=1;document.getElementById('s').textContent=0;document.getElementById('t').textContent=t;nw();
document.getElementById('i').focus();
const tm=setInterval(()=>{if(!act){clearInterval(tm);return}t--;document.getElementById('t').textContent=t;
if(t<=0){clearInterval(tm);act=0;if(s>cur_word){localStorage.setItem('tB',s);document.getElementById('b').textContent=s}
document.getElementById('w').textContent='¡Fin! '+s+' puntos';document.getElementById('i').blur()}},1000)}
document.getElementById('i').addEventListener('input',e=>{if(!act)return;
if(e.target.value.trim().toLowerCase()===cur_word.toLowerCase()){s++;document.getElementById('s').textContent=s;nw()}});
document.getElementById('i').addEventListener('keydown',e=>{if(e.key=='Enter'&&!act)st()});
document.getElementById('rs').onclick=st;
</script>''' + HTML_FOOT

HTML_REACTION = HTML_HEAD + '''
<div class="info">Récord: <b id="b">—</b></div>
<canvas id="c" width="480" height="300"></canvas>
<button class="btn" id="rs">Comenzar</button>
<div class="hint">Haz clic cuando cambie de color</div>
<script>
const c=document.getElementById('c'),x=c.getContext('2d');
let st='idle',t0,to,tm=+localStorage.getItem('rtB')||0;
if(tm)document.getElementById('b').textContent=tm+'ms';
function drw(){x.fillStyle=st=='wait'?'#e74c3c':st=='ready'?'#2ecc71':st=='done'?'#3498db':'#181826';
x.fillRect(0,0,c.width,c.height);
x.fillStyle='#fff';x.font='bold 26px sans-serif';x.textAlign='center';x.textBaseline='middle';
let txt='';
if(st=='idle')txt='Pulsa Comenzar';
if(st=='wait')txt='Espera el verde...';
if(st=='ready')txt='¡CLIC AHORA!';
if(st=='done')txt=(t0/1000).toFixed(3)+'s';
if(st=='early')txt='¡Muy pronto! Reiniciando...';
x.fillText(txt,c.width/2,c.height/2)}
function stt(){st='wait';drw();to=setTimeout(()=>{st='ready';t0=performance.now();drw()},1500+Math.random()*2500)}
c.addEventListener('click',()=>{if(st=='idle'||st=='done')return;
if(st=='wait'){clearTimeout(to);st='early';drw();setTimeout(stt,1200);return}
if(st=='ready'){const d=performance.now()-t0;st='done';t0=d;drw();
if(!tm||d<tm){tm=d;localStorage.setItem('rtB',~~d);document.getElementById('b').textContent=~~d+'ms'}}});
document.getElementById('rs').onclick=()=>{clearTimeout(to);stt()};
drw();
</script>''' + HTML_FOOT

HTML_PACMAN = HTML_HEAD + '''
<div class="info">Puntos: <b id="s">0</b> · Vidas: <b id="l">3</b></div>
<canvas id="c" width="380" height="420"></canvas>
<button class="btn" id="rs">Reiniciar</button>
<div class="hint">Flechas / WASD para mover</div>
<script>
const c=document.getElementById('c'),x=c.getContext('2d'),N=19,S=c.width/N;
const MAP=[ '###################','#........#........#','#.##.###.#.###.##.#','#.................#',
'#.##.#.#####.#.##.#','#....#...#...#....#','####.### # ###.####','   #.#       #.#   ',
'####.# ##-## #.####','    .  #   #  .    ','####.# ##### #.####','   #.#       #.#   ',
'####.# ##### #.####','#........#........#','#.##.###.#.###.##.#','#..#.....P.....#..#',
'##.#.#.#####.#.#.##','#....#...#...#....#','###################'].map(r=>r.padEnd(N,' ').slice(0,N));
let p,g,gv,sc,lv,run,dn,iv;
function rs(){p={x:9,y:15,dx:0,dy:0};g=[{x:9,y:9,dx:1,dy:0,c:'#e74c3c'}];sc=0;lv=3;run=1;dn=0;
document.getElementById('s').textContent=0;document.getElementById('l').textContent=lv;tmr()}
function tmr(){clearInterval(iv);iv=setInterval(tk,180)}
function isWall(x,y){if(x<0||x>=N||y<0||y>=N)return 1;const ch=MAP[y][x];return ch=='#'}
function tk(){if(!run)return;
const nx=p.x+p.dx,ny=p.y+p.dy;if(!isWall(nx,ny)){p.x=nx;p.y=ny;
if(MAP[p.y][p.x]=='.'){sc+=10;document.getElementById('s').textContent=sc}}
for(const gh of g){const d=[[1,0],[-1,0],[0,1],[0,-1]][~~(Math.random()*4)];
if(!isWall(gh.x+d[0],gh.y+d[1])){gh.x+=d[0];gh.y+=d[1]}}
for(const gh of g)if(gh.x==p.x&&gh.y==p.y){lv--;document.getElementById('l').textContent=lv;
if(lv<=0)run=0;else{p.x=9;p.y=15;p.dx=0;p.dy=0}}
drw()}
document.addEventListener('keydown',e=>{const k=e.key.toLowerCase();
if(k=='arrowup'||k=='w'){p.dx=0;p.dy=-1}if(k=='arrowdown'||k=='s'){p.dx=0;p.dy=1}
if(k=='arrowleft'||k=='a'){p.dx=-1;p.dy=0}if(k=='arrowright'||k=='d'){p.dx=1;p.dy=0}
if(k.startsWith('arrow'))e.preventDefault()});
function drw(){x.fillStyle='#000';x.fillRect(0,0,c.width,c.height);
for(let i=0;i<N;i++)for(let j=0;j<N;j++){const ch=MAP[i][j];
if(ch=='#'){x.fillStyle='#1919a6';x.fillRect(j*S,i*S,S,S)}
if(ch=='.'){x.fillStyle='#ffb897';x.beginPath();x.arc(j*S+S/2,i*S+S/2,2,0,7);x.fill()}}
x.fillStyle='#ffff00';x.beginPath();x.arc(p.x*S+S/2,p.y*S+S/2,S/2-3,0.2,7);x.fill();
for(const gh of g){x.fillStyle=gh.c;x.beginPath();x.arc(gh.x*S+S/2,gh.y*S+S/2,S/2-3,0,7);x.fill();
x.fillStyle='#fff';x.beginPath();x.arc(gh.x*S+S/3,gh.y*S+S/3,3,0,7);x.fill()}
if(!run){x.fillStyle='rgba(0,0,0,.75)';x.fillRect(0,0,c.width,c.height);x.fillStyle='#e74c3c';
x.font='bold 32px sans-serif';x.textAlign='center';x.fillText('GAME OVER',c.width/2,c.height/2-10);
x.fillStyle='#fff';x.font='18px sans-serif';x.fillText('Puntos: '+sc,c.width/2,c.height/2+25)}}
document.getElementById('rs').onclick=rs;
rs();
</script>''' + HTML_FOOT

HTML_GENERIC = HTML_HEAD + '''
<div class="info">Puntos: <b id="s">0</b> · Tiempo: <b id="t">30</b></div>
<canvas id="c" width="440" height="400"></canvas>
<button class="btn" id="rs">Empezar</button>
<div class="hint">Haz clic en los cuadrados para ganar puntos</div>
<script>
const c=document.getElementById('c'),x=c.getContext('2d');
let box,s,t,run,to;
function rs(){s=0;t=30;run=1;document.getElementById('s').textContent=0;
document.getElementById('t').textContent=t;nw();
clearInterval(to);to=setInterval(()=>{if(!run)return;t--;document.getElementById('t').textContent=t;
if(t<=0){run=0}},1000);drw()}
function nw(){box={x:40+Math.random()*(c.width-120),y:40+Math.random()*(c.height-120),
w:40+Math.random()*40,h:40+Math.random()*40,c:'hsl('+(Math.random()*360)+',70%,55%)'}}
c.addEventListener('click',e=>{if(!run)return;const r=c.getBoundingClientRect();
const X=e.clientX-r.left,Y=e.clientY-r.top;
if(X>box.x&&X<box.x+box.w&&Y>box.y&&Y<box.y+box.h){s++;document.getElementById('s').textContent=s;nw()}drw()});
function drw(){x.fillStyle='#181826';x.fillRect(0,0,c.width,c.height);
if(run){x.fillStyle=box.c;x.fillRect(box.x,box.y,box.w,box.h)}
else{x.fillStyle='rgba(0,0,0,.7)';x.fillRect(0,0,c.width,c.height);x.fillStyle='#ffb74d';
x.font='bold 34px sans-serif';x.textAlign='center';x.fillText('¡Fin!',c.width/2,c.height/2-10);
x.fillStyle='#fff';x.font='18px sans-serif';x.fillText('Puntos: '+s,c.width/2,c.height/2+25)}}
document.getElementById('rs').onclick=rs;
drw();
</script>''' + HTML_FOOT

HTML_GAMES_MAP = {
    "snake": HTML_SNAKE, "tetris": HTML_TETRIS, "pong": HTML_PONG, "breakout": HTML_BREAKOUT,
    "brick": HTML_BREAKOUT, "2048": HTML_2048, "flappy": HTML_FLAPPY, "minesweeper": HTML_MINES,
    "mine": HTML_MINES, "maze": HTML_MAZE, "labyrinth": HTML_MAZE, "typing": HTML_TYPING,
    "reaction": HTML_REACTION, "pacman": HTML_PACMAN, "pac": HTML_PACMAN, "memory": HTML_MEMORY,
    "match": HTML_MEMORY,
}

def detect_html_game(name):
    n = name.lower()
    for k, tpl in HTML_GAMES_MAP.items():
        if k in n: return tpl
    return HTML_GENERIC

# ✅ FIX: usamos .replace() en lugar de .format() para no tocar { } de CSS/JS
def build_html_game(product, user):
    tpl = detect_html_game(product["name"])
    html = (tpl
            .replace("{title}", product["name"])
            .replace("{icon}", product["icon"])
            .replace("{description}", product["description"]))
    html = html.replace("David Shop · 100% legítimo 😉",
                        f"David Shop · {user['username']} · 100% legítimo 😉")
    return html

# ============================================================
# BASE DE DATOS
# ============================================================
class DB:
    def __init__(self, path=DB_PATH):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
        self._create(); self._seed()

    def _create(self):
        self.c.executescript("""
        CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL, email TEXT UNIQUE NOT NULL,
            pw TEXT NOT NULL, avatar TEXT DEFAULT '👤',
            is_admin INTEGER DEFAULT 0, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS categories(id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_es TEXT, name_en TEXT, name_pt TEXT, icon TEXT);
        CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, description TEXT, price REAL NOT NULL,
            stock INTEGER DEFAULT 999, category_id INTEGER,
            icon TEXT DEFAULT '📦', discount INTEGER DEFAULT 0,
            sales INTEGER DEFAULT 0, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS cart(user_id INTEGER, product_id INTEGER,
            qty INTEGER DEFAULT 1, PRIMARY KEY(user_id, product_id));
        CREATE TABLE IF NOT EXISTS wishlist(user_id INTEGER, product_id INTEGER,
            PRIMARY KEY(user_id, product_id));
        CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, subtotal REAL, tax REAL, discount REAL,
            total REAL, coupon TEXT, status TEXT DEFAULT 'completed',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS order_items(id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER, product_id INTEGER, name TEXT, qty INTEGER, price REAL);
        CREATE TABLE IF NOT EXISTS reviews(id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER, user_id INTEGER, rating INTEGER,
            comment TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS library(user_id INTEGER, product_id INTEGER,
            purchased_at TEXT DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(user_id, product_id));
        CREATE TABLE IF NOT EXISTS recent(user_id INTEGER, product_id INTEGER,
            viewed_at TEXT DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(user_id, product_id));
        CREATE TABLE IF NOT EXISTS activity(id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, text TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS downloads(id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, product_id INTEGER, filepath TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE INDEX IF NOT EXISTS idx_products_cat ON products(category_id);
        CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);
        """)
        self.conn.commit()

    def _make_name(self, rng, adjs, nouns, extras):
        a, n, n2 = rng.choice(adjs), rng.choice(nouns), rng.choice(nouns)
        e = rng.choice(extras) if extras else ""
        p = rng.randint(0, 6)
        if p == 0: return f"{a} {n}"
        if p == 1: return f"The {n} of {a}"
        if p == 2: return f"{n}: {a} {n2}"
        if p == 3: return f"{a} {n} {e}".strip()
        if p == 4: return f"{n} {rng.randint(2, 9999)}"
        if p == 5: return f"The {a} {n}"
        return f"{a} {n} of the {n2}"

    def _gen(self, count, cat_id, seed, adjs, nouns, icons,
             price_lo, price_hi, extras=None, free_prob=0.05):
        rng = random.Random(seed)
        rows, seen, attempts = [], set(), 0
        while len(rows) < count and attempts < count * 60:
            attempts += 1
            name = self._make_name(rng, adjs, nouns, extras)
            if name in seen: continue
            seen.add(name)
            icon = rng.choice(icons)
            price = 0.0 if rng.random() < free_prob else round(rng.uniform(price_lo, price_hi), 2)
            discount = rng.choice([0,0,0,0,0,0,5,10,15,20,25,30,40,50,70])
            if price * (1 - discount/100) <= 0: price, discount = 0.0, 0
            sales = rng.randint(5, 5000)
            desc = f"{name} — {rng.choice(['una experiencia única','aventura inolvidable','obra maestra imprescindible','clásico moderno','juego adictivo','para toda la familia','desafío sin fin','gráficos impresionantes'])}."
            rows.append((name, desc, price, 999, cat_id, icon, discount, sales))
        while len(rows) < count:
            i = len(rows)
            name = f"{rng.choice(adjs)} {rng.choice(nouns)} #{i}"
            if name in seen: continue
            seen.add(name)
            rows.append((name, f"{name}.", round(rng.uniform(price_lo, price_hi), 2),
                         999, cat_id, rng.choice(icons), 0, rng.randint(5, 5000)))
        return rows

    def _seed(self):
        if self.c.execute("SELECT COUNT(*) FROM categories").fetchone()[0] == 0:
            self.c.executemany(
                "INSERT INTO categories(name_es,name_en,name_pt,icon) VALUES(?,?,?,?)",
                [("Juegos Steam","Steam Games","Jogos Steam","🎮"),
                 ("Juegos Epic","Epic Games","Jogos Epic","🎯"),
                 ("Juegos HTML","HTML Games","Jogos HTML","🌐"),
                 ("Apps","Apps","Apps","📱"),
                 ("Utilidades","Utilities","Utilidades","🛠"),
                 ("Suscripciones","Subscriptions","Assinaturas","⭐")])
        if self.c.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
            rows = []
            rows += self._gen(300,1,1001,STEAM_ADJ,STEAM_NOUN,ICON_STEAM,4.99,59.99,
                extras=["II","III","IV","V","VI","VII","VIII","IX","X","Remastered","Deluxe",
                        "Ultimate","Origins","Returns","Reborn","Online","Classic",
                        "Definitive Edition","Enhanced","Complete","Legendary"],free_prob=0.06)
            rows += self._gen(300,2,2002,EPIC_ADJ,EPIC_NOUN,ICON_EPIC,0.99,49.99,
                extras=["II","III","IV","V","Remastered","Deluxe","Ultimate","Origins","Returns",
                        "Online","Complete","Legendary","Champions Edition","Founder's Pack"],
                free_prob=0.10)
            rows += self._gen(100,3,3003,HTML_ADJ,HTML_NOUN,ICON_HTML,0.0,4.99,
                extras=["2","3","Classic","Deluxe","HD","Mini","Online"],free_prob=0.75)
            rows += self._gen(100,4,4004,APPS_ADJ,APPS_NOUN,ICON_APPS,0.99,29.99,
                extras=["2024","2025","Pro","Premium","Deluxe","Suite"],free_prob=0.30)
            rows += self._gen(100,5,5005,UTIL_ADJ,UTIL_NOUN,ICON_UTIL,0.0,39.99,
                extras=["2024","2025","Pro","Premium","Plus","Portable"],free_prob=0.35)
            rows += self._gen(100,6,6006,SUBS_ADJ,SUBS_NOUN,ICON_SUBS,2.99,19.99,
                extras=["Monthly","Annual","1 Month","1 Year","Family","Premium","Basic"],
                free_prob=0.02)
            self.c.executemany(
                "INSERT INTO products(name,description,price,stock,category_id,icon,discount,sales) VALUES(?,?,?,?,?,?,?,?)",
                rows)
            self.conn.commit()
        if not self.c.execute("SELECT * FROM users WHERE is_admin=1").fetchone():
            pw = hashlib.sha256("admin123".encode()).hexdigest()
            self.c.execute("INSERT INTO users(username,email,pw,is_admin,avatar) VALUES(?,?,?,?,?)",
                           ("admin","admin@davidshop.com",pw,1,"👑"))
        self.conn.commit()

    def q(self, sql, params=()):
        self.c.execute(sql, params); self.conn.commit(); return self.c
    def one(self, sql, params=()):
        return self.c.execute(sql, params).fetchone()
    def all(self, sql, params=()):
        return self.c.execute(sql, params).fetchall()

# ============================================================
# HELPERS
# ============================================================
def fmt_money(v): return f"${v:,.2f}"
def is_valid_email(e): return "@" in e and "." in e.split("@")[-1] and len(e) > 5

def toast(root, text, kind="info"):
    t = tk.Toplevel(root); t.overrideredirect(True); t.attributes("-topmost", True)
    colors = {"info":"#333","ok":"#2e7d32","err":"#c62828"}
    tk.Label(t, text=text, bg=colors.get(kind,"#333"), fg="white",
             padx=16, pady=10, font=("Segoe UI",10,"bold")).pack()
    root.update_idletasks()
    x = root.winfo_rootx() + root.winfo_width() - 320
    y = root.winfo_rooty() + 70
    t.geometry(f"+{x}+{y}"); t.after(1800, t.destroy)

def tooltip(widget, text):
    tip = {"win": None}
    def enter(_):
        w = tk.Toplevel(widget); w.wm_overrideredirect(True)
        w.wm_geometry(f"+{widget.winfo_rootx()+20}+{widget.winfo_rooty()+20}")
        tk.Label(w, text=text, bg="#222", fg="white", padx=8, pady=4).pack()
        tip["win"] = w
    def leave(_):
        if tip["win"]: tip["win"].destroy(); tip["win"] = None
    widget.bind("<Enter>", enter); widget.bind("<Leave>", leave)

def open_folder(path):
    path = str(path)
    try:
        if sys.platform.startswith("win"): os.startfile(path)
        elif sys.platform == "darwin": subprocess.Popen(["open", path])
        else: subprocess.Popen(["xdg-open", path])
    except Exception as e:
        messagebox.showwarning("David Shop", f"No se pudo abrir:\n{e}")

def open_file(path):
    path = str(path)
    try:
        if sys.platform.startswith("win"): os.startfile(path)
        elif sys.platform == "darwin": subprocess.Popen(["open", path])
        else: subprocess.Popen(["xdg-open", path])
    except Exception as e:
        messagebox.showwarning("David Shop", f"No se pudo abrir:\n{e}")

def safe_filename(name):
    return "".join(c for c in name if c.isalnum() or c in " -_.()").strip() or "product"

EXT_BY_CAT = {1: ".exe", 2: ".exe", 3: ".html", 4: ".apk", 5: ".exe", 6: ".pdf"}

# ============================================================
# APP
# ============================================================
class DavidShop:
    def __init__(self, root):
        self.root = root
        self.db = DB()
        self.lang = "ES"; self.theme = "light"
        self.user = None
        self.cart_coupon = None; self.cart_coupon_pct = 0
        self.page = 0; self.view_mode = "grid"
        self.last_search = ""; self.last_cat = 0
        self.last_min = 0.0; self.last_max = 10000.0
        self.last_instock = False; self.last_sort = "sort_sales"
        self.current_view = "home"
        self.root.title(self.t("app_title"))
        self.root.geometry("1200x760"); self.root.minsize(1050, 680)
        DOWNLOADS_FOLDER.mkdir(parents=True, exist_ok=True)
        self.build_splash()
        self.root.after(1200, self.start)

    def t(self, k): return I18N[self.lang].get(k, k)
    def C(self, k): return THEMES[self.theme][k]
    def page_size(self): return 20 if self.view_mode == "grid" else 30
    def final_price(self, p): return p["price"] * (1 - p["discount"]/100)
    def is_free(self, p): return self.final_price(p) <= 0.001
    def owns(self, pid):
        if not self.user: return False
        return self.db.one("SELECT 1 FROM library WHERE user_id=? AND product_id=?",
                           (self.user["id"], pid)) is not None
    def get_free(self, pid):
        if not self.require_login(): return
        if self.owns(pid): toast(self.root, "ℹ "+self.t("already_owned"), "info"); return
        self.db.q("INSERT OR IGNORE INTO library(user_id,product_id) VALUES(?,?)",
                  (self.user["id"], pid))
        self.db.q("UPDATE products SET sales=sales+1 WHERE id=?", (pid,))
        self.log_activity(f"Free: {pid}")
        toast(self.root, "🆓 "+self.t("obtained"), "ok")
        if self.current_view in ("catalog","home","wishlist"): self.show_view(self.current_view)

    def build_splash(self):
        s = tk.Toplevel(self.root); s.overrideredirect(True); s.configure(bg=self.C("primary"))
        w, h = 420, 280
        s.geometry(f"{w}x{h}+{(s.winfo_screenwidth()-w)//2}+{(s.winfo_screenheight()-h)//2}")
        LogoCanvas(s, width=160, bg=self.C("primary")).pack(pady=(16,4))
        tk.Label(s, text="David Shop", bg=self.C("primary"), fg="white",
                 font=("Segoe UI",20,"bold")).pack()
        tk.Label(s, text=self.t("splash_loading"), bg=self.C("primary"), fg="white",
                 font=("Segoe UI",10)).pack(pady=4)
        bar = ttk.Progressbar(s, mode="indeterminate", length=260); bar.pack(pady=8); bar.start(12)
        self.splash = s

    def start(self):
        self.splash.destroy(); self.build_ui(); self.show_login()

    def build_ui(self):
        self.root.configure(bg=self.C("bg"))
        for w in self.root.winfo_children(): w.destroy()

        self.top = tk.Frame(self.root, bg=self.C("primary"), height=64)
        self.top.pack(fill="x", side="top"); self.top.pack_propagate(False)
        LogoCanvas(self.top, width=54, bg=self.C("primary")).pack(side="left", padx=(8,2), pady=2)
        tk.Label(self.top, text="David Shop", bg=self.C("primary"), fg=self.C("primary_fg"),
                 font=("Segoe UI",16,"bold")).pack(side="left")

        right = tk.Frame(self.top, bg=self.C("primary")); right.pack(side="right", padx=10)
        self.theme_btn = tk.Button(right, text="🌙" if self.theme=="light" else "☀",
                                   bg=self.C("primary"), fg="white", bd=0,
                                   font=("Segoe UI Emoji",14), cursor="hand2",
                                   command=self.toggle_theme)
        self.theme_btn.pack(side="right", padx=4)
        self.lang_var = tk.StringVar(value=self.lang)
        lang_cb = ttk.Combobox(right, textvariable=self.lang_var, values=["ES","EN","PT"],
                               width=4, state="readonly")
        lang_cb.pack(side="right", padx=4)
        lang_cb.bind("<<ComboboxSelected>>", lambda e: self.set_lang(self.lang_var.get()))
        self.user_btn = tk.Button(right, text=self.user_label(), bg=self.C("primary"),
                                  fg="white", bd=0, font=("Segoe UI",11), cursor="hand2",
                                  command=self.toggle_user_menu)
        self.user_btn.pack(side="right", padx=8)

        mid = tk.Frame(self.top, bg=self.C("primary"))
        mid.pack(side="left", expand=True, fill="x", padx=20)
        self.search_entry = tk.Entry(mid, font=("Segoe UI",11), relief="flat")
        self.search_entry.pack(fill="x", pady=16, ipady=4)
        self.search_entry.bind("<Return>", lambda e: self.global_search())

        self.sidebar = tk.Frame(self.root, bg=self.C("sidebar"), width=200)
        self.sidebar.pack(fill="y", side="left"); self.sidebar.pack_propagate(False)
        self.nav_buttons = {}; self.build_sidebar()

        self.content = tk.Frame(self.root, bg=self.C("bg"))
        self.content.pack(fill="both", expand=True, side="right")

        self.status = tk.Frame(self.root, bg=self.C("sidebar"), height=24)
        self.status.pack(fill="x", side="bottom")
        self.status_lbl = tk.Label(self.status, text="", bg=self.C("sidebar"),
                                   fg=self.C("sidebar_fg"), font=("Segoe UI",9))
        self.status_lbl.pack(side="left", padx=8)
        self.clock = tk.Label(self.status, text="", bg=self.C("sidebar"),
                              fg=self.C("sidebar_fg"), font=("Segoe UI",9))
        self.clock.pack(side="right", padx=8); self.tick()

        self.root.bind("<Control-f>", lambda e: self.search_entry.focus_set())
        self.root.bind("<Control-k>", lambda e: self.show_view("cart"))
        self.root.bind("<Escape>", lambda e: self.show_view("home"))

    def tick(self):
        self.clock.config(text=dt.datetime.now().strftime("%Y-%m-%d  %H:%M:%S"))
        self.root.after(1000, self.tick)

    def user_label(self):
        return f"{self.user['avatar']} {self.user['username']}" if self.user else "👤 " + self.t("login")

    def build_sidebar(self):
        for w in self.sidebar.winfo_children(): w.destroy()
        items = [("home","🏠",self.t("home")),("catalog","🛒",self.t("catalog")),
                 ("wishlist","❤",self.t("wishlist")),("cart","🛍",self.t("cart")),
                 ("library","📚",self.t("library")),("orders","📦",self.t("orders")),
                 ("profile","👤",self.t("profile"))]
        if self.user and self.user["is_admin"]: items.append(("admin","🛡",self.t("admin")))
        items.append(("about","ℹ",self.t("about")))
        tk.Label(self.sidebar, text="  MENÚ", bg=self.C("sidebar"), fg=self.C("sidebar_fg"),
                 font=("Segoe UI",9,"bold"), anchor="w").pack(fill="x", pady=(14,4))
        for key, icon, label in items:
            b = tk.Button(self.sidebar, text=f"  {icon}  {label}", bd=0, anchor="w",
                          bg=self.C("sidebar"), fg=self.C("sidebar_fg"),
                          activebackground=self.C("primary"), activeforeground="white",
                          font=("Segoe UI",11), cursor="hand2",
                          command=lambda k=key: self.show_view(k))
            b.pack(fill="x", padx=8, pady=2, ipady=6)
            self.nav_buttons[key] = b

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.build_ui(); self.show_view(self.current_view)

    def set_lang(self, lang):
        self.lang = lang; self.root.title(self.t("app_title"))
        self.build_ui(); self.show_view(self.current_view)

    def toggle_user_menu(self):
        if not self.user: self.show_login(); return
        m = tk.Menu(self.root, tearoff=0)
        m.add_command(label=f"{self.user['avatar']}  {self.user['username']}", state="disabled")
        m.add_separator()
        m.add_command(label="👤 "+self.t("profile"), command=lambda: self.show_view("profile"))
        m.add_command(label="📦 "+self.t("orders"), command=lambda: self.show_view("orders"))
        m.add_command(label="📚 "+self.t("library"), command=lambda: self.show_view("library"))
        m.add_separator()
        m.add_command(label="📁 "+self.t("downloads_folder"),
                      command=lambda: open_folder(DOWNLOADS_FOLDER))
        m.add_separator()
        m.add_command(label="🚪 "+self.t("logout"), command=self.logout)
        try: m.tk_popup(self.user_btn.winfo_rootx(), self.user_btn.winfo_rooty()+40)
        finally: m.grab_release()

    def clear_content(self):
        for w in self.content.winfo_children(): w.destroy()

    def show_login(self):
        self.clear_content()
        wrap = tk.Frame(self.content, bg=self.C("bg")); wrap.pack(expand=True)
        card = tk.Frame(wrap, bg=self.C("card"), padx=30, pady=24,
                        highlightbackground=self.C("border"), highlightthickness=1)
        card.pack()
        LogoCanvas(card, width=130, bg=self.C("card")).pack(pady=(0,4))
        tk.Label(card, text="David Shop", font=("Segoe UI",20,"bold"),
                 bg=self.C("card"), fg=self.C("fg")).pack()
        self.login_mode = tk.StringVar(value="login")
        tabs = tk.Frame(card, bg=self.C("card")); tabs.pack(pady=16)
        tk.Radiobutton(tabs, text=self.t("login"), variable=self.login_mode, value="login",
                       bg=self.C("card"), fg=self.C("fg"), selectcolor=self.C("card"),
                       command=self.render_login_fields).pack(side="left", padx=6)
        tk.Radiobutton(tabs, text=self.t("register"), variable=self.login_mode, value="register",
                       bg=self.C("card"), fg=self.C("fg"), selectcolor=self.C("card"),
                       command=self.render_login_fields).pack(side="left", padx=6)
        self.login_body = tk.Frame(card, bg=self.C("card")); self.login_body.pack()
        self.render_login_fields()

    def render_login_fields(self):
        for w in self.login_body.winfo_children(): w.destroy()
        pad = {"pady":6,"anchor":"w"}
        tk.Label(self.login_body, text=self.t("username"), bg=self.C("card"), fg=self.C("fg")).pack(**pad)
        self.e_user = tk.Entry(self.login_body, width=32, font=("Segoe UI",11)); self.e_user.pack(ipady=4)
        tk.Label(self.login_body, text=self.t("email"), bg=self.C("card"), fg=self.C("fg")).pack(**pad)
        self.e_mail = tk.Entry(self.login_body, width=32, font=("Segoe UI",11)); self.e_mail.pack(ipady=4)
        if self.login_mode.get() == "login": self.e_mail.config(state="disabled")
        tk.Label(self.login_body, text=self.t("password"), bg=self.C("card"), fg=self.C("fg")).pack(**pad)
        self.e_pw = tk.Entry(self.login_body, width=32, show="•", font=("Segoe UI",11)); self.e_pw.pack(ipady=4)
        if self.login_mode.get() == "register":
            tk.Label(self.login_body, text=self.t("confirm_password"),
                     bg=self.C("card"), fg=self.C("fg")).pack(**pad)
            self.e_pw2 = tk.Entry(self.login_body, width=32, show="•", font=("Segoe UI",11))
            self.e_pw2.pack(ipady=4)
        self.remember_var = tk.IntVar(value=1)
        if self.login_mode.get() == "login":
            tk.Checkbutton(self.login_body, text=self.t("remember"), variable=self.remember_var,
                           bg=self.C("card"), fg=self.C("fg"), selectcolor=self.C("card")).pack(pady=6)
        action = self.t("login") if self.login_mode.get() == "login" else self.t("register")
        tk.Button(self.login_body, text=action, command=self.do_auth,
                  bg=self.C("primary"), fg="white", bd=0, font=("Segoe UI",11,"bold"),
                  padx=20, pady=8, cursor="hand2").pack(pady=12, fill="x")
        if self.login_mode.get() == "login":
            tk.Label(self.login_body, text="admin / admin123", fg=self.C("muted"),
                     bg=self.C("card"), font=("Segoe UI",8)).pack()

    def do_auth(self):
        u = self.e_user.get().strip(); p = self.e_pw.get()
        if not u or not p: toast(self.root, "⚠ Campos vacíos", "err"); return
        if self.login_mode.get() == "login":
            pw_hash = hashlib.sha256(p.encode()).hexdigest()
            row = self.db.one("SELECT * FROM users WHERE username=? AND pw=?", (u, pw_hash))
            if not row: messagebox.showerror(self.t("login"), self.t("invalid_login")); return
            self.user = dict(row); self.log_activity(f"Login: {u}")
            self.build_ui(); toast(self.root, f"{self.t('welcome_back')}, {u}", "ok")
            self.show_view("home")
        else:
            e = self.e_mail.get().strip()
            pw2 = self.e_pw2.get() if hasattr(self, "e_pw2") else ""
            if not is_valid_email(e): messagebox.showerror(self.t("register"), self.t("email_invalid")); return
            if len(p) < 6: messagebox.showerror(self.t("register"), self.t("pw_short")); return
            if p != pw2: messagebox.showerror(self.t("register"), self.t("pw_mismatch")); return
            if self.db.one("SELECT 1 FROM users WHERE username=? OR email=?", (u, e)):
                messagebox.showerror(self.t("register"), self.t("user_exists")); return
            h = hashlib.sha256(p.encode()).hexdigest()
            av = random.choice(AVATARS)
            self.db.q("INSERT INTO users(username,email,pw,avatar) VALUES(?,?,?,?)", (u, e, h, av))
            self.user = dict(self.db.one("SELECT * FROM users WHERE username=?", (u,)))
            self.log_activity(f"Registro: {u}")
            self.build_ui(); toast(self.root, f"🎉 {self.t('welcome')}, {u}", "ok")
            self.show_view("home")

    def logout(self):
        if not messagebox.askyesno("David Shop", self.t("logout_confirm")): return
        self.log_activity("Logout"); self.user = None
        self.cart_coupon = None; self.cart_coupon_pct = 0
        self.build_ui(); self.show_login()

    def log_activity(self, text):
        try: self.db.q("INSERT INTO activity(user_id, text) VALUES(?,?)",
                       (self.user["id"] if self.user else 0, text))
        except: pass

    def require_login(self):
        if not self.user:
            toast(self.root, self.t("login_required"), "err"); self.show_login(); return False
        return True

    def show_view(self, name, **kw):
        if name in ("cart","wishlist","library","orders","profile","admin") and not self.user:
            self.show_login(); return
        self.current_view = name; self.clear_content()
        for k, b in self.nav_buttons.items(): b.config(bg=self.C("sidebar"))
        if name in self.nav_buttons: self.nav_buttons[name].config(bg=self.C("primary"))
        getattr(self, f"view_{name}", self.view_home)(**kw)
        self.status_lbl.config(text=f"📍 {name.upper()}")

    def breadcrumb(self, parent, text):
        tk.Label(parent, text=text, bg=self.C("bg"), fg=self.C("muted"),
                 font=("Segoe UI",9)).pack(anchor="w", padx=16, pady=(8,0))

    # ---------- HOME ----------
    def view_home(self):
        wrap = tk.Frame(self.content, bg=self.C("bg")); wrap.pack(fill="both", expand=True)
        self.breadcrumb(wrap, "David Shop / Home")
        hi = tk.Frame(wrap, bg=self.C("bg")); hi.pack(fill="x", padx=16, pady=6)
        txt = f"{self.t('welcome')}, {self.user['username']}" if self.user else "David Shop"
        tk.Label(hi, text=txt, font=("Segoe UI",20,"bold"),
                 bg=self.C("bg"), fg=self.C("fg")).pack(anchor="w")
        self.section(wrap, "⭐ "+self.t("featured"),
                     self.db.all("SELECT * FROM products ORDER BY sales DESC LIMIT 4"))
        if self.user:
            recs = self.recommendations()
            if recs: self.section(wrap, "🎯 "+self.t("recommended"), recs)
            recent = self.db.all("""SELECT p.* FROM products p JOIN recent r ON r.product_id=p.id
                WHERE r.user_id=? ORDER BY r.viewed_at DESC LIMIT 4""", (self.user["id"],))
            if recent: self.section(wrap, "🕘 "+self.t("recent"), recent)
        free = self.db.all("SELECT * FROM products WHERE price=0 OR (price*(1-discount/100.0))<=0 ORDER BY RANDOM() LIMIT 4")
        if free: self.section(wrap, "🆓 "+self.t("free"), free)
        sales = self.db.all("SELECT * FROM products WHERE discount>0 AND price>0 ORDER BY RANDOM() LIMIT 4")
        if sales: self.section(wrap, "🔥 "+self.t("on_sale"), sales)

    def section(self, parent, title, products):
        tk.Label(parent, text=title, font=("Segoe UI",14,"bold"),
                 bg=self.C("bg"), fg=self.C("fg")).pack(anchor="w", padx=16, pady=(12,4))
        row = tk.Frame(parent, bg=self.C("bg")); row.pack(fill="x", padx=16)
        for i, p in enumerate(products):
            self.product_card(row, p).grid(row=0, column=i, padx=4, pady=4, sticky="nsew")
            row.columnconfigure(i, weight=1, uniform="homecard")

    def recommendations(self):
        return self.db.all("""SELECT DISTINCT p.* FROM products p
            WHERE p.category_id IN (SELECT category_id FROM products WHERE id IN
                (SELECT product_id FROM library WHERE user_id=?))
            AND p.id NOT IN (SELECT product_id FROM library WHERE user_id=?)
            ORDER BY RANDOM() LIMIT 4""", (self.user["id"], self.user["id"]))

    # ---------- CATALOG ----------
    def view_catalog(self):
        wrap = tk.Frame(self.content, bg=self.C("bg")); wrap.pack(fill="both", expand=True)
        self.breadcrumb(wrap, "David Shop / "+self.t("catalog"))
        fl = tk.Frame(wrap, bg=self.C("card"), padx=10, pady=8,
                      highlightbackground=self.C("border"), highlightthickness=1)
        fl.pack(fill="x", padx=16, pady=8)
        cats = self.db.all("SELECT * FROM categories")
        cat_names = [self.t("all")] + [c[f"name_{self.lang.lower()}"] for c in cats]
        self.cat_var = tk.StringVar(value=cat_names[0])
        tk.Label(fl, text=self.t("categories"), bg=self.C("card"), fg=self.C("fg")).pack(side="left", padx=(0,4))
        ttk.Combobox(fl, textvariable=self.cat_var, values=cat_names, width=18,
                     state="readonly").pack(side="left", padx=4)
        tk.Label(fl, text=self.t("min_price"), bg=self.C("card"), fg=self.C("fg")).pack(side="left", padx=(10,4))
        self.min_e = tk.Entry(fl, width=8); self.min_e.pack(side="left")
        tk.Label(fl, text=self.t("max_price"), bg=self.C("card"), fg=self.C("fg")).pack(side="left", padx=(10,4))
        self.max_e = tk.Entry(fl, width=8); self.max_e.pack(side="left")
        self.instock_var = tk.IntVar(value=0)
        tk.Checkbutton(fl, text=self.t("in_stock"), variable=self.instock_var,
                       bg=self.C("card"), fg=self.C("fg"), selectcolor=self.C("card")).pack(side="left", padx=10)
        sort_map = [self.t("sort_sales"), self.t("sort_name"), self.t("sort_price_asc"),
                    self.t("sort_price_desc"), self.t("sort_new")]
        self.sort_var = tk.StringVar(value=self.t(self.last_sort))
        tk.Label(fl, text=self.t("sort"), bg=self.C("card"), fg=self.C("fg")).pack(side="left", padx=(10,4))
        ttk.Combobox(fl, textvariable=self.sort_var, values=sort_map, width=14,
                     state="readonly").pack(side="left")
        tk.Button(fl, text="🔍 "+self.t("apply"), command=self.apply_filters,
                  bg=self.C("primary"), fg="white", bd=0, padx=10).pack(side="left", padx=8)
        self.mode_btn = tk.Button(fl, text="🔳" if self.view_mode=="grid" else "📋",
                                  command=self.toggle_view, bg=self.C("accent"),
                                  fg="white", bd=0, padx=8)
        self.mode_btn.pack(side="right")
        self.results = tk.Frame(wrap, bg=self.C("bg"))
        self.results.pack(fill="both", expand=True, padx=16, pady=(4,8))
        self.pagination_bar = tk.Frame(wrap, bg=self.C("bg"))
        self.pagination_bar.pack(fill="x", padx=16, pady=4)
        self.render_results()

    def toggle_view(self):
        self.view_mode = "list" if self.view_mode == "grid" else "grid"
        self.mode_btn.config(text="🔳" if self.view_mode=="grid" else "📋")
        self.page = 0; self.render_results()

    def apply_filters(self):
        self.last_search = self.search_entry.get().strip(); self.last_cat = 0
        if self.cat_var.get() != self.t("all"):
            for c in self.db.all("SELECT * FROM categories"):
                if c[f"name_{self.lang.lower()}"] == self.cat_var.get():
                    self.last_cat = c["id"]; break
        try: self.last_min = float(self.min_e.get() or 0)
        except: self.last_min = 0
        try: self.last_max = float(self.max_e.get() or 10000)
        except: self.last_max = 10000
        self.last_instock = bool(self.instock_var.get())
        sv = self.sort_var.get()
        if sv == self.t("sort_name"): self.last_sort = "sort_name"
        elif sv == self.t("sort_price_asc"): self.last_sort = "sort_price_asc"
        elif sv == self.t("sort_price_desc"): self.last_sort = "sort_price_desc"
        elif sv == self.t("sort_new"): self.last_sort = "sort_new"
        else: self.last_sort = "sort_sales"
        self.page = 0; self.render_results()

    def query_products(self):
        sql = "SELECT * FROM products WHERE 1=1"; params = []
        if self.last_search:
            sql += " AND (name LIKE ? OR description LIKE ?)"
            params += [f"%{self.last_search}%"]*2
        if self.last_cat: sql += " AND category_id=?"; params.append(self.last_cat)
        sql += " AND price BETWEEN ? AND ?"; params += [self.last_min, self.last_max]
        if self.last_instock: sql += " AND stock>0"
        order = {"sort_name":"name ASC","sort_price_asc":"price ASC","sort_price_desc":"price DESC",
                 "sort_sales":"sales DESC","sort_new":"id DESC"}.get(self.last_sort, "sales DESC")
        return self.db.all(sql + f" ORDER BY {order}", params)

    def render_results(self):
        for w in self.results.winfo_children(): w.destroy()
        for w in self.pagination_bar.winfo_children(): w.destroy()
        rows = self.query_products(); total = len(rows)
        ps = self.page_size(); start = self.page * ps; page_rows = rows[start:start+ps]
        if not page_rows:
            tk.Label(self.results, text="🚫 "+self.t("no_results"), bg=self.C("bg"),
                     fg=self.C("muted"), font=("Segoe UI",14)).pack(pady=40); return
        canvas = tk.Canvas(self.results, bg=self.C("bg"), highlightthickness=0)
        sb = ttk.Scrollbar(self.results, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=self.C("bg"))
        cwin = canvas.create_window((0,0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(cwin, width=e.width))
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")
        def _wheel(e): canvas.yview_scroll(int(-e.delta/120), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _wheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        if self.view_mode == "grid":
            cols = 4
            for i, p in enumerate(page_rows):
                self.product_card(inner, p, w=220).grid(row=i//cols, column=i%cols,
                                                        padx=6, pady=6, sticky="nsew")
            for c in range(cols): inner.columnconfigure(c, weight=1, uniform="card")
        else:
            for p in page_rows: self.product_row(inner, p).pack(fill="x", pady=3, padx=6)
        pages = max(1, (total + ps - 1) // ps)
        tk.Label(self.pagination_bar, text=f"{total} {self.t('total_products')}",
                 bg=self.C("bg"), fg=self.C("muted")).pack(side="left")
        if pages > 1:
            btns = tk.Frame(self.pagination_bar, bg=self.C("bg")); btns.pack(side="right")
            tk.Button(btns, text="◀◀", command=self.first_page, bg=self.C("card"), bd=0).pack(side="left", padx=1)
            tk.Button(btns, text="◀", command=self.prev_page, bg=self.C("card"), bd=0).pack(side="left", padx=1)
            self.page_var = tk.StringVar(value=str(self.page+1))
            pe = tk.Entry(btns, textvariable=self.page_var, width=4, justify="center")
            pe.pack(side="left", padx=4); pe.bind("<Return>", lambda e: self.jump_page())
            tk.Label(btns, text=f"/ {pages}", bg=self.C("bg"), fg=self.C("fg")).pack(side="left", padx=2)
            tk.Button(btns, text="▶", command=self.next_page, bg=self.C("card"), bd=0).pack(side="left", padx=1)
            tk.Button(btns, text="▶▶", command=self.last_page, bg=self.C("card"), bd=0).pack(side="left", padx=1)

    def first_page(self): self.page = 0; self.render_results()
    def last_page(self):
        self.page = max(0, (len(self.query_products())-1)//self.page_size()); self.render_results()
    def prev_page(self):
        if self.page > 0: self.page -= 1; self.render_results()
    def next_page(self):
        total = len(self.query_products()); ps = self.page_size()
        if self.page + 1 < (total+ps-1)//ps: self.page += 1; self.render_results()
    def jump_page(self):
        try:
            p = int(self.page_var.get())-1; total = len(self.query_products()); ps = self.page_size()
            pages = max(1, (total+ps-1)//ps); self.page = max(0, min(p, pages-1)); self.render_results()
        except: pass

    def product_card(self, parent, p, w=200):
        p = dict(p)
        avg = self.db.one("SELECT AVG(rating) a FROM reviews WHERE product_id=?", (p["id"],))
        rating = avg["a"] or 0
        free = self.is_free(p); owned = free and self.owns(p["id"])
        card = tk.Frame(parent, bg=self.C("card"), width=w,
                        highlightbackground=self.C("border"), highlightthickness=1)
        ic = tk.Label(card, text=p["icon"], font=("Segoe UI Emoji",40),
                      bg=self.C("card"), cursor="hand2"); ic.pack(pady=(10,0))
        ic.bind("<Button-1>", lambda e, pid=p["id"]: self.open_product(pid))
        badges = tk.Frame(card, bg=self.C("card")); badges.pack()
        if free:
            tk.Label(badges, text="🆓 "+self.t("free"), bg=self.C("success"),
                     fg="white", font=("Segoe UI",7,"bold"), padx=4).pack(side="left", padx=2)
        elif p["discount"] > 0:
            tk.Label(badges, text=self.t("on_sale"), bg=self.C("danger"),
                     fg="white", font=("Segoe UI",7,"bold"), padx=4).pack(side="left", padx=2)
        tk.Label(card, text=p["name"], bg=self.C("card"), fg=self.C("fg"),
                 font=("Segoe UI",10,"bold"), wraplength=w-16, justify="center"
                 ).pack(pady=(6,2), padx=6)
        stars = "⭐"*int(round(rating)) + "☆"*(5-int(round(rating)))
        tk.Label(card, text=f"{stars} ({rating:.1f})", bg=self.C("card"),
                 fg=self.C("muted"), font=("Segoe UI",8)).pack()
        pf = tk.Frame(card, bg=self.C("card")); pf.pack(pady=4)
        if free:
            tk.Label(pf, text="🆓 "+self.t("free"), bg=self.C("card"), fg=self.C("success"),
                     font=("Segoe UI",12,"bold")).pack(side="left")
        else:
            if p["discount"] > 0:
                tk.Label(pf, text=fmt_money(p["price"]), bg=self.C("card"), fg=self.C("muted"),
                         font=("Segoe UI",8,"overstrike")).pack(side="left", padx=2)
            tk.Label(pf, text=fmt_money(self.final_price(p)), bg=self.C("card"),
                     fg=self.C("primary"), font=("Segoe UI",12,"bold")).pack(side="left")
        btns = tk.Frame(card, bg=self.C("card")); btns.pack(pady=(0,8))
        if free:
            if owned:
                tk.Button(btns, text="✅ "+self.t("owned"), state="disabled", bg=self.C("card"),
                          fg=self.C("success"), bd=0, font=("Segoe UI",8,"bold")).pack(side="left", padx=2)
            else:
                tk.Button(btns, text="🆓 "+self.t("get_free"),
                          command=lambda pid=p["id"]: self.get_free(pid),
                          bg=self.C("success"), fg="white", bd=0,
                          font=("Segoe UI",8,"bold"), padx=6).pack(side="left", padx=2)
        else:
            tk.Button(btns, text="🛒", command=lambda pid=p["id"]: self.add_to_cart(pid),
                      bg=self.C("primary"), fg="white", bd=0, padx=6).pack(side="left", padx=2)
        in_w = self.user and self.db.one("SELECT 1 FROM wishlist WHERE user_id=? AND product_id=?",
                                         (self.user["id"], p["id"]))
        tk.Button(btns, text="❤" if in_w else "🤍",
                  command=lambda pid=p["id"]: self.toggle_wish(pid),
                  bg=self.C("card"), fg=self.C("danger"), bd=0).pack(side="left", padx=2)
        tk.Button(btns, text="ℹ", command=lambda pid=p["id"]: self.open_product(pid),
                  bg=self.C("card"), fg=self.C("primary"), bd=0).pack(side="left", padx=2)
        return card

    def product_row(self, parent, p):
        p = dict(p); free = self.is_free(p); owned = free and self.owns(p["id"])
        row = tk.Frame(parent, bg=self.C("card"), highlightbackground=self.C("border"),
                       highlightthickness=1)
        tk.Label(row, text=p["icon"], font=("Segoe UI Emoji",26), bg=self.C("card")).pack(side="left", padx=8, pady=6)
        mid = tk.Frame(row, bg=self.C("card")); mid.pack(side="left", fill="x", expand=True)
        tk.Label(mid, text=p["name"], bg=self.C("card"), fg=self.C("fg"),
                 font=("Segoe UI",11,"bold")).pack(anchor="w")
        tk.Label(mid, text=p["description"][:90], bg=self.C("card"), fg=self.C("muted"),
                 font=("Segoe UI",9)).pack(anchor="w")
        if free:
            tk.Label(row, text="🆓 "+self.t("free"), bg=self.C("card"), fg=self.C("success"),
                     font=("Segoe UI",12,"bold")).pack(side="right", padx=10)
            if owned:
                tk.Button(row, text="✅ "+self.t("owned"), state="disabled",
                          bg=self.C("card"), fg=self.C("success"), bd=0).pack(side="right")
            else:
                tk.Button(row, text="🆓 "+self.t("get_free"),
                          command=lambda pid=p["id"]: self.get_free(pid),
                          bg=self.C("success"), fg="white", bd=0, padx=8).pack(side="right")
        else:
            tk.Label(row, text=fmt_money(self.final_price(p)), bg=self.C("card"),
                     fg=self.C("primary"), font=("Segoe UI",12,"bold")).pack(side="right", padx=10)
            tk.Button(row, text="🛒", command=lambda pid=p["id"]: self.add_to_cart(pid),
                      bg=self.C("primary"), fg="white", bd=0, padx=8).pack(side="right")
        return row

    def open_product(self, pid):
        p = dict(self.db.one("SELECT * FROM products WHERE id=?", (pid,)))
        if not p: return
        if self.user:
            self.db.q("INSERT OR REPLACE INTO recent(user_id,product_id,viewed_at) VALUES(?,?,CURRENT_TIMESTAMP)",
                      (self.user["id"], pid))
        free = self.is_free(p); owned = free and self.owns(pid)
        win = tk.Toplevel(self.root); win.title(p["name"])
        win.geometry("640x600"); win.configure(bg=self.C("bg")); win.transient(self.root)
        tk.Label(win, text=p["icon"], font=("Segoe UI Emoji",70), bg=self.C("bg")).pack(pady=(16,0))
        tk.Label(win, text=p["name"], font=("Segoe UI",18,"bold"),
                 bg=self.C("bg"), fg=self.C("fg")).pack()
        if free:
            tk.Label(win, text="🆓 "+self.t("free_no_pay"), bg=self.C("bg"),
                     fg=self.C("success"), font=("Segoe UI",10,"italic")).pack(pady=2)
        avg = self.db.one("SELECT AVG(rating) a, COUNT(*) c FROM reviews WHERE product_id=?", (pid,))
        rating = avg["a"] or 0
        tk.Label(win, text=f"{'⭐'*int(round(rating))}{'☆'*(5-int(round(rating)))}  ({rating:.1f} · {avg['c']} {self.t('reviews')})",
                 bg=self.C("bg"), fg=self.C("muted")).pack()
        pf = tk.Frame(win, bg=self.C("bg")); pf.pack(pady=8)
        if free:
            tk.Label(pf, text="🆓 "+self.t("free"), bg=self.C("bg"), fg=self.C("success"),
                     font=("Segoe UI",22,"bold")).pack()
        else:
            if p["discount"] > 0:
                tk.Label(pf, text=fmt_money(p["price"]), bg=self.C("bg"), fg=self.C("muted"),
                         font=("Segoe UI",11,"overstrike")).pack(side="left", padx=4)
            tk.Label(pf, text=fmt_money(self.final_price(p)), bg=self.C("bg"),
                     fg=self.C("primary"), font=("Segoe UI",22,"bold")).pack(side="left")
        tk.Label(win, text=f"{self.t('stock')}: {p['stock']}   ·   {self.t('sales')}: {p['sales']}",
                 bg=self.C("bg"), fg=self.C("muted")).pack()
        tk.Label(win, text=p["description"], bg=self.C("bg"), fg=self.C("fg"),
                 wraplength=520, justify="left").pack(padx=20, pady=10)
        btns = tk.Frame(win, bg=self.C("bg")); btns.pack(pady=6)
        if free:
            if owned:
                tk.Button(btns, text="✅ "+self.t("owned"), state="disabled", bg=self.C("card"),
                          fg=self.C("success"), bd=0, font=("Segoe UI",11,"bold"),
                          padx=14, pady=6).pack(side="left", padx=4)
            else:
                tk.Button(btns, text="🆓 "+self.t("get_free"),
                          command=lambda: (self.get_free(pid), win.destroy()),
                          bg=self.C("success"), fg="white", bd=0,
                          font=("Segoe UI",11,"bold"), padx=14, pady=6).pack(side="left", padx=4)
        else:
            tk.Button(btns, text="🛒 "+self.t("add_cart"), command=lambda: self.add_to_cart(pid),
                      bg=self.C("primary"), fg="white", bd=0, padx=14, pady=6).pack(side="left", padx=4)
            tk.Button(btns, text="⚡ "+self.t("buy"),
                      command=lambda: (self.add_to_cart(pid), win.destroy(), self.show_view("cart")),
                      bg=self.C("accent"), fg="white", bd=0, padx=14, pady=6).pack(side="left", padx=4)
        in_w = self.user and self.db.one("SELECT 1 FROM wishlist WHERE user_id=? AND product_id=?",
                                         (self.user["id"], pid))
        tk.Button(btns, text=("❤ " if in_w else "🤍 ")+self.t("wishlist"),
                  command=lambda: (self.toggle_wish(pid), win.destroy()),
                  bg=self.C("card"), fg=self.C("danger"), bd=0, padx=14, pady=6).pack(side="left", padx=4)
        tk.Label(win, text="— "+self.t("reviews")+" —", font=("Segoe UI",12,"bold"),
                 bg=self.C("bg"), fg=self.C("fg")).pack(pady=(12,4))
        rev_frame = tk.Frame(win, bg=self.C("bg")); rev_frame.pack(fill="both", expand=True, padx=20)
        rv = self.db.all("""SELECT r.*, u.username, u.avatar FROM reviews r
            JOIN users u ON u.id=r.user_id WHERE r.product_id=?
            ORDER BY r.created_at DESC LIMIT 20""", (pid,))
        if not rv:
            tk.Label(rev_frame, text=self.t("empty"), bg=self.C("bg"), fg=self.C("muted")).pack()
        for r in rv:
            rr = tk.Frame(rev_frame, bg=self.C("card"), padx=8, pady=6); rr.pack(fill="x", pady=2)
            tk.Label(rr, text=f"{r['avatar']} {r['username']}  {'⭐'*r['rating']}",
                     bg=self.C("card"), fg=self.C("fg"), font=("Segoe UI",9,"bold")).pack(anchor="w")
            tk.Label(rr, text=r["comment"], bg=self.C("card"), fg=self.C("muted"),
                     wraplength=500, justify="left").pack(anchor="w")
        if self.user:
            wf = tk.Frame(win, bg=self.C("bg")); wf.pack(fill="x", padx=20, pady=8)
            tk.Label(wf, text=self.t("write_review"), bg=self.C("bg"), fg=self.C("fg")).pack(anchor="w")
            row = tk.Frame(wf, bg=self.C("bg")); row.pack(fill="x")
            self.rev_rating = tk.IntVar(value=5)
            for i in range(1,6):
                tk.Radiobutton(row, text=f"{i}⭐", variable=self.rev_rating, value=i,
                               bg=self.C("bg"), fg=self.C("fg"), selectcolor=self.C("bg")).pack(side="left")
            self.rev_comment = tk.Entry(row, width=30)
            self.rev_comment.pack(side="left", padx=6, fill="x", expand=True)
            tk.Button(row, text=self.t("submit"), command=lambda: self.submit_review(pid),
                      bg=self.C("primary"), fg="white", bd=0, padx=8).pack(side="right")

    def submit_review(self, pid):
        if not self.require_login(): return
        comment = self.rev_comment.get().strip()
        if not comment: toast(self.root, "✍ "+self.t("comment"), "err"); return
        self.db.q("INSERT INTO reviews(product_id,user_id,rating,comment) VALUES(?,?,?,?)",
                  (pid, self.user["id"], self.rev_rating.get(), comment))
        toast(self.root, "✅ "+self.t("submit"), "ok")

    # ---------- CARRITO ----------
    def add_to_cart(self, pid):
        if not self.require_login(): return
        p = self.db.one("SELECT * FROM products WHERE id=?", (pid,))
        if p and self.is_free(p): self.get_free(pid); return
        row = self.db.one("SELECT * FROM cart WHERE user_id=? AND product_id=?",
                          (self.user["id"], pid))
        if row: self.db.q("UPDATE cart SET qty=qty+1 WHERE user_id=? AND product_id=?",
                          (self.user["id"], pid))
        else: self.db.q("INSERT INTO cart(user_id,product_id,qty) VALUES(?,?,1)",
                        (self.user["id"], pid))
        self.log_activity(f"Add cart: {pid}"); toast(self.root, "🛒 "+self.t("added_cart"), "ok")

    def remove_from_cart(self, pid):
        self.db.q("DELETE FROM cart WHERE user_id=? AND product_id=?", (self.user["id"], pid))
        self.show_view("cart"); toast(self.root, "🗑 "+self.t("removed_cart"), "info")

    def change_qty(self, pid, delta):
        row = self.db.one("SELECT qty FROM cart WHERE user_id=? AND product_id=?",
                          (self.user["id"], pid))
        if not row: return
        nq = row["qty"] + delta
        if nq <= 0: self.remove_from_cart(pid); return
        self.db.q("UPDATE cart SET qty=? WHERE user_id=? AND product_id=?",
                  (nq, self.user["id"], pid)); self.show_view("cart")

    def cart_totals(self):
        rows = self.db.all("""SELECT c.qty, p.* FROM cart c JOIN products p ON p.id=c.product_id
            WHERE c.user_id=?""", (self.user["id"],))
        subtotal = sum(self.final_price(r) * r["qty"] for r in rows)
        discount = subtotal * self.cart_coupon_pct / 100
        taxed = (subtotal - discount) * 0.16
        total = subtotal - discount + taxed
        return rows, subtotal, discount, taxed, total

    def view_cart(self):
        wrap = tk.Frame(self.content, bg=self.C("bg")); wrap.pack(fill="both", expand=True)
        self.breadcrumb(wrap, "David Shop / "+self.t("cart"))
        tk.Label(wrap, text="🛍 "+self.t("cart"), font=("Segoe UI",18,"bold"),
                 bg=self.C("bg"), fg=self.C("fg")).pack(anchor="w", padx=16, pady=6)
        rows, subtotal, discount, taxed, total = self.cart_totals()
        if not rows:
            tk.Label(wrap, text="🛒 "+self.t("empty_cart"), bg=self.C("bg"),
                     fg=self.C("muted"), font=("Segoe UI",14)).pack(pady=40)
            tk.Label(wrap, text="ℹ "+self.t("free_no_pay"), bg=self.C("bg"),
                     fg=self.C("muted"), font=("Segoe UI",9,"italic")).pack(); return
        body = tk.Frame(wrap, bg=self.C("bg")); body.pack(fill="both", expand=True, padx=16)
        left = tk.Frame(body, bg=self.C("bg")); left.pack(side="left", fill="both", expand=True)
        for r in rows:
            row = tk.Frame(left, bg=self.C("card"), highlightbackground=self.C("border"),
                           highlightthickness=1)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=r["icon"], font=("Segoe UI Emoji",24), bg=self.C("card")).pack(side="left", padx=8, pady=8)
            info = tk.Frame(row, bg=self.C("card")); info.pack(side="left", fill="x", expand=True)
            tk.Label(info, text=r["name"], bg=self.C("card"), fg=self.C("fg"),
                     font=("Segoe UI",11,"bold")).pack(anchor="w")
            tk.Label(info, text=fmt_money(self.final_price(r)), bg=self.C("card"),
                     fg=self.C("primary")).pack(anchor="w")
            qf = tk.Frame(row, bg=self.C("card")); qf.pack(side="right", padx=8)
            tk.Button(qf, text="−", command=lambda pid=r["id"]: self.change_qty(pid,-1),
                      bg=self.C("card"), fg=self.C("fg"), bd=0, width=2).pack(side="left")
            tk.Label(qf, text=str(r["qty"]), width=3, bg=self.C("card"), fg=self.C("fg")).pack(side="left")
            tk.Button(qf, text="+", command=lambda pid=r["id"]: self.change_qty(pid,1),
                      bg=self.C("card"), fg=self.C("fg"), bd=0, width=2).pack(side="left")
            tk.Button(qf, text="🗑", command=lambda pid=r["id"]: self.remove_from_cart(pid),
                      bg=self.C("card"), fg=self.C("danger"), bd=0).pack(side="left", padx=4)
        right = tk.Frame(body, bg=self.C("card"), padx=14, pady=14,
                         highlightbackground=self.C("border"), highlightthickness=1)
        right.pack(side="right", fill="y", padx=(10,0))
        tk.Label(right, text=self.t("subtotal"), bg=self.C("card"), fg=self.C("fg")).pack(anchor="w")
        tk.Label(right, text=fmt_money(subtotal), bg=self.C("card"), fg=self.C("fg"),
                 font=("Segoe UI",11,"bold")).pack(anchor="e")
        if discount:
            tk.Label(right, text=f"{self.t('coupon')} ({self.cart_coupon})", bg=self.C("card"),
                     fg=self.C("success")).pack(anchor="w", pady=(6,0))
            tk.Label(right, text="− "+fmt_money(discount), bg=self.C("card"),
                     fg=self.C("success")).pack(anchor="e")
        tk.Label(right, text=self.t("tax"), bg=self.C("card"), fg=self.C("fg")).pack(anchor="w", pady=(6,0))
        tk.Label(right, text=fmt_money(taxed), bg=self.C("card"), fg=self.C("fg")).pack(anchor="e")
        tk.Frame(right, bg=self.C("border"), height=1).pack(fill="x", pady=8)
        tk.Label(right, text=self.t("total"), bg=self.C("card"), fg=self.C("fg"),
                 font=("Segoe UI",13,"bold")).pack(anchor="w")
        tk.Label(right, text=fmt_money(total), bg=self.C("card"), fg=self.C("primary"),
                 font=("Segoe UI",18,"bold")).pack(anchor="e")
        cf = tk.Frame(right, bg=self.C("card")); cf.pack(pady=10, fill="x")
        tk.Label(cf, text=self.t("coupon"), bg=self.C("card"), fg=self.C("fg")).pack(anchor="w")
        c2 = tk.Frame(cf, bg=self.C("card")); c2.pack(fill="x")
        self.coupon_e = tk.Entry(c2, width=14); self.coupon_e.pack(side="left", fill="x", expand=True)
        tk.Button(c2, text=self.t("apply"), command=self.apply_coupon,
                  bg=self.C("accent"), fg="white", bd=0, padx=6).pack(side="left")
        tk.Button(right, text="💳 "+self.t("checkout"), command=self.checkout,
                  bg=self.C("primary"), fg="white", bd=0, pady=10,
                  font=("Segoe UI",11,"bold")).pack(fill="x", pady=6)
        tk.Button(right, text="🗑 "+self.t("clear"), command=self.clear_cart,
                  bg=self.C("card"), fg=self.C("danger"), bd=0).pack(fill="x")

    def apply_coupon(self):
        code = self.coupon_e.get().strip().upper(); pct = COUPONS.get(code)
        if pct:
            self.cart_coupon = code; self.cart_coupon_pct = pct
            toast(self.root, f"✅ {self.t('coupon_ok')}: -{pct}%", "ok")
        else:
            self.cart_coupon = None; self.cart_coupon_pct = 0
            toast(self.root, "❌ "+self.t("coupon_bad"), "err")
        self.show_view("cart")

    def clear_cart(self):
        if not messagebox.askyesno("David Shop", self.t("confirm_delete")): return
        self.db.q("DELETE FROM cart WHERE user_id=?", (self.user["id"],))
        self.cart_coupon = None; self.cart_coupon_pct = 0; self.show_view("cart")

    def checkout(self):
        rows, subtotal, discount, taxed, total = self.cart_totals()
        if not rows: return
        cur = self.db.q("INSERT INTO orders(user_id,subtotal,tax,discount,total,coupon) VALUES(?,?,?,?,?,?)",
                        (self.user["id"], subtotal, taxed, discount, total, self.cart_coupon))
        oid = cur.lastrowid
        for r in rows:
            self.db.q("INSERT INTO order_items(order_id,product_id,name,qty,price) VALUES(?,?,?,?,?)",
                      (oid, r["id"], r["name"], r["qty"], r["price"]))
            self.db.q("INSERT OR IGNORE INTO library(user_id,product_id) VALUES(?,?)",
                      (self.user["id"], r["id"]))
            self.db.q("UPDATE products SET sales=sales+?, stock=MAX(stock-?,0) WHERE id=?",
                      (r["qty"], r["qty"], r["id"]))
        self.db.q("DELETE FROM cart WHERE user_id=?", (self.user["id"],))
        self.cart_coupon = None; self.cart_coupon_pct = 0
        self.log_activity(f"Compra: ${total:.2f}")
        messagebox.showinfo("David Shop", f"✅ {self.t('purchase_ok')}\n{self.t('total')}: {fmt_money(total)}")
        self.show_view("orders")

    # ---------- WISHLIST ----------
    def toggle_wish(self, pid):
        if not self.require_login(): return
        row = self.db.one("SELECT 1 FROM wishlist WHERE user_id=? AND product_id=?",
                          (self.user["id"], pid))
        if row:
            self.db.q("DELETE FROM wishlist WHERE user_id=? AND product_id=?", (self.user["id"], pid))
            toast(self.root, self.t("removed_wish"), "info")
        else:
            self.db.q("INSERT INTO wishlist(user_id,product_id) VALUES(?,?)", (self.user["id"], pid))
            toast(self.root, "❤ "+self.t("added_wish"), "ok")
        self.show_view(self.current_view)

    def view_wishlist(self):
        wrap = tk.Frame(self.content, bg=self.C("bg")); wrap.pack(fill="both", expand=True)
        self.breadcrumb(wrap, "David Shop / "+self.t("wishlist"))
        tk.Label(wrap, text="❤ "+self.t("wishlist"), font=("Segoe UI",18,"bold"),
                 bg=self.C("bg"), fg=self.C("fg")).pack(anchor="w", padx=16, pady=6)
        rows = self.db.all("""SELECT p.* FROM products p JOIN wishlist w ON w.product_id=p.id
            WHERE w.user_id=?""", (self.user["id"],))
        if not rows:
            tk.Label(wrap, text=self.t("empty"), bg=self.C("bg"), fg=self.C("muted")).pack(pady=40); return
        grid = tk.Frame(wrap, bg=self.C("bg")); grid.pack(fill="both", expand=True, padx=16)
        for i, p in enumerate(rows):
            self.product_card(grid, p, w=220).grid(row=i//4, column=i%4, padx=6, pady=6, sticky="nsew")
        for c in range(4): grid.columnconfigure(c, weight=1, uniform="wishcard")

    # ---------- LIBRARY ----------
    def view_library(self):
        wrap = tk.Frame(self.content, bg=self.C("bg")); wrap.pack(fill="both", expand=True)
        self.breadcrumb(wrap, "David Shop / "+self.t("library"))
        tk.Label(wrap, text="📚 "+self.t("library"), font=("Segoe UI",18,"bold"),
                 bg=self.C("bg"), fg=self.C("fg")).pack(anchor="w", padx=16, pady=6)
        top_bar = tk.Frame(wrap, bg=self.C("bg")); top_bar.pack(fill="x", padx=16)
        tk.Button(top_bar, text=self.t("open_folder_btn"),
                  command=lambda: open_folder(DOWNLOADS_FOLDER),
                  bg=self.C("accent"), fg="white", bd=0, padx=10, pady=4).pack(side="left")
        tk.Label(top_bar, text=f"📁 {DOWNLOADS_FOLDER}", bg=self.C("bg"),
                 fg=self.C("muted"), font=("Segoe UI",8)).pack(side="left", padx=8)
        rows = self.db.all("""SELECT p.*, l.purchased_at FROM products p JOIN library l ON l.product_id=p.id
            WHERE l.user_id=? ORDER BY l.purchased_at DESC""", (self.user["id"],))
        if not rows:
            tk.Label(wrap, text=self.t("empty"), bg=self.C("bg"), fg=self.C("muted")).pack(pady=40); return
        for r in rows:
            row = tk.Frame(wrap, bg=self.C("card"), highlightbackground=self.C("border"),
                           highlightthickness=1)
            row.pack(fill="x", padx=16, pady=3)
            tk.Label(row, text=r["icon"], font=("Segoe UI Emoji",26), bg=self.C("card")).pack(side="left", padx=8, pady=6)
            info = tk.Frame(row, bg=self.C("card")); info.pack(side="left", fill="x", expand=True)
            tk.Label(info, text=r["name"], bg=self.C("card"), fg=self.C("fg"),
                     font=("Segoe UI",11,"bold")).pack(anchor="w")
            tk.Label(info, text=f"{self.t('saved_at')}: {r['purchased_at']}", bg=self.C("card"),
                     fg=self.C("muted"), font=("Segoe UI",8)).pack(anchor="w")
            dl = self.db.one("SELECT filepath FROM downloads WHERE user_id=? AND product_id=?",
                             (self.user["id"], r["id"]))
            if r["category_id"] == 3:
                if dl:
                    tk.Button(row, text=self.t("play_html"),
                              command=lambda p=dl["filepath"]: open_file(p),
                              bg=self.C("success"), fg="white", bd=0, padx=10).pack(side="right", padx=4)
                tk.Button(row, text="⬇ "+self.t("download"),
                          command=lambda p=r: self.real_download(p),
                          bg=self.C("primary"), fg="white", bd=0, padx=10).pack(side="right", padx=4)
            else:
                if dl:
                    tk.Button(row, text="📂 "+self.t("open_folder_btn"),
                              command=lambda p=dl["filepath"]: open_folder(pathlib.Path(p).parent),
                              bg=self.C("accent"), fg="white", bd=0, padx=10).pack(side="right", padx=4)
                    tk.Button(row, text="⬇ "+self.t("download")+" ↻",
                              command=lambda p=r: self.real_download(p),
                              bg=self.C("primary"), fg="white", bd=0, padx=10).pack(side="right", padx=4)
                else:
                    tk.Button(row, text="⬇ "+self.t("download"),
                              command=lambda p=r: self.real_download(p),
                              bg=self.C("primary"), fg="white", bd=0, padx=10).pack(side="right", padx=8)

    # ---------- DESCARGA REAL ----------
    def real_download(self, p):
        if not self.require_login(): return
        DOWNLOADS_FOLDER.mkdir(parents=True, exist_ok=True)
        ext = EXT_BY_CAT.get(p["category_id"], ".txt")
        base = safe_filename(p["name"])
        target = DOWNLOADS_FOLDER / f"{base}{ext}"
        if target.exists():
            i = 2
            while True:
                cand = DOWNLOADS_FOLDER / f"{base} ({i}){ext}"
                if not cand.exists(): target = cand; break
                i += 1
        now = dt.datetime.now()
        if ext == ".html":
            content = build_html_game(p, self.user).encode("utf-8")
        else:
            header = (
                f"=== David Shop — Archivo de {p['name']} ===\n"
                f"Producto: {p['name']}\nID: {p['id']}\nCategoría: {p['category_id']}\n"
                f"Precio original: ${p['price']:.2f}\nDescuento: {p['discount']}%\n"
                f"Precio final: ${self.final_price(p):.2f}\n"
                f"Usuario: {self.user['username']} ({self.user['email']})\n"
                f"Fecha: {now:%Y-%m-%d %H:%M:%S}\nArchivo: {target.name}\n"
                f"\nDescripción:\n{p['description']}\n\n"
                f"--- Gracias por confiar en David Shop ---\n"
            )
            content = header.encode("utf-8")
        win = tk.Toplevel(self.root); win.title(self.t("downloading"))
        win.geometry("440x200"); win.configure(bg=self.C("bg"))
        win.transient(self.root); win.grab_set()
        tk.Label(win, text=f"{p['icon']} {p['name']}", bg=self.C("bg"), fg=self.C("fg"),
                 font=("Segoe UI",11,"bold")).pack(pady=(10,4))
        pb = ttk.Progressbar(win, length=380, maximum=100); pb.pack(pady=8)
        lbl = tk.Label(win, text="0%", bg=self.C("bg"), fg=self.C("muted")); lbl.pack()
        path_lbl = tk.Label(win, text="", bg=self.C("bg"), fg=self.C("accent"),
                            font=("Segoe UI",8), wraplength=420); path_lbl.pack(pady=4)
        def worker():
            try:
                total = len(content); chunk = max(1, total // 40)
                with open(target, "wb") as f:
                    for i in range(0, total, chunk):
                        f.write(content[i:i+chunk])
                        pct = min(100, int((i+chunk)/total*100))
                        self.root.after(0, lambda pct=pct: (pb.config(value=pct),
                                                            lbl.config(text=f"{pct}%")))
                        time.sleep(0.04)
                self.root.after(0, lambda: (pb.config(value=100),
                    lbl.config(text=self.t("done")+" ✅"),
                    path_lbl.config(text=f"📁 {target}")))
                self.db.q("INSERT INTO downloads(user_id,product_id,filepath) VALUES(?,?,?)",
                          (self.user["id"], p["id"], str(target)))
                self.log_activity(f"Descarga real: {target.name}")
                self.root.after(0, lambda: self._finish_download(win, target, p))
            except Exception as e:
                self.root.after(0, lambda: (messagebox.showerror(self.t("download_error"), str(e)),
                                            win.destroy()))
        threading.Thread(target=worker, daemon=True).start()

    def _finish_download(self, win, target, product):
        win.destroy()
        if product["category_id"] == 3 and str(target).endswith(".html"):
            if messagebox.askyesno("David Shop",
                    f"{self.t('saved_at')}:\n{target}\n\n¿Abrir el juego ahora?"):
                open_file(target)
        else:
            if messagebox.askyesno("David Shop",
                    f"{self.t('saved_at')}:\n{target}\n\n{self.t('open_folder')}"):
                open_folder(target.parent)
        if self.current_view == "library": self.show_view("library")

    # ---------- ORDERS ----------
    def view_orders(self):
        wrap = tk.Frame(self.content, bg=self.C("bg")); wrap.pack(fill="both", expand=True)
        self.breadcrumb(wrap, "David Shop / "+self.t("orders"))
        tk.Label(wrap, text="📦 "+self.t("orders"), font=("Segoe UI",18,"bold"),
                 bg=self.C("bg"), fg=self.C("fg")).pack(anchor="w", padx=16, pady=6)
        rows = self.db.all("SELECT * FROM orders WHERE user_id=? ORDER BY created_at DESC",
                           (self.user["id"],))
        if not rows:
            tk.Label(wrap, text=self.t("orders_empty"), bg=self.C("bg"), fg=self.C("muted")).pack(pady=40); return
        for o in rows:
            row = tk.Frame(wrap, bg=self.C("card"), highlightbackground=self.C("border"),
                           highlightthickness=1)
            row.pack(fill="x", padx=16, pady=3)
            tk.Label(row, text=f"#{o['id']}", bg=self.C("card"), fg=self.C("fg"),
                     font=("Segoe UI",11,"bold")).pack(side="left", padx=10, pady=8)
            tk.Label(row, text=o["created_at"], bg=self.C("card"), fg=self.C("muted")).pack(side="left", padx=6)
            tk.Label(row, text=fmt_money(o["total"]), bg=self.C("card"), fg=self.C("primary"),
                     font=("Segoe UI",11,"bold")).pack(side="right", padx=10)
            tk.Button(row, text="👁", command=lambda oid=o["id"]: self.order_detail(oid),
                      bg=self.C("card"), bd=0).pack(side="right")

    def order_detail(self, oid):
        items = self.db.all("SELECT * FROM order_items WHERE order_id=?", (oid,))
        txt = "\n".join(f"• {it['name']} x{it['qty']}  —  {fmt_money(it['price'])}" for it in items)
        messagebox.showinfo(f"#{oid}", txt or self.t("empty"))

    # ---------- PROFILE ----------
    def view_profile(self):
        wrap = tk.Frame(self.content, bg=self.C("bg")); wrap.pack(fill="both", expand=True)
        self.breadcrumb(wrap, "David Shop / "+self.t("profile"))
        tk.Label(wrap, text="👤 "+self.t("profile"), font=("Segoe UI",18,"bold"),
                 bg=self.C("bg"), fg=self.C("fg")).pack(anchor="w", padx=16, pady=6)
        card = tk.Frame(wrap, bg=self.C("card"), padx=20, pady=20,
                        highlightbackground=self.C("border"), highlightthickness=1)
        card.pack(padx=16, pady=6, fill="x")
        av_frame = tk.Frame(card, bg=self.C("card")); av_frame.pack(anchor="w", pady=4)
        tk.Label(av_frame, text=self.t("avatar"), bg=self.C("card"), fg=self.C("fg")).pack(side="left")
        self.av_var = tk.StringVar(value=self.user["avatar"])
        ttk.Combobox(av_frame, textvariable=self.av_var, values=AVATARS, width=4,
                     state="readonly").pack(side="left", padx=8)
        tk.Label(card, text=self.t("email"), bg=self.C("card"), fg=self.C("fg")).pack(anchor="w", pady=(8,0))
        self.prof_email = tk.Entry(card, width=40); self.prof_email.pack(anchor="w", ipady=4)
        self.prof_email.insert(0, self.user["email"])
        tk.Label(card, text=self.t("new_password"), bg=self.C("card"), fg=self.C("fg")).pack(anchor="w", pady=(8,0))
        self.prof_pw = tk.Entry(card, width=40, show="•"); self.prof_pw.pack(anchor="w", ipady=4)
        btns = tk.Frame(card, bg=self.C("card")); btns.pack(anchor="w", pady=12)
        tk.Button(btns, text="💾 "+self.t("save_changes"), command=self.save_profile,
                  bg=self.C("primary"), fg="white", bd=0, padx=12, pady=6).pack(side="left")
        tk.Button(btns, text="🚪 "+self.t("logout"), command=self.logout,
                  bg=self.C("card"), fg=self.C("fg"), bd=0, padx=12, pady=6).pack(side="left", padx=6)
        tk.Button(btns, text="🗑 "+self.t("delete_account"), command=self.delete_account,
                  bg=self.C("card"), fg=self.C("danger"), bd=0, padx=12, pady=6).pack(side="left")
        stats = tk.Frame(wrap, bg=self.C("bg")); stats.pack(fill="x", padx=16, pady=10)
        o = self.db.one("SELECT COUNT(*) c, COALESCE(SUM(total),0) s FROM orders WHERE user_id=?",
                        (self.user["id"],))
        l = self.db.one("SELECT COUNT(*) c FROM library WHERE user_id=?", (self.user["id"],))
        d = self.db.one("SELECT COUNT(*) c FROM downloads WHERE user_id=?", (self.user["id"],))
        for label, val in [(self.t("orders"), o["c"]), (self.t("library"), l["c"]),
                           (self.t("download"), d["c"]), (self.t("revenue"), fmt_money(o["s"]))]:
            f = tk.Frame(stats, bg=self.C("card"), padx=20, pady=14,
                         highlightbackground=self.C("border"), highlightthickness=1)
            f.pack(side="left", padx=6, fill="y")
            tk.Label(f, text=str(val), bg=self.C("card"), fg=self.C("primary"),
                     font=("Segoe UI",16,"bold")).pack()
            tk.Label(f, text=label, bg=self.C("card"), fg=self.C("muted")).pack()

    def save_profile(self):
        e = self.prof_email.get().strip()
        if not is_valid_email(e): messagebox.showerror("David Shop", self.t("email_invalid")); return
        av = self.av_var.get()
        self.db.q("UPDATE users SET email=?, avatar=? WHERE id=?", (e, av, self.user["id"]))
        np = self.prof_pw.get()
        if np:
            if len(np) < 6: messagebox.showerror("David Shop", self.t("pw_short")); return
            h = hashlib.sha256(np.encode()).hexdigest()
            self.db.q("UPDATE users SET pw=? WHERE id=?", (h, self.user["id"]))
        self.user = dict(self.db.one("SELECT * FROM users WHERE id=?", (self.user["id"],)))
        self.build_ui(); toast(self.root, "💾 "+self.t("save_changes"), "ok"); self.show_view("profile")

    def delete_account(self):
        if not messagebox.askyesno("David Shop", self.t("confirm_delete")): return
        uid = self.user["id"]
        for t in ("cart","wishlist","library","recent","reviews","activity","downloads"):
            self.db.q(f"DELETE FROM {t} WHERE user_id=?", (uid,))
        self.db.q("DELETE FROM order_items WHERE order_id IN (SELECT id FROM orders WHERE user_id=?)", (uid,))
        self.db.q("DELETE FROM orders WHERE user_id=?", (uid,))
        self.db.q("DELETE FROM users WHERE id=?", (uid,))
        toast(self.root, self.t("user_deleted"), "ok")
        self.user = None; self.build_ui(); self.show_login()

    # ---------- ADMIN ----------
    def view_admin(self):
        if not (self.user and self.user["is_admin"]):
            tk.Label(self.content, text=self.t("admin_only"), bg=self.C("bg"),
                     fg=self.C("danger")).pack(pady=40); return
        wrap = tk.Frame(self.content, bg=self.C("bg")); wrap.pack(fill="both", expand=True)
        self.breadcrumb(wrap, "David Shop / "+self.t("admin"))
        tk.Label(wrap, text="🛡 "+self.t("admin"), font=("Segoe UI",18,"bold"),
                 bg=self.C("bg"), fg=self.C("fg")).pack(anchor="w", padx=16, pady=6)
        stats = tk.Frame(wrap, bg=self.C("bg")); stats.pack(fill="x", padx=16)
        tr = self.db.one("SELECT COALESCE(SUM(total),0) s FROM orders")["s"]
        no = self.db.one("SELECT COUNT(*) c FROM orders")["c"]
        nu = self.db.one("SELECT COUNT(*) c FROM users")["c"]
        np_ = self.db.one("SELECT COUNT(*) c FROM products")["c"]
        for label, val in [(self.t("users"), nu), (self.t("products"), np_),
                           (self.t("orders"), no), (self.t("revenue"), fmt_money(tr))]:
            f = tk.Frame(stats, bg=self.C("card"), padx=20, pady=12,
                         highlightbackground=self.C("border"), highlightthickness=1)
            f.pack(side="left", padx=6, fill="y")
            tk.Label(f, text=str(val), bg=self.C("card"), fg=self.C("primary"),
                     font=("Segoe UI",14,"bold")).pack()
            tk.Label(f, text=label, bg=self.C("card"), fg=self.C("muted")).pack()
        nb = ttk.Notebook(wrap); nb.pack(fill="both", expand=True, padx=16, pady=10)
        ptab = tk.Frame(nb, bg=self.C("bg")); nb.add(ptab, text="📦 "+self.t("products"))
        self.admin_products_table(ptab)
        utab = tk.Frame(nb, bg=self.C("bg")); nb.add(utab, text="👥 "+self.t("users"))
        self.admin_users_table(utab)
        otab = tk.Frame(nb, bg=self.C("bg")); nb.add(otab, text="📦 "+self.t("orders"))
        self.admin_orders_table(otab)
        ctab = tk.Frame(nb, bg=self.C("bg")); nb.add(ctab, text="🎟 "+self.t("coupons"))
        self.admin_coupons_tab(ctab)
        ttab = tk.Frame(nb, bg=self.C("bg")); nb.add(ttab, text="🛠 Tools")
        self.admin_tools_tab(ttab)

    def admin_products_table(self, parent):
        top = tk.Frame(parent, bg=self.C("bg")); top.pack(fill="x", pady=4)
        tk.Button(top, text="➕ "+self.t("new"), command=self.admin_new_product,
                  bg=self.C("primary"), fg="white", bd=0, padx=10).pack(side="left")
        cols = ("id","name","price","stock","sales","discount")
        tree = ttk.Treeview(parent, columns=cols, show="headings", height=16)
        for c in cols: tree.heading(c, text=c.upper()); tree.column(c, width=110)
        tree.pack(fill="both", expand=True, pady=4)
        for p in self.db.all("SELECT * FROM products ORDER BY id"):
            tree.insert("", "end", values=(p["id"], p["name"], p["price"], p["stock"], p["sales"], p["discount"]))
        def on_double(_):
            sel = tree.selection()
            if not sel: return
            self.admin_edit_product(int(tree.item(sel[0])["values"][0])); self.show_view("admin")
        tree.bind("<Double-1>", on_double)
        bf = tk.Frame(parent, bg=self.C("bg")); bf.pack(fill="x")
        def dele():
            sel = tree.selection()
            if not sel: return
            if messagebox.askyesno("David Shop", self.t("confirm_delete")):
                self.db.q("DELETE FROM products WHERE id=?", (int(tree.item(sel[0])["values"][0]),))
                self.show_view("admin")
        tk.Button(bf, text="🗑 "+self.t("delete"), command=dele,
                  bg=self.C("card"), fg=self.C("danger"), bd=0).pack(side="left")

    def admin_new_product(self): self.admin_product_dialog()
    def admin_edit_product(self, pid): self.admin_product_dialog(pid)

    def admin_product_dialog(self, pid=None):
        p = dict(self.db.one("SELECT * FROM products WHERE id=?", (pid,))) if pid else None
        win = tk.Toplevel(self.root); win.title(self.t("products")); win.geometry("420x480")
        win.configure(bg=self.C("bg")); entries = {}
        for k in ["name","description","price","stock","icon","discount","sales","category_id"]:
            tk.Label(win, text=k.capitalize(), bg=self.C("bg"), fg=self.C("fg")).pack(anchor="w", padx=16, pady=(6,0))
            e = tk.Entry(win, width=40); e.pack(padx=16)
            if p: e.insert(0, str(p[k]))
            entries[k] = e
        def save():
            try:
                v = {k: entries[k].get().strip() for k in entries}
                if not v["name"]: return
                if pid:
                    self.db.q("""UPDATE products SET name=?,description=?,price=?,stock=?,icon=?,discount=?,sales=?,category_id=?
                                 WHERE id=?""",
                              (v["name"], v["description"], float(v["price"] or 0), int(v["stock"] or 0),
                               v["icon"] or "📦", int(v["discount"] or 0), int(v["sales"] or 0),
                               int(v["category_id"] or 1), pid))
                else:
                    self.db.q("""INSERT INTO products(name,description,price,stock,icon,discount,sales,category_id)
                                 VALUES(?,?,?,?,?,?,?,?)""",
                              (v["name"], v["description"], float(v["price"] or 0), int(v["stock"] or 0),
                               v["icon"] or "📦", int(v["discount"] or 0), int(v["sales"] or 0),
                               int(v["category_id"] or 1)))
                win.destroy(); self.show_view("admin")
            except Exception as e: messagebox.showerror("David Shop", str(e))
        tk.Button(win, text="💾 "+self.t("save"), command=save,
                  bg=self.C("primary"), fg="white", bd=0, padx=16, pady=8).pack(pady=12)

    def admin_users_table(self, parent):
        cols = ("id","username","email","avatar","is_admin","created_at")
        tree = ttk.Treeview(parent, columns=cols, show="headings", height=16)
        for c in cols: tree.heading(c, text=c.upper()); tree.column(c, width=120)
        tree.pack(fill="both", expand=True, padx=4, pady=4)
        for u in self.db.all("SELECT * FROM users ORDER BY id"):
            tree.insert("", "end", values=(u["id"], u["username"], u["email"], u["avatar"],
                                           u["is_admin"], u["created_at"]))
        bf = tk.Frame(parent, bg=self.C("bg")); bf.pack(fill="x")
        def dele():
            sel = tree.selection()
            if not sel: return
            uid = int(tree.item(sel[0])["values"][0])
            if uid == self.user["id"]:
                messagebox.showwarning("David Shop", "No puedes eliminar tu propia cuenta"); return
            if messagebox.askyesno("David Shop", self.t("confirm_delete")):
                self.db.q("DELETE FROM users WHERE id=?", (uid,)); self.show_view("admin")
        def toggle_admin():
            sel = tree.selection()
            if not sel: return
            uid = int(tree.item(sel[0])["values"][0])
            cur = self.db.one("SELECT is_admin FROM users WHERE id=?", (uid,))["is_admin"]
            self.db.q("UPDATE users SET is_admin=? WHERE id=?", (0 if cur else 1, uid))
            self.show_view("admin")
        tk.Button(bf, text="🗑 "+self.t("delete"), command=dele,
                  bg=self.C("card"), fg=self.C("danger"), bd=0).pack(side="left")
        tk.Button(bf, text="🛡 Toggle Admin", command=toggle_admin,
                  bg=self.C("card"), fg=self.C("fg"), bd=0).pack(side="left", padx=6)

    def admin_orders_table(self, parent):
        top = tk.Frame(parent, bg=self.C("bg")); top.pack(fill="x", pady=4)
        tk.Button(top, text="📤 "+self.t("export_csv"), command=self.export_orders_csv,
                  bg=self.C("primary"), fg="white", bd=0, padx=10).pack(side="left")
        cols = ("id","user_id","subtotal","tax","discount","total","coupon","created_at")
        tree = ttk.Treeview(parent, columns=cols, show="headings", height=16)
        for c in cols: tree.heading(c, text=c.upper()); tree.column(c, width=110)
        tree.pack(fill="both", expand=True, padx=4, pady=4)
        for o in self.db.all("SELECT * FROM orders ORDER BY id DESC"):
            tree.insert("", "end", values=tuple(o))

    def export_orders_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")],
                                            initialfile="orders.csv")
        if not path: return
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["id","user_id","subtotal","tax","discount","total","coupon","created_at"])
            for o in self.db.all("SELECT * FROM orders"): w.writerow(tuple(o))
        toast(self.root, "📤 CSV exportado", "ok")

    def admin_coupons_tab(self, parent):
        tk.Label(parent, text="Cupones disponibles:", bg=self.C("bg"), fg=self.C("fg")).pack(anchor="w", padx=8, pady=6)
        for c, v in COUPONS.items():
            tk.Label(parent, text=f"  • {c}  →  -{v}%", bg=self.C("bg"), fg=self.C("fg")).pack(anchor="w", padx=8)
        tk.Label(parent, text="ℹ Los productos gratuitos no usan cupones ni carrito.",
                 bg=self.C("bg"), fg=self.C("success"), font=("Segoe UI",9,"italic")).pack(anchor="w", padx=8, pady=8)

    def admin_tools_tab(self, parent):
        tk.Button(parent, text="💾 "+self.t("backup"), command=self.backup_db,
                  bg=self.C("primary"), fg="white", bd=0, padx=14, pady=8).pack(pady=6, anchor="w", padx=8)
        tk.Button(parent, text="📥 "+self.t("restore"), command=self.restore_db,
                  bg=self.C("accent"), fg="white", bd=0, padx=14, pady=8).pack(pady=6, anchor="w", padx=8)
        tk.Button(parent, text=self.t("open_folder_btn")+" (Downloads)",
                  command=lambda: open_folder(DOWNLOADS_FOLDER),
                  bg=self.C("card"), fg=self.C("fg"), bd=0, padx=14, pady=8).pack(pady=6, anchor="w", padx=8)
        tk.Label(parent, text="— "+self.t("activity")+" —", bg=self.C("bg"), fg=self.C("fg"),
                 font=("Segoe UI",11,"bold")).pack(anchor="w", padx=8, pady=(12,4))
        for a in self.db.all("SELECT * FROM activity ORDER BY id DESC LIMIT 30"):
            tk.Label(parent, text=f"  [{a['created_at']}] {a['text']}",
                     bg=self.C("bg"), fg=self.C("muted"), font=("Segoe UI",8), anchor="w").pack(fill="x", padx=8)

    def backup_db(self):
        path = filedialog.asksaveasfilename(defaultextension=".db", initialfile="david_shop_backup.db")
        if not path: return
        shutil.copy(DB_PATH, path); toast(self.root, "💾 Backup guardado", "ok")

    def restore_db(self):
        path = filedialog.askopenfilename(filetypes=[("DB","*.db")])
        if not path: return
        if not messagebox.askyesno("David Shop", "¿Reemplazar la base de datos?"): return
        self.db.conn.close(); shutil.copy(path, DB_PATH); self.db = DB()
        toast(self.root, "📥 Restaurado", "ok"); self.show_view("admin")

    def view_about(self):
        wrap = tk.Frame(self.content, bg=self.C("bg")); wrap.pack(expand=True)
        LogoCanvas(wrap, width=180, bg=self.C("bg")).pack(pady=(20,4))
        tk.Label(wrap, text="David Shop", font=("Segoe UI",22,"bold"),
                 bg=self.C("bg"), fg=self.C("fg")).pack()
        tk.Label(wrap, text="v4.1 — Tienda 100% Legítima 😉", bg=self.C("bg"),
                 fg=self.C("muted")).pack(pady=4)
        tk.Label(wrap, text="1000 productos: 300 Steam + 300 Epic + 400 entre HTML, Apps, Utilidades y Subs",
                 bg=self.C("bg"), fg=self.C("muted"), font=("Segoe UI",10)).pack(pady=8)
        tk.Label(wrap, text="🎮 Los juegos HTML se descargan y son jugables de verdad",
                 bg=self.C("bg"), fg=self.C("success"), font=("Segoe UI",10,"italic")).pack(pady=2)
        tk.Label(wrap, text=f"📁 Descargas reales en: {DOWNLOADS_FOLDER}",
                 bg=self.C("bg"), fg=self.C("accent"), font=("Segoe UI",10,"italic")).pack(pady=2)
        tk.Label(wrap, text="Python + Tkinter + SQLite", bg=self.C("bg"),
                 fg=self.C("muted"), font=("Segoe UI",10)).pack(pady=6)
        tk.Label(wrap, text="Cupones activos: " + ", ".join(COUPONS.keys()),
                 bg=self.C("bg"), fg=self.C("accent")).pack(pady=6)

    def global_search(self):
        self.last_search = self.search_entry.get().strip()
        self.page = 0; self.last_cat = 0; self.last_min = 0.0; self.last_max = 10000.0
        self.last_instock = False; self.last_sort = "sort_sales"
        self.show_view("catalog")

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = DavidShop(root)
    root.mainloop()
