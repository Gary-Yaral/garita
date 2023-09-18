function redirectToForm(current_path) {
  if(current_path !== 'access') {
    window.location.href = '/access';
  }
}

function redirectToHome(current_path) {
  if(current_path === 'access' || current_path === '') {
    window.location.href = '/home';
  }
}

async function authGuard() {
  // Verificar el token almacenado en localStorage
  const data = localStorage.getItem(STORAGE_KEY);
  current_path = window.location.pathname.replace("/","")

  if (!data) {
      redirectToForm(current_path)
  } else {
    let token = JSON.parse(data).token
    if(token) {
      // Verificamos si tenemos autorizacion
      const result = await fetch('/auth', {
          method: 'POST',
          headers: {
              'Authorization': `Bearer ${token}`
          }
      })
      const json = await result.json()
      if(!json.access) {
        redirectToForm(current_path)
      } else {
        redirectToHome(current_path)
      }
    } else {
      redirectToForm(current_path)
    }
  }
}

(async () => await authGuard())()