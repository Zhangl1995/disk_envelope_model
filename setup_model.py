# Import the radmc3dPy module
import radmc3dPy
import matplotlib.pylab as plb
import numpy as np
import os
import natconst

# Write the parameter file with the default parameters
# To modify the input file write in problem_params.inp
# Generic protoplanetary disk model with a simple chemistry
# Example model: A 2D envelope with density dependence on the theta coordinate in spherical grid
#radmc3dPy.analyze.writeDefaultParfile('ppdisk')

# Dust model setup with ascii input files
radmc3dPy.setup.problemSetupDust('carolina',binary=True)

# Calculate the dust temperature
os.system('radmc3d mctherm setthreads 4')
os.system('radmc3d sed incl 67 phi 30 setthreads 4')

#Making SED
#in terminal xman
radmc3d spectrum incl 45 phi 30 lambdarange 1 1500 nlam 100
radmc3d spectrum incl 45 phi 30 lambdarange 10 3000 nlam 100
radmc3d spectrum incl 45 phi 30 lambdarange 10 3000 nlam 1000


#in IDL
.r readradmc
s=readspectrum()
set_plot,'ps'
device,filename='spectrum_avthin5_45_phi30_lambdarange_1_1500_100.ps'
plotspectrum,s,dpc=240.,/jy
device,/close_file


#Make an image
radmc3dPy.image.makeImage(npix=1000,sizeau=100.,wav=3000.,incl=67,posang=80)
imag=radmc3dPy.image.readImage()
#radmc3dPy.image.plotImage(imag,au=True,dpc=240.,log=True,maxlog=5,cmap='afmhot')
radmc3dPy.image.plotImage(imag,au=True,dpc=240.,log=True,vmin=-3,vmax=-10,cmap='CMRmap',bunit='snu')
#plb.savefig('figure+e6pho.eps', bbox_inches='tight')
#plb.savefig("/Users/cagurto/Documents/Newradmc3d/version_0.39/python/model-py/figure1.png")
plb.clf()

# 2D TEMPERATURE CONTOUR (natconst.au=1.496e13)
data = radmc3dPy.analyze.readData(dtemp=True)
c = plb.contourf(data.grid.x/natconst.au, np.pi/2.-data.grid.y, data.dusttemp[:,:,0,0].T, 30)
plb.xlabel('r [AU]')
plb.ylabel(r'$\pi/2-\theta$')
plb.xscale('log')
cb = plb.colorbar(c)
cb.set_label('T [K]', rotation=270.)
c = plb.contour(data.grid.x/natconst.au, np.pi/2.-data.grid.y, data.dusttemp[:,:,0,0].T, 10, colors='k',linestyles='solid')
plb.clabel(c, inline=1, fontsize=10)
#plb.savefig('figure2Dtempcontour.eps', bbox_inches='tight')
plb.show()

# Dust density contours

data = radmc3dPy.analyze.readData(ddens=True)
c2 = plb.contourf(data.grid.x/natconst.au, np.pi/2.-data.grid.y, np.log10(data.rhodust[:,:,0,0].T), 30)
plb.xlabel('r [AU]')
plb.ylabel(r'$\pi/2-\theta$')
plb.xscale('log')
cb = plb.colorbar(c2)
cb.set_label(r'$\log_{10}{\rho}$', rotation=270.)
#plb.savefig('figure-dustdesnity.eps', bbox_inches='tight')
plb.show()

# dust opacity

opac = radmc3dPy.analyze.readOpac(ext=['silicate'])
#opac = radmc3dPy.analyze.readOpac(idust=[0])]
plb.loglog(opac.wav[0], opac.kabs[0])
plb.xlabel(r'$\lambda$ [$\mu$m]')
plb.ylabel(r'$\kappa_{\rm abs}$ [cm$^2$/g]')
plb.savefig('fig-dust-opacity.eps', bbox_inches='tight')
plb.show()

#Optical depth
#It is useful to display where the radial optical depth in the continuum at the peak of the stellar radiation field is located.

data = radmc3dPy.analyze.readData(ddens=True)
data.getTau(wav=1300)
c = plb.contour(data.grid.x/natconst.au, np.pi/2.-data.grid.y, data.taux[:,:,0].T, [1.0],  colors='w', linestyles='solid')
plb.clabel(c, inline=1, fontsize=10)
plb.savefig('fig-optdepth.eps', bbox_inches='tight')
plb.show()

#Calculates visibilities for a given set of projected baselines and position angles with Discrete Fourier Transform.

radmc3dPy.image.makeImage(npix=500,sizeau=2000.,wav=2775.,incl=45,posang=43.)
imag=radmc3dPy.image.readImage()
dat = [1,10,50]
radmc3dPy.image.radmc3dImage.getVisibility(imag,bl=dat,pa=43,dpc=240)
