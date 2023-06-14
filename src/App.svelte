<script>
  import Router from 'svelte-spa-router'
  import Login from './pages/Login.svelte';
  import Main from './pages/Main.svelte';
  import NotFound from './pages/NotFound.svelte';
  import Signup from './pages/Signup.svelte';
  import Write from './pages/Write.svelte';
  import '../src/css/style.css';
  import { GoogleAuthProvider, getAuth, signInWithCredential } from "firebase/auth";
  import { user$ } from './store';
  import { onMount } from 'svelte';
  import Loading from './pages/Loading.svelte';
  import Mypage from './pages/Mypage.svelte';
  
  
  const routes = {
      // Exact path
      '/': Main,
      '/signup': Signup,
      '/write': Write,
      '/my': Mypage,
      '*': NotFound,
  }

  const provider = new GoogleAuthProvider();
  provider.addScope('https://www.googleapis.com/auth/contacts.readonly');
  
  const auth = getAuth();

  let isLoading = true;

  const checkLogin = async () => {
    const token = localStorage.getItem('token');
    if(!token) return (isLoading = false);

    const credential = GoogleAuthProvider.credential(null, token);
    const result = await signInWithCredential(auth, credential)
    const user = result.user;
    user$.set(user)
    isLoading = false;
  }

  onMount(()=> checkLogin())
</script>

<main></main>

{#if isLoading}
  <Loading />
{:else if !$user$}
  <Login />
{:else}
  <Router routes={routes} />
{/if}