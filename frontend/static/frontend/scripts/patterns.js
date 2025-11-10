const isAuthenticated = document.currentScript.dataset.isAuthenticated === 'True'
const csrfToken = document.currentScript.dataset.csrfToken

/** @type {EventSource} */
const statusEventSource = new ReconnectingEventSource('/runner/events/status')

/** @type {number} */
let countdownInterval = undefined

/**
 * @typedef {Object} Pattern
 * @property {string} identifier
 * @property {string} name
 * @property {string} [description]
 * @property {string} [source]
 * @property {string} docker
 * @property {number} duration
 * @property {string} [author]
 * @property {string} [school]
 * @property {string} changed
 * @property {boolean} enabled
 * @property {boolean} visible
 */

/** @type {Pattern[]} */
let patterns = []

/**
 * @typedef {Object} State
 * @property {string|null} currentPatternIdentifier - The current pattern identifier.
 * @property {string|null} currentPatternStarted - An ISO-8601 timestamp representing when the current pattern started.
 * @property {number} currentPatternRemaining - The number of seconds remaining for the current pattern.
 * @property {string|null} runnerLastActive - An ISO-8601 timestamp representing when the runner was last active.
 * @property {boolean} runnerIsActive - Whether the runner is currently active.
 */

/** @type {State} */
let state = undefined

// == Time Utilities

/**
 * Format a number of seconds into MM:SS format.
 *
 * @param {number} seconds
 *
 * @returns {string}
 */
function formatTime (seconds) {
  const MM = `${Math.floor(seconds / 60) % 60}`.padStart(2, '0')
  const SS = `${Math.round(seconds % 60)}`.padStart(2, '0')
  return [MM, SS].join(':')
}

/**
 * Update the countdown timers for all active countdown elements.
 */
function handleCountdown () {
  for (const elem of document.querySelectorAll('[data-seconds]')) {
    let seconds = parseFloat(elem.dataset.seconds)
    if (seconds <= 0 || isNaN(seconds)) continue

    seconds = Math.max(seconds - 1, 0)

    elem.dataset.seconds = seconds.toString()
    elem.textContent = formatTime(seconds)
  }
}

// == Pattern List Utilities

/**
 * Call a specified action for a pattern.
 *
 * @param {string} patternId
 * @param {'run'|'enable'|'disable'} actionType
 *
 * @returns {Promise<void>}
 */
async function patternAction (patternId, actionType) {
  await fetch(
    `/runner/patterns/${patternId}/${actionType}`,
    { method: 'POST', headers: { 'X-CSRFToken': csrfToken } },
  )
}

/**
 * Construct a table row for a pattern.
 *
 * @param {Pattern} pattern
 *
 * @returns {Node}
 */
function createPatternRow (pattern) {
  const template = document.getElementById('pattern-template')
  const row = template.content.cloneNode(true).querySelector('tr')

  row.dataset.identifier = pattern.identifier

  const countdown = row.querySelector('.pattern-countdown')
  countdown.textContent = '--:--'

  const name = row.querySelector('.pattern-name')
  const nameLink = name.querySelector('.pattern-name-link')
  const nameText = name.querySelector('.pattern-name-text')

  if (pattern.description) {
    name.title = pattern.description
  }

  if (pattern.source) {
    nameLink.href = pattern.source
    nameLink.textContent = pattern.name
    nameText.classList.add('d-none')
  } else {
    nameText.textContent = pattern.name
    nameLink.classList.add('d-none')
  }

  const author = row.querySelector('.pattern-author')
  author.textContent = [pattern.author, pattern.school].filter(Boolean).join(', ') || '/'

  if (!pattern.enabled) {
    countdown.classList.add('text-body-secondary', 'text-decoration-line-through')
    name.classList.add('text-body-secondary', 'text-decoration-line-through')
    author.classList.add('text-body-secondary', 'text-decoration-line-through')
  }

  if (isAuthenticated) {
    row.querySelector('.pattern-run-btn').onclick = () => patternAction(pattern.identifier, 'run')
    row.querySelector('.pattern-enable-btn').onclick = () => patternAction(pattern.identifier, 'enable')
    row.querySelector('.pattern-disable-btn').onclick = () => patternAction(pattern.identifier, 'disable')

    row.querySelector(`.pattern-${pattern.enabled ? 'enable' : 'disable'}-btn`).classList.add('d-none')
  }

  return row
}

