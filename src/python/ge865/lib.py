
def hexdump( src, length=8 ):
  """
  Return a string representing the bytes in src, length bytes per
  line.

  """
  if len( src ) == 0:
    return ''
  src = bytearray(src)
  result = [ ]
  digits = 4 if isinstance( src, unicode ) else 2
  for i in xrange( 0, len( src ), length ):
    s    = src[i:i+length]
    hexa = ' '.join( [ '%#04x' %  x for x in list( s ) ] )
    text = ''.join( [ chr(x) if 0x20 <= x < 0x7F else '.' \
                    for x in s ] )
    result.append( "%04X   %-*s   %s" % \
                 ( i, length * ( digits + 1 )
                 , hexa, text ) )
  return '\n'.join(result)

#####
# EOF
