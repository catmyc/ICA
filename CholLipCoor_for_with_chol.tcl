# Author: Yuncheng Mao <catmyc@gmail.com; maoyuncheng@mail.nankai.edu.cn>
#

namespace eval chol_lip_coor {
	puts "INFO: Evaluate the position of cholesterol and lipid molecule."
	puts "INFO: Minimum image is considered. With the first frame as reference, the coordinates of the closest image in latter frames are recorded rather than the original image."
	puts "INFO: PBC dimensions and the coordinates are written in a temporary file for later process."
	
	variable cholCoorArray
	variable lipCoorArray

	package require pbctools

	proc writePBC_and_coor { sel filename } {
		set ofil [open $filename a+]
		puts "INFO: Opened file $filename for writing..."
		puts "INFO IMPORTANT!!!) The first TWO columns are the dimensions of a PBC cell in x and y."
		puts "INFO IMPORTANT!!!) The latter columns are the coordinates of cholesterol or lipids."
		set nframes [molinfo top get numframes]
		set pbcTraj [pbc get -all]
		for {set i 0} {$i < $nframes} {incr i} {
			$sel frame $i
			set rawCoor [$sel get {x y z}]
			set allCoor [eval "concat $rawCoor"]
			set currentPBC [lindex $pbcTraj $i]
			set Pxy [lrange $currentPBC 0 1]
			set outputLine [concat $Pxy $allCoor]
			puts $ofil $outputLine
		}
		close $ofil
		puts "INFO: Finished writing file $filename."
	}

	# Execution
	mol load psf input.psf
	set chol [atomselect top "resname CHL1 and name O3"]
	set lip [atomselect top "lipid and name P"]
	for {set i 1} {$i <= 60} {incr i} {
		animate read dcd run.$i.dcd waitfor all
		writePBC_and_coor $chol "D:/work/2014_Deactivation_GPCR/with_chol/eq/pbc_coor_chol.dat"
		writePBC_and_coor $lip  "D:/work/2014_Deactivation_GPCR/with_chol/eq/pbc_coor_lip.dat"
		animate delete all
	}
	
#########################################################################################
# The following may never be put into use.
	proc init_chol {} {
		variable cholCoorArray
		set chol [atomselect top "resname CHL1 and name O3"]
		$chol global
		for {set i 0} {$i < [$chol num]} {
			set cholCoorArray($i) {}
		}
		for {set i 0} {$i < [$lip num]} {
			set lipCoorArray($i) {}
		}
		set chol_ind_list [$chol get index]
		set lip_ind_list [$lip get index]
		
	}
	
	proc xyimageCoor { coor pbc } {
		# return a list of coordinates in all images replicated in x-y direction
		set vx [lindex $pbc 0]
		set vy [lindex $pbc 1]
		set coorlist {}
		set left [list -$vx 0 0]
		set right [list $vx 0 0]
		set up [list 0 $vy 0]
		set down [list 0 -$vy 0]
		# create te coordination list
		lappend coorlist $coor
		set coor [vecadd $coor $left]
		lappend coorlist $coor
		set coor [vecadd $coor $up]
		lappend coorlist $coor
		set coor [vecadd $coor $right]
		lappend coorlist $coor
		set coor [vecadd $coor $right]
		lappend coorlist $coor
		set coor [vecadd $coor $down]
		lappend coorlist $coor
		set coor [vecadd $coor $down]
		lappend coorlist $coor
		set coor [vecadd $coor $left]
		lappend coorlist $coor
		set coor [vecadd $coor $left]
		lappend coorlist $coor

		# The order of recorded coordinates in all images:
		#     3 -> 4 -> 5
		#     /\        |
		#     |         \/
		#     2 <- 1    6
		#     /\        |
		#     |         \/
		#     9 <- 8 <- 7

		return $coorlist
	}

	proc minElementIndex { list } {
		# return the index of the minimum element in the list
		set count 0
		foreach l $list {
			if { $count == 0} {
				set minval $l
				set minind 0
				incr count
			} else {
				if { $l <= $min } {
					set minval $l
					set minind $count
				}
			}
		}
		return $minind
	}

	proc minDistImageCoor { imageCoorList refCoor } {
		set distList {}
		foreach coor $imageCoorList {
			lappend distList [vecdist $coor $refCoor]
		}
		set minInd [minElementIndex $distList]
		return [lindex $imageCoorList $minInd]
	}


}
