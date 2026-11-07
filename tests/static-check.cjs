const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const html=fs.readFileSync('index.html','utf8');new vm.Script(html.match(/<script>([\s\S]*?)<\/script>/)[1]);
const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);assert.equal(ids.length,new Set(ids).size,'duplicate DOM IDs');
for(const m of html.matchAll(/\$\('([^']+)'\)/g))assert(ids.includes(m[1]),'Missing DOM ID '+m[1]);
const manifest=JSON.parse(fs.readFileSync('assets/manifest.json'));
for(const a of manifest.avatars){const b=fs.readFileSync(a.file.split('?')[0]);assert.equal(b.readUInt32LE(0),0x46546c67);assert.equal(b.readUInt32LE(8),b.length);const doc=JSON.parse(b.subarray(20,20+b.readUInt32LE(12)).toString());for(const key of ['ArmL','ArmR','LegL','LegR'])assert(doc.nodes.some(n=>n.name===key));assert(doc.materials.length>=6);}
for(const f of Object.values(manifest.sounds))assert.equal(fs.readFileSync(f).subarray(0,4).toString(),'OggS');
const rules=JSON.parse(fs.readFileSync('database.rules.json'));assert.equal(rules.rules['.read'],false);assert.equal(rules.rules['.write'],false);
assert(!html.includes('innerHTML=m.text'));console.log('PASS: JS syntax, DOM wiring, four GLB assets, seven sound assets, rules JSON.');
