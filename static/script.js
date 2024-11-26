// const canvas = document.createElement('canvas');
// document.body.appendChild(canvas);
// const ctx = canvas.getContext('2d');

// canvas.style.position = 'fixed';
// canvas.style.top = '0';
// canvas.style.left = '0';
// canvas.style.width = '100%';
// canvas.style.height = '100%';
// canvas.style.zIndex = '-1';
// canvas.width = window.innerWidth;
// canvas.height = window.innerHeight;

// const particles = [];

// function drawStar(ctx, x, y, radius, points, inset) {
//   ctx.beginPath();
//   const angle = Math.PI / points;
//   for (let i = 0; i < 2 * points; i++) {
//     const r = i % 2 === 0 ? radius : radius * inset;
//     const xPos = x + Math.cos(i * angle) * r;
//     const yPos = y + Math.sin(i * angle) * r;
//     ctx.lineTo(xPos, yPos);
//   }
//   ctx.closePath();
// }

// function createParticles() {
//     /**
//      * my function for creating particles
//      * for (let i = 0; i < 10; i++) allows me to know how many particles to create
//      * create stars at random points inside the canvas
//      */
//     for (let i = 0; i < 2; i++) {
//         particles.push({
//         x: Math.random() * canvas.width,
//         y: Math.random() * canvas.height,
//         size: Math.random() * 5 + 1, // Size of the star
//         speedX: Math.random() * 3 - 1.5,
//         speedY: Math.random() * 3 - 1.5,
//         points: 5, // Number of star points
//         inset: 0.5, // Depth of star points
//         });
//     }
// }

// function animateParticles() {
//   ctx.clearRect(0, 0, canvas.width, canvas.height);
//   particles.forEach((particle) => {
//     particle.x += particle.speedX;
//     particle.y += particle.speedY;

//     if (particle.x < 0 || particle.x > canvas.width) particle.speedX *= -1;
//     if (particle.y < 0 || particle.y > canvas.height) particle.speedY *= -1;

//     ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
//     ctx.shadowBlur = 10;
//     ctx.shadowColor = 'white';
//     drawStar(ctx, particle.x, particle.y, 600, particle.points, particle.inset);
//     ctx.fill();
//   });
//   requestAnimationFrame(animateParticles);
// }

// createParticles();
// animateParticles();

// window.addEventListener('resize', () => {
//   canvas.width = window.innerWidth;
//   canvas.height = window.innerHeight;
// });

// const canvas = document.createElement('canvas');
// document.body.appendChild(canvas);
// const ctx = canvas.getContext('2d');

// canvas.style.position = 'fixed';
// canvas.style.top = '0';
// canvas.style.left = '0';
// canvas.style.width = '100%';
// canvas.style.height = '100%';
// canvas.style.zIndex = '10';
// canvas.width = window.innerWidth;
// canvas.height = window.innerHeight;

// const particles = [];

// function random(min, max) {
//   return Math.random() * (max - min) + min;
// }

// class Particle {
//   constructor(x, y) {
//     this.x = x;
//     this.y = y;
//     this.size = random(5, 10);
//     this.speedX = random(-1, 1);
//     this.speedY = random(-1, 1);
//     this.opacity = 1;
//   }

//   update() {
//     this.x += this.speedX;
//     this.y += this.speedY;
//     this.opacity -= 0.02; // Fade effect
//   }

//   draw() {
//     ctx.beginPath();
//     ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
//     ctx.fillStyle = `rgba(0, 0, 0, ${this.opacity})`; // White particles
//     ctx.shadowBlur = 10;
//     ctx.shadowColor = 'white';
//     ctx.fill();
//   }
// }

// function handleParticles() {
//   particles.forEach((particle, index) => {
//     particle.update();
//     particle.draw();

//     // I will remove particles when they are fully transparent
//     if (particle.opacity <= 0) {
//       particles.splice(index, 1);
//     }
//   });
// }

// function animate() {
//   ctx.clearRect(0, 0, canvas.width, canvas.height);
//   handleParticles();
//   requestAnimationFrame(animate);
// }

// // Create particles when the mouse moves
// canvas.addEventListener('mousemove', (e) => {
//   const { clientX, clientY } = e;
//   for (let i = 0; i < 5; i++) {
//     particles.push(new Particle(clientX, clientY));
//   }
// });

// // Resize canvas on window resize
// window.addEventListener('resize', () => {
//   canvas.width = window.innerWidth;
//   canvas.height = window.innerHeight;
// });

// animate();






