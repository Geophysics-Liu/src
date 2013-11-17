try:    from rsf.cluster import *
except: from rsf.proj    import *
import pplot

# default parameters
def param(par):
    
    if(not par.has_key('ot')):       par['ot']=0.
    if(not par.has_key('nt')):       par['nt']=1
    if(not par.has_key('dt')):       par['dt']=1.
    if(not par.has_key('lt')):       par['lt']='t'
    if(not par.has_key('ut')):       par['ut']='s'
            
    if(not par.has_key('ox')):       par['ox']=0.
    if(not par.has_key('nx')):       par['nx']=1
    if(not par.has_key('dx')):       par['dx']=1.
    if(not par.has_key('lx')):       par['lx']='x'
    if(not par.has_key('ux')):       par['ux']='km'
    
    if(not par.has_key('oy')):       par['oy']=0.
    if(not par.has_key('ny')):       par['ny']=1
    if(not par.has_key('dy')):       par['dy']=1.
    if(not par.has_key('ly')):       par['ly']='y'    
    if(not par.has_key('uy')):       par['uy']='km'
     
    if(not par.has_key('oz')):       par['oz']=0.
    if(not par.has_key('nz')):       par['nz']=1
    if(not par.has_key('dz')):       par['dz']=1.
    if(not par.has_key('lz')):       par['lz']='z'
    if(not par.has_key('uz')):       par['uz']='km'

    if(not par.has_key('tmin')):     par['tmin']=par['ot']
    if(not par.has_key('tmax')):     par['tmax']=par['ot'] + (par['nt']-1) * par['dt']
    if(not par.has_key('xmin')):     par['xmin']=par['ox']
    if(not par.has_key('xmax')):     par['xmax']=par['ox'] + (par['nx']-1) * par['dx']
    if(not par.has_key('ymin')):     par['ymin']=par['oy']
    if(not par.has_key('ymax')):     par['ymax']=par['oy'] + (par['ny']-1) * par['dy']
    if(not par.has_key('zmin')):     par['zmin']=par['oz']
    if(not par.has_key('zmax')):     par['zmax']=par['oz'] + (par['nz']-1) * par['dz']

    # make room to plot acquisition
    par['zmin']=-0.025*(par['zmax']-par['zmin'])

    dx=par['xmax']-par['xmin'];
    dy=par['ymax']-par['ymin'];
    dz=par['zmax']-par['zmin'];
    dt=par['tmax']-par['tmin'];
   
    if(not par.has_key('iratio')):
        if(dx==0.0): par['iratio']=1.0
        else:        par['iratio']=1.0*(dz)/(dx)

    if(not par.has_key('iheight')):
        if(par['iratio']>=0.8): par['iheight']=10
        else:                   par['iheight']=14*par['iratio']

    if(not par.has_key('dratio')):
#        par['dratio']=par['iratio']
        par['dratio']=0.7

    if(not par.has_key('dheight')):
#       par['dheight']=par['iheight']
       par['dheight']=14*par['dratio']

    if(not par.has_key('scalebar')): par['scalebar']='n'    
    if(not par.has_key('labelattr')): par['labelattr']=' parallel2=n labelsz=6 labelfat=3 titlesz=12 titlefat=3 xll=2 ' + ' '
    
    par['labelrot0']=' parallel2=n format1=%3.0f format2=%3.0f format3=%3.0f '
    par['labelrot1']=' parallel2=n format1=%3.1f format2=%3.1f format3=%3.1f '
    par['labelrot2']=' parallel2=n format1=%3.2f format2=%3.2f format3=%3.2f '
    
# ------------------------------------------------------------
# grey 2D image
def igrey2d(custom,par):
    return '''
    grey title="" pclip=100 gainpanel=a
    min1=%g max1=%g label1=%s unit1=%s
    min2=%g max2=%g label2=%s unit2=%s
    screenratio=%g screenht=%g wantscalebar=%s
    %s
    ''' % (par['zmin'],par['zmax'],par['lz'],par['uz'],
           par['xmin'],par['xmax'],par['lx'],par['ux'],
           par['iratio'],par['iheight'],par['scalebar'],
           par['labelattr']+custom)

