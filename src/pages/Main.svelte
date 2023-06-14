<script>
  import { getDatabase, ref, onValue} from "firebase/database";
  import Footer from "../components/Footer.svelte";
  import { onMount } from "svelte";

  let date = new Date();
  let hours = date.getHours();
  let minutes = date.getMinutes();
  
  const calcTime = (timeStamp) => {
    const curTime = new Date().getTime() - 9 * 60 * 60 * 1000;
    const time = new Date(curTime - timeStamp);
    const hours = time.getHours();
    const minutes = time.getMinutes();
    const seconds = time.getSeconds();

    if (hours > 0) return `${hours} 시간 전`;
    else if (minutes > 0) return `${minutes} 분 전`;
    else if (seconds > 0) return `${seconds} 초 전`;
    else return "방금 전";
  };

  $: items = []

  const db = getDatabase();
  const itemRef = ref(db, 'items/');

  onMount(()=>{
    onValue(itemRef, (snapshot) => {
      const data = snapshot.val();
      items = Object.values(data).reverse();
    });

  })
</script>

<header>
    <div class="info-bar">
      <div class="info-bar__time">{hours}:{minutes}</div>
      <div class="info-bar__icons">
        <img src="assets/chart-bar.svg" alt="chart-bar" />
        <img src="assets/wifi.svg" alt="wifi" />
        <img src="assets/battery.svg" alt="battery" />
      </div>
    </div>
    <div class="menu-bar">
      <div class="menu-bar__location">
        <div>잠실3동</div>
        <div class="menu-bar__location-icon">
          <img src="assets/arrow-down.svg" alt="arrow-down" />
        </div>
      </div>
      <div class="menu-bar__icons">
        <img src="assets/search.svg" alt="search" />
        <img src="assets/menu.svg" alt="menu" />
        <img src="assets/alert.svg" alt="alert" />
      </div>
    </div>
  </header>

  <main>
    {#each items as item}
    <div class="item-list">
      <div class="item-list__img">
        <img src={item.imgUrl} alt={item.title}>
      </div>
      <div class="item-list__info">
        <div class="item-list__info-title">{item.title}</div>
        <div class="item-list__info-meta">{item.place} {calcTime(item.createAt)}</div>
        <div class="item-list__info-price">{item.price}</div>
        <div>{item.desc}</div>

      </div>
    </div>
    {/each}
    <a class="write-btn" href="/#/write">+ 글쓰기</a>
  </main>

  <Footer location="home"/>

  <div class="media-info-msg">화면을 줄여주세요</div>