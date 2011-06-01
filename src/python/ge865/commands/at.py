 
"""
#############
3gpp commands
#############

These would be much better off hierarchly organized.
I started going down the first pages of the reference manual, skipping the
utterly useless material at the front.  I switched at some point from the
reference manual to Telit's IP Guide and also tried to make sure that the
commands from the Jasper User Guide included.


Creating new commands
~~~~~~~~~~~~~~~~~~~~~
Defining a new AT Command is fairly simple.

Simple commands that don't take any arguments, such as GCAP should inherit
from ATCommand.  The link command processor expects a parse and format method
on commands.  parse currently creates an instance of the __Response__ from
both instances and classes subclasses from ATCommand.  The __Response__ is
already wired up to a generic object.  The Response is attached as the
'response' attribute of the command while a Link process' it.  The interesting
bit of Response is the getData method which might be overridden in order to
customize how data is presented to other python objects after it's reported by
the device.

Most commands have a few variants, which I've called 'query', 'assign', and
'inspect'.
These Commands with a format method
that inserts = and ? along with user input when necessary.  There are a number
of special classes that do slightly different things with formatting.  Some
commands use '&' and '#' as separators.

Rather than create lots of braindead classes procedurally encoding these
invariants, I've used a little python magic to help smooth the process.

The WellDefinedCommand uses some python trickery to inspect the name of the
class you've just created, and uses a normalized (uppercase) version of it as
the base command for both the 'plain', 'query', and 'assign' variants.

The __Response__ used by these new classes can be influenced in several ways.
Most commands can be implemented like this:

    >>> class MyCom(WellDefinedCommand):
    ...   "Some documentation about this command."
    ...

    >>> str(MyCom().format())
    'AT+MYCOM\\r'
    >>> str(MyCom.assign(1).format())
    'AT+MYCOM=1\\r'
    >>> str(MyCom.assign(1,2).format())
    'AT+MYCOM=1, 2\\r'
    >>> str(MyCom.query().format())
    'AT+MYCOM?\\r'
    >>> str(MyCom.inspect().format())
    'AT+MYCOM=?\\r'
    >>> str(MyCom.inspect(1).format())
    'AT+MYCOM=?1\\r'
    >>> str(MyCom.inspect(1,2).format())
    'AT+MYCOM=?1, 2\\r'



Note getData() will currently produce a blob of text in most cases.
It's unclear whether putting parsing logic in getData is better than using
some other set of classes for modeling data and grouping commands together.


"""
import re

import logging
logger = logging.getLogger(__name__)

from core import Command, ATCommand, Response, NullSettable, NullQueryable
from core import IdentCommand, WellDefinedCommand, PoundSeparatedCommand, MetaCommand



"""
Generic Modem Control
~~~~~~~~~~~~~~~~~~~~~
"""
class GCAP(ATCommand):
  """List device capabilities."""
  cmd = 'GCAP'


class CMEE(WellDefinedCommand):
  """Set/read extended error reporting."""


class X(ATCommand):
  """Extended result codes. pg 53"""
  sep = ''
  cmd = 'X'

class I(IdentCommand):
  """Identification information"""
  cmd = 'I'

class C(IdentCommand):
  """Data Carrier Detect
  """
  sep = '&'
  cmd = 'C'

class D(IdentCommand):
  """Dial"""
  sep = ''
  cmd = 'D'
  tail = '{0}'

class H(ATCommand):
  """Hangup."""
  cmd = 'D'
  sep = ''

class CGMI(PoundSeparatedCommand):
  """Manufacturer Information."""

class CGMM(PoundSeparatedCommand):
  """Manufacturer ID Code."""

class CGMR(PoundSeparatedCommand):
  """Manufacturer Revision ID."""

class CGSN(PoundSeparatedCommand):
  """Product Serial No."""

class CIMI(PoundSeparatedCommand):
  """Request internal mobile subscriber number on SIM."""

class CCID(PoundSeparatedCommand):
  """Read ICCID."""

class SPN(PoundSeparatedCommand):
  """Service provider name."""

class CEER(PoundSeparatedCommand):
  """Extended error report."""

class CEERNET(PoundSeparatedCommand):
  """Extended error report for network reject cause."""

class REGMODE(PoundSeparatedCommand):
  """Select registration operation mode."""

class SMSMODE(PoundSeparatedCommand):
  """SMS commands operation mode."""

class PLMNMODE(PoundSeparatedCommand):
  """PLMN List selection."""

class PCT(PoundSeparatedCommand):
  """Display PIN Counter."""

class SHDN(PoundSeparatedCommand):
  """Software shutdown."""

