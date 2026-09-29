import json, os, glob, copy
S=64
SRC='mc/data/minecraft'; OUT='/home/user/shiftworld/data/minecraft'
W=SRC+'/worldgen'
def load(p): return json.load(open(p))
def rid(p,kind): return 'minecraft:'+os.path.relpath(p,f'{W}/{kind}')[:-5]

def shift(o):
  if isinstance(o,list): return [shift(v) for v in o]
  if not isinstance(o,dict): return o
  o={k:shift(v) for k,v in o.items()}
  t=o.get('type')
  if set(o)=={'absolute'}: o['absolute']+=S
  if t=='minecraft:y_clamped_gradient':
    o['from_y']+=S; o['to_y']+=S
    # codec limits from_y/to_y to [-4064, 4062]; clip while keeping the same line
    k=(o['to_value']-o['from_value'])/(o['to_y']-o['from_y'])
    for y,v,lim in (('to_y','to_value',4062),('from_y','from_value',4062)):
      if o[y]>lim: o[v]-=k*(o[y]-lim); o[y]=lim
  if t=='minecraft:noise' and o.get('y_scale',0):
    o={'type':'minecraft:shifted_noise','noise':o['noise'],'xz_scale':o['xz_scale'],'y_scale':o['y_scale'],
       'shift_x':0.0,'shift_y':-S*o['y_scale'],'shift_z':0.0}
  if t=='minecraft:shifted_noise' and o.get('y_scale',0) and isinstance(o['shift_y'],(int,float)):
    o['shift_y']-=S*o['y_scale']
  return o

# which placed features / carvers belong to nether/end biomes only
ow_feat,other_feat,ow_carv,other_carv=set(),set(),set(),set()
tags={os.path.basename(p)[:-5]:load(p)['values'] for p in glob.glob(SRC+'/tags/worldgen/biome/is_*.json')}
netherend=set(tags['is_nether'])|set(tags['is_end'])
for p in glob.glob(W+'/biome/*.json'):
  b=load(p); ne=rid(p,'biome') in netherend
  fs={f for step in b['features'] for f in step}; cs=b['carvers'] if isinstance(b['carvers'],list) else [b['carvers']]
  (other_feat if ne else ow_feat).update(fs); (other_carv if ne else ow_carv).update(c for c in cs if isinstance(c,str))
def structure_ok(d):
  if 'project_start_to_heightmap' in d: return False
  b=d.get('biomes'); b=b if isinstance(b,str) else ''
  if b.startswith('#'):
    t=load(SRC+'/tags/worldgen/biome/'+b[11:]+'.json')['values']
    return not all(x in netherend or 'nether' in x or 'end' in x for x in t)
  return True

out={}
def consider(p,kind,cond=True):
  if not cond: return
  d=load(p); n=shift(d)
  if n!=d: out[f'worldgen/{kind}/'+os.path.relpath(p,f'{W}/{kind}')]=n
for p in glob.glob(W+'/density_function/**/*.json',recursive=True):
  r=rid(p,'density_function'); consider(p,'density_function',not r.startswith(('minecraft:nether','minecraft:end')))
for p in glob.glob(W+'/placed_feature/*.json'):
  r=rid(p,'placed_feature')
  if r in other_feat and r in ow_feat: print('SHARED feature',r)
  consider(p,'placed_feature',r not in other_feat)
for p in glob.glob(W+'/configured_carver/*.json'):
  consider(p,'configured_carver',rid(p,'configured_carver') not in other_carv)
for p in glob.glob(W+'/structure/*.json'):
  consider(p,'structure',structure_ok(load(p)))
for n in ('overworld','amplified','large_biomes'):
  d=shift(load(f'{W}/noise_settings/{n}.json'))
  d['noise']['min_y']=0; d['sea_level']+=S
  out[f'worldgen/noise_settings/{n}.json']=d
d=load(SRC+'/dimension_type/overworld.json')
d.update(min_y=0,height=384,logical_height=384); d['attributes']['minecraft:visual/cloud_height']+=S
out['dimension_type/overworld.json']=d
# check other noise settings don't use changed density functions
changed={'minecraft:'+k[len('worldgen/density_function/'):-5] for k in out if 'density_function' in k}
for n in ('nether','end','caves','floating_islands'):
  s=open(f'{W}/noise_settings/{n}.json').read()
  bad=[c for c in changed if f'"{c}"' in s]
  if bad: print('WARN',n,bad[:5])
import shutil; shutil.rmtree(OUT,ignore_errors=True)
for k,v in out.items():
  p=f'{OUT}/{k}'; os.makedirs(os.path.dirname(p),exist_ok=True); json.dump(v,open(p,'w'),indent=2)
from collections import Counter; print(Counter(k.split('/')[-2] if 'density' not in k else 'density_function' for k in out))
print(sorted(k for k in out if 'structure/' in k or 'carver' in k))
