from hashlib import md5
from array import array
from itertools import izip

class BloomFilter(object):
  def __init__(self, m, k):
    #m bits, k hash functions
    self.salts = range(k)
    self.bits = array('h', [0]*m)
    self.m = m
    self.k = k
  
  def get_hash(self, item):
    m = self.m
    bits = array('h', [0]*m)
    for salt in self.salts:
      h = md5(str((salt, item))).hexdigest()
      bits[int(h, 16) % m] = 1
    return bits
      
  def add(self, item):
    h = self.get_hash(item)
    bits = self.bits
    for i, b in enumerate(h):
      if b:
        bits[i] = 1
  
  def __contains__(self, item):
    h = self.get_hash(item)
    return all(a==b for a, b in izip(self.bits, h) if b)