# lirc-replay
Tools to replay mode2 recorded sequences using lirc on Raspberry Pi 

This is geared primarily towards aircons and other devices which have all-at-once remote controls
which cannot be supported by lirc "as is". The command portion exceeds 64 bits in size and can never be supported in legacy lirc without a major rewrite.

1. You will need a model 3 or 4 Raspberry Pi and GPIO transmitter. The old model B, Zero and the early Pis are too slow to replay a
log LIRC sequence. You will need to set up the transmitter according to the instructions in this Raspberry Pi github issue: https://github.com/raspberrypi/linux/issues/2993

2. You will need to read the rationale and the instructions on how and what to capture at: https://primus.kot-begemot.co.uk/node/94

3. You will most likely need to patch your kernel using the supplied patch which removes a number of restrictions on replaying long sequences via the lirc driver.

4. You will then be able to replay the sequences you grabbed.
