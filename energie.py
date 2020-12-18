import RPi.GPIO as GPIO
import time
import sys
import datetime
import sqlite3

import utils

def message(address, conn):
  now = datetime.datetime.utcnow().isoformat()
  conn.execute('INSERT INTO energie (messaged_on, address) VALUES(?, ?)', (now, address))
  conn.commit()
  __energie(address)

def __energie(address):
  '''Signal the Energie devices based on 4-bit address:
  Light on:  1111
  Light off: 0111
  Heat on:   1110
  Heat off:  0110
  '''
  # [BOARD, BCM (GPIO)]
  pins = [[11, 17], [13, 27], [15, 22], [16, 23], [18, 24], [22, 25]]
  BOARD = 0
  BCM = 1

  # set the pins numbering mode
  mode = GPIO.getmode()
  if not mode or mode == GPIO.BOARD:
    GPIO.setmode(GPIO.BOARD)
    mode = BOARD
  elif mode == GPIO.BCM:
    mode = BCM
  else:
    print('Uknown mode: ', mode)
    exit(1)

  # Select the GPIO pins used for the encoder K0-K3 data inputs
  GPIO.setup(pins[0][mode], GPIO.OUT) # 11
  GPIO.setup(pins[2][mode], GPIO.OUT) # 15
  GPIO.setup(pins[3][mode], GPIO.OUT) # 16
  GPIO.setup(pins[1][mode], GPIO.OUT) # 13

  GPIO.setup(pins[4][mode], GPIO.OUT) # 18 - Select the signal to select ASK/FSK
  GPIO.setup(pins[5][mode], GPIO.OUT) # 22 - Select the signal used to enable/disable the modulator

  GPIO.output(pins[5][mode], False)  # 22 - Disable the modulator by setting CE pin lo

  # Set the modulator to ASK for On Off Keying by setting MODSEL pin lo
  GPIO.output(pins[4][mode], False) # 18

  bits = []
  for char in address:
    bits.append(char == "1")

  loops = int(len(bits) / 4)

  if loops >= 0:
    for i in range(loops):
      print(i, bits[4*i : 4*i + 4])

      # Set K0-K3
      GPIO.output(pins[0][mode], bits[4*i + 3])
      GPIO.output(pins[2][mode], bits[4*i + 2])
      GPIO.output(pins[3][mode], bits[4*i + 1])
      GPIO.output(pins[1][mode], bits[4*i + 0])

      time.sleep(0.1)         # let it settle, encoder requires this
      GPIO.output(pins[5][mode], True)  # 22 - Enable the modulator
      time.sleep(0.25)        # keep enabled for a period
      GPIO.output(pins[5][mode], False) # 22 - Disable the modulator

if __name__ == "__main__":
  conn = utils.get_conn()
  message(sys.argv[1], conn)
  conn.close()
  GPIO.cleanup()
