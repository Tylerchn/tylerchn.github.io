"""Regenerate both language pages from the shared publication list."""
from html import escape as h
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PAPERS = json.loads((ROOT / 'data/publications.json').read_text())
SITE = 'https://tylerchn.github.io/'
EMAIL = 'tang_fengliang@tju.edu.cn'
ORCID = 'https://orcid.org/0000-0001-6671-1217'
RG = 'https://www.researchgate.net/profile/Fengliang_Tang2/research'
GITHUB = 'https://github.com/Tylerchn'
PLATFORM = SITE + 'BTH-Flood-Disaster-Resilience/'
CV = 'assets/fengliang-tang-cv.pdf'

def link(url, label, attrs=''):
    return f'<a href="{h(url, quote=True)}"{attrs}>{h(label)}</a>'

def publication(p, en, featured=False):
    lang = p['language']
    marked = []
    for name in p['authors']:
        role = p['role']
        person = name in ('Tang, F.', '唐缝梁')
        marker = ''
        if person and role != 'Co-author':
            detail = {
                'First author': ('第一作者', 'First author', '★'),
                'Corresponding author': ('通讯作者', 'Corresponding author', '✉'),
                'Co-corresponding author': ('共同通讯作者', 'Co-corresponding author', '✉'),
            }[role]
            marker = f' <span class="author-mark" title="{detail[int(en)]}"><span aria-hidden="true">{detail[2]}</span><span class="sr-only"> ({detail[int(en)]})</span></span>'
        marked.append(f'<strong>{h(name)}</strong>{marker}' if person else h(name))
    separator = '、' if lang == 'zh-CN' else '; '
    attrs = f' lang="{lang}"'
    labels = {'doi':'DOI', 'program': 'Conference program' if en else '会议日程', 'source':'Publisher' if en else '出版社'}
    source = link(p['url'], labels[p['link_label']], ' class="paper-link"') if p['url'] else ''
    detail = ', ' + h(p['details']) if p['details'] else ''
    title = h(p['title'])
    if p['url'] and p['link_label']=='doi':
        title=link(p['url'],p['title'])
    title_tag='h3' if featured else 'h4'
    anchor='' if featured else f' id="{p["id"]}"'
    return f'''<li class="paper"{anchor}><{title_tag}{attrs}>{title}</{title_tag}>
      <p class="authors"{attrs}>{separator.join(marked)}</p>
      <div class="paper-meta"><span><cite{attrs}>{h(p['venue'])}</cite>{detail} · {p['year']}</span>{source}</div></li>'''

