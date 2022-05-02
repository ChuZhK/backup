let cols, rows;
let w = 10; // 单个方格的宽度
let maze_width = 400; // 地图宽度
let maze_height = 400; // 地图高度

// 所有方格均按行排列存在该数组中
// 如果地图为2x2，则grid为：
// grid = [Cell(0, 0), Cell(1, 0), Cell(0, 1), Cell(1, 1)]
// 所以迷宫起点为：grid[0], 迷宫终点为 grid[grid.length - 1]
let grid = []; 
let started = false;

function setup() {
  let c = createCanvas(830, 400);
  c.parent('canvasArea');
  generateMaze(maze_width, maze_height); // 生成地图
}

function draw() {
  push();
  translate(width - maze_width * 1.5, 0);
  fill(51);
  noStroke();
  rect(0, 0, maze_width, maze_height);
  for (let i = 0; i < grid.length; i++) {
    grid[i].show();
  }
  grid[0].start();
  grid[grid.length - 1].end();
  drawPath();
  pop();

  if (started == false) {
    // 迷宫探索出发位置，从左上角开始。
    // 起点处的方格不存在previous方格，所以第二个参数为undefined
    traverseMaze(grid[0], undefined);
    started = true;
  }
}

function index(i, j) {
  if (i < 0 || j < 0 || i > cols - 1 || j > rows - 1) {
    return -1;
  }
  return i + j * cols;
}