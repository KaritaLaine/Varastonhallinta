const lahetaHakuData = (tuote) => {
    // Avataan Ajax-metodi ja määritellään tarvittavat tiedot, 
    //     kuten aikaisemmin määritetty osoite.
    $.ajax({
        type: 'POST',
        url: '/haku/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'tuote': tuote,
        },

        // Success-funktioon tallenetaan näkymistä palautettu response-muuttuja.
        success: (response)=> {
            const data = response.data 
            
            if (Array.isArray(data)) {
                if (window.location.href.indexOf("sivu") > -1) {
                    document.location.href = 'http://127.0.0.1:8000/lainattavat/';
                }
                // Jos tuloksia on, lisätään ne tulostauluun `innerHTML`:n avulla.
                tulosTaulukko.innerHTML = ""
                    data.forEach(tuote=> {
                        tulosTaulukko.innerHTML += `
                            <tr>
                                <td> <img src="${tuote.tuotekuva}" class="tuotekuva" alt="Tuotekuva"> </td>
                                <td> ${tuote.nimike} </td>
                                <td> ${tuote.kappalemaara} </td>
                                <td> <button type="button" class="palautus-nappi"><a href="${url}suorita-lainaus/${tuote.pk}"> Lainaa </a></button> </td>
                            </tr>
                        `
                    })
            // Jos hakukentässä on tekstiä ja tuloksia ei löydy, tulostetaan
            //     näkymissä määritelty "Ei hakutulosta.." teksti.        
            } else {
                if (hakusyote.value.length > 0) {
                    tulosTaulukko.innerHTML = `<b>${data}</b>`
                // Jos käyttäjä on poistanut tekstin hakukentästä, tulostaulu ja tulokset piilotetaan,
                //     ja alkuperäinen lainaustaulu laitetaan näkyviin.
                } else {
                    tulosTaulukko.classList.add('piilossa')
                    taulukkoTulos.style.display = "none";
                    lainausTaulukko.style.display = "block";
                    pagination.style.display = "block";
                }
            }
        },
         // Jos tapahtuu virhe, errorfunktio tulostaa konsoliin virhekoodin
        error: (error) => {
            console.log(error)
        },
    })
}

// Tallenetaan html-tiedoston taulukko-tulos classin sisältö tulosTaulu muuttujaan.
const taulukkoTulos = document.querySelector('.taulukko-tulos');
// Piilotetaan tulostaulu
taulukkoTulos.style.display = "none";

const lainausTaulukko = document.querySelector('.taulukko-perus');
const url = window.location.href;
const hakuForm = document.getElementById('haku-form');
const hakusyote = document.getElementById('hakusyote');
const tulosTaulukko = document.getElementById('tulos-taulukko');
const pagination = document.getElementById('pagination');

const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
console.log(csrf);

// Luodaan tapahtumakuuntelija, eli `addEvent.Listener`, jota kutsutaan joka kerta,
//     kun hakukenttään kirjoitetaan jotain. Sen seurauksena suoritetaan event-funktio (e).
hakusyote.addEventListener('keyup', e=>{
    // Tulokset ja tulostaulu tuodaan näkyviin ja alkuperäinen lainaustaulu piilotetaan.
    if (tulosTaulukko.classList.contains('piilossa')){
        tulosTaulukko.classList.remove('piilossa')
        taulukkoTulos.style.display = "block";
        lainausTaulukko.style.display = "none";
        pagination.style.display = "none";
    }
    // Siirretään event data lahetaHakuData-funktioon.
    lahetaHakuData(e.target.value);
}) 
