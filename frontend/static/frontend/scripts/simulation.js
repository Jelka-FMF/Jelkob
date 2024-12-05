let isMouseDown = false
let lastMouseX = 0
let lastMouseY = 0

let rotationScale = 0.01
let sizeScale = 1.1
let lightSize = 2

let alpha = 0
let beta = 0

/** @type {EventSource} */
const driverEventSource = new ReconnectingEventSource(document.currentScript.dataset.driverUrl)

const colorStates = {}

const canvas = document.getElementById('canvas')
const ctx = canvas.getContext('2d')

window.addEventListener('resize', () => {
    renderView()
}, true)

// Add event listeners for mouse events
canvas.addEventListener('mousedown', onMouseDown)
canvas.addEventListener('mousemove', onMouseMove)
canvas.addEventListener('mouseup', onMouseUp)
canvas.addEventListener('mouseleave', onMouseUp)
canvas.addEventListener('wheel', onWheel)

function renderView () {
    const origin = { x: canvas.width / 2, y: canvas.width / 2 , z: 3 * canvas.height / 4 }

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
    // console.log(`Mouse moved: deltaX=${deltaX}, deltaY=${deltaY}`)
    alpha = alpha + deltaX * rotationScale
    beta = beta - deltaY * rotationScale

    // Re-render the view
    renderView()
}

// function drawing canvas rotatet for alpha, beta
function getRotatedCoordinates (x, y, z, alpha, beta) {
    // Rotation matrix
    let newx = Math.cos(alpha) * Math.cos(beta) * x - Math.sin(alpha) * y - Math.cos(alpha) * Math.sin(beta) * z
    let newy = Math.sin(alpha) * Math.cos(beta) * x + Math.cos(alpha) * y - Math.sin(alpha) * Math.sin(beta) * z
    let newz =                   Math.sin(beta) * x +                                         Math.cos(beta) * z 

    return { x: newx, y: newy, z: newz }
}

function drawCoordinateSystem (ctx, origin , scale) {
    let xaxis = getRotatedCoordinates(100, 0, 0,  alpha, - beta)
    let yaxis = getRotatedCoordinates(0, 100, 0,  alpha, - beta)
    let zaxis = getRotatedCoordinates(0, 0, 100,  alpha, - beta)

    // Draw x axis
    ctx.beginPath();
    ctx.moveTo(origin.y, origin.z);
    ctx.lineTo(xaxis.y * scale + origin.y, xaxis.z * scale + origin.z);
    ctx.strokeStyle = 'red';
    ctx.stroke();

    // Draw y axis
    ctx.moveTo(origin.y, origin.z);
    ctx.lineTo(yaxis.y * scale + origin.y, yaxis.z * scale + origin.z);
    ctx.strokeStyle = 'green';
    ctx.stroke();

    // Draw z axis
    ctx.moveTo(origin.y, origin.z);
    ctx.lineTo( - zaxis.y * scale + origin.y, - zaxis.z * scale + origin.z);
    ctx.strokeStyle = 'blue';
    ctx.stroke();

    ctx.closePath();    
}

function drawLights (ctx, origin,  scale) {
    // const relativeHeight = Math.max(...Object.values(positions).map(pos => pos.y)) - Math.min(...Object.values(positions).map(pos => pos.y))
    // const lowestPoint = Math.max(...Object.values(positions).map(pos => pos.y))

        for (const [index, color] of Object.entries(positions)) {
        const position = positions[parseInt(index)]

        if (!position) {
            // Skip lights with no position
            continue
        }

        const color = colorStates[parseInt(index)] || { red: 0, green: 0, blue: 0 }
        
        let y = origin.y + sizeScale * getRotatedCoordinates(position.x, position.y, position.z, alpha, beta).y
        let z = origin.z - sizeScale * (getRotatedCoordinates(position.x, position.y, position.z, alpha, beta).z)

        if (color.green == 0 && color.red == 0 && color.blue == 0) {
            ctx.beginPath()
            ctx.strokeStyle = '#d0d0d0'
            ctx.arc(y, z, lightSize, 0, 2 * Math.PI)
            ctx.stroke()
        }
        else {
            ctx.beginPath()
            ctx.fillStyle = `rgb(${color.red}, ${color.green}, ${color.blue})`
            ctx.arc(y, z, lightSize, 0, 2 * Math.PI)
            ctx.fill()
        }
        
    }
}

driverEventSource.addEventListener('message', function (event) {
    // TODO: Parse the event data
    // TODO: Set colorStates to the parsed data

    // Render the view
    renderView()
})

// Render the initial view
// We need to call it twice
setTimeout(renderView, 100)
renderView()
