var swarm = require('./pso');

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




function main() {

    var initial = [];
    var bounds = [];

    var args = read_args();

    

    if (args.fn == 1)
        var fn = fn1;
    else
        console.log("ERROR : FUNCTION NOT FOUND");


    var box_limit = [-args.box, args.box];


    for (var i = 0; i < args.d; i++) {
        initial.push(args.x0);
        bounds.push(box_limit);
    }

    var pso = new swarm.Swarm(args, bounds);

    console.log('*****************************');
    console.time('pso.run');
    var solution = pso.run(args);
    console.timeEnd('pso.run');
    console.log('ERROR:\t', solution.error);
    console.log('SOLUTION:\t', solution.value);
    console.log('*****************************');


};


main();