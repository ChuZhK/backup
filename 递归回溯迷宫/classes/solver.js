var path = []; // 存储可行路径上的方格
var w_, h_; // 用于画可行的路径

// 画出可行的路径
function drawPath() {
    noFill();
    stroke(242, 196, 56);
    strokeWeight(w_ / 2);
    beginShape();
    for (let i = 0; i < path.length; i++) {
      vertex(path[i].i * w_ + w_ / 2, path[i].j * h_ + h_ / 2);
    }
    endShape();
}

// 创建可行的路径
function createPath(current) {
    if(current) {
        path = [];
        let temp = current;
        path.push(temp);
        while (temp.previous) {                       //此处循环是利用类似栈的方式，栈底存放可行路径的终点，栈顶存放可行路径的起点
            //   再像弹出栈顶元素一样出栈，就可以从起点开始画出可行路径
          path.push(temp.previous);
          temp = temp.previous;
        }
    }
}

// 本次作业需要完成该函数，用于探索迷宫中的可行路径
// current 表示当前访问的方格，类型为 Cell
// previous 表示在探索过程中的上一个方格，类型为Cell
async function traverseMaze(current, previous) {
    current.visited = true;
    if (grid[index(current.i, current.j)] === grid[grid.length - 1]) {
        path.push(current);
        return 1;
    }
    // 有用的代码片段:
    // 为实现动画效果，每探索一步需要等待一段时间:
     await sleep(0);
    // 如果要用递归的形式调用traverseMaze函数，请在函数调用前加上 await:
    //await traverseMaze(<one cell>, <previous cell>);
   
    let m = 0;
    if (current.getBottom() != undefined) {
        m++;
    }
    if (current.getLeft() != undefined) {
        m++;
    }
    if (current.getRight() != undefined) {
        m++;
    }
    if (current.getTop() != undefined) {
        m++;
    }

    if (m == 3) {
        stack.push(current);
        stack.push(current);
        stack.push(current);
    }
     else if (m >= 2) {
        stack.push(current);
    }
    if (m === 0) {
        current = stack.pop();
        m = 0;
        if (current.getBottom() != undefined) {
            m++;
        }
        if (current.getLeft() != undefined) {
            m++;
        }
        if (current.getRight() != undefined) {
            m++;
        }
        if (current.getTop() != undefined) {
            m++;
        }
        if (m === 0) {
            current = stack.pop();
        }
        previous = current.previous;
        while (path.pop() != current) {
            ;
        }
        path.push(current);
    }
    if (current.getBottom() != undefined) {              //      *****************************************************************
        current.visited = true;
        path.push(current);
        previous = current;                                                 //*********************
        current = current.getBottom();
        await traverseMaze(current, previous);
        return 1;
    }
   if (current.getRight() != undefined) {
       current.visited = true;
       path.push(current);
        previous = current;
       current = current.getRight();
        await traverseMaze(current, previous);
        return 1;
    }
     if (current.getLeft() != undefined) {
         current.visited = true;
         path.push(current);
        previous = current;
         current= current.getLeft();
        await traverseMaze(current, previous);
        return 1;
    }
    if (current.getTop() != undefined) {
        current.visited = true;
        path.push(current);
        previous = current;
        current= current.getTop();
        await traverseMaze(current, previous);
        return 1;
    }
   
    
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}