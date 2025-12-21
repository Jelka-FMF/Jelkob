/** @type {string} */
const interactionUrl = document.currentScript.dataset.interactionUrl

/** @type {WebSocket} */
let interactionSocket = undefined

// == Joystick

// But I wonder if I myself shall ever find joy. Ooooh, so edgy.
const joystick = document.getElementById('joystick')
const joystickKnob = document.getElementById('joystick-knob')

let joystickIsDragging = false

/**
 * Send the joystick state to the server.
 *
 * @param {number} distance
 * @param {number} angle
 */
function sendJoystickState (distance, angle) {
  const degrees = (angle * 180 / Math.PI + 360) % 360

  sendInteractionMessage([
    { sensor: 'joystick-distance', value: distance },
    { sensor: 'joystick-angle', value: degrees },
  ])
}

/**
 * Update the joystick knob position based on pointer coordinates.
 *
 * @param {number} x
 * @param {number} y
 */
function updateKnobPosition (x, y) {
  const rect = joystick.getBoundingClientRect()
  const centerX = rect.width / 2
  const centerY = rect.height / 2
  const maxRadius = rect.width / 2 - 40 // Account for the knob size

  // Calculate relative position
  const relX = x - rect.left - centerX
  const relY = y - rect.top - centerY
  const distance = Math.sqrt(relX * relX + relY * relY)
  const angle = Math.atan2(relY, relX)

  // Constrain to circle
  const constrainedDistance = Math.min(distance, maxRadius)
  const finalX = Math.cos(angle) * constrainedDistance
  const finalY = Math.sin(angle) * constrainedDistance

  // Update knob position
  joystickKnob.style.transform = `translate(calc(-50% + ${finalX}px), calc(-50% + ${finalY}px))`

  // Send the joystick state
  sendJoystickState(constrainedDistance / maxRadius, angle)
}

/**
 * Reset the joystick knob to the center position.
 */
function resetKnobPosition () {
  // Mark knob as inactive
  joystickKnob.classList.remove('active')

  // Reset knob to center
  joystickKnob.style.transform = 'translate(-50%, -50%)'

  // Send the reset joystick state
  sendJoystickState(0, 0)
}

function handleJoystickStart (event) {
  if (joystick.classList.contains('disabled')) return

  // Mark joystick as dragging
  joystickIsDragging = true

  // Capture pointer events outside the element
  joystick.setPointerCapture(event.pointerId)
  event.preventDefault()

  // Register update handlers
  document.addEventListener('pointermove', handleJoystickMove)
  document.addEventListener('pointerup', handleJoystickEnd)
  document.addEventListener('pointercancel', handleJoystickEnd)

  // Mark knob as active
  joystickKnob.classList.add('active')

  // Set the initial position
  updateKnobPosition(event.clientX, event.clientY)
}

function handleJoystickMove (event) {
  if (joystick.classList.contains('disabled')) return
  if (!joystickIsDragging) return

  // Prevent default behavior
  event.preventDefault()

  // Update the knob position
  updateKnobPosition(event.clientX, event.clientY)
}

function handleJoystickEnd (event) {
  // Mark joystick as not dragging
  joystickIsDragging = false

  // Release pointer capture
  joystick.releasePointerCapture(event.pointerId)
  event.preventDefault()

  // Unregister update handlers
  document.removeEventListener('pointermove', handleJoystickMove)
  document.removeEventListener('pointerup', handleJoystickEnd)
  document.removeEventListener('pointercancel', handleJoystickEnd)

  // Reset knob position
  resetKnobPosition()
}

function initializeJoystick () {
  joystick.addEventListener('pointerdown', handleJoystickStart)
}

function enableJoystick () {
  joystick.classList.remove('disabled')
}

function disableJoystick () {
  joystick.classList.add('disabled')
}

// == Buttons

const keyboardArrowButtons = {
  ArrowUp: document.getElementById('button-arrow-up'),
  ArrowDown: document.getElementById('button-arrow-down'),
  ArrowLeft: document.getElementById('button-arrow-left'),
  ArrowRight: document.getElementById('button-arrow-right'),
}

const keyboardLetterButtons = {
  KeyA: document.getElementById('button-letter-a'),
  KeyB: document.getElementById('button-letter-b'),
  KeyC: document.getElementById('button-letter-c'),
  KeyD: document.getElementById('button-letter-d'),
}

const keyboardButtons = { ...keyboardArrowButtons, ...keyboardLetterButtons }

