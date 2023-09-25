# processReceiveBuffer() is the function that you need to modify.
# 
# This function is called when a byte of data is received.
# 
# Setting screenInUse to 1 pauses the background process that shows the current state of the sendBuffer on the micro:bit's LEDs. Setting it back to 0 will resume the display.

def on_button_pressed_ab():
    global screenInUse
    if len(sendBuffer) == 8:
        screenInUse = 1
        basic.show_leds("""
            . . # . .
            . . . # .
            # # # # #
            . . . # .
            . . # . .
            """)
        transmitSendBuffer()
        basic.show_leds("""
            . . . . #
            . . . # .
            # . # . .
            . # . . .
            . . . . .
            """)
        basic.pause(500)
        basic.clear_screen()
        screenInUse = 0
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def on_button_pressed_b():
    sendBuffer[currentBit] = 1
    incrementCurrentBit()
input.on_button_pressed(Button.B, on_button_pressed_b)

def showBufferOnLED():
    for index in range(4):
        led.plot_brightness(index, 0, 64 + 191 * sendBuffer[index])
        led.plot_brightness(index, 3, 64 + 191 * sendBuffer[4 + index])
"""

processReceiveBuffer() is the function that you should modify to determine what your micro:bit should do once a byte of data has been received. 

You could write your handling code directly in here, or create new functions to call.

Setting screenInUse to 1 "takes over" the screen and disables the background process that shows the state of the sendBuffer on the micro:bit's LED display. Setting it back to 0 releases the screen once again.

"""
def processReceiveBuffer():
    global screenInUse
    screenInUse = 1
    basic.show_number(decodeBitArray(receiveBuffer))
    basic.pause(200)
    basic.clear_screen()
    screenInUse = 0
def decodeBitArray(bits: List[any]):
    global byteValue
    byteValue = 0
    index2 = 0
    while index2 <= len(bits) - 1:
        byteValue = byteValue + bits[index2] * 2 ** (7 - index2)
        index2 += 1
    return byteValue

def on_button_pressed_a():
    sendBuffer[currentBit] = 0
    incrementCurrentBit()
input.on_button_pressed(Button.A, on_button_pressed_a)

def decodeHighNibble(bits2: List[number]):
    global nibbleValue
    nibbleValue = 0
    for index3 in range(4):
        nibbleValue = nibbleValue + bits2[index3] * 2 ** (3 - index3)
    return nibbleValue
def transmitSendBuffer():
    global currentBit, sendBuffer
    for index4 in range(8):
        radio.send_number(sendBuffer[index4])
        basic.pause(200)
    currentBit = 0
    sendBuffer = []

def on_received_number(receivedNumber):
    global receiveBuffer
    receiveBuffer.append(receivedNumber)
    if len(receiveBuffer) == 8:
        processReceiveBuffer()
        receiveBuffer = []
radio.on_received_number(on_received_number)

def showCurrentBitOnLED():
    for index32 in range(4):
        led.unplot(index32, 1)
        led.unplot(index32, 4)
    led.plot(currentBit % 4, 1 + Math.idiv(currentBit, 4) * 3)

def on_gesture_shake():
    global screenInUse, currentBit, sendBuffer
    screenInUse = 0
    currentBit = 0
    sendBuffer = []
input.on_gesture(Gesture.SHAKE, on_gesture_shake)

def decodeLowNibble(bits3: List[number]):
    global nibbleValue
    nibbleValue = 0
    for index5 in range(4):
        nibbleValue = nibbleValue + bits3[index5 + 4] * 2 ** (3 - index5)
    return nibbleValue
def incrementCurrentBit():
    global currentBit
    currentBit = currentBit + 1
    if currentBit == 8:
        currentBit = 0
"""

Each micro:bit in your group must be using the same radio group value.

Update this value before downloading your code and loading onto your micro:bits!

"""
nibbleValue = 0
byteValue = 0
receiveBuffer: List[number] = []
sendBuffer: List[number] = []
currentBit = 0
screenInUse = 0
radio.set_group(0)
screenInUse = 0
currentBit = 0
sendBuffer = []
receiveBuffer = []

def on_forever():
    if screenInUse == 0:
        showBufferOnLED()
        showCurrentBitOnLED()
basic.forever(on_forever)
