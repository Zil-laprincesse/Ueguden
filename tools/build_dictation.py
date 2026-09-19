# -*- coding: utf-8 -*-
"""build_dictation.py — 由词典 JSON 生成默写材料

    python tools/build_dictation.py --html     # tools/dictation.html（单文件默写器，离线可用）
    python tools/build_dictation.py --docx     # study/维古登语默写卷（第七版）.docx
    python tools/build_dictation.py --all      # 两份都出

docx 的范围与提示（html 的同类选项在页面上选）：
    --limit 300            随机抽 300 条（配 --seed 可复现）
    --seed 20260919        指定随机种子
    --letters A B C        只出这些字母分节
    --pos 名词 --pos 动词   只出这些词类
    --hint none|ipa|first  卷面提示列（默认 none）
    --no-answers           不出答案册
"""
from __future__ import annotations

import json
import os
import random
import sys
import unicodedata
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DICT_JSON = os.path.join(ROOT, "dictionary", "ueguden_dict.json")
HTML_OUT = os.path.join(HERE, "dictation.html")
DOCX_OUT = os.path.join(ROOT, "study", "维古登语默写卷（第七版）.docx")

POS_NAMES = ["名词", "动词", "形容词", "副词", "介词", "代词", "连词", "数词", "前缀", "后缀", "中缀",
             "助词", "叹词", "分词", "疑问副词", "疑问代词", "不定代词", "指示代词", "指示词", "字母",
             "词根", "动词词根", "动词短语", "助动"]


def norm_key(s: str) -> str:
    """归并排序/分节键：与 tools/gen_ipa.js 的 normKey 保持一致"""
    s = "".join(c for c in unicodedata.normalize("NFD", s.lower())
                if unicodedata.category(c) != "Mn")
    for a, b in (("ç", "c"), ("ĝ", "g"), ("ĉ", "c"), ("ʌ", "{"), ("ø", "o"),
                 ("æ", "a"), ("å", "a"), ("ã", "a"), ("ǽ", "a")):
        s = s.replace(a, b)
    return s.lstrip("-")


def group_of(word: str) -> str:
    k = norm_key(word)
    c = k[:1].upper() if k else "·"
    return c if c.isalpha() and c.isascii() else "词缀与符号"


def load() -> dict:
    with open(DICT_JSON, encoding="utf-8") as fh:
        return json.load(fh)


