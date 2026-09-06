const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let drawing = false;

// Initialize canvas
function initCanvas() {
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = 'white';
    ctx.lineWidth = 18;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
}
initCanvas();

function getPos(e) {
    const rect = canvas.getBoundingClientRect();
    return {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
    };
    
}

function startDraw(e) {
    drawing = true;
    const pos = getPos(e);
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
    e.preventDefault();
}

function draw(e) {
    if (!drawing) return;
    const pos = getPos(e);
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
    e.preventDefault();
}

function stopDraw(e) {
    drawing = false;
    e.preventDefault();
}

// Mouse Events
canvas.addEventListener('mousedown', startDraw);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDraw);
canvas.addEventListener('mouseout', stopDraw);

// Clear Button
document.getElementById('clearBtn').addEventListener('click', () => {
    initCanvas();
    document.getElementById('result').textContent = 'Prediction: ';
});

const API_URL = 'http://localhost:8000/predict';

// Predict Button
document.getElementById('predictBtn').addEventListener('click', async () => {
    const result = document.getElementById('result');
    result.textContent = 'Prediction: ';

    // Sending base64 PNG data URL
    const dataURL = canvas.toDataURL('image/png');

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: dataURL })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        result.textContent = `Prediction: ${data.prediction}`;
    }
    catch {
        console.error('Error occurred while fetching prediction.');
    }
});