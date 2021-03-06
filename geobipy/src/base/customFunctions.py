import numpy as np
from numpy import issubdtype
from math import exp as mExp

def isInt(this):
    """Check whether an entry is a subtype of an int

    Parameters
    ----------
    this : variable
        Variable to check whether an int or not

    Returns
    -------
    out : bool
        Is or is not an int

    """
    return isinstance(this, (int, np.integer))

def isIntorSlice(this):
    """Check whether an entry is a subtype of an int or a slice

    Parameters
    ----------
    this : variable
        Variable to check whether an int/slice or not

    Returns
    -------
    out : bool
        Is or is not an int/slice

    """
    if (isInt(this)):
        return True
    if isinstance(this, slice):
        return True
    return any([isinstance(x,slice) for x in this])


def str_to_raw(s):
    """Helper function for latex

    Parameters
    ----------
    s : str
        String with special latex commands.

    Returns
    -------
    out : str
        String with latex special characters.

    """
    raw_map = {8:r'\b', 7:r'\a', 12:r'\f', 10:r'\n', 13:r'\r', 9:r'\t', 11:r'\v'}
    return r''.join(i if ord(i) > 32 else raw_map.get(ord(i), i) for i in s)

#def is_Numeric(num):
#    """Checks whether num is a number
#
#    Parameters
#    ----------
#    num: str
#        A string that could potentially contain a number
#
#    """
#    try:
#        float(num)
#        return True
#    except ValueError:
#        return False

def findNotNans(this):
    """Find the indicies to non NaN values.

    Parameters
    ----------
    this : array_like
        An array of numbers.

    Returns
    -------
    out : array_like
        Integer array to locations of non nans.

    """
    i = np.isnan(this)
    i ^= True
    return(np.argwhere(i).squeeze())


def findNans(this):
    """Find the indicies to NaN values.

    Parameters
    ----------
    this : array_like
        An array of numbers.

    Returns
    -------
    out : array_like
        Integer array to locations of nans.

    """
    i = np.isnan(this)
    return(np.argwhere(i).squeeze())


def getName(self, default=''):
    """Tries to obtain an attached name to a variable.

    If the variable is an object with a getName() procedure, that function will take precedence.
    If the variable does not have that procedure, a variable called name will be sought.
    If this fails, the specified default will be returned.

    Parameters
    ----------
    self : any type
        Any type of variable.

    Returns
    -------
    out : str
        A string containing the variable's name or the default.

    """
    try:
        return self.getName()
    except:
        pass

    try:
        name = self.name
        if (name is None):
            return default
        return name
    except:
        pass

    return default


def getUnits(self, default=''):
    """Tries to obtain an attached units to a variable.

    If the variable is an object with a getUnits() procedure, that function will take precedence.
    If the variable does not have that procedure, a variable called units will be sought.
    If this fails, the specified default will be returned.

    Parameters
    ----------
    self : any type
        Any type of variable.

    Returns
    -------
    out : str
        A string containing the variable's units or the default.

    """
    try:
        return self.getUnits()
    except:
        pass

    try:
        units = self.units
        if (units is None):
            return default
        return units
    except:
        pass

    return default


def getNameUnits(self, defaultName = '', defaultUnits = ''):
    """Tries to obtain any attached name and units to a variable. Any units are surrounded by round brackets.

    Parameters
    ----------
    self : any type
        Any type of variable.

    Returns
    -------
    out : str
        A string containing the variable's name and units or the defaults.

    """
    tmp = getName(self, defaultName)
    u = getUnits(self, defaultUnits)
    if (not u == ""):
        tmp += " (" + u + ")"
    return (tmp)

def cosSin1(x, y, a, p):
    """Simple function for creating tests. """
    return x * (1.0 - x) * np.cos(a * np.pi * x) * np.sin(a * np.pi * y**p)**p


def rosenbrock(x, y, a, b):
    """ Generates values from the Rosenbrock function. """
    return (a - x**2.0)**2.0 + b * (y - x**2.0)**2.0