# --------------------------------------------------------------------------- HTML

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>维古登语 · 默写器</title>
<meta name="description" content="维古登语默写器：看汉语释义，默写词形。__COUNT__ 条词目，离线单文件。">
<style>
  :root{--paper:#F7F2EB;--ink:#081F5C;--mid:#334EAC;--soft:#7096D1;--line:#D0E3FF;--card:#FBFAF6;
        --ok:#1F7A4D;--no:#B03A2E}
  *{box-sizing:border-box}
  html,body{margin:0;padding:0}
  body{background:var(--paper);color:var(--mid);
       font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;
       font-size:15px;line-height:1.75;-webkit-font-smoothing:antialiased}
  .wrap{max-width:760px;margin:0;padding:40px 26px 64px}
  .badge{display:inline-block;border:1px dashed var(--soft);border-radius:999px;padding:4px 13px;
         font-size:11px;letter-spacing:.16em}
  h1{font-family:Georgia,'Songti SC','SimSun',serif;font-size:38px;color:var(--ink);margin:16px 0 4px;font-weight:800}
  .sub{font-size:12px;color:var(--soft);letter-spacing:.06em;margin:0 0 26px}
  .card{background:var(--card);border-left:2px solid var(--soft);border-radius:0 12px 12px 0;
        padding:18px 20px;margin:0 0 16px}
  .row{display:block;margin:0 0 12px}
  label{display:inline-block;font-size:12px;color:var(--soft);letter-spacing:.08em;margin-right:6px}
  select,input[type=text]{font:inherit;font-size:14px;color:var(--ink);background:#fff;
        border:1px solid var(--line);border-radius:8px;padding:7px 10px;margin-right:14px}
  select{cursor:pointer}
  button{font:inherit;font-size:14px;font-weight:700;color:var(--paper);background:var(--ink);
        border:0;border-radius:10px;padding:11px 22px;margin:6px 8px 0 0;cursor:pointer}
  button.ghost{background:transparent;color:var(--mid);border:1px solid var(--line);font-weight:600}
  button:hover{background:var(--mid)}
  button.ghost:hover{background:#fff;color:var(--ink)}
  .hidden{display:none}
  .qhead{display:block;font-size:12px;color:var(--soft);letter-spacing:.06em;margin:0 0 14px}
  .qhead span{margin-right:18px}
  .postag{display:inline-block;font-size:11px;letter-spacing:.1em;color:var(--mid);
          border:1px solid var(--line);border-radius:999px;padding:2px 10px;margin-bottom:10px}
  .gloss{font-family:Georgia,'Songti SC','SimSun',serif;font-size:26px;line-height:1.5;color:var(--ink);
         font-weight:800;margin:6px 0 10px}
  .hint{font-size:13px;color:var(--soft);letter-spacing:.04em;margin:0 0 14px}
  #answer{display:block;width:100%;font-size:20px;padding:12px 14px;margin:4px 0 12px}
  .fb{font-size:14px;margin:2px 0 10px;min-height:26px}
  .fb.ok{color:var(--ok)}
  .fb.no{color:var(--no)}
  .fb b{color:var(--ink);font-size:17px}
  .keys{margin:0 0 8px}
  .keys button{font-size:14px;font-weight:600;background:#EAF1FB;color:var(--ink);padding:6px 11px;margin:0 5px 5px 0;border-radius:8px}
  .keys button:hover{background:var(--line)}
  .stat{font-family:Georgia,serif;font-size:30px;color:var(--ink);font-weight:700}
  .wronglist{margin:12px 0 0;padding:0;list-style:none;font-size:13px}
  .wronglist li{border-bottom:1px solid var(--line);padding:7px 0}
  .wronglist b{color:var(--ink);font-size:15px}
  .wronglist i{color:var(--soft);font-style:normal;font-size:12px}
  footer{margin-top:34px;padding-top:12px;border-top:1px solid var(--line);font-size:11px;color:var(--soft);letter-spacing:.04em}
  #printArea{display:none}
  @media print{
    body{background:#fff}
    .wrap{max-width:none;padding:0}
    header,#setup,#quiz,#result,footer{display:none!important}
    #printArea{display:block}
    #printArea h2{font-size:15px;color:#000;margin:0 0 10px}
    #printArea .pitem{font-size:12px;color:#000;border-bottom:1px solid #999;padding:9px 0 20px}
    #printArea .pnum{color:#666;margin-right:6px}
  }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <span class="badge">UEGUDEN · 默写器</span>
    <h1>默写</h1>
    <p class="sub">看汉语释义，默写维古登语词形 · 共 __COUNT__ 条 · 离线单文件</p>
  </header>

  <section id="setup" class="card">
    <div class="row">
      <label>首字母</label><select id="fLetter"></select>
      <label>词类</label><select id="fPos"></select>
    </div>
    <div class="row">
      <label>题量</label><select id="fCount">
        <option value="10">10 题</option><option value="20" selected>20 题</option>
        <option value="30">30 题</option><option value="50">50 题</option>
        <option value="100">100 题</option><option value="0">全部</option>
      </select>
      <label>顺序</label><select id="fOrder">
        <option value="rand" selected>随机</option><option value="seq">顺序</option>
      </select>
    </div>
    <div class="row">
      <label>提示</label><select id="fHint">
        <option value="none" selected>不给提示</option>
        <option value="ipa">给音标</option>
        <option value="first">给首字母与词长</option>
      </select>
      <label><input type="checkbox" id="fWrong"> 只练错词本</label>
    </div>
    <button id="btnStart">开始默写</button>
    <p class="sub" style="margin:14px 0 0">错词本：<b id="wrongN">0</b> 条 ·
      <a href="#" id="btnClearWrong" style="color:var(--soft)">清空</a> ·
      作答按回车提交，答对再按回车进下一题</p>
  </section>

  <section id="quiz" class="card hidden">
    <div class="qhead"><span id="qProgress">第 1 / 20</span><span id="qScore">✓ 0 ｜ ✗ 0</span></div>
    <div><span class="postag" id="qPos"></span></div>
    <div class="gloss" id="qGloss"></div>
    <div class="hint" id="qHint"></div>
    <input type="text" id="answer" autocomplete="off" autocorrect="off" autocapitalize="off"
           spellcheck="false" placeholder="在这儿默写词形，回车提交">
    <div class="fb" id="fb"></div>
    <div class="keys" id="keys"></div>
    <div>
      <button id="btnSubmit">提交</button>
      <button class="ghost" id="btnSkip">跳过</button>
      <button class="ghost" id="btnReveal">看答案</button>
      <button class="ghost" id="btnQuit">结束本轮</button>
    </div>
  </section>

  <section id="result" class="card hidden">
    <div class="qhead"><span>本轮成绩</span></div>
    <p><span class="stat" id="rRate">0%</span></p>
    <p class="sub" id="rLine" style="margin:0 0 6px"></p>
    <div>
      <button id="btnAgain">再来一轮</button>
      <button class="ghost" id="btnRedoWrong">重做错词</button>
      <button class="ghost" id="btnPrint">打印本卷</button>
      <button class="ghost" id="btnSetup">回到设置</button>
    </div>
    <ul class="wronglist" id="rWrong"></ul>
  </section>

  <div id="printArea"></div>
  <footer>
    数据源：dictionary/ueguden_dict.json（词典第七版 · __COUNT__ 条 · DICT_REV = __REV__）｜
    错词本存在本机浏览器里，不上传任何数据 ｜ 文档/词典/语料：CC BY-SA 4.0
  </footer>
</div>

<script>
'use strict';
const RAW = `__RAW__`;
const KEYS = ['í','á','é','ó','ú','ǽ','æ','ø','å','ŭ','ã','ç','ĉ','ĝ','à','ò','ë','ö','ü'];
const STORE = 'ueguden_dictation_wrong_v1';

const items = RAW.split('\n').filter(function(l){return l.indexOf('|')>0;}).map(function(l){
  const f = l.split('|');
  return {w:f[0], ipa:f[1], pos:f[2], gloss:f[3], etym:f[4]||''};
});

function norm(s){ return s.normalize('NFC').trim().replace(/\s+/g,' ').toLowerCase(); }
function bare(s){ return norm(s).normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[̀-ͯ]/g,''); }
function groupOf(w){
  let k = bare(w).replace(/ç/g,'c').replace(/ĝ/g,'g').replace(/ĉ/g,'c').replace(/ø/g,'o').replace(/æ/g,'a').replace(/å/g,'a').replace(/ʌ/g,'{').replace(/^-+/,'');
  const c = (k[0]||'·').toUpperCase();
  return /[A-Z]/.test(c) ? c : '词缀与符号';
}
function shuffle(a){
  for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); const t=a[i];a[i]=a[j];a[j]=t; }
  return a;
}
function loadWrong(){ try{ return JSON.parse(localStorage.getItem(STORE)||'{}'); }catch(e){ return {}; } }
function saveWrong(o){ try{ localStorage.setItem(STORE, JSON.stringify(o)); }catch(e){} }
function wrongCount(){ return Object.keys(loadWrong()).length; }

const $ = function(id){ return document.getElementById(id); };
let round = [], idx = 0, right = 0, wrong = 0, answered = false, curWrong = [];

function fillFilters(){
  const letters = Array.from(new Set(items.map(function(x){return groupOf(x.w);})))
        .sort(function(a,b){ return a.localeCompare(b,'en'); });
  const sel = $('fLetter');
  sel.innerHTML = '<option value="">全部</option>' + letters.map(function(g){
      const n = items.filter(function(x){return groupOf(x.w)===g;}).length;
      return '<option value="'+g+'">'+g+'（'+n+'）</option>'; }).join('');
  const poss = Array.from(new Set(items.map(function(x){return x.pos;})))
        .sort(function(a,b){ return items.filter(function(x){return x.pos===b;}).length
                                 - items.filter(function(x){return x.pos===a;}).length; });
  $('fPos').innerHTML = '<option value="">全部</option>' + poss.map(function(p){
      const n = items.filter(function(x){return x.pos===p;}).length;
      return '<option value="'+p+'">'+p+'（'+n+'）</option>'; }).join('');
}
function buildKeys(){
  $('keys').innerHTML = KEYS.map(function(k){ return '<button data-k="'+k+'">'+k+'</button>'; }).join('');
  $('keys').addEventListener('click', function(e){
    const b = e.target.closest('button'); if(!b) return;
    const inp = $('answer'), k = b.getAttribute('data-k');
    const s = inp.selectionStart || 0, t = inp.value;
    inp.value = t.slice(0,s) + k + t.slice(s);
    inp.focus(); inp.selectionStart = inp.selectionEnd = s + k.length;
  });
}
function candidates(){
  let pool = items;
  const L = $('fLetter').value, P = $('fPos').value;
  if(L) pool = pool.filter(function(x){ return groupOf(x.w)===L; });
  if(P) pool = pool.filter(function(x){ return x.pos===P; });
  if($('fWrong').checked){
    const wb = loadWrong();
    pool = pool.filter(function(x){ return wb[x.w]; });
    if(!pool.length) pool = items.filter(function(x){ return loadWrong()[x.w]; });
  }
  return pool.slice();
}
function start(){
  let pool = candidates();
  if(!pool.length){ alert('这个范围里没有词条，换个筛选试试'); return; }
  if($('fOrder').value === 'seq'){
    pool.sort(function(a,b){ return a.w.localeCompare(b.w,'en'); });
  } else { shuffle(pool); }
  const n = parseInt($('fCount').value, 10);
  round = n > 0 ? pool.slice(0, n) : pool;
  idx = 0; right = 0; wrong = 0; curWrong = [];
  $('setup').classList.add('hidden'); $('result').classList.add('hidden');
  $('quiz').classList.remove('hidden');
  show();
}
function show(){
  answered = false;
  const it = round[idx];
  $('qProgress').textContent = '第 ' + (idx+1) + ' / ' + round.length;
  $('qScore').textContent = '✓ ' + right + ' ｜ ✗ ' + wrong;
  $('qPos').textContent = it.pos;
  $('qGloss').textContent = it.gloss.replace(/。$/,'');
  const h = $('fHint').value;
  if(h === 'ipa'){ $('qHint').textContent = it.ipa; }
  else if(h === 'first'){
    const body = it.w.slice(1).replace(/[^\s]/g,'·');
    $('qHint').textContent = it.w.slice(0,1) + body + '（' + it.w.length + ' 个字母）';
  } else { $('qHint').textContent = ''; }
  $('fb').textContent = ''; $('fb').className = 'fb';
  $('answer').value = ''; $('answer').disabled = false; $('answer').readOnly = false;
  $('answer').focus();
}
function reveal(mark){
  const it = round[idx];
  answered = true;
  $('fb').className = 'fb no';
  $('fb').innerHTML = '答案：<b>' + it.w + '</b>　' + it.ipa;
  if(mark){ wrong++; curWrong.push(it); const wb = loadWrong(); wb[it.w] = {gloss:it.gloss, ipa:it.ipa}; saveWrong(wb); $('wrongN').textContent = wrongCount(); }
  $('qScore').textContent = '✓ ' + right + ' ｜ ✗ ' + wrong;
  $('answer').readOnly = true;
}
function submit(){
  if(answered){ next(); return; }
  const it = round[idx], val = $('answer').value;
  if(!val.trim()){ $('answer').focus(); return; }
  if(norm(val) === norm(it.w)){
    answered = true; right++;
    $('fb').className = 'fb ok';
    $('fb').innerHTML = '✓ 对了　<b>' + it.w + '</b>　' + it.ipa + '　（回车继续）';
    const wb = loadWrong(); if(wb[it.w]){ delete wb[it.w]; saveWrong(wb); $('wrongN').textContent = wrongCount(); }
    $('answer').readOnly = true;
    $('qScore').textContent = '✓ ' + right + ' ｜ ✗ ' + wrong;
    return;
  }
  if(bare(val) === bare(it.w)){
    answered = true; wrong++; curWrong.push(it);
    $('fb').className = 'fb no';
    $('fb').innerHTML = '⚠ 字母对了，符号不对　正解：<b>' + it.w + '</b>　' + it.ipa + '　（回车继续）';
  } else {
    answered = true; wrong++; curWrong.push(it);
    const wb = loadWrong(); wb[it.w] = {gloss:it.gloss, ipa:it.ipa}; saveWrong(wb); $('wrongN').textContent = wrongCount();
    $('fb').className = 'fb no';
    $('fb').innerHTML = '✗ 不对　你写的：' + val + '　正解：<b>' + it.w + '</b>　' + it.ipa + '　（回车继续）';
  }
  $('qScore').textContent = '✓ ' + right + ' ｜ ✗ ' + wrong;
  $('answer').readOnly = true;
}
function next(){
  idx++;
  if(idx >= round.length){ finish(); return; }
  show();
}
function finish(){
  $('quiz').classList.add('hidden'); $('result').classList.remove('hidden');
  const total = right + wrong;
  const rate = total ? Math.round(right*100/total) : 0;
  $('rRate').textContent = rate + '%';
  $('rLine').textContent = '共 ' + round.length + ' 题 ｜ 答对 ' + right + ' ｜ 答错 ' + wrong
      + ' ｜ 错词本现有 ' + wrongCount() + ' 条';
  $('rWrong').innerHTML = curWrong.length
    ? curWrong.map(function(x){ return '<li><b>'+x.w+'</b> <i>'+x.ipa+'　'+x.pos+'　'+x.gloss+'</i></li>'; }).join('')
    : '<li>这一轮全对，没有错词。</li>';
}
function printRound(){
  const list = round.map(function(x,i){
    return '<div class="pitem"><span class="pnum">'+(i+1)+'.</span>'
         + x.gloss.replace(/。$/,'') + '（' + x.pos + '）</div>';
  }).join('');
  $('printArea').innerHTML = '<h2>维古登语默写卷 · ' + round.length + ' 题</h2>' + list;
  window.print();
}

fillFilters(); buildKeys();
$('wrongN').textContent = wrongCount();
$('btnStart').addEventListener('click', start);
$('btnSubmit').addEventListener('click', submit);
$('btnSkip').addEventListener('click', function(){ reveal(false); });
$('btnReveal').addEventListener('click', function(){ reveal(true); });
$('btnQuit').addEventListener('click', finish);
$('btnAgain').addEventListener('click', start);
$('btnRedoWrong').addEventListener('click', function(){ $('fWrong').checked = true; start(); });
$('btnPrint').addEventListener('click', printRound);
$('btnSetup').addEventListener('click', function(){
  $('result').classList.add('hidden'); $('setup').classList.remove('hidden'); });
$('btnClearWrong').addEventListener('click', function(e){
  e.preventDefault(); if(confirm('清空错词本？')){ saveWrong({}); $('wrongN').textContent = 0; } });
$('answer').addEventListener('keydown', function(e){
  if(e.key === 'Enter'){ e.preventDefault(); e.stopPropagation(); submit(); } });
document.addEventListener('keydown', function(e){
  if(e.key === 'Enter' && answered && !$('quiz').classList.contains('hidden')){
    e.preventDefault(); next(); } });
</script>
</body>
</html>
"""


def build_html(data: dict) -> None:
    rows = ["%s|%s|%s|%s|%s" % (e["word"], e["ipa"], e["pos"], e["gloss"], e["etym"])
            for e in data["entries"]]
    html = (HTML_TEMPLATE
            .replace("__RAW__", "\n".join(rows))
            .replace("__COUNT__", str(data["count"]))
            .replace("__REV__", str(data.get("dict_rev"))))
    with open(HTML_OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    print("  OK  %s（%d 条内嵌 · %d 字节）" % (HTML_OUT, len(rows), os.path.getsize(HTML_OUT)))


# --------------------------------------------------------------------------- DOCX

def build_docx(data: dict, argv: list[str]) -> None:
    from docx import Document
    from docx.enum.section import WD_SECTION
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor

    def opt(name, n=1, default=None):
        if name not in argv:
            return default
        i = argv.index(name)
        return argv[i + 1:i + 1 + n] if n > 1 else argv[i + 1]

    def set_widths(tbl, widths):
        """固定表格布局并逐列设宽（否则 Word/WPS 会把各列均分）"""
        tbl.autofit = False
        for i, w in enumerate(widths):
            tbl.columns[i].width = w
        for row in tbl.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = w

    entries = list(data["entries"])
    letters = opt("--letters", 99, [])
    if letters:
        want = {x.upper() for x in letters}
        entries = [e for e in entries if group_of(e["word"]) in want]
    poss = opt("--pos", 99, [])
    if poss:
        entries = [e for e in entries if e["pos"] in poss]
    limit = opt("--limit")
    if limit:
        random.Random(int(opt("--seed", 1, [0])[0]) if opt("--seed") else 0).shuffle(entries)
        entries = sorted(entries[:int(limit)], key=lambda e: norm_key(e["word"]))
    hint = opt("--hint", 1, ["none"])[0]

    doc = Document()
    for s in doc.sections:
        s.top_margin = s.bottom_margin = Cm(1.8)
        s.left_margin = s.right_margin = Cm(1.8)
    base = doc.styles["Normal"]
    base.font.name = "Times New Roman"
    base.font.size = Pt(10)
    base.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
    for name, size in (("Heading 1", 15), ("Heading 2", 12)):
        st = doc.styles[name]
        st.font.name = "Microsoft YaHei"
        st.font.size = Pt(size)
        st.font.color.rgb = RGBColor(0x08, 0x1F, 0x5C)
        st.font.bold = True

    doc.add_heading("维古登语 · 默写卷", level=0)
    p = doc.add_paragraph()
    p.add_run("Ueguden ｜ 词典第七版 ｜ 共 %d 条词目 ｜ 生成日期 %s"
              % (len(entries), date.today().isoformat())).italic = True
    doc.add_paragraph(
        "用法：卷面只给汉语释义与词类，请在「默写」栏手写维古登语词形；"
        "答案按同一序号排在卷末，核对时逐行对照即可。")
    doc.add_paragraph(
        "范围：%s ｜ 提示列：%s ｜ 词形须带正字法要求的变音符号（í á é ó ú ǽ æ ø å ŭ ã ç ĉ ĝ à ò），"
        "默写时符号写错也算错。"
        % ("全部条目" if not (letters or poss or limit) else
           " ".join(filter(None, ["字母 " + " ".join(letters) if letters else "",
                                  "词类 " + " ".join(poss) if poss else "",
                                  "随机 %s 条" % limit if limit else ""])),
           {"none": "无", "ipa": "音标", "first": "首字母与词长"}.get(hint, "无")))
    doc.add_page_break()

    # 卷面：按字母分节
    groups: dict[str, list] = {}
    for e in entries:
        groups.setdefault(group_of(e["word"]), []).append(e)
    order = sorted(groups, key=lambda g: (not g[:1].isalpha(), g))
    n = 0
    for g in order:
        doc.add_heading("%s（%d 条）" % (g, len(groups[g])), level=1)
        cols = ["#", "汉语释义", "词类", "默写"] + (["提示"] if hint != "none" else [])
        tbl = doc.add_table(rows=1, cols=len(cols))
        tbl.style = "Table Grid"
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        for i, c in enumerate(cols):
            cell = tbl.rows[0].cells[i]
            cell.text = ""
            r = cell.paragraphs[0].add_run(c)
            r.bold = True
            r.font.size = Pt(9)
        for e in groups[g]:
            n += 1
            row = tbl.add_row()
            vals = [str(n), e["gloss"], e["pos"], ""]
            if hint == "ipa":
                vals.append(e["ipa"])
            elif hint == "first":
                vals.append(e["word"][:1] + "·" * (len(e["word"]) - 1))
            for i, v in enumerate(vals):
                cell = row.cells[i]
                cell.text = ""
                run = cell.paragraphs[0].add_run(v)
                run.font.size = Pt(9)
                if i == 0:
                    run.font.name = "Times New Roman"
            row.height = Cm(0.68)
        widths = {"none": [Cm(0.9), Cm(9.0), Cm(1.8), Cm(5.0)],
                  "ipa": [Cm(0.9), Cm(6.8), Cm(1.8), Cm(4.4), Cm(3.4)],
                  "first": [Cm(0.9), Cm(7.4), Cm(1.8), Cm(4.4), Cm(2.8)]}[hint]
        set_widths(tbl, widths)

    if "--no-answers" not in argv:
        doc.add_page_break()
        doc.add_heading("答案", level=1)
        doc.add_paragraph("序号与卷面一致，逐行核对。").italic = True
        head = ["#", "词形", "音标", "汉语释义"]
        atbl = doc.add_table(rows=1, cols=len(head))
        atbl.style = "Table Grid"
        atbl.autofit = False
        for i, c in enumerate(head):
            cell = atbl.rows[0].cells[i]
            cell.text = ""
            r = cell.paragraphs[0].add_run(c)
            r.bold = True
            r.font.size = Pt(9)
        n = 0
        for g in order:
            for e in groups[g]:
                n += 1
                row = atbl.add_row()
                for i, v in enumerate([str(n), e["word"], e["ipa"], e["gloss"]]):
                    cell = row.cells[i]
                    cell.text = ""
                    r = cell.paragraphs[0].add_run(v)
                    r.font.size = Pt(9)
                    if i in (0, 1, 2):
                        r.font.name = "Times New Roman"
        for row in atbl.rows:
            for i, w in enumerate([Cm(0.9), Cm(4.2), Cm(4.4), Cm(7.4)]):
                row.cells[i].width = w
        set_widths(atbl, [Cm(0.9), Cm(4.2), Cm(4.4), Cm(7.4)])

    os.makedirs(os.path.dirname(DOCX_OUT), exist_ok=True)
    doc.save(DOCX_OUT)
    print("  OK  %s（卷面 %d 条%s · %d 字节）"
          % (DOCX_OUT, n, "" if "--no-answers" in argv else " + 答案 %d 条" % n,
             os.path.getsize(DOCX_OUT)))


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    data = load()
    print("词典：%d 条 ｜ DICT_REV = %s" % (data["count"], data.get("dict_rev")))
    do_all = "--all" in argv or not ({"--html", "--docx"} & set(argv))
    if do_all or "--html" in argv:
        build_html(data)
    if do_all or "--docx" in argv:
        build_docx(data, argv)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
