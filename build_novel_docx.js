// 生成《阈界·永夜之狂澜》第二卷 维古登语双语对照 docx —— 文章式排版（无表格）
// 用法：node build_novel_docx.js
const fs = require('fs');
const path = require('path');

const NOVEL = vm_run(path.join(__dirname, 'novel_ueguden_data.js'));
function vm_run(file){
  const vm = require('vm');
  const code = fs.readFileSync(file, 'utf8');
  return vm.runInNewContext(code + '\nNOVEL;');
}

// --- 简易 zip 打包（store 方式）---
function crc32(str){
  const table = [];
  for(let n=0;n<256;n++){ let c=n; for(let k=0;k<8;k++) c = (c&1) ? (0xEDB88320 ^ (c>>>1)) : (c>>>1); table[n]=c>>>0; }
  let crc = 0xFFFFFFFF;
  for(let i=0;i<str.length;i++){ crc = table[(crc ^ str.charCodeAt(i)) & 0xFF] ^ (crc >>> 8); }
  return (crc ^ 0xFFFFFFFF) >>> 0;
}
function makeZip(files){
  const enc = new TextEncoder();
  const chunks = []; let offset = 0; const central = [];
  for(const f of files){
    const nameBytes = enc.encode(f.name);
    const dataBytes = enc.encode(f.data);
    const crc = crc32(f.data);
    const lh = new Uint8Array(30);
    const dv = new DataView(lh.buffer);
    dv.setUint32(0, 0x04034b50, true); dv.setUint16(4, 20, true); dv.setUint16(6, 0x0800, true);
    dv.setUint16(8, 0, true); dv.setUint16(10, 0, true); dv.setUint16(12, 0, true);
    dv.setUint32(14, crc, true); dv.setUint32(18, dataBytes.length, true); dv.setUint32(22, dataBytes.length, true);
    dv.setUint16(26, nameBytes.length, true); dv.setUint16(28, 0, true);
    chunks.push(lh, nameBytes, dataBytes);
    central.push({ name: nameBytes, crc, size: dataBytes.length, offset });
    offset += 30 + nameBytes.length + dataBytes.length;
  }
  const centralSize = central.reduce((s,c) => s + 46 + c.name.length, 0);
  const cdStart = offset;
  for(const c of central){
    const ch = new Uint8Array(46);
    const dv = new DataView(ch.buffer);
    dv.setUint32(0, 0x02014b50, true); dv.setUint16(4, 20, true); dv.setUint16(6, 20, true);
    dv.setUint16(8, 0x0800, true); dv.setUint16(10, 0, true); dv.setUint16(12, 0, true); dv.setUint16(14, 0, true);
    dv.setUint32(16, c.crc, true); dv.setUint32(20, c.size, true); dv.setUint32(24, c.size, true);
    dv.setUint16(28, c.name.length, true); dv.setUint32(42, c.offset, true);
    chunks.push(ch, c.name);
  }
  const eocd = new Uint8Array(22);
  const edv = new DataView(eocd.buffer);
  edv.setUint32(0, 0x06054b50, true); edv.setUint16(8, central.length, true); edv.setUint16(10, central.length, true);
  edv.setUint32(12, centralSize, true); edv.setUint32(16, cdStart, true);
  chunks.push(eocd);
  return Buffer.concat(chunks.map(c => Buffer.from(c.buffer ? c : c)));
}

function xmlEsc(s){ return String(s==null?'':s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c])); }

// ---- 段落构建辅助 ----
// 通用 run：text, bold, italic, color, sz(half-point), eastAsia 字体
function run(text, { bold=false, italic=false, color='000000', sz=21, lang='mix' } = {}){
  const east = lang==='zh' ? '宋体' : 'Times New Roman';
  const ascii = 'Times New Roman';
  return '<w:r><w:rPr>' +
    (bold?'<w:b/>':'') + (italic?'<w:i/>':'') +
    '<w:color w:val="' + color + '"/>' +
    '<w:rFonts w:ascii="' + ascii + '" w:hAnsi="' + ascii + '" w:eastAsia="' + east + '"/>' +
    '<w:sz w:val="' + sz + '"/><w:szCs w:val="' + sz + '"/>' +
    '</w:rPr><w:t xml:space="preserve">' + xmlEsc(text) + '</w:t></w:r>';
}
// 段落：runs 数组，opts: jc(center/both/right/left), indentChars(首行缩进字符数), before/after(twips), line(lineRule auto 的 line 值, 240=单倍 360=1.5 倍)
function para(runs, { jc='both', indentChars=0, before=0, after=0, line=360 } = {}){
  let ind = '';
  if(indentChars > 0){
    const tw = Math.round(indentChars * 10.5 * 20); // 每字符 ≈10.5pt
    ind = '<w:ind w:firstLineChars="' + (indentChars*100) + '" w:firstLine="' + tw + '"/>';
  }
  return '<w:p><w:pPr>' +
    (jc!=='left' ? '<w:jc w:val="' + jc + '"/>' : '') +
    '<w:spacing w:line="' + line + '" w:lineRule="auto" w:before="' + before + '" w:after="' + after + '"/>' +
    ind +
    '</w:pPr>' + runs.join('') + '</w:p>';
}
// 空行
function blank(after=60){ return para([], { jc:'left', before:0, after }); }

