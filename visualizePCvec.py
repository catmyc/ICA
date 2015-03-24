'''
Write a tcl script for VMD, to display the eigen vectors onto the molecule structure.
Here I have to files to load into VMD first: protein.psf and prosample.pdb
'''
__Author__ = "Yuncheng Mao"
__Email__ = '''catmyc@gmail.com; maoyuncheng@mail.nankai.edu.cn'''

# The script begin with defining a process for drawing an arrow. The arrow starts from the position of the corresponding atom (alpha atom of the residue).
tclHead = '''# Adapted process from the VMD user's guide.
proc vmd_draw_arrow {mol start vector} {
    # middle is the bottom center of the cone
    set middle [vecadd $start [vecscale 0.9 $vector]]
    # end is the end of the arrow
    set end [vecadd $start $vector]
    graphics $mol cylinder $start $middle radius 0.15
    graphics $mol cone $middle $end radius 0.25
}

# load the molecule
mol delete all
mol load psf protein.psf pdb prosample.pdb

# script for drawing arrows...

'''

drawFormat = '''#-------------------------------------------------
set sel [atomselect top "residue %d and name CA"]
set start [lindex [$sel get {x y z}] 0]
set vec {%f %f %f}
draw arrow $start $vec
$sel delete
'''
drawScript = tclHead
vecscale = 10
# The eigenvectors are written as column vectors...
eigvecfile = r'D:\work\2014_Deactivation_GPCR\with_chol\eq\tICA_on_protein\eigenvec.txt'
eigenInd = int(input('Type a number, which eigenvector to draw (1-based)? '))
vec = []
for line in open(eigvecfile):
    buff = [float(f) for f in line.split()]
    vec.append(buff[eigenInd - 1])
print("Eigenvector retrieved. The eigenvector has %d coordinates." % len(vec))
for i in range(int(len(vec)/3)):
    vx = vec[3 * i] * vecscale
    vy = vec[3 * i + 1] * vecscale
    vz = vec[3 * i + 2] * vecscale
    drawScript += drawFormat % (i, vx, vy, vz) 

open('drawEigenVector_%d.tcl' % eigenInd, 'w').write(drawScript)
