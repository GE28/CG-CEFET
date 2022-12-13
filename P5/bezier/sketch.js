const offset = 20;
const bezierPoints = 100;
const radius = 15;
const points = [];

class SetOnceData {
  constructor() {
    this.data = null;
  }

  set(data) {
    if (this.data === null) {
      this.data = data;
    }
  }

  get() {
    return this.data;
  }
}

class FakePoint {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.mode = new PointNormalMode(this);
    this.instance = null;
  }

  get() {
    return [this.x, this.y];
  }

  set(x, y) {
    this.x = x;
    this.y = y;
  }

  getVector() {
    return createVector(this.x, this.y);
  }

  draw() {
    this.instance = this.mode.draw(this.x, this.y);
  }

  setMode(mode) {
    this.mode = mode;
  }

  isSelected() {
    return this.mode instanceof PointSelectedMode;
  }
}

class PointMode {
  draw(x, y) {
    push();
    this.drawPoint(x, y);
    pop();
  }

  drawPoint(x, y) {
    throw new Error("Subclasses must implement this method");
  }
}

class PointNormalMode extends PointMode {
  drawPoint(x, y) {
    strokeWeight(2);
    circle(x, y, radius * 2);
  }
}

class PointSelectedMode extends PointMode {
  drawPoint(x, y) {
    strokeWeight(2);
    fill(255, 0, 0);
    circle(x, y, radius * 2);
  }
}

function setup() {
  createCanvas(800, 600);
  noLoop();
  fill(0, 102, 153);
  textSize(width / 3);
  textAlign(CENTER, CENTER);
}

function draw() {
  background(200);

  push();
  drawPoints();
  connectPoints();
  pop();

  push();
  drawBezierCurve();
  pop();

  function drawPoints() {
    points.forEach((point) => {
      point.draw();
    });
  }

  function connectPoints() {
    beginShape();
    stroke(0, 0, 0, 50);
    strokeWeight(2);
    noFill();
    points.forEach((point) => {
      vertex(...point.get());
    });
    endShape();
  }

  function drawBezierCurve() {
    beginShape();
    noFill();
    strokeWeight(5);
    for (let i = 0; i <= bezierPoints; i++) {
      vertex(...getBezierPoint(points, i / bezierPoints));
    }
    endShape();
  }
}

function getPointNearTheMouse() {
  return points.findIndex((point) => {
    const distance = dist(
      point.get()[0],
      point.get()[1],
      getMousePoint()[0],
      getMousePoint()[1]
    );
    return distance <= radius * 2;
  });
}

let lastSelectedIndex = null;
let textObject = null;
let pointOffset = new SetOnceData();

function mousePressed() {
  const index = getPointNearTheMouse();
  const point = points[index];
  if (point) {
    point.setMode(new PointSelectedMode(point));
    pointOffset.set(getMouseVector().sub(point.getVector()));
    lastSelectedIndex = index;
  } else {
    createPoint(...getMousePoint());
  }
  redraw();
}

function keyPressed() {
  if (keyCode === DELETE) {
    points.splice(lastSelectedIndex, 1);
  }
  redraw();
}

function mouseDragged() {
  loop();
  const point = points.find((point) => {
    return point.isSelected();
  });
  if (point) {
    point.set(
      getMousePoint()[0] - pointOffset.get().x,
      getMousePoint()[1] - pointOffset.get().y
    );
  }
}

function mouseReleased() {
  points.forEach((point) => {
    if (point.isSelected()) {
      point.setMode(new PointNormalMode(point));
      pointOffset = new SetOnceData();
    }
  });
  redraw();
  noLoop();
}

function createPoint(x, y) {
  points.push(new FakePoint(x, y));
}

function lineVector(coordinateObject, originPoint = { x: 0, y: 0 }) {
  const { x, y } = coordinateObject;
  const { x: xO, y: yO } = originPoint;
  line(x, y, xO, yO);
}

function getPixelDensityMatrix() {
  const realPixelMatrix = drawingContext
    .getTransform()
    .inverse()
    .transformPoint(
      new DOMPoint(mouseX * pixelDensity(), mouseY * pixelDensity())
    );
  return [realPixelMatrix.x, realPixelMatrix.y];
}

function getMousePoint() {
  const [x, y] = getPixelDensityMatrix();
  return [x, y];
}

function getMouseVector() {
  const [x, y] = getPixelDensityMatrix();
  return createVector(x, y);
}

function getSize(vector) {
  return vector.mag();
}

function getBezierPoint(points, t) {
  const cachedData = new Map();
  const n = points.length - 1;
  return points
    .map((point, k) => {
      return [
        point.x * comb(n, k) * (Math.pow(1 - t, n - k) * Math.pow(t, k)),
        point.y * comb(n, k) * (Math.pow(1 - t, n - k) * Math.pow(t, k)),
      ];
    })
    .reduce(
      (points, result) => [result[0] + points[0], result[1] + points[1]],
      [0, 0]
    );

  function getCachedData(key) {
    const data = cachedData.get(key);
    return data ? data : null;
  }

  function setCachedData(key, value) {
    cachedData.set(key, value);
  }

  function fact(n) {
    n = floor(n);
    if (getCachedData(["f", n])) return getCachedData(["f", n]);
    if (n < 2 || !n) return 1;

    let result = 1;
    for (let k = n; k > 1; k--) result *= k;
    setCachedData(["f", n], result);
    return result;
  }

  function comb(n, k) {
    [n, k] = [floor(n), floor(k)];
    if (getCachedData([n, k])) return getCachedData([n, k]);
    const result = fact(n) / (fact(k) * fact(n - k));
    setCachedData([n, k], result);
    return result;
  }
}
