const lahetaHakuData = (tuote) => {
    $.ajax({
        type: 'POST',
        url: '/haku/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'tuote': tuote,
        },
        success: (response)=> {
            const data = response.data 
            
            if (Array.isArray(data)) {
                tulosTaulukko.innerHTML = ""
                data.forEach(tuote=> {
                    tulosTaulukko.innerHTML += `
                        <tr>
                            <td> <img src="${tuote.tuotekuva}" class="tuotekuva"> </td>
                            <td> ${tuote.nimike} </td>
                            <td> ${tuote.kappalemaara} </td>
                            <td> - </td>
                        </tr>
                    `
                })
            } else {
                if (hakusyote.value.length > 0) {
                    tulosTaulukko.innerHTML = `<b>${data}</b>`
                } else {
                    tulosTaulukko.classList.add('piilossa')
                    taulukkoTulos.style.display = "none";
                    lainausTaulukko.style.display = "block";
                }
            }
        },
        error: (error) => {
            console.log(error)
        },
    })
}

const taulukkoTulos = document.querySelector('.taulukko-tulos');
const lainausTaulukko = document.querySelector('.taulukko-perus');
taulukkoTulos.style.display = "none";
const url = window.location.href
const hakuForm = document.getElementById('haku-form')
const hakusyote = document.getElementById('hakusyote')
const tulosTaulukko = document.getElementById('tulos-taulukko')

const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
console.log(csrf)


hakusyote.addEventListener('keyup', e=>{
    if (tulosTaulukko.classList.contains('piilossa')){
        tulosTaulukko.classList.remove('piilossa')
        taulukkoTulos.style.display = "block";
        lainausTaulukko.style.display = "none";
    }
    lahetaHakuData(e.target.value)
})
