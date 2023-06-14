import App from './App.svelte'
import '../firebase.js'

const app = new App({
  target: document.getElementById('app'),
})

export default app
