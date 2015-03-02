# Tcl codes for abstracting the trajectory of protein in a serie trajectories
# Author: Yuncheng Mao < catmyc AT gmail.com ; maoyuncheng AT mail.nankai.edu.cn >

set ifWrittenPSF 0
set pieceCount 0
set pro {}

proc init { psffile } {
	mol new $psffile
}

proc protrajCore { dcdfile interval } {
	set start [expr $interval - 1]
	animate read dcd $dcdfile beg $start skip $interval waitfor all
	global ifWrittenPSF
	global pro
	global pieceCount	
	if { $ifWrittenPSF == 0 } {
		puts "INFO) Write protein psf file!"
		set pro [atomselect top "protein"]
		$pro writepsf protein.psf
		$pro global
		incr ifWrittenPSF
	}
	set nframes [molinfo top get numframes]
	for { set i 0 } { $i < $nframes } { incr i } {
		$pro frame $i
		$pro writepdb ProPiece.$pieceCount.pdb
		incr pieceCount
	}
	animate delete all
}

proc creatDCD { outputname } {
	global pieceCount
	mol delete all
	mol load psf protein.psf
	for { set i 0 } { $i < $pieceCount } { incr i } {
		animate read pdb ProPiece.$i.pdb waitfor all
#		somehow the deletion fails. comment it out.
#		file delete ProPiece.$i.pdb
	}
	animate write dcd $outputname.dcd
	puts "WARNING) Protein traj is not aligned. Use trajectory tool to align!"
}

# The following won't work until the selection feature is OK in animate function of VMD
proc protrajCoreUnix { dcdfile interval } {
	set start [expr $interval - 1]
	animate read dcd $dcdfile beg $start skip $interval waitfor all
	global ifWrittenPSF
	global pro
	global pieceCount	
	if { $ifWrittenPSF == 0 } {
		puts "INFO) Write protein psf file!"
		set pro [atomselect top "protein"]
		$pro writepsf protein.psf
	}
	animate write dcd ProPiece.$pieceCount.dcd sel protein
	incr pieceCount
	animate delete all
}

proc creatDCDUnix { outputname } {
	global pieceCount
	mol delete all
	mol load psf protein.psf
	for { set i 0 } { $i <= $pieceCount } { incr i } {
		animate read dcd ProPiece.$i.dcd waitfor all
		file delete ProPiece.$i.dcd
	}
	animate write dcd $outputname.dcd
	puts "INFO) File $outputname.dcd written."
}

#-------execution----------
init input.psf
set dcdSkip 1

# Uncomment the following if working on Win platform
for { set i 1 } { $i <= 60 } { incr i } {
	protrajCore run.$i.dcd $dcdSkip
}
creatDCD protraj_all


#---------END of Program----------------
quit

