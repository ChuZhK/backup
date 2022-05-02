class Cell { // 地图方格
  constructor(i, j) {
    this.i = i;
    this.j = j;
    this.walls = [true, true, true, true];
    this.visited = false;
    
    this.neighbors = [];
  
    this.previous = undefined; // 指向在可行路径中上一个方格
  }

  // 判断this与target方格之间是否有墙
  wallPresent(target) {
    let x = this.i - target.i;
    if (x === 1) {
      return this.walls[3] && target.walls[1];
    } else if (x === -1) {
      return this.walls[1] && target.walls[3];
    }
    let y = this.j - target.j;
    if (y === 1) {
      return this.walls[0] && target.walls[2];
    } else if (y === -1) {
      return this.walls[2] && target.walls[0];
    }
  }

  // 向上获取邻居方格
  getTop() {
    let top = grid[index(this.i, this.j - 1)];
    if(top === undefined || top.visited || this.wallPresent(top)) {
      return undefined; // 方格不存在，或被访问过，或与方格之间有墙，均返回undefined
    }
    return top; // 向上获取邻居方格
  }

  // 向右获取邻居方格
  getRight() {
    let right = grid[index(this.i + 1, this.j)];
    if(right === undefined || right.visited || this.wallPresent(right)) {
      return undefined; // 方格不存在，或被访问过，或与方格之间有墙，均返回undefined
    }
    return right; // 向右获取邻居方格
  }

  // 向下获取邻居方格
  getBottom() {
    let bottom = grid[index(this.i, this.j + 1)];
    if(bottom === undefined || bottom.visited || this.wallPresent(bottom)) {
      return undefined; // 方格不存在，或被访问过，或与方格之间有墙，均返回undefined
    }
    return bottom; // 向下获取邻居方格
  }

  // 向左获取邻居方格
  getLeft() {
    let left = grid[index(this.i - 1, this.j)];
    if(left === undefined || left.visited || this.wallPresent(left)) {
      return undefined; // 方格不存在，或被访问过，或与方格之间有墙，均返回undefined
    }
    return left; // 向左获取邻居方格
  }

  getNeighbors() {
    let top = grid[index(this.i, this.j - 1)];
    let right = grid[index(this.i + 1, this.j)];
    let bottom = grid[index(this.i, this.j + 1)];
    let left = grid[index(this.i - 1, this.j)];

    if (top) {
      this.neighbors.push(top);
    }
    if (right) {
      this.neighbors.push(right);
    }
    if (bottom) {
      this.neighbors.push(bottom);
    }
    if (left) {
      this.neighbors.push(left);
    }
  }

  checkNeighbors() {
    let neighbors = [];

    let top = grid[index(this.i, this.j - 1)];
    let right = grid[index(this.i + 1, this.j)];
    let bottom = grid[index(this.i, this.j + 1)];
    let left = grid[index(this.i - 1, this.j)];

    if (top && !top.visited) {
      neighbors.push(top);
    }
    if (right && !right.visited) {
      neighbors.push(right);
    }
    if (bottom && !bottom.visited) {
      neighbors.push(bottom);
    }
    if (left && !left.visited) {
      neighbors.push(left);
    }

    if (neighbors.length > 0) {
      let r = floor(random(0, neighbors.length));  //floor：返回小于等于X的最大整数
      return neighbors[r];
    } else {
      return undefined;
    }
  }

  highlight() {
    let x = this.i * w;
    let y = this.j * w;
    noStroke();
    fill(242, 196, 56);
    ellipse(x + w/2, y + w/2, w - 6, w - 6);
  }

  show() {
    let x = this.i * w;
    let y = this.j * w;
    stroke(255);
    if (this.walls[0]) {
      line(x, y, x + w, y);
    }
    if (this.walls[1]) {
      line(x + w, y, x + w, y + w);
    }
    if (this.walls[2]) {
      line(x + w, y + w, x, y + w);
    }
    if (this.walls[3]) {
      line(x, y + w, x, y);
    }

    if (this.visited) {
      noStroke();
      fill(242, 87, 73, 150);
      rect(x, y, w, w);
    }
  }

  start() {
    let x = this.i * w;
    let y = this.j * w;
    noStroke();
    fill(0, 255, 0, 255);
    rect(x, y, w - 1, w - 1);
  }

  end() {
    let x = this.i * w + 1;
    let y = this.j * w + 1;
    noStroke();
    fill(255, 0, 0, 255);
    rect(x, y, w - 1, w - 1);
  }
}