#!/usr/bin/env python2
#
# MIT License
# 
# Copyright (c) 2016 Anders Steen Christensen
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np

# Vector perpendicular to (v1-v2) and (v3-v2) centered in v2.
def rotation_vector(v1, v2, v3):
    J = np.cross(v2 - v3, v2 - v1) + v2
    J = (J - v2) /(np.sqrt(np.dot(J - v2, J - v2)))
    return J

# Rotate a set of vectors
def rotate(V, J, T, center=None):

    if center is not None:
        V -= center
        
    x = V[0]
    y = V[1]
    z = V[2]
    u = J[0]
    v = J[1]
    w = J[2]
    a = (u*(u*x + v*y + w*z) + (x * (v*v + w*w) - u *(v*y + w*z))*np.cos(T) + np.sqrt(u*u + v*v + w*w)*(-w*y + v*z)*np.sin(T))/(u*u + v*v + w*w)
    b = (v*(u*x + v*y + w*z) + (y * (u*u + w*w) - v *(u*x + w*z))*np.cos(T) + np.sqrt(u*u + v*v + w*w)*( w*x - u*z)*np.sin(T))/(u*u + v*v + w*w)
    c = (w*(u*x + v*y + w*z) + (z * (u*u + v*v) - w *(u*x + v*y))*np.cos(T) + np.sqrt(u*u + v*v + w*w)*(-v*x + u*y)*np.sin(T))/(u*u + v*v + w*w)
    k =  np.array([a, b, c])

#    print "k.shape=",k.shape,"center.shape=",center.shape

    if center is not None:
        k += center

    return k

# Bond angle between three coordinates
def angle(a,b,c):
    # In case numpy.dot() returns larger than 1
    # and we cannot take acos() to that number
    acos_out_of_bound = 1.0
    v1 = a - b
    v2 = c - b
    v1 = v1 / np.sqrt(v1[0]**2 + v1[1]**2 + v1[2]**2)
    v2 = v2 / np.sqrt(v2[0]**2 + v2[1]**2 + v2[2]**2)
    dot_product = np.dot(v1,v2)

    if dot_product > acos_out_of_bound:
        dot_product = acos_out_of_bound
    if dot_product < -1.0 * acos_out_of_bound:
        dot_product = -1.0 * acos_out_of_bound

    return np.arccos(dot_product)


def connect(mol, muts, bonds,n):
    
    print "n=", n
    natoms = mol.natoms 
    for mut in muts:
        natoms += mut.natoms - 2

    del_hydrogens = [x[1]-1 for x in bonds]

    output = str(natoms)
    output += "\nTS generated by Auto-TS"
    
    for i, xyz in enumerate(mol.reac_xyz):

        if i not in del_hydrogens :
	    molspp = np.array (mol.atoms[i], dtype='string')
	    molxyz =  np.array([xyz[0],xyz[1],xyz[2]],dtype='float')
            output += "\n %-2s    %20.14f %20.14f %20.14f" % \
                (mol.atoms[i], xyz[0],  xyz[1], xyz[2])
   
    for b, mut in enumerate(muts):

        mut_xyz = connect_mol_mut(mol.reac_xyz, mut.xyz, bonds[b])

        for i in range(1, mut.natoms):

	    mutspp = np.array (mut.atoms[i], dtype='string')
	    mutxyz = np.array ([mut_xyz[i][0],mut_xyz[i][1], mut_xyz[i][2]], dtype ='float')
            xyz = np.concatenate ([molxyz,mutxyz], axis=0)
	    print xyz
 
	    output += "\n %-2s    %20.14f %20.14f %20.14f" % \
            	(mut.atoms[i], mut_xyz[i][0],mut_xyz[i][1], mut_xyz[i][2])

            Fail = True
    
    #while F  ail:
#	for i in range (n):
#		for j in range (i+1,n):
#			for k in mut[i]:
			#	for l in ra


    return output

def connect_mol_mut(molecule, mutation, bond):
    """Sets the XYZ coodinates of the Mutator so they match the bond
    """

    c = bond[0] - 1
    h = bond[1] - 1

    mol = np.array(molecule)
    mut = np.array(mutation)

    anchor = mol[c]
    translation = mut[0] - anchor
    mut = mut - translation

    a = angle(mol[h], mol[c], mut[1])
    p = rotation_vector(mol[h], mol[c], mut[1])
    b1 = mol[h] - mol[c]
 
    r  = np.random.uniform(0,360)

    for i, x in enumerate(mut):

        mut[i] = rotate(x, p, a, center=mol[c])
        mut[i] = rotate(mut[i], b1,r, center=mol[c])

    return mut

 # Locate atoms in a certain spacial proximity
