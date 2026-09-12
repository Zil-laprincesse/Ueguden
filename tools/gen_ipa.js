'use strict';
const fs = require('fs');
const htmlPath = 'C:/Users/Administrator/Desktop/UEGUDEN/Dictionary.html';
let html = fs.readFileSync(htmlPath, 'utf8');
const rs = html.indexOf('const RAW = `') + 'const RAW = `'.length;
const re = html.indexOf('`;', rs);

// 音标生成（x→ks、重音在音节起音前）
const VOW = 'aeiouæøåãʌáéíóúǽ';
const VM = {a:'a',e:'ə',i:'i',o:'o',u:'u',æ:'æ',ø:'ø',å:'ɔː',ã:'ɐ̃',ʌ:'ʌ',á:'aː',é:'eː',í:'iː',ó:'oː',ú:'uː',ǽ:'æː'};
const isV = ch => VOW.includes(ch);
const isC = ch => 'bcdfghjklmnprstvzçĝĉx'.includes(ch);
function toIpa(f){
  const vpos=[]; for(let i=0;i<f.length;i++) if(isV(f[i])) vpos.push(i);
  const stress = vpos.length>=2 ? vpos[vpos.length-2] : (vpos[0] ?? -1);
  let stressAt = stress;
  if(stress >= 0){ let j = stress - 1; while(j >= 0 && isC(f[j])) j--; stressAt = j + 1; }
  let ipa='';
  for(let i=0;i<f.length;i++){
    const ch=f[i];
    if(i===stressAt) ipa+='ˈ';
    if(ch==='x') ipa+='ks';
    else if(ch==='k') ipa+='kʰ';
    else if(ch==='t') ipa+='tʰ';
    else if(ch==='p') ipa+='p';
    else if(ch==='c') ipa+='k';
    else if(ch==='ç') ipa+='s';
    else if(ch==='g') ipa+='ɡ';
    else if(ch==='ĝ') ipa+='d͡ʒ';
    else if(ch==='ĉ') ipa+='tʃ';
    else if(ch==='j') ipa+='d͡ʒ';
    else if(ch==='r'){ const nxt=f[i+1], prv=f[i-1]; ipa += (nxt && isV(nxt)) ? ((prv && isC(prv)) ? 'r' : 'ʁ') : 'ɹ'; }
    else if(ch==='n') ipa += (f[i+1]==='k'||f[i+1]==='g') ? 'ŋ' : 'n';
    else if(ch==='s'){ ipa += (f[i+1]==='h') ? 'ʃ' : 's'; if(f[i+1]==='h') i++; }
    else if(ch==='b') ipa+='b';
    else if(ch==='d') ipa+='d';
    else if(ch==='f') ipa+='f';
    else if(ch==='v') ipa+='v';
    else if(ch==='z') ipa+='z';
    else if(ch==='h') ipa+='h';
    else if(ch==='m') ipa+='m';
    else if(ch==='l') ipa+='l';
    else if(ch==='w') ipa+='w';
    else if(ch==='y') ipa+='j';
    else if(VM[ch]) ipa+=VM[ch];
    else ipa+=ch;
  }
  return ipa;
}

