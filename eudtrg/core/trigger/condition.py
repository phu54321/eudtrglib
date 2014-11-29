from ..allocator import SCMemAddr, Evaluate


class Condition(SCMemAddr):

    '''
    Condition class.

    Memory layout:

     ======  =============  ========  ===========
     Offset  Field name     Position  EPD Player
     ======  =============  ========  ===========
       +00   locid           dword0   EPD(cond)+0
       +04   player          dword1   EPD(cond)+1
       +08   amount          dword2   EPD(cond)+2
       +0C   unitid          dword3   EPD(cond)+3
       +0E   comparison
       +0F   condtype
       +10   restype         dword4   EPD(cond)+4
       +11   flags
       +12   internal[2]
     ======  =============  ========  ===========
    '''

    def __init__(self, locid, player, amount, unitid,
                 comparison, condtype, restype, flags):

        super().__init__(self)
        self._locid = locid
        self._player = player
        self._amount = amount
        self._unitid = unitid
        self._comparison = comparison
        self._condtype = condtype
        self._restype = restype
        self._flags = flags

        self._parenttrg = None
        self._condindex = None

    def Disable(self):
        self._flags |= 2

    # -------

    def SetParentTrigger(self, trg, index):
        assert self._parenttrg is None, (
            'Condition cannot be shared by two triggers. '
            'Deep copy each conditions')

        assert trg is not None, 'Trigger should not be null.'
        assert 0 <= index < 16, 'WTF'

        self._parenttrg = trg
        self._condindex = index

    def Evaluate(self):
        assert self._parenttrg is not None, 'Orphan condition'
        return Evaluate(self._parenttrg) + 8 + self._condindex * 20

    def WritePayload(self, pbuffer):
        pbuffer.WritePack(
            'IIIHBBBBH',
            self._locid,
            self._player,
            self._amount,
            self._unitid,
            self._comparison,
            self._condtype,
            self._restype,
            self._flags,
            0
        )