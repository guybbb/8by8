import math
#import spidev
import time
from time import sleep

BLACK =  0
RED = 0xE0
GREEN  = 0x1C
BLUE  = 0x03
ORANGE  = RED|GREEN
MAGENTA =  RED|BLUE
TEAL  = BLUE|GREEN
WHITE = (RED|GREEN)-0x10
BROWN = RED|BLUE - 0X1F

def sendtogrid(purchase_price, current_price, scale_pct, demo=False):

   
    full_scale_pct = scale_pct
    ref_level = purchase_price
    current_val = current_price
    stock_sn = 0

    Matrix = [[0 for x in range(8)] for y in range(8)]
    outmatrix = []
    for stock_sn in range(8):

            #sleep(1)
            ratio = (float(current_val[stock_sn])/ref_level[stock_sn])*100-100
            resolution = (float(full_scale_pct))/4
            factor = float(ratio)/resolution
            factor = int(round(factor))
            if factor > 4:
                    factor = 4
            if factor < -4:
                    factor = -4

            trend_sign = int(math.copysign(1, factor))
            if trend_sign == -1:
                factor = factor-1
            Matrix[stock_sn] = [ 0x0 for y in range(8)]

            for idx in range(int(3.5+0.5*trend_sign),4+factor,trend_sign):
                if stock_sn == 7:
                    Matrix[stock_sn][idx] = RED

                if stock_sn == 6:
                    Matrix[stock_sn][idx] = GREEN

                if stock_sn == 5:
                    Matrix[stock_sn][idx] = BLUE

                if stock_sn == 4:
                    Matrix[stock_sn][idx] = ORANGE

                if stock_sn == 3:
                    Matrix[stock_sn][idx] = MAGENTA

                if stock_sn == 2:
                    Matrix[stock_sn][idx] = BROWN
                if stock_sn == 1:
                    Matrix[stock_sn][idx] = TEAL

                if stock_sn == 0:
                    Matrix[stock_sn][idx] = WHITE

                print(Matrix)

                outmatrix  = []

                for i in range(8):
                    for j in range(8):
                        outmatrix.append(Matrix[i][j])

    spi = spidev.SpiDev() # create spi object
    spi.open(0, 0) # open spi port 0, device (CS) 0
    resp = spi.xfer2(outmatrix) # transfer one byte
    spi.close() # . close the port

