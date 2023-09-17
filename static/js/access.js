const form = document.querySelector('form')
const usernameError = document.getElementById('username-error')
const passwordError = document.getElementById('password-error')
const accessError = document.getElementById('access-error')
const { username, password } = form
const MAX_CHARS = 100
const validator = {
  username: false,
  password: false
}
const errors = {
  empty: (input) => `Debes ingresar el ${input}`,
  maxChars: "Has excedido el máximo de caracteres",
  access: "Usuario o contraseña incorrecto"
}


username.oninput = (e) => {
  validateInput(e.target, "usuario", usernameError)
}

username.onpaste = (e) => {
  validateInput(e.target, "usuario", usernameError)
}

password.oninput = (e) => {
  validateInput(e.target, "contraseña", passwordError)
}

password.onpaste = (e) => {
  validateInput(e.target, "contraseña", passwordError)
}


function validateInput(target, errorName, errorBox) {
  errorBox.innerHTML = ""
  errorBox.classList.add("hidden")
  let txt = target.value.trim()
  txt = txt.replaceAll(" ", "")
  validator[target.name] = false
  if(txt === "") {
    errorBox.innerHTML = errors.empty(errorName)
    errorBox.classList.remove("hidden")
    return
  }
  
  if(txt.length > MAX_CHARS) {
    errorBox.innerHTML = errors.maxChars
    errorBox.classList.remove("hidden")
    return
  }
  validator[target.name] = true
}

form.onsubmit = async (e) => {
  e.preventDefault()
  if(validateForm(e)){
    const result = await senData()
    console.log(result);
    /* if(result.access) {
      console.log("redirecciona")
    } */
  } 
}

function validateForm(e) {
  const inputs = Object.fromEntries(new FormData(e.target));
  const keys = Object.keys(inputs)
  // Inputs validos
  let validInputs = 0
  // Habilitamos la propagación del evento
  const event = new Event('input', {
    bubbles: true, 
    cancelable: true,
  });
  // validamos cada input
  keys.forEach(input => {
    const element = e.target[input];
    element.dispatchEvent(event);
    if(validator[input]) {
      validInputs++
    } 
  });
  return validInputs === keys.length
}

async function senData() {
  const result = await fetch("/get-access", {
    method: "POST",
    body: new FormData(form)
  })

  return await result.json()
}