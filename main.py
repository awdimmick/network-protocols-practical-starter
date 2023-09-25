def on_received_number(receivedNumber):
    global receiveBuffer
    receiveBuffer.append(receivedNumber)
    if len(receiveBuffer) == 8:
        processReceiveBuffer()
        receiveBuffer = []
radio.on_received_number(on_received_number)

def showBufferOnLED():
    for index in range(4):
        led.plot_brightness(index, 0, 64 + 191 * sendBuffer[index])
        led.plot_brightness(index, 3, 64 + 191 * sendBuffer[4 + index])

def processReceiveBuffer():
    global screenInUse
    screenInUse = 1
    basic.show_number(processBitArray(receiveBuffer))
    basic.pause(200)
    screenInUse = 0

def on_button_pressed_a():
    sendBuffer[currentBit] = 0
    incrementCurrentBit()
input.on_button_pressed(Button.A, on_button_pressed_a)

def transmitSendBuffer():
    global sendBitIndex, currentBit, sendBuffer
    sendBitIndex = len(sendBuffer) - 1
    while sendBitIndex >= 0:
        radio.send_number(sendBuffer[sendBitIndex])
        basic.pause(200)
        sendBitIndex += -1
    currentBit = 0
    sendBuffer = []

def processBitArray(bits: List[any]):
    global byteValue
    byteValue = 0
    index = 0
    while index <= len(bits) - 1:
        byteValue = byteValue + bits[index] * 2 ** index
        index += 1
    return byteValue

def showCurrentBitOnLED():
    for index in range(4):
        led.unplot(index, 1)
        led.unplot(index, 4)
    led.plot(currentBit % 4, 1 + Math.idiv(currentBit, 4) * 3)

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

def on_gesture_shake():
    global screenInUse, currentBit, sendBuffer
    screenInUse = 0
    currentBit = 0
    sendBuffer = []
input.on_gesture(Gesture.SHAKE, on_gesture_shake)

def incrementCurrentBit():
    global currentBit
    currentBit = currentBit + 1
    if currentBit == 8:
        currentBit = 0
byteValue = 0
sendBitIndex = 0
receiveBuffer: List[number] = []
sendBuffer: List[number] = []
currentBit = 0
screenInUse = 0
screenInUse = 0
currentBit = 0
sendBuffer = []
receiveBuffer = []

def on_forever():
    if screenInUse == 0:
        showBufferOnLED()
        showCurrentBitOnLED()
basic.forever(on_forever)
