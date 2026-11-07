const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const {createCanvas}=require('@napi-rs/canvas');
global.OffscreenCanvas=function(w,h){return createCanvas(w,h)};
const B=require('babylonjs');
require('babylonjs-loaders');
class Headless extends B.NullEngine {runRenderLoop(fn){this.testLoop=fn}setHardwareScalingLevel(){}getDeltaTime(){return 16}}
const Wrapped={...B,Engine:Headless};
const els=new Map();const el=id=>{if(!els.has(id))els.set(id,{id,hidden:false,checked:false,value:'',style:{},textContent:'',addEventListener(){},replaceChildren(){},append(){},setAttribute(){},classList:{toggle(){}},options:[]});return els.get(id)};
const context={console,BABYLON:Wrapped,document:{getElementById:el,activeElement:null,hidden:false,querySelector:()=>el('locationTitle'),createElement:()=>({style:{},append(){},classList:{toggle(){}}})},localStorage:{getItem:()=>null},crypto:require('crypto').webcrypto,devicePixelRatio:1,addEventListener(){},performance,Date,Math,URL,URLSearchParams,setTimeout,clearTimeout,matchMedia:()=>({matches:false}),location:{href:'http://localhost/'}};
vm.createContext(context);const source=fs.readFileSync('index.html','utf8').match(/<script>([\s\S]*?)<\/script>/)[1].replace(/boot\(\);\s*$/,'');vm.runInContext(source,context);
vm.runInContext('B=BABYLON; buildWorld();',context);
console.log('World created:',vm.runInContext('scene.meshes.length',context),'meshes');
for(const type of ['rocket','flower','chakri','anar','phuljhadi','ladi']){vm.runInContext(`receiveEffect({id:'test-${type}',uid:'test',type:'${type}',x:0,z:0,seed:42,at:now()-200});updateEffects(.016);`,context)}
for(let i=0;i<30;i++)vm.runInContext('tick()',context);
assert(vm.runInContext('particles.length>0',context));assert(vm.runInContext('particles.length<=650',context));
vm.runInContext("receiveEffect({id:'bad',type:'rocket',x:100000,z:0,at:now()});",context);assert(!vm.runInContext("eventSeen.has('bad')",context));
console.log('PASS: world construction, frame loop, all six effect paths, bounds validation and particle budget.');
(async()=>{
context.manifestData=JSON.parse(fs.readFileSync('assets/manifest.json'));
vm.runInContext('manifest=manifestData',context);
for(const a of context.manifestData.avatars){
const bytes=fs.readFileSync(a.file.split('?')[0]),len=bytes.readUInt32LE(12),gltf=JSON.parse(bytes.subarray(20,20+len).toString());
const binary=bytes.subarray(28+len);gltf.buffers[0].uri='data:application/octet-stream;base64,'+binary.toString('base64');
const container=await B.SceneLoader.LoadAssetContainerAsync('','data:'+JSON.stringify(gltf),vm.runInContext('scene',context),undefined,'.gltf');
context.loaded=container;context.avatarId=a.id;
vm.runInContext('templates.set(avatarId,Promise.resolve(loaded))',context);
const model=await vm.runInContext("makeAvatar(avatarId,'Test Player')",context);
assert.equal(Object.keys(model.joints).length,13,'thirteen animated joints');
const limits=model.root.getHierarchyBoundingVectors();assert(limits.max.y>2 && limits.max.y<3,'human-sized avatar');
for(const n of model.root.getDescendants())assert(!n.position||Number.isFinite(n.position.y));
context.testModel=model;
const foot=model.joints.FootL;foot.computeWorldMatrix(true);const rest=foot.getAbsolutePosition().clone();
for(let i=0;i<20;i++)vm.runInContext('animateAvatar(testModel,RUN_SPEED,2,.016)',context);
model.root.computeWorldMatrix(true);model.root.getDescendants().forEach(n=>n.computeWorldMatrix(true));
assert(B.Vector3.Distance(rest,foot.getAbsolutePosition())>.03,'joint animation must move the foot in world space');
assert(model.joints.KneeR.rotation.x>0.1 || model.joints.KneeL.rotation.x>0.1,'running bends knees');
assert(model.joints.ElbowL.rotation.x<-.5,'running bends elbows');
model.dispose();console.log('PASS: GLB loaded and avatar instantiated:',a.id);
}

vm.runInContext("game=true;solo=true;avatar=null;keys={KeyW:true};player={x:0,z:12,yaw:Math.PI};camYaw=Math.PI;runMode=false;moveSpeed=0;",context);
for(let i=0;i<60;i++)vm.runInContext('tick()',context);
const walking=vm.runInContext('12-player.z',context);
vm.runInContext('player.z=12;runMode=true;moveSpeed=0;',context);
for(let i=0;i<60;i++)vm.runInContext('tick()',context);
const running=vm.runInContext('12-player.z',context);assert(running>walking*2.5,'run must be substantially faster than walk');
assert(vm.runInContext('cameraFrame({x:0,z:0},0,1.45,5).forward.y>.99',context),'camera can aim almost straight up');
assert(vm.runInContext('cameraFrame({x:0,z:0},0,-.8,5).forward.y<-.7',context),'camera can look down');
assert(vm.runInContext('resolveMovement(6.8,12,8,0).x<7.2',context),'cannot run through a house');
assert(vm.runInContext('resolveMovement(0,24,8,0).x>7',context),'new plaza is accessible');
vm.runInContext("clearEffects();receiveEffect({id:'timing',uid:'test',type:'rocket',x:0,z:0,seed:1,at:now()-2900});updateEffects(.016);",context);
assert.equal(vm.runInContext('effects[0].burst',context),false,'rocket must not burst at 2.9 seconds');
assert(vm.runInContext('effects[0].prop.rocket.position.y>20',context),'visible rocket climbs before burst');
vm.runInContext('effects[0].at=now()-3010;updateEffects(.016)',context);
assert(vm.runInContext('effects[0].burst && !effects[0].prop.rocket.isEnabled()',context),'rocket bursts at 3 seconds and hides its shell');
vm.runInContext("effects[0].at=now()-8100;updateEffects(.016);",context);
assert.equal(vm.runInContext('effects.length',context),0,'expired props clean up');
console.log('PASS: actual walk/run ticks, camera elevation, building collision, plaza access, 3-second rocket transition and cleanup.');
vm.runInContext('engine.dispose()',context);
})().catch(e=>{console.error(e);process.exitCode=1});
