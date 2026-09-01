let indice = 0;
const slides = document.querySelectorAll('.slide');

const dots = document.getElementById('dots');


function crearDots(){
    slides.forEach((_, i) => {
        const d = document.createElement('span');
        d.className = 'dot' + (i === 0 ? ' active'  : '');
        d.onclick = () => irA(i);
        dots.appendClild(d);
    });
}

function muestra() {
    slides.forEach((s, i) => s.classList.toggle('active', i === indice));
    document.querySelectorAll('.dot').forEach((d, i) =>
        d.classList.toggle('active', i === indice));
}

function irA(n){
    indice = n
    muestra();
}

function mover(n){
    indice = n;
    muestra();
}

crearDots();