class Z(PoundSeparatedCommand):
  """Extended reset."""

class ENHRST(PoundSeparatedCommand):
  """periodic reset."""

class WAKE(PoundSeparatedCommand):
  """wake from alarm mode."""

class QTEMP(PoundSeparatedCommand):
  """query temperature overflow."""

class TEMPMON(PoundSeparatedCommand):
  """temperature monitor."""

class SGPO(PoundSeparatedCommand):
  """set general purpose output."""

class SGPI(PoundSeparatedCommand):
  """set general purpose input."""

class GPIO(PoundSeparatedCommand):
  """general purpose i/o control."""

class SLED(PoundSeparatedCommand):
  """STAT_LED_GPIO setting."""

class SLEDSAV(PoundSeparatedCommand):
  """save STAT_LED_GPIO setting."""

class E2SMSRI(PoundSeparatedCommand):
  """SMS Ring Indicator."""

class ADC(PoundSeparatedCommand):
  """analog/digital converter input."""

class DAC(PoundSeparatedCommand):
  """digital/analog converter control."""

class VAUX(PoundSeparatedCommand):
  """auxiliary voltage output control."""

class VAUXSAV(PoundSeparatedCommand):
  """#VAUX saving."""

class V24MODE(PoundSeparatedCommand):
  """V24 output pins mode."""

class V24CFG(PoundSeparatedCommand):
  """V24 output pins configuration."""

class V24(PoundSeparatedCommand):
  """V24 output pins control."""

class TXMONMODE(PoundSeparatedCommand):
  """TTY-CTM-DSP operation mode."""

class CBC(PoundSeparatedCommand):
  """battery and charger status"""

class AUTOATT(PoundSeparatedCommand):
  """GPRS Auto-attach property"""

class MSCCLASS(PoundSeparatedCommand):
  """multislot class control."""

class MON1(PoundSeparatedCommand):
  """cell monitor."""

class SERVINFO(PoundSeparatedCommand):
  """serving cell information."""

class COPSMODE(PoundSeparatedCommand):
  """+COPS mode."""

class QSS(PoundSeparatedCommand):
  """Query SIM status.
  """

class DIALMODE(PoundSeparatedCommand):
  """ATD Dialing Mode."""

class ACAL(PoundSeparatedCommand):
  """automatic call."""

class ACALEXT(PoundSeparatedCommand):
  """Extended automatic call."""

class ECAM(PoundSeparatedCommand):
  """Extended call monitoring."""

class SMOV(PoundSeparatedCommand):
  """sms overflow."""

class MBN(PoundSeparatedCommand):
  """mailbox numbers."""

class MWI(PoundSeparatedCommand):
  """message waiting indicator."""

class CODEC(PoundSeparatedCommand):
  """audio codec."""

class SHFEC(PoundSeparatedCommand):
  """handsfree echo canceller."""

class HSMICG(PoundSeparatedCommand):
  """handset microphone gain."""

class SPKMUT(PoundSeparatedCommand):
  """speaker mute control."""

class HFRECG(PoundSeparatedCommand):
  """handsfree receiver gain."""

class HSRECG(PoundSeparatedCommand):
  """handset receiver gain."""

class NITZ(PoundSeparatedCommand):
  """network timezone."""

class CCLK(PoundSeparatedCommand):
  """clock management."""

class ENS(PoundSeparatedCommand):
  """enhanced network selection."""

class BND(PoundSeparatedCommand):
  """select band."""

class AUTOBND(PoundSeparatedCommand):
  """automatic band selection."""

class SKIPESC(PoundSeparatedCommand):
  """skip escape sequence."""

class E2ESC(PoundSeparatedCommand):
  """escape sequence guard time."""

class GAUTH(PoundSeparatedCommand):
  """pPP-GPRS connection authentication type."""

class GPPPCFG(PoundSeparatedCommand):
  """PPP-GPRS parameters configuration."""

class RTCSTAT(PoundSeparatedCommand):
  """RTC status."""

class GSMAD(PoundSeparatedCommand):
  """GSM Antenna Detection."""

class SIMDET(PoundSeparatedCommand):
  """SIM Detection mode."""

class ENHSIM(PoundSeparatedCommand):
  """SIM Enhanced speed."""

class SNUM(PoundSeparatedCommand):
  """subscriber number."""

class SIMATR(PoundSeparatedCommand):
  """sim answer to reset."""

class CPUMODE(PoundSeparatedCommand):
  """cpu clock mode."""

class GSMCONT(PoundSeparatedCommand):
  """GSM context definition."""

class GSMCONTCFG(PoundSeparatedCommand):
  """IPEGSM configurations."""

