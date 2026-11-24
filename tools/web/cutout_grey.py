import sys, numpy as np, cv2
from skimage import color
from scipy import ndimage as ndi
from PIL import Image
src,out=sys.argv[1],sys.argv[2]
im=np.asarray(Image.open(src).convert('RGB')); H,W,_=im.shape
lab=color.rgb2lab(im/255.0)
border=np.zeros((H,W),bool); b=25; border[:b]=1; border[:,:b]=1; border[:,-b:]=1; border[-b:]=1
yy,xx=np.mgrid[0:H,0:W]; X=np.stack([np.ones(H*W),xx.ravel()/W,yy.ravel()/H,(xx.ravel()/W)**2,(yy.ravel()/H)**2,(xx.ravel()*yy.ravel())/(W*H)],1)
bgfit=np.zeros_like(lab)
for c in range(3):
    co,*_=np.linalg.lstsq(X[border.ravel()],lab[...,c].ravel()[border.ravel()],rcond=None); bgfit[...,c]=(X@co).reshape(H,W)
dab=np.hypot(lab[...,1]-bgfit[...,1],lab[...,2]-bgfit[...,2]); dL=lab[...,0]-bgfit[...,0]
chroma=np.hypot(lab[...,1],lab[...,2])
# edges help: object outlines have strong gradients, bg is smooth
gray=cv2.cvtColor(im,cv2.COLOR_RGB2GRAY).astype(np.float32)
grad=cv2.GaussianBlur(np.hypot(cv2.Sobel(gray,cv2.CV_32F,1,0,ksize=3),cv2.Sobel(gray,cv2.CV_32F,0,1,ksize=3)),(0,0),1.5)
tex=cv2.GaussianBlur(np.sqrt(np.maximum(cv2.GaussianBlur(gray**2,(0,0),2)-cv2.GaussianBlur(gray,(0,0),2)**2,0)),(0,0),2)
score=dab*1.6+np.abs(dL)*0.9+(tex*0.8 if len(sys.argv)>=4 else 0)
# soft floor shadow: darker, neutral, smooth (low gradient) and in the lower part
shadow=(dL<0)&(dL>-30)&(chroma<10)&(grad<10)&(yy>H*0.6)
score=np.where(shadow,0,score)
lowgrey=(len(sys.argv)<4)&(yy>H*0.68)&(chroma<9)&(lab[...,0]>38)&(lab[...,0]<88)
score=np.where(lowgrey,0,score)
if len(sys.argv)>=4:
    legs=(yy>H*0.66)&(chroma<8)&(lab[...,0]>55)&(lab[...,0]<86)&(tex<6)
    score=np.where(legs,0,score)
fg=score>9
lbl,n=ndi.label(~fg); bs=ndi.sum(~fg,lbl,range(1,n+1)); keep=np.unique(np.concatenate([lbl[0],lbl[-1],lbl[:,0],lbl[:,-1]] + ([1+np.where(bs>350)[0]] if len(sys.argv)<4 else []))); keep=keep[keep>0]
fgm=~np.isin(lbl,keep); fgm=ndi.binary_opening(fgm,iterations=2)
lbl2,n2=ndi.label(fgm); sizes=ndi.sum(fgm,lbl2,range(1,n2+1)); fgm=np.isin(lbl2,1+np.where(sizes>max(600,0.03*sizes.max()))[0])
fgm=ndi.binary_erosion(fgm,iterations=2) if len(sys.argv)>=4 else fgm
alpha=cv2.GaussianBlur(fgm.astype(np.float32),(0,0),0.9)
o=Image.fromarray(np.dstack([im,alpha*255]).astype(np.uint8),'RGBA')
bb=Image.fromarray((alpha*255).astype(np.uint8)).point(lambda v:255 if v>30 else 0).getbbox(); o=o.crop(bb); o.save(out)
for name,col in (('navy',(10,26,143)),('white',(240,240,240))):
    bg=Image.new('RGBA',o.size,col+(255,)); bg.alpha_composite(o); bg.convert('RGB').resize((o.size[0]//2,o.size[1]//2)).save(out.replace('.png','_'+name+'.png'))
print(bb)
