import sys, numpy as np, cv2
from skimage import color
from scipy import ndimage as ndi
from PIL import Image
src, out, thr = sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 20
im=np.asarray(Image.open(src).convert('RGB')); H,W,_=im.shape
lab=color.rgb2lab(im/255.0)
border=np.zeros((H,W),bool); b=30; border[:b]=1; border[-b:]=1; border[:,:b]=1; border[:,-b:]=1
yy,xx=np.mgrid[0:H,0:W]; X=np.stack([np.ones(H*W),xx.ravel()/W,yy.ravel()/H,(xx.ravel()/W)**2,(yy.ravel()/H)**2,(xx.ravel()*yy.ravel())/(W*H)],1)
bgfit=np.zeros_like(lab)
for c in range(3):
    co,*_=np.linalg.lstsq(X[border.ravel()],lab[...,c].ravel()[border.ravel()],rcond=None); bgfit[...,c]=(X@co).reshape(H,W)
dab=np.hypot(lab[...,1]-bgfit[...,1],lab[...,2]-bgfit[...,2]); dL=np.abs(lab[...,0]-bgfit[...,0])
hue=np.degrees(np.arctan2(lab[...,2],lab[...,1])); hbg=np.degrees(np.arctan2(bgfit[...,2],bgfit[...,1]))
dh=np.abs((hue-hbg+180)%360-180); chroma=np.hypot(lab[...,1],lab[...,2])
shadowlike=(dh<25)&(chroma>33)
score=np.where(shadowlike,0.0,dab+0.35*dL)
lighter=(lab[...,0]>bgfit[...,0]+9)
score=np.where(lighter,np.maximum(score,40),score)
fg=score>thr
lbl,n=ndi.label(~fg); keep=np.unique(np.concatenate([lbl[0],lbl[-1],lbl[:,0],lbl[:,-1]])); keep=keep[keep>0]
fgm=~np.isin(lbl,keep); fgm=ndi.binary_opening(fgm,iterations=1)
lbl2,n2=ndi.label(fgm); sizes=ndi.sum(fgm,lbl2,range(1,n2+1)); fgm=np.isin(lbl2,1+np.where(sizes>max(600,0.05*sizes.max()))[0])
soft=np.clip((score-(thr-8))/16,0,1); alpha=cv2.GaussianBlur((fgm*np.maximum(soft,(score>thr+8))).astype(np.float32),(0,0),0.8)
a=im.astype(np.float32)/255
# despill blue on edges
r,g,bl=a[...,0],a[...,1],a[...,2]; spill=np.clip(bl-np.maximum(r,g)-0.04,0,1)*(alpha<0.98)
a[...,2]-=spill*0.7
o=Image.fromarray(np.dstack([np.clip(a,0,1)*255,alpha*255]).astype(np.uint8),'RGBA')
bb=Image.fromarray((alpha*255).astype(np.uint8)).point(lambda v:255 if v>30 else 0).getbbox(); o=o.crop(bb); o.save(out)
for name,col in (('navy',(10,26,143)),('white',(240,240,240))):
    bgim=Image.new('RGBA',o.size,col+(255,)); bgim.alpha_composite(o); bgim.convert('RGB').resize((o.size[0]//2,o.size[1]//2)).save(out.replace('.png','_'+name+'.png'))
print(bb)
