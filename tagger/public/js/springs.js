/* This file is part of Tagger.
 *
 * Tagger is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Tagger is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Tagger.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Original Copyright (c) 2010, Lorenzo Pierfederici <lpierfederici@gmail.com>
 * Contributor(s): 
 */

/* we put all our functions and objects inside "springs" so we don't clutter
 * the namespace */
springs = new(Object);

/* if firebug is not active we create a fake "console" */
if (typeof(console)=="undefined") {
    console = new(Object);
    console.log = function() {};
}

/* data structure */
springs.P = [];
springs.DISTMATRIX = [];

/* DOM elements */
springs.CLASS = 'tag';
springs.SELECTOR = '.' + springs.CLASS;
springs.ANISPEED = 100;
springs.ANIEASING = 'linear';

/* max iterations per solver */
springs.IMAX = 200;

/* simulation constants */
springs.DAMPING = 0.4;       // 0 < DAMPING < 1
springs.SCONST = 1;          // spring constant
springs.RCONST = 6;          // repulsion constant
springs.STEP = 0.4;          // time step for velocities
springs.KMIN = 16;           // min kinetic energy per iteration, below this
                             // value the loop stops


/* return a random integer between rmax and rmin */
springs.rand = function(rmax, rmin) {
    rmin = (typeof(rmin)=='undefined') ? 0 : rmin;
    return Math.floor(Math.random() * (rmax-rmin) + rmin);
}

/* prototype for the Pivot object, that stores the center of gravity of a tag
 * and its current velocity, and the dimensions of the rectangle containing
 * containing the tag */
springs.Pivot = function() {
    this.x = 0;
    this.y = 0;
    this.z = 0;
    this.velocity = [0, 0, 0];
    this.width = 0;
    this.height = 0;
    this.bottomleft = function() {
        return [this.x - (this.width/2), this.y - (this.height/2), 0]
    }
    this.topleft = function() {
        return [this.x - (this.width/2), this.y + (this.height/2), 0]
    }
    this.bottomright = function() {
        return [this.x + (this.width/2), this.y - (this.height/2), 0]
    }
    this.topright = function() {
        return [this.x + (this.width/2), this.y + (this.height/2), 0]
    }
}

/* find if two tags overlap
 * the "mult" parameter can be used do enlarge or shrink the area occupied by
 * a tag when calculating the overlapping and defaults to 1.0 (the actual
 * size of the tag element) */
springs.overlap = function(a, b, mult) {
    mult = (typeof(mult)=='undefined') ? 1.0 : mult;
    var ix = !(b.bottomleft()[0]/mult >= a.bottomright()[0]*mult ||
               b.bottomright()[0]*mult <= a.bottomleft()[0]/mult);
    var iy = !(b.bottomleft()[1]/mult >= a.topleft()[1]*mult ||
               b.topleft()[1]*mult <= a.bottomleft()[1]/mult);
    return ix && iy;
}

/* calculate the force of a spring of length "len" between two pivots */
springs.spring_force = function(n, o) {
    var f = [0, 0, 0];
    var len = springs.DISTMATRIX[n][o];     // spring length
    
    if (len > 0) {
        var a = springs.P[n];
        var b = springs.P[o];

        /* if the two pivots are on the same point, offset the first one
         * otherwise the spring calculation will fail */
        if (a.x==b.x && a.y==b.y) {
            a.x += (a.x >= springs.XMAX) ? -1 : 1;
            a.y += (a.y >= springs.YMAX) ? -1 : 1;
        }

        var v_ab = V3.sub([b.x, b.y, b.z], [a.x, a.y, a.z]);
        var l_ab = V3.length(v_ab);
        
        f = V3.scale(v_ab, springs.SCONST*((l_ab-len)/l_ab));
    }
    return f;
}

/* calculate the vertical repulsion force between two overlapping tags */
springs.vert_repulsion = function(n, o) {
    var f = [0, 0, 0];
    var a = springs.P[n];
    var b = springs.P[o];

    if (springs.overlap(a, b, 1.0)) {
        /* if the two pivots have same y, offset the first one
         * otherwise the spring calculation will fail */
        if (a.y == b.y) {
            a.y += (a.y == springs.YMAX) ? -1 : 1;
        }

        /* linear */
        var v_ab = V3.sub([0, b.y, 0], [0, a.y, 0]);
        var l_ab = V3.length(v_ab);

        f = V3.scale(v_ab, springs.RCONST*((l_ab-(a.height/2 + b.height/2))/l_ab));
    }
    return f;
}

