let stack = [];

// 随机算法生成迷宫
function generateMaze(width_, height_) {
  cols = floor(width_ / w);
  rows = floor(height_ / w);

  w_ = width_ / cols;
  h_ = height_ / rows;

  for (let j = 0; j < rows; j++) {
    for (let i = 0; i < cols; i++) {
      var cell = new Cell(i, j);
      grid.push(cell);
    }
  }
  
  for (let i = 0; i < grid.length; i++) {
    grid[i].getNeighbors();
  }

  current = grid[0];
  stack.push(current);
  
  while(stack.length > 0) {
    current.visited = true;
    //current.highlight();
    let next = current.checkNeighbors();
    if (next) {
      next.visited = true;

      stack.push(current);

      removeWalls(current, next);

      current = next;
    } else {
      current = stack.pop();
    }
  }

  clearVisisted();
}


function removeWalls(a, b) {
  let x = a.i - b.i;
  if (x === 1) {
    a.walls[3] = false;
    b.walls[1] = false;
  } else if (x === -1) {
    a.walls[1] = false;
    b.walls[3] = false;
  }
  let y = a.j - b.j;
  if (y === 1) {
    a.walls[0] = false;
    b.walls[2] = false;
  } else if (y === -1) {
    a.walls[2] = false;
    b.walls[0] = false;
  }
}

function clearVisisted() {
  for(let i = 0; i < grid.length; i++) {
    grid[i].visited = false;
  }
}