const getImageUrl = async (itemId) => {
    const res = await fetch(`/images/${itemId}`)
    const data = await res.blob()
    const url = URL.createObjectURL(data)
    return url
}

const calcTime = (timeStamp) => {
    const curTime = new Date().getTime() - 9 * 60 * 60 * 1000
    const time = new Date(curTime - timeStamp)
    const hours = time.getHours()
    const minutes = time.getMinutes()
    const seconds = time.getSeconds()

    if (hours > 0) return `${hours} 시간 전`
    else if (minutes > 0) return `${minutes} 분 전`
    else if (seconds > 0) return `${seconds} 초 전`
    else return '방금 전'
}

const renderData = (data) => {
    const main = document.querySelector('main')
    data.reverse().forEach(async (obj) => {
        const itemListDiv = document.createElement('div')
        itemListDiv.className = 'item-list'

        const imgDiv = document.createElement('div')
        imgDiv.className = 'item-list__img'

        const img = document.createElement('img')
        img.src = await getImageUrl(obj.id)

        const infoDiv = document.createElement('div')
        infoDiv.className = 'item-list__info'

        const infoTitleDiv = document.createElement('div')
        infoTitleDiv.className = 'item-list__info-title'
        infoTitleDiv.innerText = obj.title

        const infoMetaDiv = document.createElement('div')
        infoMetaDiv.className = 'item-list__info-meta'
        infoMetaDiv.innerText = obj.place + ' ' + calcTime(obj.createAt)

        const infoPriceDiv = document.createElement('div')
        infoPriceDiv.className = 'item-list__info-price'
        infoPriceDiv.innerText = obj.price

        imgDiv.appendChild(img)

        infoDiv.appendChild(infoTitleDiv)
        infoDiv.appendChild(infoMetaDiv)
        infoDiv.appendChild(infoPriceDiv)

        itemListDiv.appendChild(imgDiv)
        itemListDiv.appendChild(infoDiv)

        main.appendChild(itemListDiv)
    })
}

const fetchList = async () => {
    const res = await fetch('/items')
    const data = await res.json()
    renderData(data)
}

fetchList()