const sensorNames = {
  ArrowUp: 'button-arrow-up',
  ArrowDown: 'button-arrow-down',
  ArrowLeft: 'button-arrow-left',
  ArrowRight: 'button-arrow-right',
  KeyA: 'button-letter-a',
  KeyB: 'button-letter-b',
  KeyC: 'button-letter-c',
  KeyD: 'button-letter-d',
}

const arrowKeyboardCheckbox = document.getElementById('hardware-arrow-keys')
const letterKeyboardCheckbox = document.getElementById('hardware-letter-keys')

const keyboardState = {}
Object.keys(keyboardButtons).forEach(key => keyboardState[key] = { pointer: false, keyboard: false, enter: false })

/**
 * Check if a keyboard is enabled for this key.
 */
function isKeyboardEnabled (key) {
  if (keyboardArrowButtons.hasOwnProperty(key)) return arrowKeyboardCheckbox?.checked
  if (keyboardLetterButtons.hasOwnProperty(key)) return letterKeyboardCheckbox?.checked
  return false
}

/**
 * Send the button state to the server.
 */
function sendButtonState (key, pressed) {
  sendInteractionMessage([
    { sensor: sensorNames[key], value: pressed },
  ])
}

/**
 * Update the button visual state.
 */
function updateButton (key) {
  const button = keyboardButtons[key]
  if (!button) return

  const state = keyboardState[key]
  const shouldBePressed = state.pointer || state.keyboard || state.enter
  const isPressed = button.classList.contains('active')

  if (shouldBePressed !== isPressed) {
    button.classList.toggle('active', shouldBePressed)
    sendButtonState(key, shouldBePressed)
  }
}

/**
 * Handle the keyboard button when an actual key is pressed or released.
 */
function handleButtonKeyChange (event, pressed) {
  // Handle enter key on the focused button
  if (event.code === 'Enter') {
    const focusedKey = Object.entries(keyboardButtons).find(([, btn]) => btn === document.activeElement)?.[0]
    if (!focusedKey) return

    event.preventDefault()

    keyboardState[focusedKey].enter = pressed
    updateButton(focusedKey)

    return
  }

  // Physical keyboard mapped keys
  if (!isKeyboardEnabled(event.code)) return

  event.preventDefault()

  keyboardState[event.code].keyboard = pressed
  updateButton(event.code)
}

/**
 * Handle the keyboard button when a pointer event starts.
 */
function handledButtonPointerDown (event, key) {
  // Capture pointer events outside the element
  event.target.setPointerCapture(event.pointerId)
  event.preventDefault()

  // Update the button state
  keyboardState[key].pointer = true
  updateButton(key)
}

/**
 * Handle the keyboard button when a pointer event ends.
 */
function handleButtonPointerUp (event, key) {
  // Release pointer capture
  event.target.releasePointerCapture(event.pointerId)
  event.preventDefault()

  // Update the button state
  keyboardState[key].pointer = false
  updateButton(key)
}

function releaseAllButtons () {
  Object.keys(keyboardButtons).forEach(key => {
    keyboardState[key].keyboard = false
    keyboardState[key].pointer = false
    keyboardState[key].enter = false
    updateButton(key)
  })
}

function initializeButtons () {
  // Global keyboard handlers
  document.addEventListener('keydown', (event) => handleButtonKeyChange(event, true))
  document.addEventListener('keyup', (event) => handleButtonKeyChange(event, false))

  // Release all keyboard buttons on checkbox change
  arrowKeyboardCheckbox.addEventListener('change', releaseAllButtons)
  letterKeyboardCheckbox.addEventListener('change', releaseAllButtons)

  // Release all keyboard inputs on the window blur
  window.addEventListener('blur', releaseAllButtons)

  Object.entries(keyboardButtons).forEach(([key, button]) => {
    button.addEventListener('pointerdown', (event) => handledButtonPointerDown(event, key))
    button.addEventListener('pointerup', (event) => handleButtonPointerUp(event, key))
    button.addEventListener('pointercancel', (event) => handleButtonPointerUp(event, key))
  })
}

function enableButtons () {
  // Enable all buttons
  Object.values(keyboardButtons).forEach(button => button.disabled = false)

  // Enable keyboard toggles
  arrowKeyboardCheckbox.disabled = false
  letterKeyboardCheckbox.disabled = false
}

function disableButtons () {
  // Disable all buttons
  Object.values(keyboardButtons).forEach(button => button.disabled = true)

  // Disable keyboard toggles
  arrowKeyboardCheckbox.disabled = true
  letterKeyboardCheckbox.disabled = true

  // Disable keyboard controls
  arrowKeyboardCheckbox.checked = false
  letterKeyboardCheckbox.checked = false

  // Release all button states
  releaseAllButtons()
}

