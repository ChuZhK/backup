let current_node=null;
let cla_current=null;
var particles = [];
var cx,cy;

var numOfParticles = 1500; // 需要调整这个星体个数
var my_judge_num=45;      //该数值越大模拟越精确，帧率越低（以某一点为圆心进行K近邻搜索的半径）

var zoom=0.4;
var offset={'x':0,'y':0};

var Mass = 10;
var Walls = true;
var Collision = false;
var Kill = true;



function clearAll() {
	particles=[];
}

function setup() {
	createCanvas(windowWidth, windowHeight);
	cx=windowWidth/2;
	cy=windowHeight/2;
	my_cx=windowWidth;
    my_cy=windowHeight;
	stroke(255);
	for (var i = numOfParticles; i >= 0; i--) {
		var p = new Particle(cx *(1 + Math.cos(i * 2 * 3.14 / numOfParticles)), cy * (1 + Math.sin(i * 2 * 3.14 / numOfParticles)), 0, 0, 0, 0, random(20, 30), 1);
		particles.push(p);
	}
}
function draw() {
	

	background(0,40,100);
	push();
	scale(zoom);
	translate(offset.x,offset.y);
	calcNewton(); // 主要是这个计算耗时
	for (var i = particles.length - 1; i >= 0; i--) {
		particles[i].render();
		particles[i].update();
	}
	pop();
	textSize(12);
	fill(255);
	text('Frame Rate: ' + frameRate().toFixed(0) + ' Particles:' + particles.length,20,windowHeight-20);
}

class Particle {
	constructor(x,y,vx,vy,ax,ay,mass){
		this.x=x; // x 坐标
		this.y=y; // y 坐标
		this.vx=vx; // x 轴速度
		this.vy=vy; // y 轴速度
		this.ax=ax; // x 轴加速度
		this.ay=ay; // y 轴加速度
		this.mass=mass; // 质量
		this.r=Math.log(Math.abs(mass)); // 半径
		this.myColor=color(255,255,255,128);
		
	}
	// Skips Math.sqrt for faster comparisons
	sqDistanceFrom(other) {
		const dx = other.x - this.x;
		const dy = other.y - this.y;
	
		return dx * dx + dy * dy;
	  }
	
	  // Pythagorus: a^2 = b^2 + c^2
	  distanceFrom(other) {
		return Math.sqrt(this.sqDistanceFrom(other));
	  }
	  //******************** */
	visit=false;

	render(){
		fill(this.myColor);
		stroke(this.myColor)
		ellipse(this.x,this.y,this.r*4);
	}

	updateAcc(ax,ay) {
		this.ax=ax*0.5;
		this.ay=ay*0.5;
	}; 

	update() {
		this.vx+=this.ax;
		this.vy+=this.ay;
		this.x+=this.vx;
		this.y+=this.vy;
		this.myColor=color(255,255,255,12+Math.log(this.mass)*8);	
	}; 
}


// 四叉树

class Point {
	constructor(x, y, data) {
	  this.x = x;
	  this.y = y;
	  this.userData = data;
	}
  
	//计算两点间距离的平方
	sqDistanceFrom(other) {
	  const dx = other.x - this.x;
	  const dy = other.y - this.y;
  
	  return dx * dx + dy * dy;
	}
  
