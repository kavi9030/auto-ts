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

from autots import Molecule
from autots import Mutation
from autots import connect

import random

if __name__=="__main__":

    mol = Molecule("examples/diels-alder.xyz")

    muts = [Mutation("mutations/8.xyz")]


    unique_structures =  []

    n = 2 
    new_bonds = random.sample(mol.bonds,n)
    new_muts = [random.choice(muts)for _ in range (n)]  

    for i in range(1):

        output = connect(mol,new_muts, new_bonds,n)

        filename = "TS%03i.xyz" % (i + 1)
        f = open(filename, "w")
        f.write(output)
        f.close()

        
