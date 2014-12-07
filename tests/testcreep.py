import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))

from eudtrg import *

'''
Creep reading
'''

mapwidth, mapheight, creepaddr_epd = EUDCreateVariables(3)


@EUDFunc
def f_creepread_init():
    # Get creepmap address
    creepaddr_epd << f_epd(f_dwread_epd(EPD(0x6D0E84)))
    SetVariables(
        [mapwidth, mapheight],
        f_dwbreak(f_dwread_epd(EPD(0x57F1D4)))[0:2]
    )


@EUDFunc
def f_creepread(x, y):
    ret = EUDCreateVariables(1)

    creepindex = f_mul(y, mapwidth) + x
    creepdwordindex, creepevenodd = f_div(creepindex, 2)

    # read tile data
    creepdat_epd = creepaddr_epd + creepdwordindex
    creepdat_word0, creepdat_word1 = f_dwbreak(f_dwread_epd(creepdat_epd))[0:2]

    # select word0/word1 by evenodd
    if EUDIf(creepevenodd == 0):
        ret << creepdat_word0

    if EUDElse():
        ret << creepdat_word1

    EUDEndIf()

    return ret


'''
Main logic
'''

LoadMap('outputmap/basemap/creeptest_basemap.scx')


@EUDFunc
def main():
    # Iterate through each units.
    unitptr, unitepd = EUDCreateVariables(2)

    f_creepread_init()

    # Turbo trigger

    if EUDWhile(Always()):
        DoActions(SetDeaths(203151, SetTo, 1, 0))
        f_setcurpl(0)

        # Loop for every units
        unitptr << f_dwread_epd(EPD(0x628430))

        if EUDWhileNot(unitptr.Exactly(0)):
            unitepd << f_epd(unitptr)

            # check unittype
            # /*0x064*/ u16         unitType;
            unittype = f_dwbreak(f_dwread_epd(unitepd + (0x64 // 4)))[0]
            EUDContinueIfNot(unittype == EncodeUnit('Zerg Zergling'))

            # Get x, y coordinates of this unit.
            # uint16 unitx : unit + 0x28
            # uint16 unity : unit + 0x2A
            coord = f_dwread_epd(unitepd + (0x28 // 4))
            unitx, unity = f_dwbreak(coord)[0:2]

            # Convert coordinates to tile coordinates
            tileunitx = f_div(unitx, 32)[0]
            tileunity = f_div(unity, 32)[0]

            # creep -> continue
            creepval = f_creepread(tileunitx, tileunity)
            EUDContinueIf([creepval >= 16, creepval <= 31])

            # Slow down zergling.
            # Creating kakaru and killing them slows down zergling.
            SeqCompute([
                (EPD(0x58DC60 + 0), SetTo, unitx),
                (EPD(0x58DC60 + 4), SetTo, unity),
                (EPD(0x58DC60 + 8), SetTo, unitx),
                (EPD(0x58DC60 + 12), SetTo, unity)
            ])

            DoActions([
                CreateUnit(1, 'Kakaru (Twilight Critter)', 1, Player1),
                KillUnitAt(All, 'Kakaru (Twilight Critter)', 1, Player1)
            ])

            # Loop done. Get next unit pointer
            EUDSetContinuePoint()
            unitptr << f_dwread_epd(unitepd + (4 // 4))

        EUDEndWhile()

        EUDDoEvents()

    EUDEndWhile()


SaveMap('outputmap/creeptest.scx', main)