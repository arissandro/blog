
const canvas = document.getElementById("matrix");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight / 2;

const opacity = 1;

const characters = "01000001 01110010 01101001 01110011 01110011 01100001 01101110 01100100 01110010 01101111 00100000 01000110 01110010 01100001 01101110 01100011 01101001 01110011 01100011 01101111";
const charactersArray = characters.split("");

const fontSize = 16;
const columns = canvas.width / fontSize;
const drops = [];
for (let i = 0; i < columns; i++) {
    drops[i] = Math.floor(Math.random() * canvas.height);
}

function drawMatrixRain() {

const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);

gradient.addColorStop(0, `rgba(0, 255, 255, ${opacity})`); // Cor inicial: Azul 
gradient.addColorStop(1, `rgba(0, 255, 0, ${opacity})`); // Cor final: Verde 


    ctx.fillStyle = `rgba(1, 1, 1, ${opacity})`;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = gradient;
    ctx.font = `${fontSize}px monospace`;

    for (let i = 0; i < drops.length; i++) {
        const character = charactersArray[Math.floor(Math.random() * charactersArray.length)];
        ctx.fillText(character, i * fontSize, drops[i] * fontSize);

        if (drops[i] * fontSize > canvas.height && Math.random() > 0.95) {
            drops[i] = 0;
        }

        drops[i]++;
    }

    setTimeout(drawMatrixRain, 100);
}

drawMatrixRain();
