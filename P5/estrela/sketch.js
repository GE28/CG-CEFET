const radius = 200;
const minorRadius = 100;

function setup() {
  createCanvas(800, 600);
}

function draw() {
  background(200);
  centerOrigin();
  rotateFromMouseVector();
  const sides = getStarSides(getMouseVector(), radius, 3, 10);
  drawStar(minorRadius, radius, sides);
}

function centerOrigin() {
  translate(width / 2, height / 2);
}

function rotateFromMouseVector() {
  function rotateFromVector(v) {
    rotate(createVector(1, 0).angleBetween(v));
  }

  return rotateFromVector(getMouseVector());
}

function getStarSides(vector, maxSize, minSides, maxSides) {
  return floor(map(getSize(vector), 0, maxSize, minSides, maxSides));
}

function drawStar(minRadius, maxRadius, sides) {
  const angle = TWO_PI / sides;

  beginShape();
  for (let i = 0; i < sides; i++) {
    vertex(maxRadius * cos(i * angle), maxRadius * sin(i * angle));
    vertex(
      minRadius * cos((i + 0.5) * angle),
      minRadius * sin((i + 0.5) * angle)
    );
  }
  endShape(CLOSE);
}

function relativeMouse() {
  const matrix = drawingContext.getTransform().inverse();
  const rp = matrix.transformPoint(
    new DOMPoint(mouseX * pixelDensity(), mouseY * pixelDensity())
  );
  return [rp.x, rp.y];
}

function getMouseVector() {
  const [x, y] = relativeMouse();
  return createVector(x, y);
}

function getSize(vector) {
  return vector.mag();
}
