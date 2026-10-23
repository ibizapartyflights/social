"""Original royalty-free house loop for reels. Usage: python3 beat.py out.wav SECONDS [BPM] [SEED]
Different SEED -> different chord progression/bass so weeks don't sound identical."""
import sys, wave, numpy as np
out=sys.argv[1]; dur=float(sys.argv[2]); bpm=float(sys.argv[3]) if len(sys.argv)>3 else 124; seed=int(sys.argv[4]) if len(sys.argv)>4 else 0
rng=np.random.default_rng(seed); sr=44100; beat=60/bpm; n=int(sr*dur); mix=np.zeros(n)
def add(sig,st,g):
    i=int(st*sr); j=min(n,i+len(sig))
    if i<n: mix[i:j]+=g*sig[:j-i]
def env(L,a,d): x=np.arange(int(sr*L))/sr; return np.minimum(1,x/a)*np.exp(-x/d)
x=np.arange(int(sr*.35))/sr; kick=np.sin(2*np.pi*np.cumsum(50+120*np.exp(-x*35))/sr)*np.exp(-x*9)
hat=np.diff(np.concatenate([[0],rng.standard_normal(int(sr*.06))]))*np.exp(-np.arange(int(sr*.06))/sr*70)
clap=rng.standard_normal(int(sr*.18))*np.exp(-np.arange(int(sr*.18))/sr*25)
progs=[([57,60,64],[53,57,60],[48,52,55],[55,59,62]),([50,53,57],[46,50,53],[53,57,60],[48,52,55]),([52,55,59],[48,52,55],[55,59,62],[50,54,57])]
prog=progs[seed%len(progs)]; mtof=lambda m:440*2**((m-69)/12)
def saw(f,L): t=np.arange(int(sr*L))/sr; return sum(np.sin(2*np.pi*f*k*t)/k for k in range(1,8))
for b in range(int(dur/beat)+1):
    st=b*beat; add(kick,st,.9); add(hat,st+beat/2,.25)
    if b%2: add(clap,st,.35)
    ch=prog[(b//4)%4]
    add(np.sin(2*np.pi*mtof(ch[0]-12)*np.arange(int(sr*beat*.45))/sr)*env(beat*.45,.005,.25),st+beat/2,.45)
    if b%4 in (0,1):
        off=0 if b%4==0 else beat*1.5
        add(sum(saw(mtof(m),beat*.5) for m in ch)/len(ch)*env(beat*.5,.004,.12),st+off,.22)
f=np.ones(n); a=int(.3*sr); z=int(1.2*sr); f[:a]=np.linspace(0,1,a); f[-z:]=np.linspace(1,0,z)
mix*=f; mix/=np.abs(mix).max()*1.12
with wave.open(out,'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.stack([mix,mix],1)*32767).astype(np.int16).tobytes())