class CGPADDR(PoundSeparatedCommand):
  """Inspect/show IP address.
  """

class NWSCANTMR(PoundSeparatedCommand):
  """network selection timer."""

class CESTHLCK(PoundSeparatedCommand):
  """call establishment lock."""

class CPASMODE(PoundSeparatedCommand):
  """phone activity status."""

class FASTCCID(PoundSeparatedCommand):
  """ICCID SIM file reading mode."""

class I2CWR(PoundSeparatedCommand):
  """I2C data via GPIO."""

class I2CRD(PoundSeparatedCommand):
  """I2C data from GPIO."""

class PSMRI(PoundSeparatedCommand):
  """power saving mode ring."""

class SWLEVEL(PoundSeparatedCommand):
  """software level selection."""

class CFLO(PoundSeparatedCommand):
  """command flow control."""

class CMGLCONCINDEX(PoundSeparatedCommand):
  """report concatenated SMS index."""

class CODECINFO(PoundSeparatedCommand):
  """codec information."""

class SII(PoundSeparatedCommand):
  """second interface instance."""

class SYSHALT(PoundSeparatedCommand):
  """system turn-off."""

class ENAUSIM(PoundSeparatedCommand):
  """enable USIM application."""

class SIMINCFG(PoundSeparatedCommand):
  """SIMN pin configuration."""

class LANG(PoundSeparatedCommand):
  """select language."""

class CAPD(WellDefinedCommand):
  """Postpone alarm."""

class CCWE(WellDefinedCommand):
  """Call meter maxmimum event."""

class CSDF(WellDefinedCommand):
  """setting date fromat."""

class CSIL(WellDefinedCommand):
  """silence command."""

class CSTF(WellDefinedCommand):
  """setting time format."""

class CTFR(WellDefinedCommand):
  """call deflection."""

class CTZR(WellDefinedCommand):
  """time-zone reporting."""

class CTZU(WellDefinedCommand):
  """automatic time zone update."""

class CSIM(WellDefinedCommand):
  """generic SIM access."""

class CAP(PoundSeparatedCommand):
  """change audio path."""

class AXE(PoundSeparatedCommand):
  """AXE pin reading."""

class SRS(PoundSeparatedCommand):
  """select ringer sound."""

class SRP(PoundSeparatedCommand):
  """select ringer path."""

class HFMICG(PoundSeparatedCommand):
  """hands free microphone gain."""

class HSMICG(PoundSeparatedCommand):
  """handset microphone gain."""

class HFRECG(PoundSeparatedCommand):
  """handsfree receiver gain."""

class SHFSD(PoundSeparatedCommand):
  """set handsfree side tone."""

class SHSSD(PoundSeparatedCommand):
  """set handset side tone."""

"""
ALSO seen here:

SPKMUT


"""

class OAP(PoundSeparatedCommand):
  """open audio path."""

class STM(PoundSeparatedCommand):
  """signaling tones mode."""

class TONE(PoundSeparatedCommand):
  """tone playback."""

class TONEEXT(PoundSeparatedCommand):
  """extended tone generation."""

class TSVOL(PoundSeparatedCommand):
  """tone classes volume."""

class UDTSET(PoundSeparatedCommand):
  """UDTSET command."""

class UDTSAV(PoundSeparatedCommand):
  """UDTSAV command."""

class UDTRST(PoundSeparatedCommand):
  """UDTRST command."""




class CMUX(WellDefinedCommand):
  """Multiplexing Mode

  Set command is used to enable/disable the 3GPP TS 27.010 multiplexing
  protocol control channel.
  AT+CMUX= <mode> [,<subset>]
  Parameters:

    * <mode> multiplexer transparency mechanism
      0 - basic option; it is currently the only supported value.

    * <subset>
      0 - UIH frames used only; it is currently the only supported value.
  Note: after entering the Multiplexed Mode an inactive timer of five seconds
  starts. If no CMUX control channel is established before this inactivity
  timer
  expires the engine returns to AT Command Mode
  Note: all the CMUX protocol parameter are fixed as defined in GSM07.10
  and cannot be changed.
  AT+CMUX?
  AT+CMUX=?
  Reference
  3.5.4.1.8.
  Note: the maximum frame size is fixed: N1=128
  Read command returns the current value of <mode> and <subset>
  parameters, in the format:
  +CMUX: <mode>,<subset>
  Test command returns t


    >>> str(CMUX.assign(0, 0).format())
    'AT+CMUX=0, 0\\r'
  
  """
  #class assign(NullSettable):
    #tail = '{mode},{subset}'
    