# grey 2D frame of a cube
def ifrm2d(index,custom,par):
    return '''
    window n3=1 f3=%d |
    grey title=""
    min1=%g max1=%g label1=%s unit1=%s
    min2=%g max2=%g label2=%s unit2=%s
    screenratio=%g screenht=%g wantscalebar=%s
    %s
    ''' % (index,
           par['zmin'],par['zmax'],par['lz'],par['uz'],
           par['xmin'],par['xmax'],par['lx'],par['ux'],
           par['iratio'],par['iheight'],par['scalebar'],
           par['labelattr']+custom)

def ifrmE2d(wfrm,wbyt,index,custom,par,xscale=0.5,yscale=0.5,shift=-11):
    Plot(wfrm+'_V',wbyt,'window n3=1 f3=0 |'+ ifrm2d(index,'',par))
    Plot(wfrm+'_H',wbyt,'window n3=1 f3=1 |'+ ifrm2d(index,'',par)) 
    pplot.p1x2(wfrm,wfrm+'_V',wfrm+'_H',xscale,yscale,shift)

def iovlE2d(out,inp,par,xscale=0.5,yscale=0.5,shift=-11):
    Plot(out+'_V',inp,'Overlay')
    Plot(out+'_H',inp,'Overlay')
    pplot.p1x2(out,out+'_V',out+'_H',xscale,yscale,shift)

# grey 2D data
def dgrey2d(custom,par):
    return '''
    grey title="" pclip=100 gainpanel=a
    min1=%g max1=%g label1=%s unit1=%s
    min2=%g max2=%g label2=%s unit2=%s
    screenratio=%g screenht=%g wantscalebar=%s
    %s
    ''' % (par['tmin'],par['tmax'],par['lt'],par['ut'],
           par['xmin'],par['xmax'],par['lx'],par['ux'],
           par['dratio'],par['dheight'],par['scalebar'],
           par['labelattr']+custom)

# wiggle 2D data
def dwigl2d(custom,par):
    return '''
    wiggle title="" pclip=100
    transp=y yreverse=y wherexlabel=t poly=y seamean=n
    min1=%g max1=%g label1=%s unit1=%s
    min2=%g max2=%g label2=%s unit2=%s
    screenratio=%g screenht=%g wantscalebar=%s
    %s
    ''' % (par['tmin'],par['tmax'],par['lt'],par['ut'],
           par['xmin'],par['xmax'],par['lx'],par['ux'],
           par['dratio'],par['dheight'],par['scalebar'],
           par['labelattr']+custom)

def egrey2d(custom,par):
    return '''
    grey title="" pclip=100
    min2=%g max2=%g label2=%s unit2=%s
    min1=%g max1=%g label1=%s unit1=%s
    screenratio=%g screenht=%g wantscalebar=%s
    %s
    ''' % (par['tmin'],par['tmax'],par['lt'],par['ut'],
           par['zmin'],par['zmax'],par['lz'],par['uz'],
           par['dratio'],par['dheight'],par['scalebar'],
           par['labelattr']+custom)

def ewigl2d(custom,par):
    return '''
    transp |
    wiggle title="" pclip=100
    transp=n yreverse=y wherexlabel=t poly=y seamean=n
    min1=%g max1=%g label1=%s unit1=%s
    min2=%g max2=%g label2=%s unit2=%s
    screenratio=%g screenht=%g wantscalebar=%s
    %s
    ''' % (par['tmin'],par['tmax'],par['lt'],par['ut'],
           par['zmin'],par['zmax'],par['lz'],par['uz'],
           par['dratio'],par['dheight'],par['scalebar'],
           par['labelattr']+custom)

# ------------------------------------------------------------
def gainall(custom,par):
    return '''
    byte gainpanel=a pclip=100 %s
    '''%custom

def frame2d(frame,movie,index,custom,par):
    Flow(movie+'_p',movie,gainall(custom,par))
    Result(frame,movie+'_p',
           'window n3=1 f3=%d |'%index
           + igrey2d(custom,par))
    
# ------------------------------------------------------------
# plot wavelet
def waveplot(custom,par):
    return '''
    graph title=""
    min2=-1 max2=+1 
    plotfat=5 plotcol=5
    label1=%s unit1=%s
    label2="" unit2=""
    screenratio=0.5 screenht=7
    %s
    ''' % (par['lt'],par['ut'],
           par['labelattr']+custom)

