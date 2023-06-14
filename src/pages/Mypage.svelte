<script>
  import Footer from "../components/Footer.svelte";
  import { user$ } from "../store";

  const logout = () => {
    user$.set(null)
    localStorage.removeItem('token');
  }
</script>

<div>나의 당근</div>
<button on:click={logout}>로그아웃</button>

<Footer location='my'/>

<style>
    button {
        cursor: pointer;
        border: 1px solid rgba(0, 0, 0, 0.3);
    }
</style>