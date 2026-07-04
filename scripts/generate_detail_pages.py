#!/usr/bin/env python3
"""Generates the 8 static travel-diary detail pages (Simplified Chinese)
from one template + data dict. Each entry is a real photo, illustrated
afterward — captions stay observational (what's visible in frame) rather
than invented backstory. Re-run after editing TRIPS below to regenerate."""
import os

ROOT = "/Volumes/Raid16/Claude/code/漫画作品展示网站"

TRIPS = [
    dict(
        slug="paris", title="巴黎", vol="卷一", date="2026", place="法国·巴黎",
        deck="在「爱之路」街角比出的胜利手势,埃菲尔铁塔就在两个街区之外。",
        notes=[
            "十字路口一角是可颂摊,另一角是 Café de Paris——抬头就能看见铁塔在下午的阳光里。",
        ],
        alt="插画风格的巴黎街景,画面中有埃菲尔铁塔、街角咖啡馆与比着胜利手势的人",
    ),
    dict(
        slug="canada-cup", title="加拿大杯", vol="卷二", date="2026", place="市中心广场",
        deck="遮阳帽、墨镜,还有比赛日里挤满星巴克门口的一片红色人潮。",
        notes=[
            "上午还没到中午,广场已经被红白两色占满——球衣、国旗,队伍长到快看不见咖啡店的门。",
        ],
        alt="插画风格的自拍,两人穿着加拿大队球衣站在星巴克门口的比赛日人群中",
    ),
    dict(
        slug="old-town", title="老城", vol="卷三", date="2026", place="老城区",
        deck="头顶的油纸伞,一只绣花包摆过挂满灯笼的老铺子。",
        notes=[
            "老城区的一条小巷——悬挂的油纸伞、系着流苏的纪念品,还有一条绿裙子,始终没能被拍下第二张同款的照片。",
        ],
        alt="插画风格的老城小巷,挂着油纸伞、灯笼与各式店铺招牌",
    ),
    dict(
        slug="match-day", title="赛场日", vol="卷四", date="2026", place="市中心球场",
        deck="还是那两件红色球衣,还是那片草坪,球却怎么也不肯乖乖听话。",
        notes=[
            "球场边草坪上的中场小对抗——球衣和早上那张照片里一模一样,脚下功夫明显差了不少。",
        ],
        alt="两人穿着加拿大球衣在草坪上踢球的插画",
    ),
    dict(
        slug="run-van-marathon", title="温哥华马拉松", vol="卷五", date="2026", place="温哥华",
        deck="奖牌还带着体温,一整队人挤在 FINISH 横幅下咧嘴笑。",
        notes=[
            "所有一起冲过终点线的人,举着那张手写的名单——从出发时的名字,一路举到了终点。",
        ],
        alt="插画风格的温哥华马拉松终点合影,众人戴着奖牌站在 FINISH 横幅下",
    ),
    dict(
        slug="alaska", title="阿拉斯加", vol="卷六", date="2026", place="阿拉斯加",
        deck="比想象中高两层楼的邮轮,还有一只格外友好的卡通虎鲸。",
        notes=[
            "邮轮停靠在阿拉斯加探险码头,海鸥在头顶盘旋,水面平静得能看清船身的倒影被慢慢揉碎又拼回去。",
        ],
        alt="插画风格的阿拉斯加码头场景,画面中有邮轮、海鸥与山脉",
    ),
    dict(
        slug="yixin-chicken", title="又记壹心鸡", vol="卷七", date="2026", place="又记壹心鸡",
        deck="咖啡还没上桌,手指已经点在了菜单的第一页。",
        notes=[
            "又记壹心鸡的窗边桌——门口挂着灯笼,菜单上的招牌整鸡,在茶还没泡开之前就已经点好了。",
        ],
        alt="插画风格的又记壹心鸡餐厅场景,画面中有菜单、咖啡杯与红灯笼",
    ),
    dict(
        slug="amsterdam", title="阿姆斯特丹", vol="卷八", date="2026", place="阿姆斯特丹",
        deck="靠窗的位子,一辆有轨电车驶过,还有一盘好看到舍不得快点吃完的早餐。",
        notes=[
            "Café de Amsterdam,上午——一份煎蛋卷,窗外电车缓缓驶过,没有急着要去别的地方。",
        ],
        alt="插画风格的阿姆斯特丹咖啡馆窗边场景,窗外有电车驶过,桌上摆着早餐",
    ),
]


