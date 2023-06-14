<script>
  import { getDatabase, ref, push } from "firebase/database";
  import Footer from "../components/Footer.svelte";
  import { getStorage, ref as refImg, uploadBytes, getDownloadURL } from "firebase/storage";
  
  
  let title;
  let price;
  let desc;
  let place;
  let files;
  
  const storage = getStorage();
  const db = getDatabase();

  function writeUserData(imgUrl) {
    push(ref(db, 'items/'), {
      title,
      price,
      desc,
      place,
      createAt: new Date().getTime(),
      imgUrl,
    });
    alert("글쓰기가 완료되었습니다.");
    window.location.hash = '/';
  }

  const uploadFile = async () => {
    const file = files[0];
    const name = file.name;
    const imgRef = refImg(storage, name)
    await uploadBytes(imgRef, file);
    const url = getDownloadURL(imgRef)
    return url
  }

  const handleSubmit = async () => {
    const url = await uploadFile();
    writeUserData(url)
  }
</script>

<form id="write-form" on:submit|preventDefault={handleSubmit}>
    <div>
      <label for="image">이미지</label>
      <input type="file" id="image" name="image" bind:files />
    </div>
    <div>
      <label for="title">제목</label>
      <input type="text" id="title" name="title" bind:value={title}/>
    </div>
    <div>
      <label for="price">가격</label>
      <input type="number" id="price" name="price" bind:value={price}/>
    </div>
    <div>
      <label for="description">설명</label>
      <input type="text" id="description" name="description" bind:value={desc}/>
    </div>
    <div>
      <label for="place">장소</label>
      <input type="text" id="place" name="place" bind:value={place} />
    </div>
    <button class="write-button" type="submit">저장</button>

    <Footer location="write"/>
  </form>

  <style>
    .write-button {
      background-color: tomato;
      margin: 10px;
      border-radius: 10px;
      padding: 5px 12px;
      color: white;
      cursor: pointer;
    }
  </style>