	//两点间的欧氏距离
	distanceFrom(other) {     
	  return Math.sqrt(this.sqDistanceFrom(other));
	}
  }
  
  class Rectangle {
	constructor(x, y, w, h) {
	  this.x = x;
	  this.y = y;
	  this.w = w;
	  this.h = h;
	  this.left = x - w / 2;
	  this.right = x + w / 2;
	  this.top = y - h / 2;
	  this.bottom = y + h / 2;
	}
  
	contains(particle) {
	  return (
		this.left <= particle.x && particle.x <= this.right &&
		this.top <= particle.y && particle.y <= this.bottom
	  );
	}
  
	intersects(range) {
	  return !(
		this.right < range.left || range.right < this.left ||
		this.bottom < range.top || range.bottom < this.top
	  );
	}
  
	subdivide(quadrant) {
	  switch (quadrant) {
		case 'ne':
		  return new Rectangle(this.x + this.w / 4, this.y - this.h / 4, this.w / 2, this.h / 2);
		case 'nw':
		  return new Rectangle(this.x - this.w / 4, this.y - this.h / 4, this.w / 2, this.h / 2);
		case 'se':
		  return new Rectangle(this.x + this.w / 4, this.y + this.h / 4, this.w / 2, this.h / 2);
		case 'sw':
		  return new Rectangle(this.x - this.w / 4, this.y + this.h / 4, this.w / 2, this.h / 2);
	  }
	}
  
	xDistanceFrom(particle) {
	  if (this.left <= particle.x && particle.x <= this.right) {
		return 0;
	  }
  
	  return Math.min(
		Math.abs(particle.x - this.left),
		Math.abs(particle.x - this.right)
	  );
	}
  
	yDistanceFrom(particle) {
	  if (this.top <= particle.y && particle.y <= this.bottom) {
		return 0;
	  }
  
	  return Math.min(
		Math.abs(particle.y - this.top),
		Math.abs(particle.y - this.bottom)
	  );
	}
  
	sqDistanceFrom(particle) {
	  const dx = this.xDistanceFrom(particle);
	  const dy = this.yDistanceFrom(particle);
  
	  return dx * dx + dy * dy;
	}
  
	
	distanceFrom(particle) {
	  return Math.sqrt(this.sqDistanceFrom(particle));
	}
  }
  
  //用于范围检测的圆类
  class Circle {
	constructor(x, y, r) {
	  this.x = x;
	  this.y = y;
	  this.r = r;
	  this.rSquared = this.r * this.r;
	}
  
	contains(particle) {
	 //检测1某一个行星是否在该圆类的内部
	  let d = Math.pow((particle.x - this.x), 2) + Math.pow((particle.y - this.y), 2);
	  return d <= this.rSquared;
	}
  
	intersects(range) {
  
	  let xDist = Math.abs(range.x - this.x);
	  let yDist = Math.abs(range.y - this.y);
  
	  // 圆的半径
	  let r = this.r;
  
	  let w = range.w / 2;
	  let h = range.h / 2;
  
	  let edges = Math.pow((xDist - w), 2) + Math.pow((yDist - h), 2);
  
	  // 不在园内
	  if (xDist > (r + w) || yDist > (r + h))
		return false;
  
	  // 在园的内部
	  if (xDist <= w || yDist <= h)
		return true;
  
	  // 在园的边上
	  return edges <= this.rSquared;
	}
  }
  
  class QuadTree {
	constructor(boundary, capacity) {
	  if (!boundary) {
		throw TypeError('boundary is null or undefined');
	  }
	  if (!(boundary instanceof Rectangle)) {
		throw TypeError('boundary should be a Rectangle');
	  }
	  if (typeof capacity !== 'number') {
		throw TypeError(`capacity should be a number but is a ${typeof capacity}`);
	  }
	  if (capacity < 1) {
		throw RangeError('capacity must be greater than 0');
	  }
	  this.boundary = boundary;
	  this.capacity = capacity;
	  this.particles = [];
	  this.divided = false;
	}
  
	get children() {
	  if (this.divided) {
		return [
		  this.northeast,
		  this.northwest,
		  this.southeast,
		  this.southwest
		];
	  } else {
		return [];
	  }
	}
  

    
	static create() {
	  let DEFAULT_CAPACITY = 8;
	  if (arguments.length === 0) {
		if (typeof width === "undefined") {
		  throw new TypeError("No global width defined");
		}
		if (typeof height === "undefined") {
		  throw new TypeError("No global height defined");
		}
		let bounds = new Rectangle(width / 2, height / 2, width, height);
		return new QuadTree(bounds, DEFAULT_CAPACITY);
	  }
	  if (arguments[0] instanceof Rectangle) {
		let capacity = arguments[1] || DEFAULT_CAPACITY;
		return new QuadTree(arguments[0], capacity);
	  }
	  if (typeof arguments[0] === "number" &&
		  typeof arguments[1] === "number" &&
		  typeof arguments[2] === "number" &&
		  typeof arguments[3] === "number") {
		let capacity = arguments[4] || DEFAULT_CAPACITY;
		return new QuadTree(new Rectangle(arguments[0], arguments[1], arguments[2], arguments[3]), capacity);
	  }
	  throw new TypeError('Invalid parameters');
	}
  
	toJSON(isChild) {
	  let obj = { particles: this.particles };
	  if (this.divided) {
		if (this.northeast.particles.length > 0) {
		  obj.ne = this.northeast.toJSON(true);
		}
		if (this.northwest.particles.length > 0) {
		  obj.nw = this.northwest.toJSON(true);
		}
		if (this.southeast.particles.length > 0) {
		  obj.se = this.southeast.toJSON(true);
		}
		if (this.southwest.particles.length > 0) {
		  obj.sw = this.southwest.toJSON(true);
		}
	  }
	  if (!isChild) {
		obj.capacity = this.capacity;
		obj.x = this.boundary.x;
		obj.y = this.boundary.y;
		obj.w = this.boundary.w;
		obj.h = this.boundary.h;
	  }
	  return obj;
	}
  
	static fromJSON(obj, x, y, w, h, capacity) {
	  if (typeof x === "undefined") {
		if ("x" in obj) {
		  x = obj.x;
		  y = obj.y;
		  w = obj.w;
		  h = obj.h;
		  capacity = obj.capacity;
		} else {
		  throw TypeError("JSON missing boundary information");
		}
	  }
	  let qt = new QuadTree(new Rectangle(x, y, w, h), capacity);
	  qt.particles = obj.particles;
	  if (
		"ne" in obj ||
		"nw" in obj ||
		"se" in obj ||
		"sw" in obj
	  ) {
		let x = qt.boundary.x;
		let y = qt.boundary.y;
		let w = qt.boundary.w / 2;
		let h = qt.boundary.h / 2;
  
		if ("ne" in obj) {
		  qt.northeast = QuadTree.fromJSON(obj.ne, x + w/2, y - h/2, w, h, capacity);
		} else {
		  qt.northeast = new QuadTree(qt.boundary.subdivide('ne'), capacity);
		}
		if ("nw" in obj) {
		  qt.northwest = QuadTree.fromJSON(obj.nw, x - w/2, y - h/2, w, h, capacity);
		} else {
		  qt.northwest = new QuadTree(qt.boundary.subdivide('nw'), capacity);
		}
		if ("se" in obj) {
		  qt.southeast = QuadTree.fromJSON(obj.se, x + w/2, y + h/2, w, h, capacity);
		} else {
		  qt.southeast = new QuadTree(qt.boundary.subdivide('se'), capacity);
		}
		if ("sw" in obj) {
		  qt.southwest = QuadTree.fromJSON(obj.sw, x - w/2, y + h/2, w, h, capacity);
		} else {
		  qt.southwest = new QuadTree(qt.boundary.subdivide('sw'), capacity);
		}
  
		qt.divided = true;
	  }
	  return qt;
	}
  
	subdivide() {
	  this.northeast = new QuadTree(this.boundary.subdivide('ne'), this.capacity);
	  this.northwest = new QuadTree(this.boundary.subdivide('nw'), this.capacity);
	  this.southeast = new QuadTree(this.boundary.subdivide('se'), this.capacity);
	  this.southwest = new QuadTree(this.boundary.subdivide('sw'), this.capacity);
  
	  this.divided = true;
	}
  
	insert(particle) {
	  if (!this.boundary.contains(particle)) {
		return false;
	  }
  
	  if (this.particles.length < this.capacity) {
		this.particles.push(particle);
		return true;
	  }
  
	  if (!this.divided) {
		this.subdivide();
	  }
  
	  return (
		this.northeast.insert(particle) ||
		this.northwest.insert(particle) ||
		this.southeast.insert(particle) ||
		this.southwest.insert(particle)
	  );
	}
  
	query(range, found) {
	  if (!found) {
		found = [];
	  }
  
	  if (!range.intersects(this.boundary)) {
		return found;
	  }
  
	  for (let p of this.particles) {
		if (range.contains(p)) {
		  found.push(p);
		}
	  }
	  if (this.divided) {
		this.northwest.query(range, found);
		this.northeast.query(range, found);
		this.southwest.query(range, found);
		this.southeast.query(range, found);
	  }
  
	  return found;
	}
  
	closest(searchPoint, maxCount = 1, maxDistance = Infinity) {
	  if (typeof searchPoint === "undefined") {
		throw TypeError("Method 'closest' needs a point");
	  }
  
	  const sqMaxDistance = maxDistance ** 2;
	  return this.kNearest(searchPoint, maxCount, sqMaxDistance, 0, 0).found;
	}
  
	//最近邻查找函数
	kNearest(searchPoint, maxCount, sqMaxDistance, furthestSqDistance, foundSoFar) {
	  let found = [];
  
	  this.children.sort((a, b) => a.boundary.sqDistanceFrom(searchPoint) - b.boundary.sqDistanceFrom(searchPoint))
		.forEach((child) => {
		  const sqDist = child.boundary.sqDistanceFrom(searchPoint);
		  if (sqDist > sqMaxDistance) {
			return;
		  } else if (foundSoFar < maxCount || sqDist < furthestSqDistance) {
			const result = child.kNearest(searchPoint, maxCount, sqMaxDistance, furthestSqDistance, foundSoFar);
			const childPoints = result.found;
			found = found.concat(childPoints);
			foundSoFar += childPoints.length;
			furthestSqDistance = result.furthestSqDistance;
		  }
		});
  
	  this.particles
		.sort((a, b) => a.sqDistanceFrom(searchPoint) - b.sqDistanceFrom(searchPoint))
		.forEach((p) => {
		  const sqDist = p.sqDistanceFrom(searchPoint);
		  if (sqDist > sqMaxDistance) {
			return;
		  } else if (foundSoFar < maxCount || sqDist < furthestSqDistance) {
			found.push(p);
			furthestSqDistance = Math.max(sqDist, furthestSqDistance);
			foundSoFar++;
		  }
		});
  
	  return {
		found: found.sort((a, b) => a.sqDistanceFrom(searchPoint) - b.sqDistanceFrom(searchPoint)).slice(0, maxCount),
		furthestDistance: Math.sqrt(furthestSqDistance),
	  };
	}
  
	forEach(fn) {
	  this.particles.forEach(fn);
	  if (this.divided) {
		this.northeast.forEach(fn);
		this.northwest.forEach(fn);
		this.southeast.forEach(fn);
		this.southwest.forEach(fn);
	  }
	}
  
	merge(other, capacity) {
	  let left = Math.min(this.boundary.left, other.boundary.left);
	  let right = Math.max(this.boundary.right, other.boundary.right);
	  let top = Math.min(this.boundary.top, other.boundary.top);
	  let bottom = Math.max(this.boundary.bottom, other.boundary.bottom);
  
	  let height = bottom - top;
	  let width = right - left;
  
	  let midX = left + width / 2;
	  let midY = top + height / 2;
  
	  let boundary = new Rectangle(midX, midY, width, height);
	  let result = new QuadTree(boundary, capacity);
  
	  this.forEach(particle => result.insert(particle));
	  other.forEach(particle => result.insert(particle));
  
	  return result;
	}
  
	get length() {
	  let count = this.particles.length;
	  if (this.divided) {
		count += this.northwest.length;
		count += this.northeast.length;
		count += this.southwest.length;
		count += this.southeast.length;
	  }
	  return count;
	}
  }
  
  if (typeof module !== "undefined") {
	module.exports = { Point, Rectangle, QuadTree, Circle };
  }
  



