// Päädokumentointi lainaus-hakukentta.js-tiedostossa..

const lahetaHakuData = (tapahtuma) => {
    $.ajax({
        type: 'POST',
        url: '/hakuu/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'tapahtuma': tapahtuma,
        },
        success: (response)=> {
            const data = response.data 
            
            if (Array.isArray(data)) {
                if (window.location.href.indexOf("sivu") > -1) {
                    document.location.href = 'http://127.0.0.1:8000/palautettavat/';
                }
                tulosTaulukko.innerHTML = ""
                    data.forEach(tapahtuma => {
                        tulosTaulukko.innerHTML += `
                            <tr>
                                <td> <img src="${tapahtuma.tuotekuva}" class="tuotekuva" alt="varastotapahtumakuva"> </td>
                                <td> ${tapahtuma.nimike} </td>
                                <td> ${tapahtuma.kappalemaara} </td>
                                <td> ${tapahtuma.lainaaja} </td>
                                <td><button type="button" class="palautus-nappi"><a href="${url}suorita-palautus/${tapahtuma.pk}"> Palauta </a></button></td>
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
                    pagination.style.display = "block";
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
const url = window.location.href;
const hakuForm = document.getElementById('haku-form');
const hakusyote = document.getElementById('hakusyote');
const tulosTaulukko = document.getElementById('tulos-taulukko');
const pagination = document.getElementById('pagination');

const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
console.log(csrf);


hakusyote.addEventListener('keyup', e=>{
    if (tulosTaulukko.classList.contains('piilossa')){
        tulosTaulukko.classList.remove('piilossa')
        taulukkoTulos.style.display = "block";
        lainausTaulukko.style.display = "none";
        pagination.style.display = "none";
    }
    lahetaHakuData(e.target.value);
})
