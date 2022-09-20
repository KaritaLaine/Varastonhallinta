// Päädokumentointi lainaus-hakukentta.js-tiedostossa..

const lahetaHakuData = (tuote) => {
    $.ajax({
        type: 'POST',
        url: '/haku/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'tuote': tuote,
        },
        success: (response) => {
            const data = response.data

            if (Array.isArray(data)) {
                tulosTaulukko.innerHTML = ""
                if (rooli == "varastonhoitaja") {
                    data.forEach(tuote => {
                        tulosTaulukko.innerHTML += `
                            <tr>
                                <td> <img src="${tuote.tuotekuva}" class="tuotekuva" alt="Tuotekuva"> </td>
                                <td> ${tuote.nimike}</td>
                                <td> ${tuote.tuoteryhma}</td>
                                <td> ${tuote.valmistaja || "-"}</td>
                                <td> ${tuote.kappalemaara}</td>
                                <td><button type="button" id="muokkaa-nappi"><a id="muokkaa-linkki" href="${url}muokkaa-tuotetta/${tuote.pk}">Muokkaa</a></button></td>
                                <td><button type="button" id="poista-nappi"><a id="poista-linkki" href="${url}poista-tuote/${tuote.pk}">Poista</a></button></td>
                            </tr>
                        `
                    })
                } else {
                    data.forEach(tuote => {
                        tulosTaulukko.innerHTML += `
                            <tr>
                                <td> <img src="${tuote.tuotekuva}" class="tuotekuva" alt="Tuotekuva"> </td>
                                <td> ${tuote.nimike}</td>
                                <td> ${tuote.tuoteryhma}</td>
                                <td> ${tuote.valmistaja || "-"}</td>
                                <td> ${tuote.kappalemaara}</td>
                                <td> ${tuote.hankintapaikka || "-"}</td>
                                <td> ${tuote.hankintapaiva || "-"}</td>
                                <td> ${tuote.hankintahinta || "-"}</td>
                                <td> ${tuote.laskun_numero || "-"} </td>
                                <td> ${tuote.kustannuspaikka || "-"}</td>
                                <td> ${tuote.takuuaika || "-"}</td>
                                <td><button type="button" id="muokkaa-nappi"><a id="muokkaa-linkki" href="${url}muokkaa-tuotetta/${tuote.pk}">Muokkaa</a></button></td>
                                <td><button type="button" id="poista-nappi"><a id="poista-linkki" href="${url}poista-tuote/${tuote.pk}">Poista</a></button></td>
                            </tr>
                        `
                    })
                }

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
const rooli = JSON.parse(document.getElementById('user_rooli').textContent);

const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
console.log(csrf)

hakusyote.addEventListener('keyup', e => {
    if (tulosTaulukko.classList.contains('piilossa')) {
        tulosTaulukko.classList.remove('piilossa')
        taulukkoTulos.style.display = "block";
        lainausTaulukko.style.display = "none";
    }
    lahetaHakuData(e.target.value)
})



// Lisätään classeja, jotta eri näkymien cssää voisi muuttaa.

if (rooli == "opettaja" || rooli == "hallinto") {
    $('#hallinta-koko').addClass('hallinto');
} else {
    $('#hallinta-koko').addClass('varastonhoitaja');
}