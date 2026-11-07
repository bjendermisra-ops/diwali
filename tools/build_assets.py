"""Original festive avatar meshes and synthesized SFX; Python standard library only.
Run from repository root. Optional ffmpeg converts WAVs to small Ogg assets.
"""
import math, struct, json, pathlib, wave, random, subprocess
P=pathlib.Path('assets'); (P/'models').mkdir(parents=True,exist_ok=True); (P/'audio').mkdir(exist_ok=True)
def avatar(filename, outfit, longhair=False):
    blob=bytearray(); views=[]; access=[]; meshes=[]; nodes=[]; materials=[]
    def acc(vals,kind,components):
        while len(blob)%4: blob.append(0)
        off=len(blob); flat=[v for row in vals for v in row] if components>1 else vals
        blob.extend(struct.pack('<'+('f' if kind==5126 else 'H')*len(flat),*flat)); views.append({'buffer':0,'byteOffset':off,'byteLength':len(blob)-off})
        a={'bufferView':len(views)-1,'componentType':kind,'count':len(vals),'type':{1:'SCALAR',3:'VEC3'}[components]}
        if components==3:a.update(min=[min(v[i] for v in vals) for i in range(3)],max=[max(v[i] for v in vals) for i in range(3)])
        access.append(a); return len(access)-1
    colors={'skin':[.70,.40,.24,1],'cloth':outfit,'gold':[.98,.66,.19,1],'hair':[.045,.025,.026,1],'white':[.95,.93,.86,1],'dark':[.028,.019,.025,1],'rose':[.63,.11,.16,1],'shoe':[.16,.065,.028,1]}
    for name,c in colors.items():materials.append({'name':name,'pbrMetallicRoughness':{'baseColorFactor':c,'metallicFactor':.55 if name=='gold' else 0,'roughnessFactor':.38 if name=='gold' else .82}})
    def geom(shape,mat):
        pos=[]; norm=[]; inds=[]; N=20; rings=12
        for j in range(rings+1):
            t=j/rings
            for i in range(N+1):
                a=i/N*math.tau
                if shape=='sphere':
                    q=t*math.pi; v=[math.sin(q)*math.cos(a),math.cos(q),math.sin(q)*math.sin(a)]; n=v[:]
                else:
                    r=(.72+.28*t) if shape=='skirt' else (1-.2*t); v=[r*math.cos(a),1-2*t,r*math.sin(a)]; n=[math.cos(a),.1,math.sin(a)]
                pos.append(v);norm.append(n)
        for j in range(rings):
            for i in range(N):
                a=j*(N+1)+i; b=a+N+1; inds.extend([a,a+1,b,a+1,b+1,b])
        meshes.append({'primitives':[{'attributes':{'POSITION':acc(pos,5126,3),'NORMAL':acc(norm,5126,3)},'indices':acc(inds,5123,1),'material':list(colors).index(mat)}]});return len(meshes)-1
    cache={}
    def node(name,pos=(0,0,0),scale=(1,1,1),shape=None,mat='cloth',parent=None):
        n={'name':name,'translation':list(pos),'scale':list(scale)}
        if shape:
            key=(shape,mat)
            if key not in cache:cache[key]=geom(*key)
            n['mesh']=cache[key]
        nodes.append(n); idx=len(nodes)-1
        if parent is not None:nodes[parent].setdefault('children',[]).append(idx)
        return idx
    root=node('FestiveAvatar')
    node('Kurta' if not longhair else 'Lehenga', (0,1.03,0),(.28,.43,.17),'skirt' if longhair else 'cylinder',parent=root)
    node('Hem',(0,.61,0),(.278,.035,.175),'cylinder','gold',root)
    node('Collar',(0,1.43,0),(.12,.045,.12),'cylinder','gold',root)
    for y in [1.32,1.20,1.08]:node('Button',(0,y,.174),(.018,.018,.012),'sphere','gold',root)
    node('Head',(0,1.75,0),(.24,.29,.215),'sphere','skin',root)
    node('Hair',(0,1.91,-.035),(.248,.16,.215),'sphere','hair',root)
    if longhair:
        node('Braid',(0,1.44,-.18),(.12,.34,.10),'sphere','hair',root)
        node('Bindi',(0,1.88,.19),(.016,.02,.012),'sphere','rose',root)
        node('Dupatta',(.19,1.12,-.05),(.10,.38,.18),'cylinder','gold',root)
    for s in [-1,1]:
        node('Ear',(s*.23,1.74,0),(.05,.065,.045),'sphere','skin',root)
        if longhair:node('Earring',(s*.25,1.64,.015),(.03,.05,.025),'sphere','gold',root)
        node('EyeWhite',(s*.086,1.79,.187),(.052,.058,.027),'sphere','white',root)
        node('Eye',(s*.086,1.79,.210),(.029,.037,.012),'sphere','dark',root)
        node('EyeLight',(s*.08,1.805,.222),(.009,.012,.005),'sphere','white',root)
        arm=node('ArmL' if s<0 else 'ArmR',(s*.33,1.37,0),parent=root)
        node('Sleeve',(0,-.16,0),(.10,.21,.11),'cylinder','cloth',arm)
        node('Cuff',(0,-.34,0),(.085,.025,.09),'cylinder','gold',arm)
        node('Hand',(0,-.43,0),(.077,.11,.076),'sphere','skin',arm)
        leg=node('LegL' if s<0 else 'LegR',(s*.13,.67,0),parent=root)
        node('Trouser',(0,-.24,0),(.095,.27,.10),'cylinder','white',leg)
        node('Jutti',(0,-.59,.055),(.10,.075,.17),'sphere','shoe',leg)
    node('Nose',(0,1.73,.215),(.035,.043,.05),'sphere','skin',root)
    node('Smile',(0,1.63,.196),(.065,.014,.018),'sphere','rose',root)
    doc={'asset':{'version':'2.0','generator':'Diwali Together original festive models'},'scene':0,'scenes':[{'nodes':[root]}],'nodes':nodes,'meshes':meshes,'materials':materials,'accessors':access,'bufferViews':views,'buffers':[{'byteLength':len(blob)}]}
    js=json.dumps(doc,separators=(',',':')).encode(); js+=b' '*((-len(js))%4);blob+=b'\0'*((-len(blob))%4)
    out=struct.pack('<III',0x46546c67,2,12+8+len(js)+8+len(blob))+struct.pack('<II',len(js),0x4e4f534a)+js+struct.pack('<II',len(blob),0x004e4942)+blob
    (P/'models'/filename).write_bytes(out)