def Inv(A):
    """Custom matrix inversion upto 2 dimensions.

    Parameters
    ----------
    A : float or ndarray of floats
        A scalar, 1D array, or 2D array.
        If A is scalar, assume it represents a diagonal matrix with constant value and take the reciprocal.
        If A is 1D, assume it is the diagonal of a matrix: take reciprocal of entries.
        If A is 2D, invert using linalg.

    Returns
    -------
    out : float or ndarray of floats
        The inversion of A.

    """

    ndim = A.ndim

    assert ndim <= 2, TypeError('The number of dimesions of A must be <= 2')

    if (A.ndim == 0):
        return 1.0 / A

    if (A.ndim == 1):
        return 1.0 / A

    if (A.ndim == 2):
        return np.linalg.inv(A)


def isNumpy(x):
    """Test that the variable is a compatible numpy type with built ins like .ndim

    Paramters
    ---------
    x : anything
        A variable to check

    Returns
    -------
    out : bool
        Whether the variable is a compatible numpy type

    """
    try:
        x.ndim
        return True
    except:
        return False


def Ax(A, x):
    """Custom matrix vector multiplication for different representations of the matrix.

    Parameters
    ----------
    A : float or ndarray of floats
        A scalar, 1D array, or 2D array.
        If A is scalar, assume it represents a diagonal matrix with constant value.
        If A is 1D, assume it represents a diagonal matrix and do an element wise multiply.
        If A is 2D, take the dot product.
    x : numpy.ndarray
        The 1D vector to multiply A with.

    Returns
    -------
    out : ndarray of floats
        Resultant matrix vector multiplication.
    """

    ndim = A.ndim

    assert ndim <= 2, TypeError('The number of dimesions of A must be <= 2')
    if (ndim == 0):
        return A * x
    if (ndim == 1):
        return A * x
    if (ndim == 2):
        return np.dot(A, x)


def Det(A, N=1.0):
    """Custom function to compute the determinant of a matrix.

    Parameters
    ----------
    A : float or ndarray of floats
        If A is 2D: Use numpy.linalg.det obtain determinant. Uses LU factorization.
        If A is 1D: Take the cumulative product of the numbers, assumes A represents a diagonal matrix.
        If A is scalar: Take the number to power N, assumes A represents a diagonal matrix with constant value.

    N : int, optional
        If A is a scalar, N is the number of elements in the constant valued diagonal.

    Returns
    -------
    out : float
        The determinant of the matrix.

    """

    ndim = A.ndim
    assert ndim <= 2, TypeError('The number of dimesions of A must be <= 2')

    if (ndim == 0):
        return A**N

    if (ndim == 1):
        return np.prod(A)

    if (ndim == 2):
        return np.linalg.det(A)


def LogDet(A, N=1.0):
    """Custom function to get the natural logarithm of the determinant.

    Parameters
    ----------
    A : float or numpy.ndarray of floats
        If A is 2D: Use linalg.to obtain determinant. Uses LU factorization.
        If A is 1D: Take the cumulative product of the numbers, assumes A represents a diagonal matrix.
        If A is scalar: Take the number to power N, assumes A represents a diagonal matrix with constant value.

    N : int, optional
        If A is a scalar, N is the number of elements in the constant valued diagonal.

    Returns
    -------
    out : float
        The logged determinant of the matrix.

    """

    ndim = A.ndim
    assert ndim <= 2, TypeError('The number of dimesions of A must be <= 2')

    if (ndim == 0):
        return np.log(A**N)

    if (ndim == 1):
        return np.float64(np.linalg.slogdet(np.diag(A))[1])

    if (ndim == 2):
        d = np.linalg.slogdet(A)
        return d[0] * d[1]


def splitComplex(this):
    """Splits a vector of complex numbers into a vertical concatenation of the real and imaginary components.

    Parameters
    ----------
    this : numpy.ndarray of complex128
        1D array of complex numbers.

    Returns
    -------
    out : numpy.ndarray of float64
        Vertically concatenated real then imaginary components of this.

    """
    n2 = this.size
    N = 2*n2
    out = np.ndarray(N, dtype=np.float64)
    out[:n2] = np.real(this)
    out[n2:] = np.imag(this)
    return out


