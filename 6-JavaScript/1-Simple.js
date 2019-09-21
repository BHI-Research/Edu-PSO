/* ************************************************************** */
function rrandom(min, max) {
    return Math.random() * (max - min) + min;
};
/* ************************************************************** */
function rrandNormal() {
    var u = 0,
        v = 0;
    while (u === 0) u = Math.random(); //Converting [0,1) to (0,1)
    while (v === 0) v = Math.random();
    let num = Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
    num = num / 10.0 + 0.5; // Translate to 0 -> 1
    if (num > 1 || num < 0) return randn_bm(); // resample between 0 and 1
    return num * 2 - 1;
}
/* ************************************************************** */
function fn1(x) {
    var res = 0;

    for (var i = 0; i < x.length; i++) {
        res += (x[i] * x[i]);
    }
    return res;
};
/* ************************************************************** */
function read_args() {


    

    var args = {
        w: 0.5,
        c1: 1.5,
        c2: 2.5,
        n: 50,
        d: 5,
        i: 50,
        box: 10.0,
        x0: 5.0,
        fn: 1,
        loops: 15
    };
    if (process.argv[2]){
        args.w  = parseFloat(process.argv[2]);
    }
    if (process.argv[3]){
        args.c1  = parseFloat(process.argv[3]);
    }
    if (process.argv[4]){
        args.c2  = parseFloat(process.argv[4]);
    }
    if (process.argv[5]){
        args.n  = parseFloat(process.argv[5]);
    }
    if (process.argv[6]){
        args.d  = parseFloat(process.argv[6]);
    }
    if (process.argv[7]){
        args.i  = parseFloat(process.argv[7]);
    }
    if (process.argv[8]){
        args.box  = parseFloat(process.argv[8]);
    }
    if (process.argv[9]){
        args.x0  = parseFloat(process.argv[9]);
    }
    if (process.argv[10]){
        args.fn  = parseFloat(process.argv[10]);
    }
    if (process.argv[11]){
        args.loops  = parseFloat(process.argv[11]);
    }

    return args;

};
/* ************************************************************** */

class Swarm {
    constructor(args, bounds, x0) {

        this.n = args.n;
        this.pos = [];
        this.vel = [];

        this.err = [];
        this.err_best = [];

        if (typeof x0 === "undefined") {
            this.dimensions = bounds.length;

            for (var i = 0; i < this.n; i++) {

                var v = [];
                var x = [];
                for (var j = 0; j < this.dimensions; j++) {
                    v.push(rrandom(-1, 1));
                    x.push(rrandom(bounds[j][0], bounds[j][1]));
                }
                this.vel.push(v);
                this.pos.push(x);
            }
        } else {
            this.dimensions = x0.length;
            for (var i = 0; i < this.n; i++) {
                var v = [];
                var x = [];
                for (var j = 0; j < this.dimensions; j++) {
                    v.push(rrandom(-1, 1));
                    x.push(x0[j]);
                }
                this.vel.push(v);
                this.pos.push(x);
            }
        }
        this.pos_best = this.pos;
        this.bounds = bounds;
        this.err_best_g = Infinity;
        this.pos_best_g = this.pos[0][0];
    };
    evaluate() {
        for (var i = 0; i < this.n; i++) {
            this.err[i] = fn1(this.pos[i]);
        }
    };
    update(args) {
        for (var j = 0; j < this.n; j++) {
            for (var i = 0; i < this.dimensions; i++) {

                //Update Vel
                var r1 = rrandom(0, 1);
                var r2 = rrandom(0, 1);

                var vel_cognitive = args.c1 * r1 * (this.pos_best[j][i] - this.pos[j][i]);
                var vel_social = args.c2 * r2 * (this.pos_best_g[i] - this.pos[j][i]);
                this.vel[j][i] = args.w * this.vel[j][i] + vel_cognitive + vel_social;

                // Update Pos
                this.pos[j][i] += this.vel[j][i];               
                
                if (this.pos[j][i] > this.bounds[i][1]) {
                    this.pos[j][i] = this.bounds[i][1];
                }

                if (this.pos[j][i] < this.bounds[i][0]) {
                    this.pos[j][i] = this.bounds[i][0];
                }
            }
        }
    };
    run(args) {
        var i = 0;
        while (i < args.i) {

            this.evaluate();

            for (var j = 0; j < this.n; j++) {
                if (this.err[j] < this.err_best_g) {
                    this.pos_best_g = this.pos[j];
                    this.err_best_g = this.err[j];
                }
                this.update(args);
            }
            if (args.verbose)
                console.log("#", i + 1, "\tBest Solution:\t ", this.err_best_g);
            i += 1;

        }
        return {
            value: this.pos_best_g,
            error: this.err_best_g
        };

    };
}



function main() {

    var initial = [];
    var bounds = [];

    args = read_args();

    
    console.log  (args);

    if (args.fn == 1)
        var fn = fn1;
    else
        console.log("ERROR : FUNCTION NOT FOUND");


    var box_limit = [-args.box, args.box];


    for (var i = 0; i < args.d; i++) {
        initial.push(args.x0);
        bounds.push(box_limit);
    }

     var pso = new Swarm(args, bounds);


    console.log('*****************************');
    console.time('pso.run');
    var solution = pso.run(args);
    console.timeEnd('pso.run');
    console.log('ERROR:\t', solution.error);
    console.log('SOLUTION:\t', solution.value);
    console.log('*****************************');

    /*
    if args.file:
        file_output(args, t, solution)*/

};


main();