def page(en):
    t = lambda zh, eng: eng if en else zh
    lang=t('zh-CN','en')
    name=t('唐缝梁','Fengliang Tang')
    other=t('Fengliang Tang','唐缝梁')
    title=t('唐缝梁｜城市（群）韧性','Fengliang Tang | Urban and Regional Resilience')
    description=t('唐缝梁的学术主页。研究城市群系统韧性、交通出行公平、洪涝灾害韧性与 AI 赋能城市规划。',
        'Fengliang Tang studies urban and regional resilience, mobility equity, flood resilience, and AI for urban planning.')
    url=SITE+t('','en/')
    prefix=t('./','../')
    figure_alt=t('京津冀 129 个汇水单元的洪涝风险分布','Flood risk across 129 catchments in Beijing–Tianjin–Hebei')
    affiliation=t('天津大学建筑学院 · 城乡规划系','Department of Urban and Rural Planning · School of Architecture, Tianjin University')
    intro=t(
        '我关注城市（群）作为复杂巨系统中的韧性议题，包括但不限于系统韧性评估、交通出行公平、洪涝灾害韧性等。我的研究结合空间数据、网络分析与可解释机器学习，识别风险与服务机会的空间差异。近期工作以京津冀为例，探索区域洪涝风险诊断与灾后协同恢复。',
        'I study resilience in cities and urban agglomerations as complex systems, with a focus on system resilience assessment, mobility equity, and flood resilience. I combine geospatial data, network analysis, and interpretable machine learning to investigate where risks and access to services differ. My recent work uses Beijing–Tianjin–Hebei to examine regional flood risk and coordinated recovery.')
    cards = [
        ('resilience',t('城市与区域韧性','Urban and Regional Resilience'),t('评估城市群系统韧性与洪涝风险，识别跨地区协同恢复的重点。','I assess regional resilience and flood risk to identify priorities for coordinated recovery.'),'10.1016/j.uclim.2025.102436'),
        ('mobility',t('出行与空间公平','Mobility and Spatial Equity'),t('研究街道环境与交通网络如何影响共享出行机会的空间分布。','I examine how streets and transport networks shape access to shared mobility.'),'10.1016/j.tbs.2026.101284'),
        ('geoai',t('AI赋能城市规划','AI for Urban Planning'),t('结合街景、遥感与可解释机器学习，为街道评估和规划决策提供依据。','I use street imagery, remote sensing, and interpretable machine learning to inform street assessment and planning decisions.'),'10.3390/rs16193661'),
    ]
    card_html=''.join(f'<article class="theme" id="project-{key}"><h3>{heading}</h3><p>{copy}</p>{link("https://doi.org/"+doi,t("相关论文 ↗","Related paper ↗"))}</article>' for key,heading,copy,doi in cards)
    featured=sorted((p for p in PAPERS if p.get('featured')),key=lambda p:p['featured'])
    papers=[p for p in PAPERS if p['kind']!='report']
    first=sum(p['role']=='First author' for p in papers)
    corr=sum(p['role'] in ('Corresponding author','Co-corresponding author') for p in papers)
    summary=t(f'{len(papers)} 篇论文 · 第一作者 {first} 篇 · 通讯作者 {corr} 篇',
              f'{len(papers)} papers · {first} first-author · {corr} corresponding-author')
    years=sorted({p['year'] for p in PAPERS},reverse=True)
    bibliography=''.join(f'<section class="year-group" aria-labelledby="year-{year}"><h3 id="year-{year}">{year}</h3><ol class="papers">{"" .join(publication(p,en) for p in PAPERS if p["year"]==year)}</ol></section>' for year in years)
    person={
        '@context':'https://schema.org','@type':'Person','name':name,'alternateName':other,
        'url':url,'email':'mailto:'+EMAIL,'affiliation':{'@type':'CollegeOrUniversity','name':t('天津大学','Tianjin University'),'url':'https://www.tju.edu.cn/'},
        'sameAs':[ORCID,RG,GITHUB],
        'knowsAbout':[heading for _,heading,_,_ in cards],
    }
    contacts=' '.join((link('mailto:'+EMAIL,EMAIL), link(ORCID,'ORCID'),link(RG,'ResearchGate'),link(prefix+CV,t('下载学术简历（PDF）','Download CV (PDF)'), ' class="button" download')))
    nav=''.join(link('#'+anchor,label) for anchor,label in [('publications',t('论文','Publications')),('featured',t('项目','Projects')),('cv',t('简历','CV'))])
    cover_credit=link(PLATFORM,t('数据来源：京津冀城市群洪涝韧性监测平台','Data: Beijing–Tianjin–Hebei Flood Resilience Dashboard'))
    selected_html=''.join(publication(p,en,True) for p in featured)
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="zh-CN" href="{SITE}">
<link rel="alternate" hreflang="en" href="{SITE}en/">
<link rel="alternate" hreflang="x-default" href="{SITE}">
<meta property="og:type" content="profile">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{t('zh_CN','en_US')}">
<meta property="og:image" content="{SITE}assets/bth-share.png">
<meta property="og:image:width" content="1120">
<meta property="og:image:height" content="780">
<meta property="og:image:alt" content="{figure_alt}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(person,ensure_ascii=False).replace('<',chr(92)+'u003c')}</script>
<link rel="stylesheet" href="{prefix}style.css">
<script src="{prefix}main.js" defer></script>
</head>
<body id="top">
<a class="skip" href="#main">{t('跳到正文','Skip to content')}</a>
<header class="masthead"><div class="wrap">
<a class="brand" href="#top">{name}</a>
<nav aria-label="{t('主导航','Main navigation')}">{nav}</nav>
<a class="language" href="{t('./en/','../')}" lang="{t('en','zh-CN')}" hreflang="{t('en','zh-CN')}">{t('English','中文')}</a>
</div></header>
<main class="wrap" id="main">
<section class="intro" aria-labelledby="name">
<div><h1 id="name">{name}</h1>
<p class="alternate-name" lang="{t('en','zh-CN')}">{other}</p>
<p class="affiliation">{affiliation}</p>
<p class="bio">{intro}</p>
<div class="contact-links">{contacts}</div></div>
<figure class="cover"><img src="{prefix}assets/bth-risk.svg" width="560" height="390" alt="{figure_alt}">
<figcaption>{t('京津冀洪涝风险 · 129 个汇水单元','Flood risk in Beijing–Tianjin–Hebei · 129 catchments')}<br>{cover_credit}</figcaption></figure>
</section>
<section id="research" class="section"><h2>{t('研究方向','Research interests')}</h2><div class="theme-grid">{card_html}</div></section>
<section id="selected" class="section"><div class="section-head"><h2>{t('代表作','Selected publications')}</h2>{link('#publications',t('浏览全部成果 ↓','Browse all publications ↓'))}</div>
<ol class="papers selected">{selected_html}</ol></section>
<section id="publications" class="section"><h2>{t('全部学术成果','All publications')}</h2>
<p class="summary" id="publication-stats">{summary}</p>
<p class="publication-note">{t('论文含期刊与会议论文。通讯作者含共同通讯。★ 第一作者，✉ 通讯或共同通讯作者。',
'Papers include journal articles and conference papers. ★ First author. ✉ Corresponding or co-corresponding author.')}</p>
{bibliography}</section>
<section id="featured" class="section"><h2>{t('项目与平台','Projects and platforms')}</h2>
<article class="project">
<img src="{prefix}assets/bth-recovery.svg" alt="{t('平台模拟的灾后恢复指数序列','Simulated post-disaster recovery index from the dashboard')}" width="560" height="390" loading="lazy">
<div><h3>{t('京津冀城市群洪涝韧性监测平台','Beijing–Tianjin–Hebei Flood Resilience Dashboard')}</h3>
<p>{t('平台整合区域韧性评估、洪涝风险诊断和灾后协同恢复模拟。预览图展示平台公开的灾后恢复指数序列。','The dashboard brings together regional resilience assessment, flood-risk diagnosis, and coordinated recovery. The preview shows a simulated recovery index from the published dashboard data.')}</p>
{link(PLATFORM,t('打开交互平台 ↗','Open the interactive dashboard ↗'),' class="button"')}</div></article></section>
<section id="cv" class="section"><div class="section-head"><h2>{t('教育与学术服务','Education and academic service')}</h2>{link(prefix+CV,t('下载 CV（PDF）','Download CV (PDF)'),' download')}</div>
<div class="academic-grid">
<div><h3>{t('教育经历','Education')}</h3><ul class="plain">
<li><strong>{t('天津大学','Tianjin University')}</strong><br>{t('建筑学院，资源与环境工程博士阶段研究 · 2021 年起','School of Architecture, doctoral studies in Resources and Environment · Since 2021')}</li>
<li><strong>{t('伦敦大学学院','University College London')}</strong><br>{t('跨学科城市设计研究硕士 · 2019–2020','MRes in Interdisciplinary Urban Design · 2019–2020')}</li></ul></div>
<div><h3>{t('科研项目与同行评议','Research projects and peer review')}</h3><p>{t('参与国家重点研发计划的城市（群）系统韧性功能协同恢复研究，以及天津市科技计划的地铁站域更新研究。','Contributor to a National Key R&D Program project on coordinated recovery in urban systems and a Tianjin research project on metro station-area regeneration.')}</p>
<p>{t('曾为以下期刊审稿','Journal reviewing includes')} <cite>Sustainable Cities and Society</cite>{t('、',', ')}<cite>Habitat International</cite>{t('、',', ')}<cite>Building and Environment</cite> {t('及','and')} <cite>Journal of Transport Geography</cite>.</p></div>
<div><h3>{t('会议报告','Conference presentations')}</h3><ul class="plain">
<li>{t('第 16 届国际中国规划学会年会（IACP，2022）','16th International Association for China Planning Annual Conference (2022)')}</li>
<li>{t('2022 中国城市规划年会 · 社区体检方法与应用','2022 China Annual National Planning Conference · Community assessment methods and application')}</li></ul></div>
<div><h3>{t('研究方法与工具','Methods and tools')}</h3><p>{t('GIS 空间分析、Python、空间网络分析、可解释机器学习。','GIS, Python, spatial network analysis, and interpretable machine learning.')}</p></div>
</div></section>
</main>
<footer class="footer" id="contact"><div class="wrap"><p><strong>{name}</strong><br>{affiliation}</p>
<nav aria-label="{t('联系方式','Contact links')}">{link('mailto:'+EMAIL,EMAIL)} {link(ORCID,'ORCID')} {link(RG,'ResearchGate')} {link(GITHUB,'GitHub')}</nav></div></footer>
</body>
</html>
'''

if __name__ == '__main__':
    (ROOT/'en').mkdir(exist_ok=True)
    (ROOT/'index.html').write_text(page(False),encoding='utf-8')
    (ROOT/'en/index.html').write_text(page(True),encoding='utf-8')
