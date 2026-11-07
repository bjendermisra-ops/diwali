import json
# Deny by default. Fixed player slots bound each room to eight concurrent records.
r={'rules':{'.read':False,'.write':False}}
string=lambda n:{'.validate':f'newData.isString() && newData.val().length > 0 && newData.val().length <= {n}'}
def obj(required,fields,extra=None):
    out={'.validate':"newData.hasChildren("+json.dumps(required)+")"};out.update(fields);out['$other']={'.validate':False}
    if extra:out['.validate']+=' && '+extra
    return out
stamp={'.validate':'newData.isNumber() && newData.val() >= now - 10000 && newData.val() <= now + 5000'}
num=lambda lo,hi:{'.validate':f'newData.isNumber() && newData.val() >= {lo} && newData.val() <= {hi}'}
enum=lambda vals:{'.validate':'newData.isString() && ('+' || '.join('newData.val() === '+json.dumps(x) for x in vals)+')'}
room={'meta':{'.read':'auth != null','.write':"auth != null && !data.exists() && newData.exists() && $room.matches(/^[A-F0-9]{12}$/)",**obj(['owner','createdAt','version'],{'owner':{'.validate':'newData.val() === auth.uid'},'createdAt':stamp,'version':{'.validate':'newData.val() === 1'}})}}
exists="root.child('rooms').child($room).child('meta').exists()"
owner="root.child('rooms').child($room).child('players').child($slot).child('uid').val() === auth.uid"
member='('+' || '.join("root.child('rooms').child($room).child('players').child('%s').child('uid').val() === auth.uid"%i for i in range(8))+')'
player=obj(['uid','session','name','gender','avatar','x','z','yaw','at'],{'uid':{'.validate':'newData.val() === auth.uid'},'session':string(64),'name':string(24),'gender':enum(['woman','man','nonbinary','unspecified']),'avatar':enum(['amber','peacock','rose','indigo']),'x':num(-18,18),'z':num(-40,40),'yaw':num(-3.2,3.2),'at':stamp},"$slot.matches(/^[0-7]$/)")
player['.write']="auth != null && "+exists+" && ((!newData.exists() && data.child('uid').val() === auth.uid) || (newData.exists() && newData.child('uid').val() === auth.uid && (!data.exists() || data.child('uid').val() === auth.uid || data.child('at').val() < now - 30000)))"
room['players']={'.read':'auth != null && '+exists,'$slot':player}
base={'id':string(64),'uid':{'.validate':'newData.val() === auth.uid'},'at':stamp}
event=obj(['id','uid','at','type','x','z','seed'],{**base,'type':enum(['rocket','chakri','anar','phuljhadi','ladi','flower']),'x':num(-18,18),'z':num(-40,40),'seed':num(0,4294967295)})
event['.write']='auth != null && '+owner+" && newData.exists() && (!data.exists() || data.child('at').val() <= now - 900)"
room['events']={'.read':'auth != null && '+member,'$slot':event}
chat=obj(['id','uid','at','name','text'],{**base,'name':string(24),'text':string(240)},"newData.child('name').val() === root.child('rooms').child($room).child('players').child($slot).child('name').val()")
chat['.write']='auth != null && '+owner+" && newData.exists() && (!data.exists() || data.child('at').val() <= now - 1400)"
room['chat']={'.read':'auth != null && '+member,'$slot':chat}
pickup=obj(['uid','at'],{'uid':{'.validate':'newData.val() === auth.uid'},'at':stamp},"$type.matches(/^(rocket|chakri|anar|phuljhadi|ladi|flower)$/)")
pickup['.write']='auth != null && '+member+" && newData.exists() && (!data.exists() || data.child('at').val() <= now - 12000)"
room['pickups']={'.read':'auth != null && '+member,'$type':pickup}
r['rules']['rooms']={'$room':room}
# DM mailbox is read only by the recipient. Sender can only replace its own entry.
# Both people must currently belong to the declared room; no arbitrary-user spam.
shared="root.child('rooms').child(newData.child('room').val()).child('players')"
sender='('+' || '.join(shared+".child('%s').child('uid').val() === auth.uid"%i for i in range(8))+')'
recipient='('+' || '.join(shared+".child('%s').child('uid').val() === $recipient"%i for i in range(8))+')'
dm=obj(['id','uid','at','name','text','room'],{**base,'name':string(24),'text':string(240),'room':string(12)})
dm['.write']="auth != null && auth.uid === $sender && newData.exists() && "+sender+' && '+recipient+" && (!data.exists() || data.child('at').val() <= now - 1400)"
r['rules']['inbox']={'$recipient':{'.read':'auth != null && auth.uid === $recipient','$sender':dm}}
open('database.rules.json','w').write(json.dumps(r,indent=2)+'\n')
