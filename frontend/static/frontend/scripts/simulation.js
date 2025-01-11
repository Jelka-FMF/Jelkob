/** @type {string} */
const driverUrl = document.currentScript.dataset.driverUrl

/** @type {EventSource} */
let driverEventSource = undefined

let isMouseDown = false
let lastMouseX = 0
let lastMouseY = 0

let rotationScale = 0.01
let sizeScale = 5
let lightSize = 6

let initialDistance = 0
let initialScale = sizeScale

let simulationAlpha = 0
let simulationBeta = 0

const colorStates = []

// Create a canvas and get its context
const canvas = document.getElementById('canvas')
const ctx = canvas.getContext('2d')

// Set the canvas size
canvas.width = 1500
canvas.height = 1500

// Add event listeners for mouse events
canvas.addEventListener('mousedown', onMouseDown)
canvas.addEventListener('mousemove', onMouseMove)
canvas.addEventListener('mouseup', onMouseUp)
canvas.addEventListener('mouseleave', onMouseUp)
canvas.addEventListener('wheel', onWheel)
canvas.addEventListener('touchstart', onTouchStart)
canvas.addEventListener('touchmove', onTouchMove)
canvas.addEventListener('touchend', onTouchEnd)

// Add event listeners for theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', renderView)

function renderView () {
  // Get the origin of the drawing
  const origin = { x: canvas.width / 2, y: canvas.width / 2, z: 3 * canvas.height / 4 }

  // Draw the canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  drawLights(ctx, origin, sizeScale)
  drawCoordinateSystem(ctx, origin, sizeScale)
}

function onMouseDown (event) {
  isMouseDown = true
  lastMouseX = event.clientX
  lastMouseY = event.clientY
}

function onMouseUp (event) {
  isMouseDown = false
}

function onTouchStart (event) {
  if (event.touches.length === 2) {
    // Handle pinch to zoom
    initialDistance = getDistance(event.touches[0], event.touches[1])
    initialScale = sizeScale
  } else {
    // Handle touch rotation
    isMouseDown = true
    lastMouseX = event.touches[0].clientX
    lastMouseY = event.touches[0].clientY
  }
}

function onTouchEnd (event) {
  isMouseDown = false
}

function onWheel (event) {
  // Update the view based on mouse scroll
  sizeScale *= 1 - event.deltaY * 0.001

  // Re-render the view
  renderView()

  // Prevent zooming or scrolling
  event.preventDefault()
}

function onMouseMove (event) {
  if (!isMouseDown) return

  const deltaX = event.clientX - lastMouseX
  const deltaY = event.clientY - lastMouseY

  // Update the last position
  lastMouseX = event.clientX
  lastMouseY = event.clientY

  // Update the view based on mouse movements
  simulationAlpha = simulationAlpha + deltaX * rotationScale
  simulationBeta = simulationBeta + deltaY * rotationScale

  // Re-render the view
  renderView()

  // Prevent zooming or scrolling
  event.preventDefault()
}

function onTouchMove (event) {
  if (event.touches.length === 2) {
    // Handle pinch to zoom
    const currentDistance = getDistance(event.touches[0], event.touches[1])
    sizeScale = initialScale * (currentDistance / initialDistance)
  } else if (isMouseDown) {
    // Handle touch rotation
    const deltaX = event.touches[0].clientX - lastMouseX
    const deltaY = event.touches[0].clientY - lastMouseY

    // Update the last position
    lastMouseX = event.touches[0].clientX
    lastMouseY = event.touches[0].clientY

    // Update the view based on touch movements
    simulationAlpha = simulationAlpha + deltaX * rotationScale
    simulationBeta = simulationBeta + deltaY * rotationScale
  }

  // Re-render the view
  renderView()

  // Prevent zooming or scrolling
  event.preventDefault()
}

function getDistance (touch1, touch2) {
  const dx = touch1.clientX - touch2.clientX
  const dy = touch1.clientY - touch2.clientY
  return Math.sqrt(dx * dx + dy * dy)
}

