#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <time.h>
#include <sys/time.h>
#include <float.h>
#include <math.h>
#include <string.h>
#include <omp.h>
#include "pso.h"

//  timer
//
double read_timer( )
{
    static bool initialized = false;
    static struct timeval start;
    struct timeval end;
    if( !initialized )
    {
        gettimeofday( &start, NULL );
        initialized = true;
    }
    gettimeofday( &end, NULL );
    return (end.tv_sec - start.tv_sec) + 1.0e-6 * (end.tv_usec - start.tv_usec);
}


// return default pso settings
void pso_set_default_settings(pso_settings_t *settings) {

    // set some default values
    printf("\n");
    printf("Ingrese cantidad de dimensiones: ");
    scanf("%d",&(settings->dim));
    settings->x_lo = -20;
    settings->x_hi = 20;
    settings->goal = 1e-5;
    printf("Ingrese cantidad de particulas: ");
    scanf("%d",&(settings->size));
    printf("Ingrese cantidad maxima de pasos: ");
    scanf("%d",&(settings->steps));
    printf("\n");
    settings->print_every = 1000;
    settings->c1 = 1.496;
    settings->c2 = 1.496;
    settings->w_max = PSO_INERTIA;
    settings->w_min = 0.3;

    settings->clamp_pos = 1;

}

float random_float(float min, float max)
{
    float random = ((float) rand()) / (float) RAND_MAX;
    float dif = max - min;
    float range = random * dif;
    return min + range;
}

void pso_solve(pso_obj_fun_t obj_fun, void *obj_fun_params,pso_result_t *solution, pso_settings_t *settings,FILE *guardado)
{
    double simulation_time = read_timer();

    int chunk;

    chunk=2;

    printf("Total particles number: %d\n", settings->size);

    // Particles
    double pos[settings->size][settings->dim]; // position matrix
    double vel[settings->size][settings->dim]; // velocity matrix
    double pos_b[settings->size][settings->dim]; // best position matrix
    double fit[settings->size]; // particle fitness vector
    double fit_b[settings->size]; // best fitness vector
    int part_id, dim_id,step,minfit;
    double a, b; // for matrix initialization
    double rho1, rho2; // random numbers (coefficients)
    double w; // current omega


    // INITIALIZE SOLUTION
    double gbfitness= DBL_MAX;

    for (part_id=0; part_id<settings->size; part_id++){
          // for each dimension
          for (dim_id=0; dim_id<settings->dim; dim_id++) {
              // generate two numbers within the specified range
              a = settings->x_lo + (settings->x_hi - settings->x_lo) * random_float(0,1); // Forma deterministica = settings->x_lo + (settings->x_hi - settings->x_lo) *((dim_id+part_id+1)*2)/(settings->size)
              b = settings->x_lo + (settings->x_hi - settings->x_lo) * random_float(0,1); // Forma deterministica = settings->x_lo + (settings->x_hi - settings->x_lo) *((dim_id+part_id+1)*2)/(settings->size)
              // initialize position
              pos[part_id][dim_id] = a;
              // best position is the same
              pos_b[part_id][dim_id] = a;
              // initialize velocity
              vel[part_id][dim_id] = (a-b) / 2.;
          }
          // update particle fitness
          fit[part_id] = obj_fun(pos[part_id], settings->dim, obj_fun_params);
          fit_b[part_id] = fit[part_id]; // this is also the personal best
          // update gbest??
          if (fit[part_id] < gbfitness) {
              // update best fitness
              gbfitness = fit[part_id];
              // copy particle pos to gbest vector
              memmove((void *)solution->gbest, (void *)&pos[part_id],sizeof(double) * settings->dim);
          }
   }

   // initialize omega using standard value
   w = PSO_INERTIA;


   // Algoritmo implementado con OpenOMP
   for (step=0; step<settings->steps; step++){

        #pragma omp parallel shared(minfit)
        {
          #pragma omp for schedule(static,chunk) private(rho1,rho2,part_id,dim_id)
          for(part_id=0;part_id<settings->size;part_id++)
          {
              for (dim_id=0; dim_id<settings->dim; dim_id++) {
                  // calculate stochastic coefficients
                  rho1 = settings->c1 * 0.5;
                  rho2 = settings->c2 * 0.5;
                  // update velocity
                  vel[part_id][dim_id] = w * vel[part_id][dim_id] + \
                  rho1 * (pos_b[part_id][dim_id] - pos[part_id][dim_id]) + \
                  rho2 * (solution->gbest[dim_id] - pos[part_id][dim_id]);
                   // update position
                  pos[part_id][dim_id] += vel[part_id][dim_id];
                  // clamp position within bounds?
                  if (settings->clamp_pos) {
                     if (pos[part_id][dim_id] < settings->x_lo) {
                         pos[part_id][dim_id] = settings->x_lo;
                         vel[part_id][dim_id] = 0;
                     } else if (pos[part_id][dim_id] > settings->x_hi) {
                                        pos[part_id][dim_id] = settings->x_hi;
                                        vel[part_id][dim_id] = 0;
                       }
                   }
               }

               fit[part_id] = obj_fun(pos[part_id], settings->dim, obj_fun_params);

               if (fit[part_id] < fit_b[part_id]) {
                  fit_b[part_id] = fit[part_id];
                  memmove((void *)&pos_b[part_id], (void *)&pos[part_id],sizeof(double) * settings->dim);
               }
         }

          #pragma omp for reduction(min:gbfitness)
          for(part_id=0;part_id<settings->size;part_id++)
          {
              if (fit_b[part_id] < gbfitness) {
                 gbfitness = fit_b[part_id];
              }
          }

          #pragma omp for
          for(part_id=0;part_id<settings->size;part_id++)
          {
              if(gbfitness==fit_b[part_id])
                 minfit=part_id;
          }

        }
        memmove((void *)solution->gbest, (void *)&pos_b[minfit],sizeof(double) * settings->dim);
  }

  printf("\n");
  printf("Mejor posicion: [");
  for (dim_id=0; dim_id<settings->dim; dim_id++) {
       printf(" %lf,", solution->gbest[dim_id]);
  }
  printf("]\n\n");
  printf("Fit Global de la mejor posicion= %lf\n",gbfitness);
  printf("\n");
  simulation_time = read_timer() - simulation_time;
  //copio en el archivo de texto el tiempo, particulas y dimensiones
  fprintf( guardado,"%d, %g\t                 %d, %g\n",settings->size,simulation_time,settings->dim,simulation_time);
  printf("Tiempo de ejecucion = %g segundos\n\n",simulation_time);
}