// == Sensors

// Minimum interval between sensor data captures (in milliseconds)
const sensorCaptureInterval = 15

const sensorGroups = {
  orientation: {
    button: document.getElementById('toggle-orientation'),
    enabled: false,
    handler: null,
    lastSendTime: 0,
    sliders: {
      alpha: document.getElementById('orientation-alpha'),
      beta: document.getElementById('orientation-beta'),
      gamma: document.getElementById('orientation-gamma'),
    },
    values: {
      alpha: document.getElementById('orientation-alpha-value'),
      beta: document.getElementById('orientation-beta-value'),
      gamma: document.getElementById('orientation-gamma-value'),
    },
  },
  acceleration: {
    button: document.getElementById('toggle-acceleration'),
    enabled: false,
    handler: null,
    lastSendTime: 0,
    sliders: {
      x: document.getElementById('acceleration-x'),
      y: document.getElementById('acceleration-y'),
      z: document.getElementById('acceleration-z'),
    },
    values: {
      x: document.getElementById('acceleration-x-value'),
      y: document.getElementById('acceleration-y-value'),
      z: document.getElementById('acceleration-z-value'),
    },
  },
  gyroscope: {
    button: document.getElementById('toggle-gyroscope'),
    enabled: false,
    handler: null,
    lastSendTime: 0,
    sliders: {
      alpha: document.getElementById('gyroscope-alpha'),
      beta: document.getElementById('gyroscope-beta'),
      gamma: document.getElementById('gyroscope-gamma'),
    },
    values: {
      alpha: document.getElementById('gyroscope-alpha-value'),
      beta: document.getElementById('gyroscope-beta-value'),
      gamma: document.getElementById('gyroscope-gamma-value'),
    },
  },
}

function sendOrientationState (alpha, beta, gamma) {
  sendInteractionMessage([
    { sensor: 'orientation-alpha', value: alpha },
    { sensor: 'orientation-beta', value: beta },
    { sensor: 'orientation-gamma', value: gamma },
  ])
}

function sendAccelerationState (x, y, z) {
  sendInteractionMessage([
    { sensor: 'acceleration-x', value: x },
    { sensor: 'acceleration-y', value: y },
    { sensor: 'acceleration-z', value: z },
  ])
}

function sendGyroscopeState (alpha, beta, gamma) {
  sendInteractionMessage([
    { sensor: 'gyroscope-alpha', value: alpha },
    { sensor: 'gyroscope-beta', value: beta },
    { sensor: 'gyroscope-gamma', value: gamma },
  ])
}

function updateDisplay (group, data, sender) {
  // Throttle sending updates
  const now = performance.now()
  if (now - group.lastSendTime < sensorCaptureInterval) return
  group.lastSendTime = now

  // Update sliders and labels
  Object.keys(data).forEach(key => {
    const value = data[key] ?? 0
    group.sliders[key].value = value
    group.values[key].textContent = value.toFixed(1)
  })

  // Send the sensor state
  sender(...Object.values(data))
}

async function toggleSensorGroup (groupName) {
  const group = sensorGroups[groupName]

  if (group.enabled) {
    // Enable manual sliders
    Object.values(group.sliders).forEach(slider => slider.disabled = false)

    // Remove event listener
    if (group.handler) {
      const eventType = groupName === 'orientation' ? 'deviceorientation' : 'devicemotion'
      window.removeEventListener(eventType, group.handler)
      group.handler = null
    }

    // Update the group state
    group.button.classList.replace('btn-success', 'btn-outline-primary')
    group.enabled = false

  } else {
    // Try to request permissions for device sensors
    if (typeof DeviceOrientationEvent?.requestPermission === 'function') {
      await DeviceOrientationEvent.requestPermission()
    }
    if (typeof DeviceMotionEvent?.requestPermission === 'function') {
      await DeviceMotionEvent.requestPermission()
    }

    // Disable manual sliders
    Object.values(group.sliders).forEach(slider => slider.disabled = true)

    // Register event listeners
    if (groupName === 'orientation') {
      group.handler = (event) => updateDisplay(group, {
        alpha: event.alpha ?? 0,
        beta: event.beta ?? 0,
        gamma: event.gamma ?? 0,
      }, sendOrientationState)
      window.addEventListener('deviceorientation', group.handler)
    } else if (groupName === 'acceleration') {
      group.handler = (event) => updateDisplay(group, {
        x: event.acceleration?.x ?? 0,
        y: event.acceleration?.y ?? 0,
        z: event.acceleration?.z ?? 0,
      }, sendAccelerationState)
      window.addEventListener('devicemotion', group.handler)
    } else if (groupName === 'gyroscope') {
      group.handler = (event) => updateDisplay(group, {
        alpha: event.rotationRate?.alpha ?? 0,
        beta: event.rotationRate?.beta ?? 0,
        gamma: event.rotationRate?.gamma ?? 0,
      }, sendGyroscopeState)
      window.addEventListener('devicemotion', group.handler)
    }

    // Update the group state
    group.button.classList.replace('btn-outline-primary', 'btn-success')
    group.enabled = true
  }
}

