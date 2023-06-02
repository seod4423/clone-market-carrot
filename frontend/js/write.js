const form = document.querySelector('#write-form')

const handleSubmitForm = async (e) => {
    const body = new FormData(form)
    body.append('createAt', new Date().getTime())
    e.preventDefault();
    try {
        const res = await fetch('/items', {
            method: "POST",
            body,
        })
        const data = await res.json()
        if (data === '200') window.location.pathname = '/'
    } catch (error) {
        console.error(error)

    }
}

form.addEventListener('submit', handleSubmitForm)