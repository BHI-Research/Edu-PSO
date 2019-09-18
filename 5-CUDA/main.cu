#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <float.h>
#include <math.h>
#include "pso.h"
#include "objectives.h"
#include <string.h>
#include <sys/time.h>


FILE *fp;


double read_timer( )                //LECTURA DE TIEMPOS
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

int find_option( int argc, char **argv, const char *option )        //PROCESAMIENTO DE OPCIONES DE LINEA DE COMANDOS
{
    for( int i = 1; i < argc; i++ )
        if( strcmp( argv[i], option ) == 0 )
            return i;
    return -1;
}

int read_int( int argc, char **argv, const char *option, int default_value )        //LECTURA DE ARGUMENTOS DE PROGRAMA
{
    int iplace = find_option( argc, argv, option );
    if( iplace >= 0 && iplace < argc-1 )
        return atoi( argv[iplace+1] );
    return default_value;
}
double read_double( int argc, char **argv, const char *option, double default_value )
{
    int iplace = find_option( argc, argv, option );
    if( iplace >= 0 && iplace < argc-1 )
        return strtod( argv[iplace+1],NULL );
    return default_value;
}
char *read_string( int argc, char **argv, const char *option, char *default_value )
{
    int iplace = find_option( argc, argv, option );
    if( iplace >= 0 && iplace < argc-1 )
        return argv[iplace+1];
    return default_value;
}




int main( int argc, char **argv )
{

    double simulation_time = read_timer( );             //SE LEE TIEMPO DE INICIO

    if( find_option( argc, argv, "-h" ) >= 0 )          //ARGUMENTOS DEL PROGRAMA
    {
        printf( "Options:\n" );
        printf( "-h to see this help\n" );
        printf( "-p <int> to set the number of particles\n" );
        printf( "-d <int> to set the number of dimensions\n" );
        printf( "-g <double> to set the optimization goal (error threshold)\n" );
        printf( "-L <double> to set the lower limit range \n" );
        printf( "-H <double> to set the higher limit range \n" );
        printf( "-o <filename> to specify the output file name (particles position every 100 steps)\n" );
        return 0;
    }
    int part = read_int( argc, argv, "-p", 20 );
    int dim = read_int( argc, argv, "-d", 30 );
    double goal = read_double( argc, argv, "-g", 1e-5 );
    double limlo = read_double( argc, argv, "-L", -20 );
    double limhi = read_double( argc, argv, "-H", 20 );
    char *savename = read_string( argc, argv, "-o", "Default.txt" );

    FILE *fsave = savename ? fopen( savename, "a" ) : NULL;


    // Definicion de la funcion objetivo
    pso_obj_fun_t obj_fun = pso_sphere;

    // Inicializacion de los ajustes del PSO
    pso_settings_t settings;
    settings.dim=dim;
    settings.size=part;
    settings.goal=goal;
    settings.x_lo=limlo;
    settings.x_hi=limhi;

    // Seteo de los ajustes por default del PSO
    pso_set_default_settings(&settings);

    // Inicializacion de GBEST
    pso_result_t solution;
    
    // Memoria para el buffer de mejor posicion
    solution.gbest = (double *)malloc(settings.dim * sizeof(double));

    // Algoritmo de optimizacion
    pso_solve(obj_fun, NULL, &solution, &settings, fsave);

    // Libero el buffer GBEST
    free(solution.gbest);

    simulation_time = read_timer( ) - simulation_time;          //SE LEE TIEMPO DE FINALIZACION Y SE OBTIENE TIEMPO DE EJECUCION

    fclose( fsave );
    printf( "Dimensiones = %i\nParticulas = %i\nTiempo de simulacion = %g segundos\n", settings.dim, settings.size, simulation_time);
    fp = fopen ( "TIEMPOS.txt", "a" );
    fprintf( fp, "%i   %i   %f    %g\n", settings.dim, settings.size, settings.goal, simulation_time );    //  IMPRIME ARCHIVO DE TIEMPOS
    fclose ( fp );

    return 0;
}