// Get drawing canvas rotated for alpha, beta, gama
function getRotatedCoordinates (x, y, z, alpha, beta, gama) {
  let newx = Math.sin(alpha) * Math.cos(beta) * x +  (Math.cos(alpha) * Math.cos(gama) - Math.sin(alpha) * Math.sin(beta) * Math.sin(gama)) * y + (-Math.cos(alpha) * Math.sin(gama) - Math.sin(alpha) * Math.sin(beta) * Math.cos(gama)) * z
  let newy = Math.cos(alpha) * Math.cos(beta) * x + (-Math.sin(alpha) * Math.cos(gama) - Math.cos(alpha) * Math.sin(beta) * Math.sin(gama)) * y +  (Math.sin(alpha) * Math.sin(gama) - Math.cos(alpha) * Math.sin(beta) * Math.cos(gama)) * z
  let newz =                   Math.sin(beta) * x +   Math.cos(beta)  * Math.sin(gama) * y                                                                                                             + Math.cos(beta) * Math.cos(gama) * z

  return { x: newx, y: newy, z: newz }
}

function drawCoordinateSystem (ctx, origin, scale) {
  let xaxis = getRotatedCoordinates(100, 0, 0, simulationAlpha, 0, -simulationBeta)
  let yaxis = getRotatedCoordinates(0, 100, 0, simulationAlpha, 0, -simulationBeta)
  let zaxis = getRotatedCoordinates(0, 0, 100, simulationAlpha, 0, -simulationBeta)

  // Draw x axis
  ctx.beginPath()
  ctx.moveTo(origin.y, origin.z)
  ctx.lineTo(xaxis.y * scale + origin.y, xaxis.z * scale + origin.z)
  ctx.strokeStyle = 'red'
  ctx.stroke()
  ctx.closePath()

  // Draw y axis
  ctx.beginPath()
  ctx.moveTo(origin.y, origin.z)
  ctx.lineTo(yaxis.y * scale + origin.y, yaxis.z * scale + origin.z)
  ctx.strokeStyle = 'green'
  ctx.stroke()
  ctx.closePath()

  // Draw z axis
  ctx.beginPath()
  ctx.moveTo(origin.y, origin.z)
  ctx.lineTo(-zaxis.y * scale + origin.y, -zaxis.z * scale + origin.z)
  ctx.strokeStyle = 'blue'
  ctx.stroke()
  ctx.closePath()
}

function drawLights (ctx, origin, scale) {
  const lowestLight = Object.values(positions).reduce((prev, current) => prev.z < current.z ? prev : current)

  for (const [index, position] of Object.entries(positions)) {
    const color = colorStates[parseInt(index)] || { red: 0, green: 0, blue: 0 }

    let y = origin.y + scale * getRotatedCoordinates(position.x, position.y, position.z, simulationAlpha, 0, simulationBeta).y
    let z = origin.z - scale * (getRotatedCoordinates(position.x, position.y, position.z, simulationAlpha, 0, simulationBeta).z - lowestLight.z)

    if (color.green === 0 && color.red === 0 && color.blue === 0) {
      ctx.beginPath()
      ctx.strokeStyle = window.matchMedia('(prefers-color-scheme: dark)').matches ? '#303030' : '#d0d0d0'
      ctx.arc(y, z, lightSize, 0, 2 * Math.PI)
      ctx.stroke()
    } else {
      ctx.beginPath()
      ctx.fillStyle = `rgb(${color.red}, ${color.green}, ${color.blue})`
      ctx.arc(y, z, lightSize, 0, 2 * Math.PI)
      ctx.fill()
    }
  }
}

function driverMessageHandler (event) {
  // Parse the message and skip non-data lines
  let line = event.data.trim()
  if (line[0] !== '#') return
  line = line.slice(1)

  // Parse the color states
  for (let i = 0; i < line.length / 6; i++) {
    colorStates[i] = {
      red: Number('0x' + line.slice(i * 6, i * 6 + 2)),
      green: Number('0x' + line.slice(i * 6 + 2, i * 6 + 4)),
      blue: Number('0x' + line.slice(i * 6 + 4, i * 6 + 6)),
    }
  }

  // Re-render the view
  renderView()
}

if (driverUrl !== 'None') {
  driverEventSource = new ReconnectingEventSource(driverUrl)
  driverEventSource.addEventListener('message', driverMessageHandler)
}

// Render the initial view
// We need to call it twice
setTimeout(renderView, 100)
renderView()
