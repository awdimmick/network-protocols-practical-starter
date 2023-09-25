// processReceiveBuffer() is the function that you need to modify.
// 
// This function is called when a byte of data is received.
// 
// Setting screenInUse to 1 pauses the background process that shows the current state of the sendBuffer on the micro:bit's LEDs. Setting it back to 0 will resume the display.
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
/**
 * processReceiveBuffer() is the function that you should modify to determine what your micro:bit should do once a byte of data has been received. 
 * 
 * You could write your handling code directly in here, or create new functions to call.
 * 
 * Setting screenInUse to 1 "takes over" the screen and disables the background process that shows the state of the sendBuffer on the micro:bit's LED display. Setting it back to 0 releases the screen once again.
 */
function processReceiveBuffer () {
    screenInUse = 1
    basic.showNumber(decodeBitArray(receiveBuffer))
    basic.pause(200)
    basic.clearScreen()
    screenInUse = 0
}
function decodeBitArray (bits: any[]) {
    byteValue = 0
    for (let index = 0; index <= bits.length - 1; index++) {
        byteValue = byteValue + bits[index] * 2 ** (7 - index)
    }
    return byteValue
}
input.onButtonPressed(Button.A, function () {
    sendBuffer[currentBit] = 0
    incrementCurrentBit()
})
function decodeHighNibble (bits: number[]) {
    nibbleValue = 0
    for (let index = 0; index <= 3; index++) {
        nibbleValue = nibbleValue + bits[index] * 2 ** (3 - index)
    }
    return nibbleValue
}
function transmitSendBuffer () {
    for (let index = 0; index <= 7; index++) {
        radio.sendNumber(sendBuffer[index])
        basic.pause(200)
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
function decodeLowNibble (bits: number[]) {
    nibbleValue = 0
    for (let index = 0; index <= 3; index++) {
        nibbleValue = nibbleValue + bits[index + 4] * 2 ** (3 - index)
    }
    return nibbleValue
}
function incrementCurrentBit () {
    currentBit = currentBit + 1
    if (currentBit == 8) {
        currentBit = 0
    }
}
/**
 * Each micro:bit in your group must be using the same radio group value.
 * 
 * Update this value before downloading your code and loading onto your micro:bits!
 */
let nibbleValue = 0
let byteValue = 0
let receiveBuffer: number[] = []
let sendBuffer: number[] = []
let currentBit = 0
let screenInUse = 0
radio.setGroup(0)
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