/**
 * Update the pattern table with new pattern data.
 */
function updatePatternTable () {
  const tbody = document.getElementById('patterns')
  tbody.innerHTML = ''

  for (const pattern of patterns) {
    if (!pattern.visible) continue

    const row = createPatternRow(pattern)
    tbody.appendChild(row)
  }
}

// == Pattern State Utilities

/**
 * Calculate the start times for all patterns.
 *
 * The start time for a pattern is the time at which it will become active.
 * The start time for the currently active pattern is 0 seconds, and subsequent
 * patterns start after the previous pattern's duration, taking into account the
 * remaining time for the current pattern.
 *
 * @returns {Map<string, number>}
 */
function calculateStartTimes () {
  const startTimes = new Map()

  const enabledPatterns = patterns.filter(pattern => pattern.enabled || pattern.identifier === state.currentPatternIdentifier)
  const activeIndex = enabledPatterns.findIndex(pattern => pattern.identifier === state.currentPatternIdentifier)
  if (activeIndex === -1) return startTimes

  let currentTime = 0

  for (let i = 0; i < enabledPatterns.length; i++) {
    const pattern = enabledPatterns[(activeIndex + i) % enabledPatterns.length]
    startTimes.set(pattern.identifier, currentTime)

    if (i === 0) currentTime += state.currentPatternRemaining || 0
    else currentTime += pattern.duration
  }

  return startTimes
}

/**
 * Update the state of the pattern table.
 */
function updatePatternState () {
  // Clear the existing countdown interval
  if (countdownInterval) clearInterval(countdownInterval)

  // Calculate the start times for all patterns
  const startTimes = calculateStartTimes()

  for (const element of document.getElementById('patterns').children) {
    const countdown = element.querySelector('.pattern-countdown')
    const name = element.querySelector('.pattern-name')
    const author = element.querySelector('.pattern-author')

    if (state.runnerIsActive && element.dataset.identifier === state.currentPatternIdentifier) {
      // Highlight the active pattern
      element.classList.add('active-pattern')
    } else {
      // Remove the highlight from the pattern
      element.classList.remove('active-pattern')
    }

    const startTime = startTimes.get(element.dataset.identifier)

    if (state.runnerIsActive && typeof startTime === 'number') {
      // Configure the countdown for the pattern
      countdown.dataset.seconds = startTime.toString()
      countdown.textContent = formatTime(startTime)
    } else {
      // Disable the countdown for the pattern
      countdown.dataset.seconds = undefined
      countdown.textContent = '--:--'
    }
  }

  // Start a new countdown interval
  countdownInterval = setInterval(handleCountdown, 1000)

  // Display whether the runner is active
  const runnerActive = document.getElementById('runner-active')
  const runnerInactive = document.getElementById('runner-inactive')

  if (state.runnerIsActive) {
    runnerActive.classList.remove('d-none')
    runnerInactive.classList.add('d-none')
  } else {
    runnerActive.classList.add('d-none')
    runnerInactive.classList.remove('d-none')
  }
}

// == Event Handlers

statusEventSource.addEventListener('status', function (event) {
  /** @type {{patterns: Pattern[], state: State}} */
  const data = JSON.parse(event.data)

  patterns = data.patterns
  state = data.state

  updatePatternTable()
  updatePatternState()
})

async function setupInitialData () {
  patterns = await (await fetch('/runner/patterns')).json()
  state = await (await fetch('/runner/state')).json()

  updatePatternTable()
  updatePatternState()
}

setupInitialData()