class CHUP(WellDefinedCommand):
  "Hangup call"

class CBST(WellDefinedCommand):
  """Select Bearer Service Type."""
  class assign(NullSettable):
    tail = '{speed}, {name}, {ce}'

class CRLP(WellDefinedCommand):
  """Radio Link Protocol"""
  class assign(NullSettable):
    tail = '{iws}, {mws}, {t1}, {n2}, {ver}'


class CR(WellDefinedCommand):
  """Service reporting control

  >>> str(CR.assign(1).format())
  'AT+CR=1\\r'
  """

class CRC(WellDefinedCommand):
  """Cellular result codes."""

class CSNS(WellDefinedCommand):
  """Single numbering scheme."""

class CVHU(WellDefinedCommand):
 """Sets whether ATH and drop DTR causes voice disconnect."""

class CNUM(WellDefinedCommand):
  """Get MSISDN (phone number.
  
   see also: .. py:`ENS`
  """

class COPN(WellDefinedCommand):
  """Read operator names."""

class CREG(WellDefinedCommand):
  """Network registration report.
  """


class COPS(WellDefinedCommand):
  """Operator Selection.
    >>> str(COPS.assign(1, 1, 2).format())
    'AT+COPS=1, 1, 2\\r'

  """

class CLCK(WellDefinedCommand):
  """Facility lock/unlock.
  """
  class assign(NullSettable):
    tail = '{fac}, {mode}, {passwd} {class}'

class CPWD(WellDefinedCommand):
  """change facility password.
  """
  class assign(NullSettable):
    tail = '{fac}, {oldpasswd}, {newpasswd}'

class CLIP(WellDefinedCommand):
  """Enable/disable calling line identity."""

class CLIR(WellDefinedCommand):
  """calling line identity restriction management. pg 113."""

class CLCC(WellDefinedCommand):
  """list current calls."""

class CSSN(WellDefinedCommand):
  """ss notification.
    >>> str(CSSN.assign(1,2).format())
    'AT+CSSN=1, 2\\r'
  """
  class assign(NullSettable):
    tail = '{0}, {1}'

class CPOL(WellDefinedCommand):
  """Preferred Operator List."""
  class assign(NullSettable):
    tail = '{0}, {1}, {2]'

class CPAS(WellDefinedCommand):
  """Phone activity status."""

class CFUN(WellDefinedCommand):
  """Set phone functionality."""

class CPIN(WellDefinedCommand):
  """sim/ready pin report.
  """

class CSQ(WellDefinedCommand):
  """Signal quality."""

class CIND(WellDefinedCommand):
  """Indicator control."""

class CMER(WellDefinedCommand):
  """mobile equipment event reporting."""


"""
Easy IP Operations
"""
class CGDCONT(WellDefinedCommand):
  """Set up PDP context.

  At minimum requires args:
    * cid
    * PDP type "IP" or "PPP"
    * APN
    * PDP_addr - requested IP
    * d_comp - data compressions
    * h_comp - PDP heaer compression
  """

class CGQMIN(WellDefinedCommand):
  """Miminum quality of service.
    * cid - 1..5

    * precedence - 0..3
      * 0: subscribed
      * 1: high pri
      * 2: normal
      * 3: low pri

    * delay - max delay: 0..4
      * 0: subscribed (default)
      * 1: delay class 1
      * 2: delay class 2
      * 3: delay class 3
      * 4: delay class 4

    * reliability - 0..5
      * 0: subscribed
      * 1: reliability 1 (acknowledged GTP, LLC, RLC; protected data )
      * 2: reliability 2 (unacknowledged GTP, acked LLC and RLC; protected
           data )
      * 3: reliability 3 (unacknowledged GTP and LLC, acked RLC; protected data )
      * 4: reliability 4 (unacked GTP, LLC, and RLC; protected data )
      * 5: reliability 5 (unacked GTP, LLC, and RLC; unprotected data )

    * peak -  0..9 (7.8 - 2000kbps
      * 0: subscribed
    * mean - 0..31

    Telit suggests:
    AT+CGQMIN=1,0,0,3,0,0

  """

class CGREQ(WellDefinedCommand):
  """ Request quality of service
    * cid
    * precedence
    * delay
    * reliability
    * peak
    * mean

  """