def find(slug):
    for i, t in enumerate(TRIPS):
        if t["slug"] == slug:
            return i
    return -1


PAGE_TMPL = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — HAZE 旅行日记</title>
<meta name="description" content="{deck}">
<link rel="canonical" href="{slug}.html">
<meta property="og:type" content="article">
<meta property="og:title" content="{title} — HAZE 旅行日记">
<meta property="og:description" content="{deck}">
<meta property="og:image" content="../assets/covers/{slug}.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="../site.webmanifest">
<meta name="theme-color" content="#FFFFFF">
<link rel="stylesheet" href="../css/style.css">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Photograph",
  "name": "{title}",
  "dateCreated": "{date}",
  "author": {{ "@type": "Person", "name": "HAZE" }},
  "contentLocation": "{place}",
  "image": "../assets/covers/{slug}.jpg",
  "url": "{slug}.html"
}}
</script>
</head>
<body>
  <a href="#main" class="skip-link">跳至内容</a>

  <div class="loader" data-loader aria-hidden="true">
    <div class="loader-mark">HAZE</div>
    <div class="loader-track"><div class="loader-progress" data-loader-progress></div></div>
  </div>

  <div class="scroll-progress" data-scroll-progress></div>

  <nav class="nav" data-nav aria-label="主导航">
    <a href="../index.html" class="nav-mark">HAZE</a>
    <button class="nav-toggle" data-nav-toggle aria-expanded="false" aria-controls="nav-links">菜单</button>
    <ul class="nav-links" data-nav-links id="nav-links">
      <li><a href="../work.html" class="is-active">作品</a></li>
      <li><a href="../about.html">关于</a></li>
      <li><a href="../journal.html">日记</a></li>
      <li><a href="../contact.html">联系</a></li>
    </ul>
  </nav>

  <main id="main">
    <header class="detail-hero-content">
      <div class="container">
        <p class="type-eyebrow reveal">{vol}</p>
        <h1 class="type-display mt-3 reveal reveal-1">{title}</h1>
      </div>
    </header>

    <section class="detail-hero reveal">
      <img loading="eager" decoding="async" src="../assets/covers/{slug}.jpg" alt="{alt}">
    </section>

    <div class="detail-meta-row reveal">
      <div><span class="type-meta">日期</span><span class="type-h3">{date}</span></div>
      <div><span class="type-meta">地点</span><span class="type-h3">{place}</span></div>
      <div><span class="type-meta">卷号</span><span class="type-h3">{vol}</span></div>
    </div>

    <article class="detail-body">
      <div class="container prose">
        <p class="type-body reveal">{deck}</p>
        {notes_html}
      </div>
    </article>

    <nav class="container detail-nav" aria-label="更多记录">
      <a href="{prev_slug}.html" class="link-underline" data-cursor-hover>
        <span class="type-meta dir">← 上一篇</span>
        <span class="type-h3">{prev_title}</span>
      </a>
      <a href="{next_slug}.html" class="link-underline" data-cursor-hover>
        <span class="type-meta dir next-title">下一篇 →</span>
        <span class="type-h3 next-title">{next_title}</span>
      </a>
    </nav>
  </main>

  <footer class="footer">
    <div class="container">
      <p class="footer-line reveal">感谢阅读。</p>
      <div class="footer-meta reveal reveal-1">
        <span>© 2026 HAZE</span>
        <a href="../work.html" class="link-underline">作品</a>
        <a href="../about.html" class="link-underline">关于</a>
        <a href="../contact.html" class="link-underline">联系</a>
      </div>
    </div>
  </footer>

  <script src="../js/main.js"></script>
</body>
</html>
"""


def main():
    n = len(TRIPS)
    for i, t in enumerate(TRIPS):
        prev_t = TRIPS[(i - 1) % n]
        next_t = TRIPS[(i + 1) % n]
        notes_html = "\n        ".join(f'<p class="type-body reveal">{p}</p>' for p in t["notes"])
        html = PAGE_TMPL.format(
            title=t["title"], slug=t["slug"], date=t["date"], place=t["place"],
            vol=t["vol"], deck=t["deck"], notes_html=notes_html, alt=t["alt"],
            prev_slug=prev_t["slug"], prev_title=prev_t["title"],
            next_slug=next_t["slug"], next_title=next_t["title"],
        )
        out_path = os.path.join(ROOT, "work", f"{t['slug']}.html")
        with open(out_path, "w") as f:
            f.write(html)
        print("wrote", out_path)


if __name__ == "__main__":
    main()
