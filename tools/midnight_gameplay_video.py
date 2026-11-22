import subprocess, os
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-claude-social/e4ba9ea0-3dd9-576a-999c-e4cb281a96a3/scratchpad/mid12/'
G='/root/.claude/uploads/e4ba9ea0-3dd9-576a-999c-e4cb281a96a3/df91723b-1795305059.mp4'
WEB='/root/.claude/uploads/e4ba9ea0-3dd9-576a-999c-e4cb281a96a3/3ecf2b15-ScreenRecording_11-22-2026_00-52-42_1.mov'
SEAL='/home/claude/social/assets/brand/perfil_sello_oscuro.png'
W,H=1080,1920; LIME,CYAN,INK,BLK=(200,255,46),(56,225,255),(255,255,255),(0,0,0); NAVY=(4,7,46)
PB='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'; MONO='/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'; F=ImageFont.truetype
def st(d,xy,s,f,fill,sw=7): d.text(xy,s,font=f,fill=fill,stroke_width=sw,stroke_fill=BLK)
def fit(d,s,size,maxw):
    while d.textlength(s,font=F(PB,size))>maxw: size-=4
    return F(PB,size)
def chip(d,x,y,s,f,bg,fg=BLK):
    w=d.textlength(s,font=f); d.rectangle((x,y,x+w+36,y+f.size+22),fill=bg); d.text((x+18,y+9),s,font=f,fill=fg)
PY0,PH=560,980  # gameplay panel
def ov(name,top,big,clock=None,sub=None):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    chip(d,64,150,top,F(MONO,40),LIME)
    y=230
    for s,c in big:
        f=fit(d,s,124,W-128); st(d,(64,y),s,f,c); y+=int(f.size*1.08)
    if clock: chip(d,W-64-330,PY0+140,clock,F(MONO,92),INK if clock!='00:00' else LIME)
    if sub:
        f=fit(d,sub,74,W-128); w=d.textlength(sub,font=f); st(d,((W-w)/2,PY0+PH-150),sub,f,INK,6)
    im.save(S+name+'.png')
SEG=[('a',0.0,1.4,'IBIZA AT NIGHT · POV',[("IBIZA DOESN'T",INK),('START TILL',INK),('MIDNIGHT',LIME)],'23:59',None),
     ('a2',1.4,1.4,'IBIZA AT NIGHT · POV',[("IBIZA DOESN'T",INK),('START TILL',INK),('MIDNIGHT',LIME)],'00:00',None),
     ('b',4.5,1.8,'10PM',[('10PM',LIME),('DINNER. YES,',INK),("THAT'S EARLY",INK)],None,None),
     ('c',9.5,1.8,'11PM',[('11PM',LIME),('STILL',INK),('WARMING UP',INK)],None,None),
     ('d',11.5,1.9,'12AM',[('12AM',LIME),('THE ISLAND',INK),('WAKES UP',INK)],None,None),
     ('e',25.0,1.8,'GET HOME SAFE',[('PRE-BOOK',INK),('YOUR RIDE',INK),('HOME',LIME)],None,None)]
parts=[]
for n,ss,du,top,big,clk,sub in SEG:
    ov(n,top,big,clk,sub); o=S+n+'.mp4'; parts.append(o)
    # fg: crop out sign/compass (top) and minimap (bottom-left), brighten; bg: blurred fill
    fc=(f"[0:v]setpts=PTS-STARTPTS,fps=30,eq=brightness=0.06:contrast=1.12:saturation=1.25,split[a][b];"
        f"[a]crop=812:470:50:120,scale=-2:{PH}:flags=lanczos,crop=1080:{PH},unsharp=5:5:0.6[fg];"
        f"[b]scale=-2:1920,crop=1080:1920,boxblur=30:2,eq=brightness=-0.18[bg];"
        f"[bg][fg]overlay=0:{PY0}[v];[1:v]format=rgba[t];[v][t]overlay=0:0,format=yuv420p")
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(ss),'-t',str(du),'-i',G,'-loop','1','-t',str(du),'-i',S+n+'.png',
        '-filter_complex',fc,'-an','-c:v','libx264','-crf','17','-preset','medium','-r','30',o],check=True)
