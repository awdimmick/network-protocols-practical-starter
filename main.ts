/**
 * This is the function that you need to modify. 
 * 
 * This function is called when a byte of data is received.
 * 
 * Setting screenInUse to 1 pauses the background process that shows the current state of the sendBuffer on the micro:bit's LEDs. Setting it back to 0 will resume the display.
 */
input.onButtonPressed(Button.AB, function () {
    if (sendBuffer.length == 8) {
        screenInUse = 1
        basic.showLeds(`
            . . # . .
            . . . # .
            # # # # #
            . . . # .
            . . # . .
            `)
        transmitSendBuffer()
        basic.showLeds(`
            . . . . #
            . . . # .
            # . # . .
            . # . . .
            . . . . .
            `)
        basic.pause(500)
        basic.clearScreen()
        screenInUse = 0
    }
})
input.onButtonPressed(Button.B, function () {
    sendBuffer[currentBit] = 1
    incrementCurrentBit()
})
function showBufferOnLED () {
    for (let index = 0; index <= 3; index++) {
        led.plotBrightness(index, 0, 64 + 191 * sendBuffer[index])
        led.plotBrightness(index, 3, 64 + 191 * sendBuffer[4 + index])
    }
}
function processReceiveBuffer () {
    screenInUse = 1
    basic.showNumber(processBitArray(receiveBuffer))
    basic.pause(200)
    screenInUse = 0
}
input.onButtonPressed(Button.A, function () {
    sendBuffer[currentBit] = 0
    incrementCurrentBit()
})
function transmitSendBuffer () {
    sendBitIndex = sendBuffer.length - 1
    while (sendBitIndex >= 0) {
        radio.sendNumber(sendBuffer[sendBitIndex])
        basic.pause(200)
        sendBitIndex += -1
    }
    currentBit = 0
    sendBuffer = []
}
radio.onReceivedNumber(function (receivedNumber) {
    receiveBuffer.push(receivedNumber)
    if (receiveBuffer.length == 8) {
        processReceiveBuffer()
        receiveBuffer = []
    }
})
function processBitArray (bits: any[]) {
    byteValue = 0
    for (let index = 0; index <= bits.length - 1; index++) {
        byteValue = byteValue + bits[index] * 2 ** index
    }
    return byteValue
}
function showCurrentBitOnLED () {
    for (let index = 0; index <= 3; index++) {
        led.unplot(index, 1)
        led.unplot(index, 4)
    }
    led.plot(currentBit % 4, 1 + Math.idiv(currentBit, 4) * 3)
}
input.onGesture(Gesture.Shake, function () {
    screenInUse = 0
    currentBit = 0
    sendBuffer = []
})
function incrementCurrentBit () {
    currentBit = currentBit + 1
    if (currentBit == 8) {
        currentBit = 0
    }
}
let byteValue = 0
let sendBitIndex = 0
let receiveBuffer: number[] = []
let sendBuffer: number[] = []
let currentBit = 0
let screenInUse = 0
screenInUse = 0
currentBit = 0
sendBuffer = []
receiveBuffer = []
basic.forever(function () {
    if (screenInUse == 0) {
        showBufferOnLED()
        showCurrentBitOnLED()
    }
})
