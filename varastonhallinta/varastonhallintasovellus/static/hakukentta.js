// EPÄTOIMIVA HAKUKENTTÄ, YRITYS SAADA KUVIA NÄKYMÄÄN..

const sendSearchData = (game) => {
    $.ajax({
        type: 'POST',
        url: '/search/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'game': game,
        },
        success: (res)=> {
            console.log(res)
            const data = res.data 
            if (Array.isArray(data)) {
                resultsBox.innerHTML = ""
                data.forEach(game=> {
                    resultsBox.innerHTML += `
                        <tr>
                            <td> <h1> ${game.nimike}</h1> </td>
                            <td> <img src="${game.tuotekuva}" class="game-img"> </td>
                        </tr>
                        `
                })
            } else {
                if (searchInput.value.length > 0) {
                    resultsBox.innerHTML = `<b>${data}</b>`
                } else {
                    resultsBox.classList.add('not-visible')
                }
            }
        },
        error: (err) => {
            console.log(err)
        },
    })
}

const url = window.location.href
const searchForm = document.getElementById('search-form')
const searchInput = document.getElementById('search-input')
const resultsBox = document.getElementById('results-box')

const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
console.log(csrf)


searchInput.addEventListener('keyup', e=>{
    console.log(e.target.value)
    
    if (resultsBox.classList.contains('not-visible')){
        resultsBox.classList.remove('not-visible')
    }

    sendSearchData(e.target.value)
});


/* // TOIMIVA HAKUKENTTÄ


// hakukenttä-muuttujaan tallennetaan document.querySelector:n avulla
//   lainaus.html:ssä sijaitsevan hakukenttä-id:n tiedot
const hakukentta = document.querySelector('#hakukentta');

const taulukkoTulos = document.querySelector('.taulukko-tulos');
// Poistetaan taulukkotulos näkyviltä, kun sivu avataan
taulukkoTulos.style.display = "none";
const lainausTaulukko = document.querySelector('.taulukko-perus');
const tbody = document.querySelector('.table-body');

const eiTulosta = document.querySelector('.ei-tulosta')
eiTulosta.style.display = "none";

// Tapahtumakuuntelija jota kutsutaan joka kerta, kun
//    hakukenttään kirjoitetaan jotain. Sen seurauksena
//    suoritetaan event-funktio (e).
hakukentta.addEventListener('keyup', (e) => {
    const hakuarvo = e.target.value;

    // Trimmataan hakuarvosta tyhjät osat, eli välilyönnit ja
    //    tarkistetaan onko sen pituus isompi kuin 0.
    if(hakuarvo.trim().length > 0) {      
        // Tyhjennetään tbody-classin sisältö
        tbody.innerHTML = "";

        // Tehdään api-pyyntö fetch()-menetelmän avulla, joka pyytää tiedot
        //    palvelimelle ja lataa ne verkkosivulle
        fetch("/tuotehaku/", {
            // Json.stringify()-menetelmä muuntaa JavaScript-arvot
            //   JSON-merkkijonoksi
            body: JSON.stringify({ hakuteksti: hakuarvo }),
            method: 'POST',
        })
            // Yhdistetetään jsoniin
            .then((res) => res.json())
            // Palautetaan data (hakuteksti, hakuarvo)
            .then((data) => {
                // Jos hakua vastaavaa dataa on, palautetaan tulostalukko
                //   block-elementin avulla ja alkuperäinen taulukko
                //   piilotetaan.
                taulukkoTulos.style.display = "block";
                lainausTaulukko.style.display = "none";

                // Jos hakua vastaavaa dataa ei ole, palautetaan sivulle 
                //    eiTulosta-block.
                if (data.length === 0) {
                    eiTulosta.style.display = "block";
                } else {
                    eiTulosta.style.display = "none";
                    // Lisätään jokaisen hakua vastaavan tuotteen tiedot
                    //   tbody-classiin.
                    data.forEach((tuote) => {
                        tbody.innerHTML += `
                        <tr>
                            <td>${tuote.tuotekuva.url}</td>
                            <td>${tuote.nimike}</td>
                            <td>${tuote.kappalemaara}</td>
                            <td> - </td>
                        </tr>`;
                    });
                }
            });
    // Kun hakuarvo on pienempi kuin 0, palataan normaaliin näkymään
    //   (piiloitetaan tulostaulukko)
    } else {
        taulukkoTulos.style.display = "none";
        lainausTaulukko.style.display = "block";
        eiTulosta.style.display = "none";
    }
});
 */