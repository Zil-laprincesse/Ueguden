const fs = require('fs');
const path = 'C:/Users/Administrator/Desktop/UEGUDEN/novel_ueguden_data.js';
let text = fs.readFileSync(path, 'utf8');
const fixes = [
  // P0 残留
  ['homeco yaphgòle juĝte', 'homeco yaphun juĝte'],
  ['Iuj opinige', 'Ífa opinige'],
  ['enir æ ĉeest lasgenai', 'enandar æ atendar lasgenai'],
  ['ĉeest sendigevai', 'atendar sendjevai'],
  ['komenctede', 'komençtede'],
  ['agitde startçe', 'agitçe startçe'],
  ['movde startçe', 'movçe startçe'],
  ['ĉiudirekte', 'omnidirekte'],
  // 不定式
  ['ne reĝimi', 'ne reĝim'],
  ['wara ferium est', 'wara fer est'],
  // 拼写
  ['tian situaciogàlo', 'tokan situaciogàlo'],
  ['mençionnaita', 'mençennaita'],
  ['defendinevaikŭ', 'defendevaikŭ'],
  // -ig- → -ji（报告方案）
  ['starigçe', 'starjçe'],
  ['platformogàlo starig', 'platformogàlo starji'],
  ['rememorigçe', 'rememorjçe'],
  ['publikigçe', 'publikjçe'],
  ['okazigevai', 'okazjevai'],
  ['okazig bezonge', 'okazji bezonge'],
  ['finordigçe', 'finordjçe'],
  ['lacigçe', 'lacjçe'],
  ['alfrontigevai', 'alfrontjevai'],
  ['aspektigiçe', 'aspektijçe'],
  ['stariggenailai', 'starjgenailai'],
  ['startig', 'startji'],
  ['veturig', 'veturji'],
  ['trankviligçe', 'trankviljçe'],
  ['pligrandigita', 'pligrandjita'],
];
let applied = 0, missing = [];
for (const [f, t] of fixes) {
  const n = text.split(f).length - 1;
  if (n === 0) { missing.push(f); continue; }
  text = text.split(f).join(t);
  applied += n;
}
fs.writeFileSync(path, text, 'utf8');
console.log('应用:', applied, '处; 未命中:', missing.length ? missing.join(', ') : '无');
const vm = require('vm');
try {
  const N = vm.runInNewContext(text + '\nNOVEL;');
  console.log('条目:', N.length, '结构错误:', N.filter(p => !Array.isArray(p) || p.length !== 2).length);
} catch (e) { console.log('解析失败:', e.message); }