// 新词：[词形, 词类, 义项, 词源]
const NEW = [
  ['am','动','爱。','原生词根（"amanto" 词根）。'],
  ['kelo','名','目标，目的。','源自拉丁语「celo」。'],
  ['luna','名','月亮。','源自拉丁语「luna」。'],
  ['stel','名','星星。','源自拉丁语「stella」。'],
  ['arbo','名','树。','源自拉丁语「arbor」。'],
  ['pentri','动','画（绘画）。','源自拉丁语「pingere」。'],
  ['ofte','副','经常。','源自德语「oft」。'],
  ['eĉ','副','甚至。','源自世界语「eĉ」。'],
  ['iom','副','一点，少许。','源自世界语「iom」。'],
  ['iam','副','曾经。','源自世界语「iam」。'],
  ['poste','副','后来。','源自世界语「poste」。'],
  ['karaktero','名','性格。','源自世界语「karaktero」。'],
  ['stato','名','状态。','源自拉丁语「status」。'],
  ['kompenso','名','补偿。','源自拉丁语「compensare」。'],
  ['kreto','名','粉笔。','源自拉丁语「creta」。'],
  ['sideo','名','座位。','源自拉丁语「sedeo」。'],
  ['gusto','名','味道。','源自拉丁语「gustus」。'],
  ['fako','名','科目，学科。','源自世界语「fako」。'],
  ['tenera','形','温柔的。','「tener」词根。'],
  ['preskaŭ','副','差点，几乎。','源自世界语「preskaŭ」。'],
  ['privata','形','私立的，私人的。','源自拉丁语「privatus」。'],
  ['rezulto','名','成绩。','源自拉丁语「resultare」。'],
  ['knabo','名','男孩。','源自世界语「knabo」。'],
  ['situaçia','名','情况，局面。','源自法语「situation」。'],
  ['defekto','名','缺陷。','源自拉丁语「defectus」。'],
  ['limito','名','限制。','源自拉丁语「limes」。'],
  ['presiá','名','压力。','源自法语「pression」。'],
  ['sharĝo','名','负担。','源自世界语「ŝarĝo」。'],
  ['depresio','名','抑郁。','源自拉丁语「depressio」。'],
  ['nihilismo','名','虚无主义。','源自拉丁语「nihil」。'],
  ['fortika','形','结实的。','源自拉丁语「fortis」。'],
  ['rompi','动','断裂。','源自拉丁语「rumpere」。'],
  ['níamens','名','九月。','「nía」+「mensis」。'],
  ['somerhresto','名','暑假。','「somer」+「hresto」。'],
  ['gradaçia','名','毕业。','源自拉丁语「gradatio」。'],
  ['klaso','名','班级，年级。','源自拉丁语「classis」。'],
  ['klaschefo','名','班长。','「klaso」+「ĉefo」。'],
  ['altaskola','名','高中。','「alta」+「skola」。'],
  ['bazaskola','名','初中。','「baza」+「skola」。'],
  ['baza','形','基础的。','源自拉丁语「basis」。'],
  ['semestro','名','学期。','源自拉丁语「semestris」。'],
  ['reprezento','名','代表。','源自拉丁语「repraesentare」。'],
  ['atenta','形','细心的。','源自拉丁语「attentus」。'],
  ['nostalĝia','名','怀念，怀旧。','源自希腊语「nostalgia」。'],
  ['embarasa','形','尴尬的。','源自法语「embarras」。'],
  ['rumoro','名','谣言。','源自拉丁语「rumor」。'],
  ['klaĉo','名','闲话，流言。','源自世界语「klaĉo」。'],
  ['forto','名','力量。','源自拉丁语「fortis」。'],
  ['sento','名','情感。','源自世界语「sento」。'],
  ['sperto','名','经验。','源自世界语「sperto」。'],
  ['klasamiko','名','同学。','「klaso」+「amiko」。'],
  ['lernanto','名','学生。','「lernar」+「-anto」。'],
  ['gruo','名','鹤。','源自拉丁语「grus」。'],
  ['lonkgruo','名','纸鹤。','「lonk」+「gruo」。'],
  ['sorela','名','姐姐。','源自拉丁语「soror」变体。'],
  ['fratelo','名','哥哥。','源自拉丁语「frater」变体。'],
  ['kaprico','名','任性。','源自法语「caprice」。'],
  ['kampuso','名','校园。','源自拉丁语「campus」。'],
  ['hektaro','名','公顷。','源自法语「hectare」。'],
  ['mensa','名','食堂。','源自拉丁语「mensa」。'],
  ['oble','名','倍。','源自世界语「oble」。'],
  ['preteraĝo','名','往事。','「preter」+「-aĝo」。'],
  ['introverta','形','内向的。','源自拉丁语「introvertere」。'],
  ['timida','形','害羞的。','源自拉丁语「timidus」。'],
  ['façila','形','容易的。','源自拉丁语「facilis」。'],
  ['malfaçila','形','困难的。','「mal-」+「façila」。'],
  ['kompleksa','形','复杂的。','源自拉丁语「complexus」。'],
  ['terura','形','可怕的。','源自拉丁语「terror」。'],
  ['sekreta','形','秘密的。','源自拉丁语「secretus」。'],
  ['sekretali','副','秘密地。','「sekreta」+「-li」。'],
  ['sinmortif','动','自杀。','「sin」+「mort」+「-if」。'],
  ['trejni','动','锻炼，训练。','源自英语「train」。'],
  ['redonar','动','回赠。','「re-」+「donar」。'],
  ['laca','形','累的，疲倦的。','源自世界语「laca」。'],
  ['kunevivio','名','相处，共同生活。','「kune」+「vivio」。']
];

// 解析现有词
const lines = html.slice(rs, re).split('\n');
const words = new Set(lines.map(l => l.split('|')[0]));
let added = 0, skip = 0;
for(const [w, pos, meaning, ety] of NEW){
  if(words.has(w)){ console.log('已存在跳过:', w); skip++; continue; }
  const ipa = '/' + toIpa(w) + '/';
  lines.push(w + '|' + ipa + '|' + pos + '|' + meaning + '|' + ety);
  words.add(w); added++;
}
// 排序
function normKey(s){ return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/^[-]/,'').replace(/ç/g,'c').replace(/ĝ/g,'g').replace(/ĉ/g,'c').replace(/ʌ/g,'{').replace(/ø/g,'o').replace(/æ/g,'a').replace(/å/g,'a').replace(/ã/g,'a').replace(/ǽ/g,'a'); }
lines.sort((a,b)=>{ const x=normKey(a.split('|')[0]), y=normKey(b.split('|')[0]); return x<y?-1:x>y?1:0; });
html = html.slice(0, rs) + lines.join('\n') + html.slice(re);
fs.writeFileSync(htmlPath, html, 'utf8');
console.log('新增:', added, '| 跳过:', skip, '| 总词条:', lines.length);
// 打印新词音标供核对
for(const [w,pos,meaning,ety] of NEW){ if(words.has(w)) console.log(w, '/', toIpa(w), '/', pos, meaning.slice(0,8)); }
