const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const {createCanvas}=require('@napi-rs/canvas');
global.OffscreenCanvas=function(w,h){return createCanvas(w,h)};
const B=require('babylonjs');
require('babylonjs-loaders');
class Headless extends B.NullEngine {runRenderLoop(fn){this.testLoop=fn}setHardwareScalingLevel(){}getDeltaTime(){return 16}}
const Wrapped={...B,Engine:Headless};
const els=new Map();const el=id=>{if(!els.has(id))els.set(id,{id,hidden:false,checked:false,value:'',style:{},textContent:'',addEventListener(){},replaceChildren(){},append(){},classList:{toggle(){}},options:[]});return els.get(id)};
const context={console,BABYLON:Wrapped,document:{getElementById:el,activeElement:null,hidden:false,createElement:()=>({style:{},append(){},classList:{toggle(){}}})},localStorage:{getItem:()=>null},crypto:require('crypto').webcrypto,devicePixelRatio:1,addEventListener(){},performance,Date,Math,URL,URLSearchParams,setTimeout,clearTimeout,matchMedia:()=>({matches:false}),location:{href:'http://localhost/'}};
vm.createContext(context);const source=fs.readFileSync('index.html','utf8').match(/<script>([\s\S]*?)<\/script>/)[1].replace(/boot\(\);\s*$/,'');vm.runInContext(source,context);
vm.runInContext('B=BABYLON; buildWorld();',context);
console.log('World created:',vm.runInContext('scene.meshes.length',context),'meshes');
for(const type of ['rocket','flower','chakri','anar','phuljhadi','ladi']){vm.runInContext(`receiveEffect({id:'test-${type}',uid:'test',type:'${type}',x:0,z:0,seed:42,at:now()-200});updateEffects(.016);`,context)}
for(let i=0;i<30;i++)vm.runInContext('tick()',context);
assert(vm.runInContext('particles.length>0',context));assert(vm.runInContext('particles.length<=360',context));
vm.runInContext("receiveEffect({id:'bad',type:'rocket',x:100000,z:0,at:now()});",context);assert(!vm.runInContext("eventSeen.has('bad')",context));
console.log('PASS: world construction, frame loop, all six effect paths, bounds validation and particle budget.');
(async()=>{
context.manifestData=JSON.parse(fs.readFileSync('assets/manifest.json'));
vm.runInContext('manifest=manifestData',context);
for(const a of context.manifestData.avatars){
const bytes=fs.readFileSync(a.file),len=bytes.readUInt32LE(12),gltf=JSON.parse(bytes.subarray(20,20+len).toString());
const binary=bytes.subarray(28+len);gltf.buffers[0].uri='data:application/octet-stream;base64,'+binary.toString('base64');
const container=await B.SceneLoader.LoadAssetContainerAsync('','data:'+JSON.stringify(gltf),vm.runInContext('scene',context),undefined,'.gltf');
context.loaded=container;context.avatarId=a.id;
vm.runInContext('templates.set(avatarId,Promise.resolve(loaded))',context);
const model=await vm.runInContext("makeAvatar(avatarId,'Test Player')",context);
assert.equal(Object.keys(model.joints).length,4,'four animated joints');
const limits=model.root.getHierarchyBoundingVectors();assert(limits.max.y>2 && limits.max.y<3,'human-sized avatar');
for(const n of model.root.getDescendants())assert(!n.position||Number.isFinite(n.position.y));
model.dispose();console.log('PASS: GLB loaded and avatar instantiated:',a.id);
}
vm.runInContext('engine.dispose()',context);
})().catch(e=>{console.error(e);process.exitCode=1});