function onSliderInput (groupName) {
  const group = sensorGroups[groupName]
  if (group.enabled) return

  const data = {}
  Object.keys(group.sliders).forEach(key => data[key] = parseFloat(group.sliders[key].value))

  if (groupName === 'orientation') updateDisplay(group, data, sendOrientationState)
  else if (groupName === 'acceleration') updateDisplay(group, data, sendAccelerationState)
  else if (groupName === 'gyroscope') updateDisplay(group, data, sendGyroscopeState)
}

function initializeSensors () {
  Object.keys(sensorGroups).forEach(groupName => {
    const group = sensorGroups[groupName]

    // Initialize button listener
    group.button.addEventListener('click', () => toggleSensorGroup(groupName))

    // Initialize slider listeners and labels
    Object.keys(group.sliders).forEach(key => {
      const slider = group.sliders[key]
      slider.addEventListener('input', () => onSliderInput(groupName))
      group.values[key].textContent = parseFloat(slider.value).toFixed(1)
    })
  })
}

function enableSensors () {
  Object.values(sensorGroups).forEach(group => {
    // Enable toggle buttons
    group.button.disabled = false

    // Enable sliders
    Object.values(group.sliders).forEach(slider => slider.disabled = false)
  })
}

function disableSensors () {
  Object.entries(sensorGroups).forEach(([groupName, group]) => {
    // Disable toggle buttons
    group.button.disabled = true

    // Disable sensors
    if (group.enabled) toggleSensorGroup(groupName)

    // Disable sliders
    Object.values(group.sliders).forEach(slider => slider.disabled = true)
  })
}

// == Control Management

function initControls () {
  initializeJoystick()
  initializeButtons()
  initializeSensors()
}

function enableControls () {
  enableJoystick()
  enableButtons()
  enableSensors()
}

function disableControls () {
  disableJoystick()
  disableButtons()
  disableSensors()
}

// == Connection Management

/**
 * Send a message via the interaction connection.
 *
 * @param {`{sensor: string, value: number|boolean}[]`} message
 */
function sendInteractionMessage (message) {
  if (interactionSocket && interactionSocket.readyState === WebSocket.OPEN) {
    interactionSocket.send(JSON.stringify(message))
  }
}

const interactionConnectButton = document.getElementById('interaction-connect')
const interactionDisconnectButton = document.getElementById('interaction-disconnect')

if (interactionUrl === 'None') {
  interactionConnectButton.disabled = true
  interactionDisconnectButton.disabled = true
}

function showConnectButton () {
  // Hide the close connection button
  interactionDisconnectButton.classList.add('d-none')
  interactionDisconnectButton.disabled = true

  // Show the establish connection button
  interactionConnectButton.classList.remove('d-none')
  interactionConnectButton.disabled = false
}

function showDisconnectButton () {
  // Hide the establish connection button
  interactionConnectButton.classList.add('d-none')
  interactionConnectButton.disabled = true

  // Show the close connection button
  interactionDisconnectButton.classList.remove('d-none')
  interactionDisconnectButton.disabled = false
}

interactionConnectButton.addEventListener('click', () => {
  // Show the close connection button
  showDisconnectButton()

  // Establish the WebSocket connection
  interactionSocket = new WebSocket(interactionUrl)

  interactionSocket.addEventListener('open', () => {
    console.log('Interaction WebSocket connected')
    enableControls()
  })

  interactionSocket.addEventListener('close', () => {
    console.log('Interaction WebSocket disconnected')
    disableControls()
    showConnectButton()
  })
})

interactionDisconnectButton.addEventListener('click', () => {
  // Close the WebSocket connection
  if (interactionSocket) {
    interactionSocket.close()
    interactionSocket = undefined
  }

  // Show the establish connection button
  showConnectButton()
})

// == Initialization

// Initialize all controls and disable them initially
initControls()
disableControls()