def mergeComplex(this):
    """Merge a 1D array containing a vertical concatenation of N real then N imaginary components   into an N/2 complex 1D array.

    Parameters
    ----------
    this : numpy.ndarray of float64
        1D array containing the vertical concatentation of real then imaginary values.

    Returns
    -------
    out : numpy.ndarray of complex128
        The combined real and imaginary components into a complex 1D array.

    """
    N = this.size
    n2 = (N / 2)
    out = np.ndarray(n2, dtype=np.complex128)
    out = this[:n2] + 1j * this[n2:]
    return out


def expReal(this):
    """Custom exponential of a number to allow a large negative exponent, overflow truncates without warning message.

    Parameters
    ----------
    this : float
        Real number to take exponential to.

    Returns
    -------
    out : float
        exp(this).

    """
    return np.float128(0.0) if this < -746.0 else np.float128(np.exp(this))


def tanh(this):
    """ Custom hyperbolic tangent, return correct overflow. """
#    return np.tanh(this)
    tmp = np.exp(-2.0 * this)
    that = (np.divide((1.0 - tmp), (1.0 + tmp)))
    return that


def _logSomething(values,log=None):
    """Take the log of something with the given base.
    
    Uses mask arrays for robustness and warns when masking occurs
    Also returns a LateX string of log_{base} so that auto labeling is easier.

    Parameters
    ----------
    values : array_like
        Take the log of these values.
    log : 'e' or float, optional
        Take the log of the colour to base 'e' if log = 'e', and a number e.g. log = 10.
        Values in c that are <= 0 are masked.

    Returns
    -------
    out : array_like
        The logged values

    """

    if log is None:
        return values, ''

    assert not isinstance(log, bool), TypeError('log must be either "e" or a number')
    

    # Let the user know that values were masked in order to take the log
    if (np.nanmin(values) <= 0.0):
        print(Warning('Values <= 0.0 have been masked before taking their log'))

    if (log == 'e'):
        return np.log(values),'ln'

    assert log > 0, ValueError('logBase must be a positive number')

    if (log == 10):
        return np.log10(values),'log$_{10}$'

    if (log == 2):
        return np.log2(values),'log$_{2}$'

    if (log > 2):
        return np.log10(values)/np.log10(log),'log$_{'+str(log)+'}$'

    assert False, ValueError("log must be 'e' or a positive number")
    
def histogramEqualize(values, nBins=256):
    """Equalize the histogram of the values so that all colours have an equal amount

    Parameters
    ----------
    values : array_like
        Values to be equalized.
    nBins : int
        Number of bins to use.

    Returns
    -------
    res : array_like
        Equalized values
    cdf : array_like
        Cumulative Density Function.

    """

    # get image histogram
    tmp = values.flatten()
    i = np.isfinite(tmp)
    flat = tmp[i]
    H, bins = np.histogram(flat, nBins, normed=True)
    cdf = H.cumsum() # cumulative distribution function
    cdf = (nBins-1) * cdf / cdf[-1] # normalize

    # use linear interpolation of cdf to find new pixel values
    equalized = np.interp(tmp, bins[:-1], cdf)
    # Reapply any nans
    equalized[~i] = np.nan
    # Apply any masks from isfinite
    try:
        equalized = np.ma.masked_array(equalized,i.mask)
    except:
        pass

    # Get the centers of the bins
    tmp=bins[:-1]+0.5*np.diff(bins)

    # Scale back the equalized image to the bounds of the histogram
    a1=np.nanmin(equalized)
    b1=tmp.min()
    b2=tmp.max()
    # Shifting the vector so that min(x) == 0
    equalized -= a1
    # Scaling to the range of [0, 1]
    equalized /= np.nanmax(equalized)
    # Scaling to the needed amplitude
    equalized *= (b2 - b1)
    # Shifting to the needed level
    equalized += b1

    res = values.copy()
    res[:] = equalized.reshape(values.shape)

    return res, cdf


def safeEval(string):
    
    if ('NdArray' in string):
        string = string.replace('NdArray', 'StatArray')
        return string
    if ('EmLoop' in string):
        string = string.replace('EmLoop', 'CircularLoop')
        return string
    
    allowed = ('StatArray', 'Histogram', 'Model1D', 'Hitmap', 'TdemDataPoint', 'FdemDataPoint', 'TdemSystem', 'FdemSystem', 'CircularLoop')  

    if (any(x in string for x in allowed)):
        return string

    raise  ValueError("Problem evaluating string "+string)