# web segment: Rubén's own screen recording in a phone
du=4.6; ph_h=1180; ph_w=int(1170*ph_h/1830)//2*2; px=(W-ph_w)//2; py=520
im=Image.new('RGBA',(W,H),NAVY+(255,)); d=ImageDraw.Draw(im)
for r in range(0,H,150): d.line([(0,r+60),(W,r)],fill=(10,26,143),width=34)
d.rounded_rectangle((px-22,py-22,px+ph_w+22,py+ph_h+22),60,fill=(12,14,30),outline=CYAN,width=6)
hole=Image.new('L',(W,H),0); ImageDraw.Draw(hole).rounded_rectangle((px,py,px+ph_w,py+ph_h),40,fill=255)
im.putalpha(Image.eval(hole,lambda v:255-v))
d=ImageDraw.Draw(im); chip(d,64,150,'PLAN IT IN ONE PLACE',F(MONO,40),LIME)
st(d,(64,230),"IT'S ALL ON",fit(d,"IT'S ALL ON",112,W-128),INK); st(d,(64,350),'OUR WEBSITE',fit(d,'OUR WEBSITE',112,W-128),LIME)
f=fit(d,'ibizapartyflights.co.uk',66,W-128); w=d.textlength('ibizapartyflights.co.uk',font=f); st(d,((W-w)/2,1745),'ibizapartyflights.co.uk',f,INK,5)
im.save(S+'web.png')
subprocess.run(['ffmpeg','-v','error','-y','-i',WEB,'-loop','1','-t',str(du),'-i',S+'web.png','-filter_complex',
  f"[0:v]setpts=(PTS-STARTPTS)/2,fps=30,crop=1170:1830:0:0,scale={ph_w}:{ph_h}:flags=lanczos,pad={W}:{H}:{px}:{py}:color=0x04072E[v];[v][1:v]overlay=0:0,format=yuv420p",
  '-t',str(du),'-an','-c:v','libx264','-crf','17','-r','30',S+'web.mp4'],check=True); parts.append(S+'web.mp4')
# end card on brand waves (own graphics)
du=2.6; im=Image.new('RGB',(W*2,H),(10,26,143)); d=ImageDraw.Draw(im)
import math
for y0 in range(-150,H+150,150): d.line([(x,y0+46*math.sin(2*math.pi*x/360)) for x in range(0,W*2+8,8)],fill=(49,80,255),width=34)
im.save(S+'endbg.png')
o=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(o)
d.rectangle((40,520,W-40,1330),fill=(4,7,46,225))
s=Image.open(SEAL).convert('RGBA').resize((220,220)); m=Image.new('L',(220,220),0); ImageDraw.Draw(m).ellipse((0,0,219,219),fill=255); s.putalpha(m); o.paste(s,(80,570),s)
st(d,(80,820),'FOLLOW FOR MORE',fit(d,'FOLLOW FOR MORE',104,W-170),INK); st(d,(80,945),'IBIZA 2027',F(PB,130),LIME)
chip(d,84,1120,'IBIZA 2027 · SORTED',F(MONO,46),INK); st(d,(84,1215),'@ibizapartyflights',F(PB,52),CYAN,4)
o.save(S+'end.png')
subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-t',str(du),'-i',S+'endbg.png','-loop','1','-t',str(du),'-i',S+'end.png','-filter_complex',
  "[0:v]crop=1080:1920:'mod(n*6,360)':0[v];[v][1:v]overlay=0:0,format=yuv420p",'-t',str(du),'-c:v','libx264','-crf','17','-r','30',S+'end.mp4'],check=True); parts.append(S+'end.mp4')
open(S+'list.txt','w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',S+'list.txt','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-r','30','-movflags','+faststart',S+'reel_midnight_DRAFT_tiktok.mp4'],check=True)
print('ok')
