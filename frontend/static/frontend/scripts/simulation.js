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

let simulationAlpha = 0
let simulationBeta = 0

const colorStates = {}

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
  isMouseDown = true
  lastMouseX = event.touches[0].clientX
  lastMouseY = event.touches[0].clientY
}

function onTouchEnd (event) {
  isMouseDown = false
}

function onWheel (event) {
  // Update the view based on mouse scroll
  sizeScale *= 1 - event.deltaY * 0.001

  // Re-render the view
  renderView()
}

function onMouseMove (event) {
  if (!isMouseDown) return

  const deltaX = event.clientX - lastMouseX
  const deltaY = event.clientY - lastMouseY

  lastMouseX = event.clientX
  lastMouseY = event.clientY

  // Update the view based on mouse movements
  simulationAlpha = simulationAlpha + deltaX * rotationScale
  simulationBeta = simulationBeta - deltaY * rotationScale

  // Re-render the view
  renderView()
}

function onTouchMove (event) {
  if (!isMouseDown) return

  const deltaX = event.touches[0].clientX - lastMouseX
  const deltaY = event.touches[0].clientY - lastMouseY

  lastMouseX = event.touches[0].clientX
  lastMouseY = event.touches[0].clientY

  // Update the view based on touch movements
  simulationAlpha = simulationAlpha + deltaX * rotationScale
  simulationBeta = simulationBeta - deltaY * rotationScale

  // Re-render the view
  renderView()
}

function getRotatedCoordinates (x, y, z, alpha, beta) {
  // Rotation matrix
  let newx = Math.cos(alpha) * Math.cos(beta) * x - Math.sin(alpha) * y - Math.cos(alpha) * Math.sin(beta) * z
  let newy = Math.sin(alpha) * Math.cos(beta) * x + Math.cos(alpha) * y - Math.sin(alpha) * Math.sin(beta) * z
  let newz = Math.sin(beta) * x + Math.cos(beta) * z

  // Return the new coordinates
  return { x: newx, y: newy, z: newz }
}

function drawCoordinateSystem (ctx, origin, scale) {
  let xaxis = getRotatedCoordinates(100, 0, 0, simulationAlpha, -simulationBeta)
  let yaxis = getRotatedCoordinates(0, 100, 0, simulationAlpha, -simulationBeta)
  let zaxis = getRotatedCoordinates(0, 0, 100, simulationAlpha, -simulationBeta)

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
  for (const [index, position] of Object.entries(positions)) {
    const color = colorStates[parseInt(index)] || { red: 0, green: 0, blue: 0 }

    let y = origin.y + scale * getRotatedCoordinates(position.x, position.y, position.z, simulationAlpha, simulationBeta).y
    let z = origin.z - scale * (getRotatedCoordinates(position.x, position.y, position.z, simulationAlpha, simulationBeta).z)

    if (color.green === 0 && color.red === 0 && color.blue === 0) {
      ctx.beginPath()
      ctx.strokeStyle = '#d0d0d0'
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
  // TODO: Parse the event data
  // TODO: Set color states to the parsed data

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