#
# Centralize and unify (i.e. standardize) the coordinates.
# Author: Yuncheng <catmyc@mgail.com; maoyuncheng@mail.nankai.edu.cn>
#

#-------------------------------
# Each line is the trajectory of one coordinate.
#

proc veccentral { vec } {
	# centralize a vector
	set mean [vecmean $vec]
	foreach l $vec {
		lappend meanvec $mean
	}
	return [vecsub $vec $meanvec]
}

# I like this object-oriented fashion when using namespace!

namespace eval ICA {
	# data is a matrix, with each row as the time-traj of a coordinate and each colum a 
	# trajectory frame
	variable data
	variable time_average
	variable centeralized
	variable prepared_data

	proc read_write { coor_traj_file outputname } {
		# normalization of data are performed while reading in.
		puts "INFO) Reading in file $coor_traj_file..."
		set infil [open $coor_traj_file r]
		puts "INFO) Write to file $outputname."
		set ofil [open $outputname w]
		while { [gets $infil line] != -1 } {
			set line [veccentral $line]
			# vecnorm is only available in VMD.
			set line [vecnorm $line]
			puts $ofil $line
		}
		close $infil
		close $ofil
		puts "INFO) Reading data finished."
		puts "INFO) Standardization finished."
	}

}

ICA::read_write dataMatrix.dat stand_dataMat.dat