class CGEQMIN(WellDefinedCommand):
  """ Request minimum quality of service
    * cid
    * traffic class - type of app:
      * 0: conversational
      * 1: streaming
      * 2: interactive
      * 3: background
      * 4: subscribed (default)
    * maxmimum bitrate UL([0] 1..512 max kbit/s)
    * maxmimum bitrate DL([0] 1..1600 max kbit/s)
    * guaranteed bitrate UL([0] 1..512 max kbit/s)
    * guaranteed bitrate DL([0] 1..1600 max kbit/s)
    * delivery order: UMTS bearer should privde in-sequential SDU deliveries
      * 0: no
      * 1: yes
      * 2: subscribed (default)
    * max SDU size: [0] 1.1520
    * SDU error ratio
    * residual bit error ratio
    * delivery or erroneious SUDs
      * 0: no
      * 1: yes
      * 2: no detect
      * 3: subscribed value (Default)
    * transfer delay - (ms, [0], 100..4000)
    * traffic handling priority ([0] 1..3)


  Telit suggests AT+CGEQMIN=1,4,0,0,0,0,2,0,"0E0", "0E0", 3,0,0

  """

class CGEQREQ(WellDefinedCommand):
  """ Request minimum quality of service
    * cid
    * traffic class - type of app:
      * 0: conversational
      * 1: streaming
      * 2: interactive
      * 3: background
      * 4: subscribed (default)
    * maxmimum bitrate UL([0] 1..512 max kbit/s)
    * maxmimum bitrate DL([0] 1..1600 max kbit/s)
    * guaranteed bitrate UL([0] 1..512 max kbit/s)
    * guaranteed bitrate DL([0] 1..1600 max kbit/s)
    * delivery order: UMTS bearer should privde in-sequential SDU deliveries
      * 0: no
      * 1: yes
      * 2: subscribed (default)
    * max SDU size: [0] 1.1520
    * SDU error ratio
    * residual bit error ratio
    * delivery or erroneious SUDs
      * 0: no
      * 1: yes
      * 2: no detect
      * 3: subscribed value (Default)
    * transfer delay - (ms, [0], 100..4000)
    * traffic handling priority ([0] 1..3)
  """



class CGACT(WellDefinedCommand):
  """PDP Context Activate/Deactivate
    * state 0/1
    * cid x
  """


class CGATT(WellDefinedCommand):
  """Attach GPRS"""

class SCFG(WellDefinedCommand):
  """Configure TCP/IP stack with packet size and timeouts

    * connection id
    * context id
    * pkt size (minimum default - 300 bytes)
    * global timeout - inactivity (90 sec)
    * connect timeout - (60 sec in tenths of a second)
    * tx timeout - data send timeout ( 5 sec expressed in 10ths of sec)
  """
  sep = '#'

class CGDATA(WellDefinedCommand):
  """Enter/exit data state.
  """

class PACSP(WellDefinedCommand):
  """Network selection menu availability.
  """

class SGACT(PoundSeparatedCommand):
  """ Activate/Deactivate context for TCP/IP
  """

class SGACTAUTH(PoundSeparatedCommand):
  """ Set authentication
    * 0:  no auth
    * 1:  PAP auth (factory default)
    * 2:  CHAP auth
  """

class SGACTCFG(PoundSeparatedCommand):
  """ Set authentication
    * cid id: 1..5 
    * retry: 0..15
    * delay: 180-3600 (seconds) between attempts
    * urcmode: 0..1 enable unsoluted result code of IP
    

  """

class SD(PoundSeparatedCommand):
  """ Socket Dial
    * should include dns?
    * 

    * cid
    * protocol: 0 TCP, 1 UDP
    * Remote port
    * IP address
  """

class PADFWD(PoundSeparatedCommand):
  """Choose a flush character"""

class PADCMD(PoundSeparatedCommand):
  """Enabled/disable flush character command"""

class SO(PoundSeparatedCommand):
  """ resume suspencded connection
  """

class SH(PoundSeparatedCommand):
  """ close socket."""

class TCPREASS(PoundSeparatedCommand):
  """Enable/disable TCP reassembly (off default)
  """

class TCPMAXDAT(PoundSeparatedCommand):
  """Set max payload size in one datagram (in bytes).
  """

class BASE64(PoundSeparatedCommand):
  """Base64 encode/decode in/out of a socket."""

class SL(PoundSeparatedCommand):
  """Listen on a socket (TCP/IP).
    * cid
    * listen state (1/0)
    * port
  """

class SLUDP(PoundSeparatedCommand):
  """Listen on a socket. (UDP)
    * cid
    * listen state (1/0)
    * port
  """

class SS(PoundSeparatedCommand):
  """Socket Status
  """

class SA(PoundSeparatedCommand):
  """Accept incoming connection."""

"""
Enable SIM Application Toolkit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

class STIA(WellDefinedCommand):
  sep = '#'

if __name__ == '__main__':
  import doctest
  doctest.testmod()

#####
# EOF
