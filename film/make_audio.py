"""Original 120 BPM score, 10 bars / 20 seconds, deterministic PCM + UI effects."""
from pathlib import Path
import wave
import numpy as np
SR=48000;D=20;B=.5
rng=np.random.default_rng(7206);mix=np.zeros((SR*D,2))
def put(at,a,gain=1,pan=0):
 o=round(at*SR);n=min(len(a),len(mix)-o)
 if o<0 or n<=0:return
 angle=(pan+1)*np.pi/4
 mix[o:o+n,0]+=a[:n]*gain*np.cos(angle);mix[o:o+n,1]+=a[:n]*gain*np.sin(angle)
def note(f,d=.7,decay=6):
 t=np.arange(round(SR*d))/SR
 return (np.sin(2*np.pi*f*t+.22*np.sin(2*np.pi*2*f*t)*np.exp(-8*t))+.12*np.sin(6*np.pi*f*t))*np.minimum(t*140,1)*np.exp(-decay*t)
def kick():
 t=np.arange(round(SR*.3))/SR
 return np.sin(2*np.pi*(47*t+2*(1-np.exp(-t*32))))*np.exp(-18*t)
def noise(d,decay):
 t=np.arange(round(SR*d))/SR;n=rng.normal(0,1,len(t));n-=np.convolve(n,np.ones(9)/9,'same')
 return n*np.exp(-decay*t)
C=[130.81,164.81,196,246.94];A=[110,130.81,164.81,196];F=[87.31,130.81,174.61,220];G=[98,146.83,196,246.94]
chords=[C,A,F,G,C,A,F,G,G,C]
for bar,ch in enumerate(chords):
 start=bar*2
 for k,f in enumerate(ch):put(start,note(f*2,2.6,1.3),.04,(k-1.5)/2)
 for j in range(4):
  at=start+j*B
  if at>=18:continue
  energy=.75 if bar in [0,1,7,8] else 1
  put(at,kick(),(.31 if j%2==0 else .15)*energy)
  put(at,note(ch[0]/2,.6,5),.14*energy)
  put(at+.25,noise(.08,100),.023*energy,(-1)**j*.6)
  if j%2:put(at,noise(.12,40),.038*energy)
  for sub in range(2 if 4<=bar<=6 else 1):
   put(at+sub*.25,note(ch[(j+sub)%4]*4,.55,8),.065*energy,(-1)**(j+sub)*.45)
# Reflow landings: audible grid snap and a short air sweep.
for at in [0,2,5,8,11,14,17]:
 put(at,note(520,.3,14),.075,-.1)
 t=np.arange(round(SR*.25))/SR;n=rng.normal(0,1,len(t));n=np.convolve(n,np.ones(40)/40,'same')
 put(max(0,at-.12),n*np.sin(np.pi*t/.25)**2,.16,.25)
# UI actions and success receipts; times match draw(t).
for at in [2.75,4.25,5.55,8.55,11.6,14.75]:put(at,note(1550,.13,32),.045,.3)
for at in [6.75,9.7,12.75,14.95]:
 put(at,note(1046.5,.4,10),.075,-.15);put(at+.1,note(1568,.5,8),.055,.15)
# Air movement for paper plane; filtered to avoid a harsh hiss.
t=np.arange(round(SR*.8))/SR;n=rng.normal(0,1,len(t));n=np.convolve(n,np.ones(50)/50,'same');put(11.65,n*np.sin(np.pi*t/.8)**2,.1,.45)
# Last tonic at 18 s, then only the release, not a chopped drum phrase.
for k,f in enumerate(C):put(18,note(f*2,2,2),.06,(k-1.5)/2)
mix*=np.clip((D-np.arange(len(mix))/SR)/.8,0,1)[:,None]
mix=np.tanh(mix*1.5);mix*=.82/max(.82,np.max(np.abs(mix)))
p=Path(__file__).parent/'assets/sound.wav'
with wave.open(str(p),'wb') as w:
 w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((mix*32767).astype('<i2').tobytes())
print('20.000s / 120 BPM / first beat 0.000 / peak',round(float(np.max(np.abs(mix))),4))
