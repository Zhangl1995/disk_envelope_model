# disk_envelope_model

PYTHON module for RADMC3D
(c) Attila Juhasz 2011,2012,2013,2014

Generic protoplanetary disk model with a simple chemistry + 
A 2D envelope with density dependence on the theta coordinate in spherical grid +
polar cavity created by an outflow.

    The density is given by

                Sigma(r,phi)          /   z^2    \
        rho =  ---------------- * exp| - -------- |
                Hp * sqrt(2*pi)       \   2*Hp^2 /

        Sigma - surface density
        Hp    - Pressure scale height
        Hp/r  = hrdisk * (r/rdisk)^plh

    The molecular abundance function takes into account dissociation and freeze-out of the molecules
    For photodissociation only the continuum (dust) shielding is taken into account in a way that
    whenever the continuum optical depth radially drops below a threshold value the molecular abundance
    is dropped to zero. For freeze-out the molecular abundance below a threshold temperature is decreased
    by a given fractor.
    
    
  To run the model you need to install RADMC-3D and a  folder with the following files:
  - problem_params.inp: A master parameter file containing all parameters of the model. 
  More info: http://www.ast.cam.ac.uk/~juhasz/radmc3dPyDoc/parfile.html#parfile
  - setup_model.py: Script to run the model
  - carolina.py: My model (disk+envelope+polarcavity)
  - dustkappa_silicate.inp: Dust opacity file
  
  Follow the steps in setup_model.py
  
  
