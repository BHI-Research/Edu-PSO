#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <float.h>
#include <math.h>
#include <sys/time.h>
#include "pso.h"
#include "objectives.h"

int find_option( int argc, char **argv, const char *option );
char *read_string( int argc, char **argv, const char *option, char *default_value );


int main(int argc, char **argv)
{

    //initialize random number generator
    srand(time(NULL));

    char *savename = read_string( argc, argv, "-o", NULL );

    FILE *guardado = savename ? fopen( savename, "a" ) : NULL;

    if(guardado==NULL)
    {
       printf("Error creating the file!!\n");
    }


    // define objective function
    pso_obj_fun_t obj_fun = pso_sphere;

    // initialize pso settings
    pso_settings_t settings;

    // set the default settings
    pso_set_default_settings(&settings);

    // initialize GBEST solution
    pso_result_t solution;
    // allocate memory for the best position buffer
    solution.gbest = (double *)malloc(settings.dim * sizeof(double));

    // run optimization algorithm
    
    pso_solve(obj_fun, NULL, &solution, &settings,guardado);
    

    // free the gbest buffer
    free(solution.gbest);

    if( guardado ) fclose( guardado );

    return 0;
}

char *read_string( int argc, char **argv, const char *option, char *default_value )
{
    int iplace = find_option( argc, argv, option );
    if( iplace >= 0 && iplace < argc-1 )
        return argv[iplace+1];
    return default_value;
}

int find_option( int argc, char **argv, const char *option )
{
    for( int i = 1; i < argc; i++ )
        if( strcmp( argv[i], option ) == 0 )
            return i;
    return -1;
}
