from gpglib import errors

from Crypto.Cipher import CAST
from Crypto.Hash import SHA
import zlib

####################
### MAPPINGS
####################

class Mapping(object):
    """
        Thin class that gives item access to some map of values
        That raises a NotImplementedError if you try to access something not defined on it
    """
    def __init__(self, typ, map):
        self.map = map
        self.type = typ

    def __getitem__(self, key):
        """Complain if key isn't known"""
        if key not in self.map:
            raise NotImplementedError("Haven't implemented %s : %s" % (self.type, key))
        return self.map[key]

class Algorithms(object):
    encryption = Mapping("Symmetric encryption algorithm",
        { 3 : CAST # CAST5
        }
    )

    hashes = Mapping("Hash Algorithm",
        { 2 : SHA # SHA-1
        }
    )

class Ciphers(object):
    key_sizes = Mapping("Cipher key size",
        { CAST : 16 # CAST5
        }
    )

class Compression(object):
    def decompress_zlib(compressed):
        # The -15 at the end is the window size.
        # It says to ignore the zlib header (because it's negative) and that the
        # data is compressed with up to 15 bits of compression.
        return zlib.decompress(compressed, -15)
    
    decompression = Mapping("Decompressor",
        { 1 : decompress_zlib
        }
    )

class Mapped(object):
    ciphers = Ciphers
    algorithms = Algorithms
    compression = Compression

####################
### MPI VALUES
####################

class Mpi(object):
    """Object to hold logic for getting multi precision integers from a region"""
    @classmethod
    def parse(cls, region):
        """Retrieve one MPI value from the region"""
        # Get the length of the MPI to read in
        raw_mpi_length = region.read('uint:16')
        
        # Read in the MPI bytes and return the resulting bitstream
        mpi_length = (raw_mpi_length + 7) / 8
        return region.read(mpi_length*8)

    @classmethod
    def consume(cls, region, algorithm):
        """Retrieve necessary MPI values from region for specified algorithm"""
        if algorithm in (1, 2, 3):
            return cls.rsa_mpis(region)
        
        elif algorithm in (16, 20):
            return cls.elgamal_mpis(region)
        
        elif algorithm == 17:
            return cls.dsa_mpis(region)
        
        else:
            raise errors.PGPException("Unknown mpi algorithm %d" % algorithm)

    @classmethod
    def rsa_mpis(cls, region):
        """n and e"""
        n = cls.parse(region)
        e = cls.parse(region)
        return dict(n=n, e=e)
    
    @classmethod
    def elgamal_mpis(cls, region):
        """p, g and y"""
        p = cls.parse(region)
        g = cls.parse(region)
        y = cls.parse(region)
        return dict(p=p, g=g, y=y)
    
    @classmethod
    def dsa_mpis(cls, region):
        """p, q, g and y"""
        p = cls.parse(region)
        q = cls.parse(region)
        g = cls.parse(region)
        y = cls.parse(region)
        return dict(p=p, q=q, g=g, y=y)