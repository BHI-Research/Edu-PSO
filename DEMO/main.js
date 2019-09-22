var RADIUS = 10;
var PARTICLES = 100;
var Z_LIMIT = 50;
var DAMPING = 10000;

var ctx = canvas.getContext("2d");

ctx.canvas.width = window.innerWidth;
ctx.canvas.height = window.innerHeight;

window.onresize = function () {
    ctx.canvas.width = window.innerWidth;
    ctx.canvas.height = window.innerHeight;
};



// Vars, Presets
cmpx = ctx.canvas.width / 2;
cmpy = ctx.canvas.height / 2;
cmpz = 25;

// On Mousemove
document.onmousemove = function (e) {
    cmpx = e.clientX;
    cmpy = e.clientY;
};
document.ontouchmove = function (e) {
    cmpx = e.changedTouches[0].pageX;
    cmpy = e.changedTouches[0].pageY;
}
window.addEventListener("wheel", function (e) {
    if (e.deltaY > 0 && cmpz < Z_LIMIT) {
        cmpz += 5;
    } else if (cmpz > 0) {
        cmpz -= 5;
    }

});
document.getElementById("value_w").addEventListener("keyup", update_args);
document.getElementById("value_c1").addEventListener("keyup", update_args);
document.getElementById("value_c2").addEventListener("keyup", update_args);
document.getElementById("value_n").addEventListener("keyup", update_args);

document.getElementById("value_w").addEventListener("change", update_args);
document.getElementById("value_c1").addEventListener("change", update_args);
document.getElementById("value_c2").addEventListener("change", update_args);
document.getElementById("value_n").addEventListener("change", update_args);

/* ************************************************************** */
function read_args() {



    var args = {
        w: 0.5,
        c1: 1.5,
        c2: 2.5,
        n: 100,
        d: 3,


    };

    document.getElementById("value_w").value = args.w;
    document.getElementById("value_c1").value = args.c1;
    document.getElementById("value_c2").value = args.c2;
    document.getElementById("value_n").value = args.n;


    args.w /= DAMPING;
    args.c1 /= DAMPING;
    args.c2 /= DAMPING;

    return args;

};
/* ************************************************************** */
function update_args() {

    args = {
        w: document.getElementById("value_w").value,
        c1: document.getElementById("value_c1").value,
        c2: document.getElementById("value_c2").value,
        n: document.getElementById("value_n").value,
        d: 3
    };

    args.w /= DAMPING;
    args.c1 /= DAMPING;
    args.c2 /= DAMPING;

    delete swarm;
    swarm = new Swarm(args, bounds);


};
/* ************************************************************** */
window.onclick = function () {

    delete swarm;
    swarm = new Swarm(args, bounds);
}
/* ************************************************************** */
function statsPSO(demo, objetive) {

    document.getElementById("value1").innerHTML = "(" + Math.trunc(demo.value[0]) + "," + Math.trunc(demo.value[1]) + "," + Math.trunc(demo.value[2]) + ")";
    document.getElementById("value2").innerHTML =
        Math.round(demo.error * 100) / 100;

    document.getElementById("value3").innerHTML = "(" + Math.trunc(objetive[0]) + "," + Math.trunc(objetive[1]) + "," + Math.trunc(objetive[2]) + ")";


}

/* ************************************************************** */
function drawFrame() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);


    ctx.beginPath();
    var mouse_mark = RADIUS + cmpz + 10;
    ctx.arc(cmpx, cmpy, mouse_mark, 0, 2 * Math.PI);
    ctx.strokeStyle = "#000";
    ctx.stroke();


    for (i = 0; i < args.n; i++) {

        //Draw Lines
        ctx.beginPath();

        ctx.moveTo(swarm.pos_best_g[0], swarm.pos_best_g[1]);
        ctx.lineTo(swarm.pos[i][0], swarm.pos[i][1]);
        ctx.strokeStyle = "hsl(" + (swarm.pos[i][0] + swarm.pos[i][1]) + ",60%,60%)";

        ctx.stroke();

        // Draw Particles
        ctx.beginPath();
        ctx.fillStyle = "hsl(" + (swarm.pos[i][0] + swarm.pos[i][1]) + ",60%,60%)";


        let r = RADIUS;
        if (swarm.pos[i][2] > 0) {
            r = RADIUS + swarm.pos[i][2];
        }

        ctx.arc(swarm.pos[i][0], swarm.pos[i][1], r, 0, 2 * Math.PI);
        ctx.fill();
        ctx.closePath();
    }

    if (cmpx != objetive[0] ||
        cmpy != objetive[1] ||
        cmpz != objetive[2]) {

        objetive[0] = cmpx;
        objetive[1] = cmpy;
        objetive[2] = cmpz;

        swarm.cleanSwarm();
    }
    statsPSO(swarm.demo(args, objetive), objetive);
};

/* ************************************************************** */


var args = read_args();
var space = [canvas.width, canvas.height, 25];
var objetive = [canvas.width / 2, canvas.height / 2, cmpz];
var bounds = [[0, space[0]], [0, space[1]], [0, space[2]]];

var swarm = new Swarm(args, bounds);

setInterval(drawFrame, 1000 / 30);