/* solver object */
springs.solver = function(force_func, run_condition) {
    this.k = 0;
    this.iterations = 0;
    this.func = force_func;
    this.run_condition = run_condition;
    
    this.run = function() {
        this.k = 0;
        this.iterations++;
        var total_pivots = springs.P.length;

        for (n = 0; n < total_pivots; n += 1) {
            var p = springs.P[n];

            /* sum forces applied to the pivot */
            var f = [0, 0, 0];
            for (o = 0; o < total_pivots; o += 1) {
                if (o == n) continue;
                var po = springs.P[o];
                f = V3.add(f, this.func(n, o));
            }

            /* update pivot velocity: v = (v + (f * STEP)) * DAMPING */
            p.velocity = V3.scale(V3.add(p.velocity, V3.scale(f, springs.STEP)),
                                  springs.DAMPING);

            /* kinetic energy for this pivot: kn = (mass * |v|^2) */
            var kn = Math.pow(V3.length(p.velocity), 2);

            if (kn > springs.KMIN) {
                /* delta movement */
                var d = V3.scale(p.velocity, springs.STEP);

                /* the new position the pivot would reach at this iteration
                 * with its kinetic energy */
                p.x += d[0];
                p.y += d[1];

                /* now we have to clamp it if it goes outside the boundaries
                 * for now me just stop the pivot in the future we could make
                 * it bounce instead, but I'm not sure the effect would be
                 * pleasant */
                if (p.x < springs.XMIN || p.x > springs.XMAX) {
                    p.velocity = [0, 0, 0];
                    kn = 0;
                    p.x = Math.max(springs.XMIN, Math.min(springs.XMAX, p.x));
                }
                if (p.y < springs.YMIN || p.y > springs.YMAX) {
                    p.velocity = [0, 0, 0];
                    kn = 0;
                    p.y = Math.max(springs.YMIN, Math.min(springs.YMAX, p.y));
                }
                
                /* animate the tag to its new position for this iteration */
                $($(springs.SELECTOR)[n]).animate({left: p.bottomleft()[0],
                                           bottom: p.bottomleft()[1]},
                                           springs.ANISPEED, springs.ANIEASING);
            } else {
                p.velocity = [0, 0, 0];
                kn = 0;
            }
            
            /* add the pivot energy to the total system energy for this
             * iteration */
            this.k += kn;
        }
    }
}

/* create solvers for spring force and vertical repulsion */
springs.solver_springs = new springs.solver(springs.spring_force);
springs.solver_overlap = new springs.solver(springs.vert_repulsion);


/* API */

/* initialize an array of pivot for the given "tags" using "weights" to
 * determine the size of each tag */
springs.init_pivots = function(frame, tags, weights, distmatrix) {
    springs.XMIN = 0;
    springs.XMAX = frame.clientWidth;
    springs.YMIN = 0;
    springs.YMAX = frame.clientHeight;
    springs.DISTMATRIX = distmatrix;

    for (i=0; i<tags.length; i += 1) {
        /* create a pivot object */
        var p = new springs.Pivot();

        /* give a random initial position to the pivot */
        p.x = springs.rand(springs.XMAX, springs.XMIN);
        p.y = springs.rand(springs.YMAX, springs.YMIN);

        /* set the size of the tag based on its weight */
        var div = $(springs.SELECTOR)[i];
        $(div).css({'font-size': weights[i] + '%'});
        p.width = div.clientWidth;
        p.height = div.clientHeight;

        /* place the tag in its initial position */
        $(div).css({left: p.bottomleft()[0], bottom: p.bottomleft()[1]});

        /* add this pivot to the array */
        springs.P[i] = p;
    }
}

/* solve will execute an iteration of the current solver and then reschedule
 * itself until the sistem is solved or the maximum number of iteration is
 * reached */ 
springs.solve = function() {
    s_springs = springs.solver_springs;
    s_overlap = springs.solver_overlap;
    
    if (s_springs.iterations == 0 ||
          (s_springs.k > springs.KMIN && s_springs.iterations < springs.IMAX)) {
        s_springs.run();
        setTimeout(springs.solve, springs.ANISPEED+10);
        console.log('solver_springs:', s_springs.k, s_springs.iterations);
    } else
           if (s_overlap.iterations == 0 ||
          (s_overlap.k > springs.KMIN && s_overlap.iterations < springs.IMAX)) {
        s_overlap.run();
        setTimeout(springs.solve, springs.ANISPEED+10);
        console.log('solver_overlap:', s_overlap.k, s_overlap.iterations);
    } else {
        console.log('solved: springs iterations =', s_springs.iterations,
                                   'overlap iterations =', s_overlap.iterations)
    }
}