function calcNewton() {
	qt_tree=QuadTree.create();
	var pnum=particles.length;
	for(var i=pnum-1;i>=0;i--){
		particles[i].visit=false;
		particles[i].ax=0;
		particles[i].ay=0;
		qt_tree.insert(particles[i]);
	}
	for(var i=pnum-1;i>=0;i--){
		
		
		let body=particles[i];
		body.visit=true;
		let R=my_judge_num*body.r;
		let range=new Circle(body.x,body.y,R);
		let near_particles=qt_tree.query(range);
		
		for(let near_body of near_particles){
			if(near_body.visit==false){
				var d=dist(body.x,body.y,near_body.x,near_body.y);
				var dx=near_body.x-body.x;
				var dy=near_body.y-body.y;
				if(d>(body.r+near_body.r)){
					body.ax += near_body.mass*dx/(d*d*d); //Sum of GM*X/r*r*r
					body.ay += near_body.mass*dy/(d*d*d); //Sum of GM*Y/r*r*r	
					near_body.ax +=(-body.mass*dx/(d*d*d));	
					near_body.ay +=(-body.mass*dy/(d*d*d));		
				}
				if(d <= (body.r+near_body.r)+5 && i!=particles.length-1 && Collision){
					var netMass=body.mass+near_body.mass;
					var temp=new Particle((body.x*body.mass+near_body.x*near_body.mass)/netMass, (body.y* body.mass + near_body.y * near_body.mass) / netMass, (body.vx * body.mass + near_body.vx * near_body.mass) / netMass, (body.vy * body.mass + near_body.vy * near_body.mass)/netMass,0,0,netMass);
					particles[i]=temp;
					particles.splice(j,1);
					pnum=particles.length;
				}
			}
		}
	
	

		r1=dist(body.x,body.y,0,body.y); // repelent wall
		r2=dist(body.x,body.y,body.x,0); // repelent wall
		r3=dist(body.x,body.y,windowWidth/zoom,body.y); // repelent wall
		r4=dist(body.x,body.y,body.x,windowHeight/zoom); // repelent wall

		if(Walls){
			body.ax+= -1000*(0-body.x)/(r1*r1*r1);
			body.ay+= -1000*(0-body.y)/(r2*r2*r2);
			body.ax+= -1000*(windowWidth/zoom-body.x)/(r3*r3*r3);
			body.ay+= -1000*(windowHeight/zoom-body.y)/(r4*r4*r4);
		}

		

		if(Kill && (body.x<0 || body.y<0||body.x>windowWidth/zoom || body.y>windowHeight/zoom)) {
			particles.splice(i,1);
			pnum--;
		}
	}
}

