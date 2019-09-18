#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <float.h>
#include <math.h>
#include <string.h>

#include "pso.h"





// For the CUDA runtime routines (prefixed with "cuda_")
#include <cuda_runtime.h>
#include <cuda.h>


/**
 * CUDA Kernel Device code
 **/
__global__ void
calc(double *vel,double *pos,double *pos_b/*,double *pos_nb*/,
     double c1, double c2,double w,int step, int numElements,
     double x_hi, double x_lo)
{
    int i = blockDim.x * blockIdx.x + threadIdx.x;
    int j = blockDim.y * blockIdx.y + threadIdx.y;


    int indice = j * numElements + i;

    if (i < numElements && j< numElements)
    {
        // calculate stochastic coefficients
        double rho1 = c1  *(0.5+/*(float)(i/1e5)+*/(double)(step/1e10));//random_float(0,1); //SE ANULA PORQUE NO PERMITE PARALIZACION
        double rho2 = c2  *(0.5+/*(float)(i/1e5)+*/(double)(step/1e10));//random_float(0,1); //SE ANULA PORQUE NO PERMITE PARALIZACION
        vel[indice] =w*vel[indice]+rho1*(pos_b[indice]-pos[indice])+rho2*(/*pos_nb[indice]*/-pos[indice]);
        pos[indice] = pos[indice] + vel[indice];
        
        if (pos[indice] < x_lo)
        {
            pos[indice] = x_lo;
            vel[indice] = 0;
        } 
        else if (pos[indice] > x_hi)
        {
            pos[indice] = x_hi;
            vel[indice] = 0;
        }
    }
}

/// Functions Propotypes
//Free GPU Memory
bool free_memGPU (double *arr1, double *arr2, double *arr3);
//Check CUDA Errors
bool check (cudaError_t error );




// calulate swarm size based on dimensionality
int pso_calc_swarm_size(int dim) {                          //NO SE UTILIZA PORQUE SE INGRESA POR CONSOLA Nro DE PARTICULAS
    int size = 10. + 2. * sqrt(dim);
    return (size > PSO_MAX_SIZE ? PSO_MAX_SIZE : size);
}