// ---- 条目分类 ----
function classify(zh, ug){
  if(zh.startsWith('阈界')) return 'book';
  if(zh.indexOf('第二卷') >= 0) return 'volume';
  if(/^序章（[一二]）/.test(zh) || /^第[一二]章\s/.test(zh)) return 'chapter';
  if(zh === '序章 完' || zh === '第一章 完') return 'chapter-end';
  if(/^—20\d\d/.test(zh) || /^—25\./.test(zh)) return 'date';
  return 'body';
}

let out = '';

// 主标题（书名）：维古登语在上（二号加粗），中文在下（三号）
out += para([run('Limenmondo · Tærnokt-Furiozo', { bold:true, color:'1F3B2C', sz:44 })], { jc:'center', before:600, after:60 });
out += para([run('阈界 · 永夜之狂澜', { bold:true, color:'4A5A4A', sz:32 })], { jc:'center', before:0, after:120 });
out += para([run('—— 第二卷 ——', { color:'8A8175', sz:24 })], { jc:'center', before:0, after:480 });
out += para([run('Dua Volumo · Ueguden-lingva Duobla Teksto', { italic:true, color:'8A8175', sz:18 })], { jc:'center', before:0, after:720 });

for(const [zh, ug] of NOVEL){
  const type = classify(zh, ug);
  if(type === 'book' || type === 'volume') continue; // 已在页眉区渲染

  if(type === 'chapter'){
    // 章题：维古登语（四号加粗居中）+ 中文（小四，深灰）
    out += para([run(ug, { bold:true, color:'1F3B2C', sz:28 })], { jc:'center', before:600, after:60 });
    out += para([run(zh, { bold:true, color:'55605A', sz:24 })], { jc:'center', before:0, after:300 });
    continue;
  }
  if(type === 'chapter-end'){
    out += para([run('◆  ' + ug + '  ◆', { bold:true, italic:true, color:'8A8175', sz:18 })], { jc:'center', before:300, after:120 });
    out += para([run(zh, { color:'8A8175', sz:18 })], { jc:'center', before:0, after:300 });
    continue;
  }
  if(type === 'date'){
    // 日期落款：右对齐，小五号灰色；若维古登语与中文不同则两行
    if(ug === zh){
      out += para([run(zh, { italic:true, color:'8A8175', sz:18 })], { jc:'right', before:200, after:120 });
    } else {
      out += para([run(ug, { italic:true, color:'8A8175', sz:18 })], { jc:'right', before:200, after:20 });
      out += para([run(zh, { color:'8A8175', sz:18 })], { jc:'right', before:0, after:120 });
    }
    continue;
  }

  // 正文组：维古登语在上（五号 10.5pt，墨绿），中文在下（小五号 9pt，深灰）
  out += para([run(ug, { color:'1F4E3D', sz:21 })], { jc:'both', indentChars:2, before:160, after:60 });
  out += para([run(zh, { color:'3A3A3A', sz:18 })], { jc:'both', indentChars:2, before:0, after:220 });
}

// 文末排版说明
out += para([run('—— 排版说明 ——', { color:'8A8175', sz:18 })], { jc:'center', before:400, after:60 });
out += para([run('本文以文章式版面呈现：维古登语在上、汉语在下（汉语小一号），全文无表格、边框与分栏；正文五号两端对齐、首行缩进两字符、1.5 倍行距，并美化了书名页、章节标题、落款日期等层级细节。', { color:'8A8175', sz:18 })], { jc:'both', indentChars:2, before:0, after:120 });

const doc = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' +
  '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">' +
  '<w:body>' + out +
  '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>' +
  '</w:body></w:document>';
const ct = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>';
const rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>';
const zip = makeZip([
  { name: '[Content_Types].xml', data: ct },
  { name: '_rels/.rels', data: rels },
  { name: 'word/document.xml', data: doc }
]);
const outPath = path.join(__dirname, '《阈界·永夜之狂澜》第二卷 - 维古登语双语对照（文章式）.docx');
fs.writeFileSync(outPath, zip);
console.log('WROTE', outPath, zip.length, 'bytes');
console.log('entries:', NOVEL.length, '| table elements:', (doc.match(/<w:tbl>/g)||[]).length);
