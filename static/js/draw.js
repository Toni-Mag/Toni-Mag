const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');
let painting = false;

canvas.addEventListener('mousedown', () => painting = true);
canvas.addEventListener('mouseup', () => painting = false);
canvas.addEventListener('mousemove', draw);

function draw(event) {
    if (!painting) return;
    ctx.lineWidth = 5;
    ctx.lineCap = 'round';
    ctx.strokeStyle = 'black';
    ctx.lineTo(event.offsetX, event.offsetY);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(event.offsetX, event.offsetY);
}
