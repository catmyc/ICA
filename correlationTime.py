'''
For the calculation of the correlation time of the trajectory projected onto specified direction (An independent component or \
a principle component).
'''
__Author__ = "Yuncheng Mao"
__Email__ = '''catmyc@gmail.com; maoyuncheng@mail.nankai.edu.cn'''

from vector import *
import time

class correlationTimeCalculator:
    '''
    Theoretically, it can be applied to an arbitrary degree of  freedom, i.e. at least applicable to principle components!
    '''
    data = []
    projectedTraj = []
    eigenMat = []
    correlationTimes = []
    autoCorrelations = []
    nframes = 0
    ncoors = 0
    
    def __init__(self, standdata = None, eigenfile = None):
        '''
        Reading standardized data.
        One can decide whether the eigenvector file shall be read or not.
        '''
        '''
        Read standdata or not.
        '''
        if standdata == None:
            return None
        else:
            self.standdataReader(standdata)
        '''
        Read eigenvectors or not.
        '''
        if eigenfile == None:
            print('INFO: eigenfile not specified, will not read eigenvectors.')
        else:
            self.eigenfileReader(eigenfile)
            
    def standdataReader(self, standdata):
        infil = open(standdata, 'r')
        line = infil.readline()
        line = line.split()
        self.nframes = len(line)
        print('INFO: Data containing %d frames.' % self.nframes)
        infil.close()
        with open(standdata) as infil:
            self.ncoors = sum([1 for x in infil])
        print('INFO: Data containing %d coordinates, i.e. %d atoms.' % (self.ncoors, self.ncoors / 3))
        print('INFO: Reading data from file %s...' % standdata)
        t_beg = time.time()
        for line in open(standdata):
            buff = line.split()
            newBuff = [float(f) for f in buff]
            self.data.append(newBuff)
        print('INFO: Reading standized coordinates finished in %d seconds.' % (time.time() - t_beg))
    
    def eigenfileReader(self, eigenfile):
        print('INFO: Reading eigen vectors from file %s...' % eigenfile)
        '''
        Remember that the eigen vectors are recorded in the columns in the file. 
        Each eigen vectors will be stored in a list. 
        '''
        # initialize the eigenMat
        for i in range(self.ncoors):
            self.eigenMat.append([])
        for line in open(eigenfile):
            buff = line.split()
            for (eigenvec, ele) in zip(self.eigenMat, buff):
                eigenvec.append(float(ele))
        print('INFO: Reading eigenvectors finished.')    
          
    def calcCorrTime(self, ICindex, eigenfile = None, frameTimeStep = 0.01, ifoutputAll = False): 
        '''
        Specify which IC to calculate with ICindex parameter.
        If eigenvectors are already read into memory, eigenfile will not be read.
        Timestep unit is in nanosecond.
        ====================
        parameters:
        ICindex: which independent component to calculate;
        eigenfile: the name of the file containing the eigenvectors;
        frameTimeStep: deltaT
        ====================
        Return:
        correlation time tau;
        evolution of autocorrelation.
        '''
        ICtraj = self.projectTraj(ICindex, eigenfile)
        deltaT = frameTimeStep
        autocorrelation = []
        '''
        upsum and downsum are respectively the sums on the numerator and denominator in the autocorrelation function.
        They will be calculated at each step.
        '''
        upsum = 0
        downsum = 2E-15 # To avoid division-by-zero error
        a0 = ICtraj[0]
        t_beg = time.time()
        for a in ICtraj:
            upsum += a
            downsum += a * a
            autocorrelation.append(a0 * upsum / downsum)
        absAutoCorr = [abs(f) * deltaT for f in autocorrelation]
        tau = sum(absAutoCorr)
        print('INFO: Calculating correlation time finished in %d seconds.' % (time.time() - t_beg))
        if ifoutputAll:
            return (tau, autocorrelation)
        else:
            return tau

        
    def getEigenVector(self,ICindex, eigenfile = None):
        eigenInd = ICindex - 1
        if eigenfile == None:
            print('INFO: Will read eigenvectors from data already read in.')
            if self.eigenMat == []:
                print('ERROR: Eigen vectors have not been read in!')
                exit()
            else:
                eigenvec = self.eigenMat[eigenInd]
        else:
            print('INFO: Abstracting eigenvectors from file %s...' % eigenfile)
            eigenvec = []
            for line in open(eigenfile):
                buff = line.split()
                eigenvec.append(float(buff[eigenInd]))
        print('INFO: Specified eigen vector has been abstracted.')
        return eigenvec
    
    def projectTraj(self, ICindex, eigenfile = None):
        '''
        Project the trajectory from original coordinate space onto the specified dimension in independent component space.
        '''
        eigenvec = self.getEigenVector(ICindex, eigenfile)
        ICtraj = []
        print('INFO: Projecting original trajectory to the %dth independent component...' % ICindex)
        t_beg = time.time()
        for i in range(self.nframes):
            frame = [l[i] for l in self.data]
            ICtraj.append(vecdot(eigenvec, frame))
        print('INFO: Calculating the projection of trajectory finished in %d seconds.' % (time.time() - t_beg))
        return ICtraj
        
    
    def writeAllProjectedTraj(self, ICtrajFile = 'ProjectedTraj.dat', eigenfile = None):
        '''
        Project the trajectory from original coordinate space into the independent component space and output to file.
        ==================
        parameter: 
        ICtrajFile: specify the filename for output.
        '''
        ofil = open(ICtrajFile, 'w')
        print('INFO: Opened file %s for writing.' % ICtrajFile)
        if self.eigenMat == []:
            print('ERROR: Eigen vectors have not been read in!')
            exit()
        t_beg = time.time()
        for i in range(self.ncoors):
            ICtraj = self.projectTraj(i + 1, eigenfile)
            outputline = ('%8.5f ' * len(ICtraj) + '\n') % tuple(ICtraj)
            ofil.write(outputline)
        ofil.close()
        print('INFO: Projection finished in %d seconds.' % (time.time() - t_beg))
    
    def calcAllAutocorr(self, eigenfile = None, frameTimeStep = 0.01, outTaufile = 'correlationTime.dat', outAutocorrFile = 'All_autocorrelation.dat'):
        '''
        Require that all projected trajetory be written already!!!
        Will calculate directly from the projected trajectory.
        '''
        outTau = open(outTaufile, 'w')
        outAutocorr = open(outAutocorrFile, 'w')
        t_beg = time.time()
        for i in range(self.ncoors):
            (tau, autoCorrelation) = self.calcCorrTime(i + 1, ifoutputAll = True)
            outTau.write('%.2f\n' % tau)
            outAutocorr.write(('%8.5f ' * len(autoCorrelation) + '\n') % tuple(autoCorrelation))
        outTau.close()
        outAutocorr.close()
        print('INFO: Written correlation time to file %s.' % outTaufile)
        print('INFO: Written autocorrelation trajectory to file %s.' % outAutocorrFile)
        print('Finished in %d seconds.' % (time.time() - t_beg))
    
    def calcAllAutocorr_from_file(self, ICtrajFile = 'ProjectedTraj.dat', frameTimeStep = 0.01, outTaufile = 'correlationTime.dat', outAutocorrFile = 'All_autocorrelation.dat'):
        '''
        Calculate autocorrelation from trajectory in the independent component space.
        This function is designed in this way so that with the ProjectedTraj.dat, it can be called alone.
        Require calling self.writeAllProjectedTraj function a priori.
        '''
        print('INFO: Starting calculation of the correlation time along all the projected directions...')
        print('INFO: Will read projected trajectory from file %s.' % ICtrajFile)
        deltaT = frameTimeStep
        outTau = open(outTaufile, 'w')
        outAutocorr = open(outAutocorrFile, 'w')
        t_beg = time.time()   
        for line in open(ICtrajFile):
            buff = line.split()
            ICtraj = [float(f) for f in buff]
            autocorrelation = []
            upsum = 0
            downsum = 2E-15 # To avoid division-by-zero error
            a0 = ICtraj[0]
            for a in ICtraj:
                upsum += a
                downsum += a * a
                autocorrelation.append(a0 * upsum / downsum)
            absAutoCorr = [abs(f) * deltaT for f in autocorrelation]
            tau = sum(absAutoCorr)
            outTau.write('%.2f\n' % tau)
            outAutocorr.write(('%8.5f ' * len(autocorrelation) + '\n') % tuple(autocorrelation))
        outTau.close()
        outAutocorr.close()
        print('INFO: Finished in %d seconds.' % (time.time() - t_beg))

