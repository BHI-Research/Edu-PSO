function distance(from, to) {


    let x = (to[0] - from[0]);
    let y = (to[1] - from[1]);
    let z = (to[2] - from[2]);
    return Math.sqrt((x * x + y * y + z * z));

}

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
function read_args() {


    var args = {
        w: 0.5,
        c1: 1.5,
        c2: 2.5,
        n: 1,
        d: 3,
     
   
    };

    return args;

};
/* ************************************************************** */

class Swarm {
    constructor(args, bounds, x0) {

        this.n = args.n;
        this.pos = [];
        this.vel = [];

        this.err = [];

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
                    v.push(rrandom(0, 10));
                    x.push(x0[j]);

                }


                this.vel.push(v);
                this.pos.push(x);

            }

        }
        this.pos_best = this.pos;
        this.bounds = bounds;
        this.err_best_g = Infinity;
        this.pos_best_g = this.pos[0];


    };
    evaluate(objetive) {
        for (var i = 0; i < this.n; i++) {
            this.err[i] = distance(this.pos[i], objetive);

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

    cleanSwarm() {

        for (var j = 0; j < this.n; j++) {

            this.pos_best[j] = this.pos[j];
            this.vel[j] = [rrandom(-1, 1), rrandom(-1, 1), rrandom(-1, 1)];
  


        }



        this.err_best_g = Infinity;
        this.pos_best_g = this.pos[0];



    }

    demo(args, objetive) {



        this.evaluate(objetive);

        for (var j = 0; j < this.n; j++) {
            if (this.err[j] < this.err_best_g) {
                this.pos_best_g = this.pos[j];
                this.err_best_g = this.err[j];
            }
            this.update(args);
        }


        return {
            error: this.err_best_g,
            value: this.pos_best_g
        }

    }

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
            i += 1;

        }


        return {
            value: this.pos_best_g,
            error: this.err_best_g
        };

    };
}

