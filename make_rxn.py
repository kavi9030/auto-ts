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

#from autots import Molecule
#from autots import Mutation
#from autots import connect

from molecule import Molecule
from mutation import Mutation
from utils import connect

import random
import os

if __name__=="__main__":

    mol = Molecule("examples/DA.xyz")

    ewg_dir = "mutations/EWG/" 
    edg_dir = "mutations/EDG/" 

    ewg_files = [Mutation(ewg_dir+f) for f in os.listdir(ewg_dir)]
    edg_files = [Mutation(edg_dir+f) for f in os.listdir(edg_dir)]

    print(ewg_files)
    print(edg_files)

    mol.bonds = [(1,7),(2,8)]
    #mol.bonds = [(6,12),(3,9)]

    unique_structures =  []

    for i in range(50):
        print('Generating',i,'...')
        # Which n mutations?
        
        # Which n mutations?
        new_ewg = random.choice(ewg_files)
        new_edg = random.choice(edg_files)
        print(new_ewg, new_edg)

        output = connect(mol, [new_edg, new_ewg], mol.bonds, 1.5)
        #output = connect(mol, [new_edg, new_ewg], mol.bonds)

        filename = "initial_p1-%04i.xyz" % (i + 1)
        f = open(filename, "w")
        f.write(output)
        f.close()

        