avatar('amber-kurta.glb',[.94,.32,.065,1]);avatar('peacock-kurta.glb',[.025,.40,.42,1]);avatar('rose-lehenga.glb',[.68,.035,.23,1],True);avatar('indigo-lehenga.glb',[.18,.10,.52,1],True)
# Layered, original synthesized samples. No third-party recordings.
rng=random.Random(42); rate=24000
for kind,duration in [('rocket',2.2),('boom',2.4),('chakri',3),('anar',3),('phuljhadi',3),('ladi',2.7),('flower',2.4)]:
    frames=bytearray(); low=0.; prev=0
    for i in range(int(rate*duration)):
        t=i/rate; n=rng.uniform(-1,1);low=.96*low+.04*n; hi=n-prev;prev=n
        if kind in ['boom','flower']:
            env=math.exp(-t*3);s=(low*5+math.sin(math.tau*(53*t-5*t*t))*.32)*env+n*.35*math.exp(-t*24)
            if kind=='flower':s+=hi*.10*math.exp(-t*1.8)*(rng.random()>.88)
        elif kind=='rocket':s=(hi*.15+math.sin(math.tau*(350*t+480*t*t))*.10)*math.sin(math.pi*t/duration)**.6
        elif kind=='ladi':
            phase=t%.16;s=(n*.65+low*2)*math.exp(-phase*55)
        else:
            s=hi*.11+low*.8
            if kind=='chakri':s*=.6+.4*math.sin(math.tau*13*t);s+=math.sin(math.tau*640*t)*.035
            if kind=='anar':s+=low*.9
            if rng.random()>.996:s+=n*.35
            s*=min(1,t*20,(duration-t)*12)
        s=math.tanh(s)*.78; frames.extend(struct.pack('<h',int(s*32767)))
    path=P/'audio'/f'{kind}.wav'
    with wave.open(str(path),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(frames)
    try:
        subprocess.run(['ffmpeg','-loglevel','error','-y','-i',str(path),'-c:a','libvorbis','-q:a','4',str(path.with_suffix('.ogg'))],check=True);path.unlink()
    except FileNotFoundError:pass
print('Built four GLB avatars and seven original sound assets')
