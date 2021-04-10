const hideErrorOutput = () => {
  errorOutput.classList.add('hidden')
}

const showError = error => {
  errorOutput.classList.remove('hidden')
  errorOutput.innerText = error
}

const handleResponse = ({result, error}) => {
  hideErrorOutput()
  outputTable.innerHTML = result

  if (error) {
    showError(error)
  }
}


const sendQuery = async e => {
  editor.selectAll()
  let body = editor.getSelectedText().trim()
  editor.clearSelection()
  if (limitCheckbox.checked) {
    body = body.replace(/;$/, '')
    body += '\nLIMIT 1000'
  }
  const options = { method: 'POST', body }
  const response = await fetch('/query', options)
  if (! response.ok) {
    showError(response.statusText)
  }
  data = await response.json()
  handleResponse(data)
}

const saveQuery = async () => {
  const filename = prompt('Filename?')
  if (! filename) {
    return
  }

  editor.selectAll()
  let body = editor.getSelectedText().trim()
  editor.clearSelection()

  const options = {method: 'post', body }

  const response = await fetch('/save/' + filename, options)
  const text = await response.text()
  alert(text)
}

const submitButton = document.querySelector('#submit')
const saveButton = document.querySelector('#save')
const outputTable = document.querySelector('#output')
const errorOutput = document.querySelector('#error')
const limitCheckbox = document.querySelector('#limit')

submitButton.addEventListener('click', sendQuery)
saveButton.addEventListener('click', saveQuery)

const editor = ace.edit('editor')
editor.session.setMode('ace/mode/sql')
editor.insert(`WITH RECURSIVE t(id, x, y) AS (
    SELECT 1, random() % 100, random() % 100
    UNION
    SELECT id + 1, random() % 100, random() % 100
    FROM t WHERE id < 10
)
SELECT * FROM t`)

editor.commands.addCommand({
  name: 'sendQuery',
  bindKey: {win: 'Ctrl-Enter',  mac: 'Command-Enter'},
  exec: sendQuery,
  readOnly: true // false if this command should not apply in readOnly mode
})

window.onbeforeunload = () => true
