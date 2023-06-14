<script>
    export let location;
    const moveToHome = () => window.location.hash = '/';
    const moveToMyPage = () => window.location.hash = '/my';
</script>

<footer>
    <div class="footer-block">
      <button class="footer-icons" on:click={moveToHome}>
        <div class="footer-icons__img">
            {#if location === "home"}
              <img src="assets/home-solid.svg" alt="home" />
            {:else}
              <img src="assets/home-outline.svg" alt="home" />
            {/if}
        </div>
        <div class="footer-icons__desc">홈</div>
      </button>
      <div class="footer-icons">
        <div class="footer-icons__img">
          <img src="assets/docu.svg" alt="docu" />
        </div>
        <div class="footer-icons__desc">동네생활</div>
      </div>
      <div class="footer-icons">
        <div class="footer-icons__img">
          <img src="assets/loca.svg" alt="loca" />
        </div>
        <div class="footer-icons__desc">내 근처</div>
      </div>
      <div class="footer-icons">
        <div class="footer-icons__img">
          <img src="assets/chat.svg" alt="chat" />
        </div>
        <div class="footer-icons__desc">채팅</div>
      </div>
      <button class="footer-icons" on:click={moveToMyPage}>
        <div class="footer-icons__img">
          {#if location === "my"}
            <img src="assets/user-solid.svg" alt="user" />
          {:else}
            <img src="assets/user-outline.svg" alt="user" />
          {/if}
        </div>
        <div class="footer-icons__desc">나의 당근</div>
      </button>
    </div>
  </footer>