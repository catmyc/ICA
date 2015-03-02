# Write each coordinate of each atom in each line. 
# The line: the time serie of a single coordinate along the trajectory file 
#
# Author: Yuncheng Mao < catmyc@gmail.com; maoyuncheng@mail.nankai.edu.cn >
#

puts "WARNING: Make sure that the protein in the trajectory file is aligned!!!"

namespace eval proCoorTraj {
	variable sel
	variable trajArr
	variable coorCount
	variable dcdname
	
	set dcdname protraj_aligned.dcd

	proc init { psffile {seltext "protein and backbone and name CA"} } {
		mol load psf $psffile
		variable sel
		set sel [atomselect top "$seltext"]
		$sel global
		set natoms [$sel num]
		variable coorCount
		set coorCount [expr 3 * $natoms]
		puts "INFO: $natoms found in selection."
		puts "INFO: $coorCount coordinates will be recorded."
		for {set i 0} {$i < $coorCount} {incr i} {
			set trajArr($i) {}
		}
	}

	proc getCoorTraj { } {
		variable sel
		variable trajArr
		variable coorCount
		set nframes [molinfo top get numframes]
		for {set i 0} {$i < $nframes} {incr i} {
			$sel frame $i
			set coorRaw [$sel get {x y z}]
			set coorFrame [eval "concat $coorRaw"]
			set j 0
			foreach f $coorFrame {
				lappend trajArr($j) $f
				incr j
			}
		}
	}

	proc writeTrajArr { filename } {
		puts "INFO: Opening file $filename for writing..."
		set ofil [open $filename w]
		variable trajArr
		variable coorCount
		puts "INFO: Writing trajectory of each coordinate..."
		for {set i 0} {$i < $coorCount} {incr i} {
			puts $ofil $trajArr($i)
		}
		close $ofil
		puts "INFO: Writing file $filename finished."
	}

	# Execution
	init protein.psf
	set nf_per_batch 10000
	puts "INFO: Processing $nf_per_batch frames per batch."
	set beg 0
	set end 59999
	for {set i $beg} {$i <= $end} {incr i $nf_per_batch} {
		animate read dcd $dcdname beg $i end [expr $i + $nf_per_batch -1] waitfor all
		puts "INFO: Reading frames $i to [expr $i + $nf_per_batch -1] completed."
		getCoorTraj
		animate delete all
	}
	writeTrajArr proCoorTraj.dat
	# End of Execution
}
