from __future__ import annotations
import json, re, shutil, subprocess, html
from pathlib import Path
from datetime import datetime, timezone
from PIL import Image, ImageDraw, ImageFont, ImageChops

variant=''; pkg=Path('.'); fig=Path('.'); va=Path('.'); NOW=''

def configure(v,p):
    global variant,pkg,fig,va,NOW
    variant=v; pkg=Path(p); fig=pkg/'assets'/'figures'; va=pkg/'visual'/'assets'
    fig.mkdir(parents=True,exist_ok=True); va.mkdir(parents=True,exist_ok=True)
    NOW=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')

def readj(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def writej(p,obj): Path(p).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def add_unique(seq,value):
    if value not in seq: seq.append(value)

def upsert_before(path,start,end,block,marker):
    text=Path(path).read_text(encoding='utf-8')
    if start in text and end in text:
        a=text.index(start); b=text.index(end,a)+len(end); text=text[:a]+block+text[b:]
    else:
        if marker not in text: raise SystemExit(f'marker not found in {path}: {marker}')
        text=text.replace(marker,block+'\n\n'+marker,1)
    Path(path).write_text(text,encoding='utf-8')

def font(size,bold=False):
    candidates=[('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'),('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')]
    for p in candidates:
        if Path(p).exists(): return ImageFont.truetype(p,size=size)
    return ImageFont.load_default()

def wrap(draw,text,fnt,width_px):
    cjk=any('\u4e00'<=c<='\u9fff' for c in text); words=list(text) if cjk else text.split(' '); sep='' if cjk else ' '
    lines=[]; cur=''
    for w in words:
        trial=(cur+sep+w) if cur else w
        if draw.textbbox((0,0),trial,font=fnt)[2]<=width_px: cur=trial
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

def card(draw,box,title,body,tag=None):
    x0,y0,x1,y1=box; draw.rounded_rectangle(box,radius=22,fill='white',outline='#cbd5e1',width=3); draw.rectangle((x0,y0,x1,y0+12),fill='#0f766e'); draw.text((x0+24,y0+28),title,font=font(33,True),fill='#172033')
    if tag: draw.text((x1-210,y0+31),tag,font=font(18,True),fill='#0f766e')
    yy=y0+82
    for line in wrap(draw,body,font(21),x1-x0-48): draw.text((x0+24,yy),line,font=font(21),fill='#475569'); yy+=32

def save_png(path,title,subtitle,cards,footer):
    im=Image.new('RGB',(1800,1100),'#f8fafc'); d=ImageDraw.Draw(im); d.text((70,52),title,font=font(54,True),fill='#111827'); d.text((72,124),subtitle,font=font(24),fill='#64748b')
    n=len(cards); gap=28; x0=70; x1=1730; y0=205; y1=980; w=(x1-x0-gap*(n-1))/n
    for i,(t,b,tag) in enumerate(cards): xa=int(x0+i*(w+gap)); card(d,(xa,y0,int(xa+w),y1),t,b,tag)
    d.text((72,1020),footer,font=font(18),fill='#64748b'); im.save(path,optimize=True)

def svg_shell(title,subtitle,columns,footer):
    W,H=1600,900; colw=(W-120-(len(columns)-1)*24)/len(columns)
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">','<rect width="1600" height="900" fill="#f8fafc"/>','<style>text{font-family:"Noto Sans CJK SC","Noto Sans",Arial,sans-serif}.t{font-weight:700;fill:#111827}.s{fill:#64748b}.h{font-weight:700;fill:#0f766e}.b{fill:#334155}</style>',f'<text x="60" y="72" font-size="42" class="t">{html.escape(title)}</text>',f'<text x="60" y="112" font-size="20" class="s">{html.escape(subtitle)}</text>']
    for i,(head,lines,accent) in enumerate(columns):
        x=60+i*(colw+24); y=170; parts += [f'<rect x="{x}" y="{y}" width="{colw}" height="620" rx="24" fill="white" stroke="#cbd5e1" stroke-width="2"/>',f'<rect x="{x}" y="{y}" width="{colw}" height="14" rx="7" fill="{accent}"/>',f'<text x="{x+28}" y="{y+62}" font-size="27" class="t">{html.escape(head)}</text>']; yy=y+118
        for label,desc in lines:
            parts += [f'<circle cx="{x+36}" cy="{yy-7}" r="8" fill="{accent}"/>',f'<text x="{x+58}" y="{yy}" font-size="19" class="h">{html.escape(label)}</text>',f'<text x="{x+58}" y="{yy+31}" font-size="16" class="b">{html.escape(desc)}</text>']; yy+=92
    parts += [f'<text x="60" y="848" font-size="16" class="s">{html.escape(footer)}</text>','</svg>']; return ''.join(parts)

def manifest_add(path,role,language=None,translation_of=None):
    mp=pkg/'manifest.json'; m=readj(mp); files=m.setdefault('files',[])
    if path not in {x.get('path') for x in files}:
        rec={'path':path,'role':role,'required':False,'sha256':'0'*64};
        if language: rec['language']=language
        if translation_of: rec['translation_of']=translation_of
        files.append(rec)
    m['generated_at']=NOW; claim=m.setdefault('validation_claim',{}); claim['self_checked']=False; claim['known_blockers']=[]; writej(mp,m)

def add_assumption(rec):
    p=pkg/'assumptions.json'; x=readj(p); x['assumptions']=[a for a in x.get('assumptions',[]) if a.get('id')!=rec['id']]+[rec]; writej(p,x)
def add_source(rec):
    p=pkg/'sources.json'; x=readj(p); x['sources']=[a for a in x.get('sources',[]) if a.get('id')!=rec['id']]+[rec]; writej(p,x)
def add_metric(mid,rec):
    p=pkg/'metrics.json'; x=readj(p); x['metrics'][mid]=rec; writej(p,x)

def update_matrices(section,mids,sids=()):
    cp=pkg/'compliance_matrix.json'; c=readj(cp)
    for item in c.get('requirements',[]):
        if item.get('requirement_id','') in {'1.3.2','1.3.3','1.4.3','1.5.1.2','1.5.2.1','1.5.2.2','agent.3','agent.4','agent.6'}:
            add_unique(item.setdefault('report_sections',[]),section)
            for m in mids: add_unique(item.setdefault('metrics',[]),m)
            for s in sids: add_unique(item.setdefault('source_ids',[]),s)
    writej(cp,c)
    dp=pkg/'design_depth_matrix.json'; d=readj(dp); targets={'existing_conditions_diagnosis','overall_spatial_structure','traffic_rail_slow_parking','blue_green_public_space','key_area_detailed_design','phasing_implementation','development_intensity_controls','height_massing_character'}
    note=' v0.8 将六类接口收束为一个可逆 1:1 城市原型，并登记无现场数值的待测槽位。' if variant=='v0.8' else ' v0.9 用公开规划原件把道路节点、绿廊界面和强度参照转成明确设计响应，同时不把参照值外推为本案控制值。'
    for item in d.get('items',[]):
        if item.get('item_id') in targets:
            add_unique(item.setdefault('proposal_sections',[]),section)
            for m in mids: add_unique(item.setdefault('metric_refs',[]),m)
            for s in sids: add_unique(item.setdefault('source_ids',[]),s)
            if note.strip() not in item.get('evidence_summary_zh',''): item['evidence_summary_zh']=item.get('evidence_summary_zh','')+note
    writej(dp,d)

def copyright_note(text):
    p=pkg/'report/copyright_statement.md'; s=p.read_text(encoding='utf-8'); marker=f'## {variant} 新增资产 / New assets'
    if marker not in s: s += f'\n\n{marker}\n\n{text}\n'
    p.write_text(s,encoding='utf-8')

def changelog(block):
    p=pkg/'changelog.md'; s=p.read_text(encoding='utf-8'); marker=f'## {variant}'
    if marker not in s:
        lines=s.splitlines(); idx=1
        while idx<len(lines) and not lines[idx].startswith('## '): idx+=1
        lines[idx:idx]=['',block,'']; s='\n'.join(lines).rstrip()+'\n'
    p.write_text(s,encoding='utf-8')

def set_iteration():
    for name in ['proposal.md','proposal.en.md']:
        p=pkg/name; s=p.read_text(encoding='utf-8'); s=re.sub(r'iteration:\s*"v0\.\d+"',f'iteration: "{variant}"',s,count=1); p.write_text(s,encoding='utf-8')

def patch_visual(path,title,img_name,section_id,badge_text,en=False):
    s=Path(path).read_text(encoding='utf-8'); s=re.sub(r'v0\.7 design-first|v0\.8 prototype-first|v0\.9 reality-anchored',badge_text,s,count=1); start=f'<!-- {section_id}-START -->'; end=f'<!-- {section_id}-END -->'; subtitle='A reviewer-visible design claim, not a scoring dashboard. Ordinary city function remains the baseline.' if en else '评委先看到设计主张，不先看到评分仪表盘；普通城市功能仍是底座。'; block=f'{start}\n<section class="sheet" id="{section_id}"><div class="head"><h2>{title}</h2><div class="muted">{subtitle}</div></div><div class="body"><img class="evidence-img" src="../assets/figures/{img_name}" alt="{title}"></div></section>\n{end}'
    if start in s and end in s: a=s.index(start); b=s.index(end,a)+len(end); s=s[:a]+block+s[b:]
    else: s=s.replace('<main class="wrap">','<main class="wrap">\n'+block,1)
    Path(path).write_text(s,encoding='utf-8')

def finalize_package(pdf_first,visual_id,visual_title,visual_title_en,visual_img,badge):
    subprocess.run(['python3','scripts/render_proposal_html.py',str(pkg)],check=True)
    en_img=Path(visual_img).with_name(Path(visual_img).stem+'.en'+Path(visual_img).suffix).name
    patch_visual(pkg/'visual/index.html',visual_title,visual_img,visual_id,badge,False); patch_visual(pkg/'visual/index.en.html',visual_title_en,en_img,visual_id,badge,True)
    chrome=shutil.which('google-chrome') or shutil.which('google-chrome-stable') or shutil.which('chromium') or shutil.which('chromium-browser')
    if not chrome: raise SystemExit('Chrome/Chromium not found')
    tmp=Path('/tmp/jz-sprint-'+variant.replace('.','')); tmp.mkdir(parents=True,exist_ok=True)
    items=[pdf_first,('三处重点区空间剖面','Three key-area spatial sections','key-areas.png'),('三条日常城市链','Three everyday journeys','everyday-journey-sections.svg'),('AI 如何改变城市形态','How AI changes urban form','ai-urban-form-change.svg'),('总体范围与 C7 方法','Site overview and C7 method','site-overview.png'),('概念用地结构','Land-use structure','land-use-structure.png'),('慢行与蓝绿系统','Mobility and blue-green system','mobility-bluegreen.png'),('公共空间组件与导视','Public-space components and wayfinding','public-space-components-wayfinding.svg'),('三个旗舰试点协议','Three flagship pilot protocols','flagship-pilot-protocols.svg'),('实施资源与 RACI','Implementation resource and RACI','implementation-resource-raci.svg'),('指标与资料边界','Metrics and evidence limits','metrics-evidence.png')]
    def loc(name,en):
        p=Path(name); cand=p.with_name(p.stem+'.en'+p.suffix); return cand if en and (fig/cand).is_file() else p
    def uri(name,en): return (fig/loc(name,en)).resolve().as_uri()
    def page(cells,en,no,total):
        title=('JING-ZHANG CITY COMPLETENESS · '+variant if en else '京张城市完整度 · '+variant); footer=('Concept proposal · design-first · provisional geometry is not an official redline' if en else '概念建议 · 设计优先 · provisional geometry 不是官方红线'); figs=[]
        for zh,eng,name in cells: figs.append(f'<figure><img src="{uri(name,en)}"><figcaption>{html.escape(eng if en else zh)}</figcaption></figure>')
        cls='one' if len(cells)==1 else ('six' if len(cells)>=5 else 'two'); return f'<section><header><b>{html.escape(title)}</b><span>{no}/{total}</span></header><div class="grid {cls}">{"".join(figs)}</div><footer>{html.escape(footer)}</footer></section>'
    def doc(pages,en,size):
        sec=''.join(page(x,en,i+1,len(pages)) for i,x in enumerate(pages)); height='277mm' if size=='A3' else '827mm'; return f'''<!doctype html><html><head><meta charset="utf-8"><style>@page{{size:{size} landscape;margin:7mm}}*{{box-sizing:border-box}}body{{margin:0;font-family:"Noto Sans CJK SC","Noto Sans",Arial,sans-serif;color:#172033;background:white}}section{{height:{height};break-after:page;display:flex;flex-direction:column;gap:3mm;overflow:hidden}}header{{display:flex;justify-content:space-between;border-bottom:1mm solid #0f766e;padding-bottom:2mm;font-size:17pt}}.grid{{flex:1;display:grid;gap:3mm;min-height:0}}.one{{grid-template-columns:1fr}}.two{{grid-template-columns:repeat(2,1fr)}}.six{{grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(2,1fr)}}figure{{margin:0;border:.3mm solid #d4dce6;border-radius:2mm;padding:1.5mm;display:flex;flex-direction:column;min-height:0;overflow:hidden}}img{{width:100%;height:100%;min-height:0;object-fit:contain}}figcaption{{font-size:8pt;font-weight:700;padding:1mm}}footer{{font-size:7.5pt;color:#667085}}</style></head><body>{sec}</body></html>'''
    a3=[[x] for x in items]; a0=[[items[0],items[1],items[2],items[3],items[6],items[7]],[items[4],items[5],items[8],items[9],items[10]]]
    for en,lang in [(False,'zh'),(True,'en')]:
        for kind,pages,outname,size in [('a3',a3,'a3-booklet.en.pdf' if en else 'a3-booklet.pdf','A3'),('a0',a0,'a0-boards.en.pdf' if en else 'a0-boards.pdf','A0')]:
            src=tmp/f'{kind}-{lang}.html'; src.write_text(doc(pages,en,size),encoding='utf-8'); out=pkg/'drawings'/outname; subprocess.run([chrome,'--headless','--no-sandbox','--disable-gpu','--allow-file-access-from-files','--virtual-time-budget=3000',f'--print-to-pdf={out}',src.resolve().as_uri()],check=True)
    subprocess.run(['python3','scripts/refresh_submission_manifest.py',str(pkg)],check=True); sc=subprocess.run(['python3','scripts/self_check_submission.py',str(pkg),'--pr-author','miyuuteshima984','--mark-self-checked','--json'],check=True,text=True,capture_output=True); print(sc.stdout); x=json.loads(sc.stdout)
    if not x.get('ok') or not x.get('can_enter_formal_review') or x.get('review_status')!='formal-review-ready': raise SystemExit('strict self-check did not reach formal-review-ready')
    for key in ['deterministic_validation','spatial_review','visual_review','professional_review']:
        if not (x.get(key) or {}).get('ok'): raise SystemExit(f'{key} not ok')
    qa=Path('/tmp/pdf-first-'+variant.replace('.','')); qa.mkdir(exist_ok=True)
    for pdf in ['a3-booklet.pdf','a3-booklet.en.pdf','a0-boards.pdf','a0-boards.en.pdf']:
        base=pdf[:-4]; subprocess.run(['pdftoppm','-f','1','-l','1','-singlefile','-png','-r','90',str(pkg/'drawings'/pdf),str(qa/base)],check=True); p=qa/(base+'.png')
        with Image.open(p).convert('RGB') as im:
            sample=im.copy(); sample.thumbnail((640,640)); bbox=ImageChops.difference(sample,Image.new('RGB',sample.size,'white')).getbbox(); px=list(sample.getdata()); ratio=sum(1 for r,g,b in px if min(r,g,b)<245)/max(1,len(px)); print('PDF_QA',pdf,im.size,ratio,bbox)
            if bbox is None or ratio<0.003: raise SystemExit(f'blank first page: {pdf}')
    for p in fig.glob('*.png'):
        with Image.open(p) as im: im.verify()
    for p in fig.glob('*.svg'):
        s=p.read_text(encoding='utf-8',errors='replace')
        if '<svg' not in s or '</svg>' not in s: raise SystemExit(f'invalid svg: {p}')
    for p in (pkg/'drawings').glob('*.pdf'):
        if p.stat().st_size<10000: raise SystemExit(f'suspiciously small pdf: {p}')
    print('SPRINT_OK',variant)