// return default pso settings
void pso_set_default_settings(pso_settings_t *settings) {

    // set some default values
    //settings->dim = 2026;         //PARAMETRO INGRESADO EN EL SCRIP (MODIFICA NUMERO DE DIMENCIONES)
    //settings->x_lo = -20;         //PARAMETRO INGRESADO EN EL SCRIP (MODIFICA EL LIMITE INFERIOR DEL RANGO)
    //settings->x_hi = 20;          //PARAMETRO INGRESADO EN EL SCRIP (MODIFICA EL LIMITE SUPERIOR DEL RANGO)
    //settings->goal = 1e-5;        //PARAMETRO INGRESADO EN EL SCRIP (MODIFICA EL UMBRAL DE ERROR)

    //settings->size = pso_calc_swarm_size(settings->dim);  //PARAMETRO INGRESADO EN EL SCRIP (MODIFICA NUMERO DE PARTICULAS)
    settings->print_every = 1000;
    settings->steps = 100000;
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

void pso_solve(pso_obj_fun_t obj_fun, void *obj_fun_params, pso_result_t *solution, pso_settings_t *settings, FILE *file)
{
    //printf("Total particles number: %d\n", settings->size);   //SE ANULA PORQUE AHORA SE IMPRIME AL FINAL

    // Particles
    double pos[settings->size][settings->dim]; // matriz posicion
    double vel[settings->size][settings->dim]; // matriz velocidad
    double pos_b[settings->size][settings->dim]; // matriz mejor  posicion
    double fit[settings->size]; // vector fitness de la particula
    double fit_b[settings->size]; // vector mejor fitness de la particula

    // Swarm
    double pos_nb[settings->size][settings->dim]; // what is the best informed

    // position for each particle
    int comm[settings->size][settings->size]; // communications:who informs who
    int improved; // whether solution->error was improved duringthe last iteration

    int part_id, dim_id, step;
    double a, b; // for matrix initialization
    double rho1, rho2; // random numbers (coefficients)
    double w; // current omega
    void (*inform_fun)(); // neighborhood update function
    double (*calc_inertia_fun)(); // inertia weight update function


    // INITIALIZE SOLUTION
    solution->error = DBL_MAX;

    // SWARM INITIALIZATION
    // for each particle
    for (part_id=0; part_id<settings->size; part_id++)
    {
        // for each dimension
        for (dim_id=0; dim_id<settings->dim; dim_id++)
        {
            // generate two numbers within the specified range
            a = settings->x_lo + (settings->x_hi - settings->x_lo) * (0.5+(double)(part_id/1e5)+(double)(dim_id/1e8));//random_float(0,1); //SE ANULA PORQUE NO PERMITE PARALIZACION
            b = settings->x_lo + (settings->x_hi - settings->x_lo) * (0.5+(double)(part_id/1e5)+(double)(dim_id/1e8));//random_float(0,1); //SE ANULA PORQUE NO PERMITE PARALIZACION
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
        if (fit[part_id] < solution->error)
        {
            // update best fitness
            solution->error = fit[part_id];
            // copy particle pos to gbest vector
            memmove((void *)solution->gbest, (void *)&pos[part_id],sizeof(double) * settings->dim);
        }
    }

    // Error code to check return values for CUDA calls
    cudaError_t err = cudaSuccess;
    int numElements = settings->size;
    size_t size = settings->size * settings->dim * sizeof(double);

    //Vectors on GPU Memory
    double *d_vel = NULL;
    double *d_pos = NULL;
    double *d_pos_b = NULL;
    //double *d_pos_nb = NULL;

    cudaMalloc((void **)&d_vel, size);
    cudaMalloc((void **)&d_pos, size);
    cudaMalloc((void **)&d_pos_b, size);
    //cudaMalloc((void **)&d_pos_nb, size);

    cudaMemcpy(d_vel, vel, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_pos, pos, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_pos_b, pos_b, size, cudaMemcpyHostToDevice);
    //cudaMemcpy(d_pos_nb, pos_nb, size, cudaMemcpyHostToDevice);

    // Launch the Vector Add CUDA Kernel
    dim3 threadsPerBlock(16,16);
    int block=(int) ceil((float)numElements / 16.0);
    dim3 blocksPerGrid(block,block);

    // initialize omega using standard value
    w = PSO_INERTIA;
    // RUN ALGORITHM
    for (step=0; step<settings->steps; step++)
    {

        //cudaMemcpy(d_pos, pos, size, cudaMemcpyHostToDevice);
        cudaMemcpy(d_pos_b, pos_b, size, cudaMemcpyHostToDevice);
        // update current step
        settings->step = step;

        // check optimization goal
        if (solution->error <= settings->goal)
        {
            // SOLVED!!
            if (settings->print_every)
                printf("Goal achieved @ step %d (error=%.3e) :-)\n", step, solution->error);
            printf("Best known position: [");
            for (part_id=0; part_id<settings->dim; part_id++) {
                printf("%6.2lf", solution->gbest[part_id]);
            }
            printf("]\n");
            break;
        }

        // the value of improved was just used; reset it
        improved = 0;



        // Operation with the GPU
        calc<<<blocksPerGrid, threadsPerBlock>>>(d_vel, d_pos, d_pos_b/*,d_pos_nb*/,settings->c1,settings->c2,w,step, numElements, settings->x_hi, settings->x_lo);

        //cudaMemcpy(vel, d_vel, size, cudaMemcpyDeviceToHost);
        cudaMemcpy(pos, d_pos, size, cudaMemcpyDeviceToHost);
        cudaMemcpy(pos_b, d_pos_b, size, cudaMemcpyDeviceToHost);
        //cudaMemcpy(pos_nb, d_pos_nb, size, cudaMemcpyDeviceToHost);





        // update all particles
        for (part_id=0; part_id<settings->size; part_id++)
        {
            // update particle fitness
            fit[part_id] = obj_fun(pos[part_id], settings->dim, obj_fun_params);
            // update personal best position?
            if (fit[part_id] < fit_b[part_id])
            {
                fit_b[part_id] = fit[part_id];
                // copy contents of pos[i] to pos_b[i]
                memmove((void *)&pos_b[part_id], (void *)&pos[part_id],sizeof(double) * settings->dim);
            }
            // update gbest??
            if (fit[part_id] < solution->error)
            {
                improved = 1;
                // update best fitness
                solution->error = fit[part_id];
                // copy particle pos to gbest vector
                memmove((void *)solution->gbest, (void *)&pos[part_id],sizeof(double) * settings->dim);
            }
        }


        if (settings->print_every && (step % settings->print_every == 0))
            printf("Step %d (w=%.2f) :: min err=%.5e\n", step, w, solution->error);

        if(step % (settings->print_every/10) == 0) //IMPRIME POSICIONES DE PARTICULAS EN UN ARCHIVO CADA 100 STEPS
        {
            for (int part_id2=0; part_id2<settings->size; part_id2++)
            {
                for (int dim_id2=0; dim_id2<settings->dim; dim_id2++)
                {
                    fprintf( file, "%f ", pos[part_id2][dim_id2]);
                }
                fprintf( file, "\n");
            }
        }

    }
            free_memGPU(d_vel,d_pos,d_pos_b/*,d_pos_nb*/);

}



bool free_memGPU (double *arr1,double *arr2,double *arr3/*,double *arr4*/){

    // Free device global memory
    cudaError_t err;
    err = cudaFree(arr1);

    if (err != cudaSuccess)
    {
        fprintf(stderr, "Failed to free device vector A (error code %s)!\n", cudaGetErrorString(err));
        return 0;
    }

    err = cudaFree(arr2);

    if (err != cudaSuccess)
    {
        fprintf(stderr, "Failed to free device vector B (error code %s)!\n", cudaGetErrorString(err));
        return 0;
    }

    err = cudaFree(arr3);

    if (err != cudaSuccess)
    {
        fprintf(stderr, "Failed to free device vector C (error code %s)!\n", cudaGetErrorString(err));
        return 0;
    }

    /*err = cudaFree(arr4);

    if (err != cudaSuccess)
    {
        fprintf(stderr, "Failed to free device vector D (error code %s)!\n", cudaGetErrorString(err));
        return 0;
    }*/
    //printf("Resources free from CUDA Device\n");
    return 1;

}

bool check (cudaError_t error ){
    if (error != cudaSuccess) return 0;
    //printf ("Error checkeado\n");
    return 1;
}