def waveplotE2d(wav,custom,par):

     Plot(wav+'_V',wav,
          'window n2=1 f2=0 | transp | window |'+
          waveplot(custom,par))
     Plot(wav+'_H',wav,
          'window n2=1 f2=1 | transp | window |'+
          waveplot(custom,par))

     pplot.p1x2(wav,wav+'_V',wav+'_H',0.5,0.5,-11.5)
     Result(wav,wav,'Overlay')

# ------------------------------------------------------------
def cgraph2d(custom,par):
    return '''
    graph title=""
    labelrot=n wantaxis=n yreverse=y wherexlabel=t
    min2=%g max2=%g label2=%s unit2=%s
    min1=%g max1=%g label1=%s unit1=%s
    screenratio=%g screenht=%g wantscalebar=%s
    %s
    ''' % (par['zmin'],par['zmax'],par['lz'],par['uz'],
           par['xmin'],par['xmax'],par['lx'],par['ux'],
           par['iratio'],par['iheight'],par['scalebar'],
           par['labelattr']+custom)

def bbplot2d(custom,par):
    return '''
    window n1=2 | dd type=complex | window |
    ''' + cgraph2d('plotcol=6 plotfat=2 %s'%custom,par)

def ssplot2d(custom,par):
    return '''
    window n1=2 | dd type=complex |
    ''' + cgraph2d('symbol=. plotcol=6 plotfat=15 %s'%custom,par)

def rrplot2d(custom,par):
    return '''
    window n1=2 | dd type=complex |
    ''' + cgraph2d('symbol=. plotcol=3 plotfat=5 %s'%custom,par)

def qqplot2d(custom,par):
    return '''
    window n1=2 | dd type=complex |
    ''' + cgraph2d('symbol=. plotcol=1 plotfat=5 %s'%custom,par)

# ------------------------------------------------------------
# rays plot
def rays2d(plot,hwt,fray,jray,custom,par):
    Plot(plot,hwt,
         'window squeeze=n f1=%d j1=%d | transp |'%(fray,jray)
         + cgraph2d('plotcol=5 wantaxis=n'+custom,par))

# wfts plot
def wfts2d(plot,hwt,fwft,jwft,custom,par):
    Plot(plot,hwt,
         'window squeeze=n f2=%d j2=%d | transp |'%(fwft,jwft)
         + cgraph2d('plotcol=2 wantaxis=n plotfat=2 symbol=.'+custom,par))

# contour plot
def ccont2d(custom,par):
    return '''
    contour labelrot=n wantaxis=n title=""
    min1=%g max1=%g label1=%s unit1=%s
    min2=%g max2=%g label2=%s unit2=%s
    screenratio=%g screenht=%g wantscalebar=n
    plotcol=2 plotfat=2
    %s
    ''' % (par['zmin'],par['zmax'],par['lz'],par['uz'],
           par['xmin'],par['xmax'],par['lx'],par['ux'],
           par['iratio'],par['iheight'],
        par['labelattr']+' '+custom)


# ------------------------------------------------------------
# ------------------------------------------------------------
# wavefield-over-model plot
def wom2d(wom,wfld,velo,vmean,nfrm,weight,par):
    M8R='$RSFROOT/bin/sf'
    DPT=os.environ.get('TMPDATAPATH',os.environ.get('DATAPATH'))

    wtmp = wfld + 'tmp'
    vtmp = wfld + 'vel'

    Flow(wom,[velo,wfld],
        '''
        %sscale < ${SOURCES[1]} axis=123 >%s datapath=%s/;
        '''%(M8R,wtmp,DPT) 
	+
        '''
        %sadd < ${SOURCES[0]} add=-%g |
        scale axis=123 |
        spray axis=3 n=%d o=%g d=%g
        >%s datapath=%s/;
        '''%(M8R,vmean,nfrm,0,1,vtmp,DPT) 
	+
        '''
        %sadd scale=1,%g <%s %s >${TARGETS[0]};
        '''%(M8R,weight,vtmp,wtmp) 
	+
        '''
        %srm %s %s
        '''%(M8R,wtmp,vtmp),
        stdin=0,
        stdout=0)