#=====================
# Execution
#=====================
print('-' * 15 + '> START <' + '-' * 15)
import platform
if platform.system() == 'Windows': # Test run only on windows platform
    datafile = r'D:\work\2014_Deactivation_GPCR\without_chol\eq\stand_dataMatrix.dat'
    eigenfile = r'D:\work\2014_Deactivation_GPCR\without_chol\eq\Eigenvectors.txt'
else: # Move to Linux or Mac for execution
    datafile = 'stand_dataMatrix.dat'
    eigenfile = 'Eigenvectors.txt'

# Formal process, will be enabled after debug.
corrT = correlationTimeCalculator(datafile, eigenfile)
corrT.writeAllProjectedTraj() # Very time consuming. Total running time estimated to be ~18 hours on cluster Dvorak.
corrT.calcAllAutocorr_from_file()

'''
#------ Debug ----------
#Debug requirements:
#Run the formal codes above for a while, then interrupt it with Ctrl+C.
#Now three partially written files exist:
#    ProjectedTraj.dat        ==> written by corrT.writeAllProjectedTraj(), which is interrupted by Ctrl+C
#    All_autocorrelation.dat  ==> written by corrT.calcAllAutocorr_from_file()
#    correlationTime.dat      ==> written by corrT.calcAllAutocorr_from_file()
corrT = correlationTimeCalculator()
corrT.calcAllAutocorr_from_file()
#-----------------------
'''
print('-' * 15 + '> END <' + '-' * 15)
