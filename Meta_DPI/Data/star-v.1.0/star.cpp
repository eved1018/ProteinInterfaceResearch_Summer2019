#include<stdio.h>
#include<string>
#include<gsl/gsl_randist.h>
#include<gsl/gsl_cdf.h>
#include<iostream>
#include <fstream>
#include <math.h>
#include<cmath>
#include "star.h"

using namespace std;

/*este programa es una version simplificada del test no parametrico reportado en:
 *"Comparing the Areas Under Two or More Correlated Receiver
 *   Operating Characteristic Curves: A Nonparametric Approach",
 *   ER DeLong, DM DeLong and DL Clarke-Pearson, Biometrics 44,
 *   p. 837-845. 

 *para comparar la diferencia entre dos o más AUC. En este caso sólose implementará pasa dos AUC y con un *contraste de L=(1,-1) de manera de construir el estadístico chi-cuadrado con rank(LSL') grados de *libertad, donde S es la estimación de la matriz de covarianza para el vector (AUC'1, AUC'2).

 *El programa recibe como input dos archivos "clase1.txt" y "clase2.txt", cada uno de los cuales es de la *siguiente forma:

 *Para clase1.txt
 *X11\tX12
 *X21\tX22
 *.
 *.
 *.
 *Xm1\tXm2
 *
 *Para clase2.txt
 *Y11\tY12
 *Y21\tY22
 *.
 *.
 *.
 *Yn1\tY22

 *El programa arroja como output el AUC de cada test (test1 y test2) y el p-value del estadístico chi-cuadrado con rank(LSL') grados de *libertad

 */

#ifndef _NO_NAMESPACE
using namespace std;
using namespace math;
#define STD std
#else
#define STD
#endif

#ifndef _NO_TEMPLATE
typedef matrix<double> Matrix;
#else
typedef matrix Matrix;
#endif

double **getMatrix(ifstream *data, char *sep, int rows, int cols)
{
	double **matrix= new double *[rows];
	for(int i=0;i<rows;i++)
		matrix[i]=new double[cols];
	int pos;
	int i=0; int j=0;

	char *separador;
	
	if(strcmp(sep,"2bl")==0)
		separador="  ";

	if(strcmp(sep,"tab")==0)
		separador="\t";

	string linea;
	string aux;
	double number;

	getline(*data,linea);

	while(!(*data).eof())
	{
		while((pos=linea.find(separador,0))!=string::npos)
		{

			aux=linea.substr(0,pos);
			linea=linea.substr(pos+1,linea.length());
			number=strtod(aux.c_str(),NULL);
			matrix[i][j]=number;
			j++;
			if(j==cols-1)
			{
				aux=linea.substr(0,linea.length());
				number=strtod(aux.c_str(),NULL);
				matrix[i][j]=(double)number;
				break;
			}
		}
		getline(*data,linea);
		i++;
		j=0;
	}
	return matrix;
}

int numberRows(char *nombre_archivo)
{
	ifstream in;
	in.open(nombre_archivo);
	string linea;
	int cont=0;
	getline(in,linea);
	
	while(!(in.eof()))
	{
		cont++;
		getline(in,linea);
	}
	in.close();
	return cont;
}
int numberColumns(char *nombre_archivo)
{
	ifstream in;
	in.open(nombre_archivo);
	string linea;
	getline(in,linea);
	int cont=0;
	int index;
	
	while((index=linea.find("\t",0))!=string::npos)
	{
		cont++;
		linea=linea.substr(index+1,linea.length());
	}

	in.close();
	return cont+1;
}

//returns a vector with the average for each column, except for the last one
double *getAverage(double **matrix, int n_rows, int n_cols)
{
	double *average;
	average=new double[n_cols];
	double avge;
	int i=0,j=0;
	double sum;

	while(j<n_cols)
	{
		sum=0;
		while(i<n_rows)
		{
			sum=sum + matrix[i][j];
			i++;
		}
		avge=sum/n_rows;
		average[j]=avge;
		j++; i=0;
	}
	return average;
}
double *computeMannWhitney(double **matrix_x, double **matrix_y, int n_rows_x, int n_rows_y, int *direccion)
{
	double *vector_estimates=new double[2]; //AUC'1 y AUC'2
	double constante=1.0/((double)n_rows_x*(double)n_rows_y); //1/m*n
	double sum_t1=0.0;
	double sum_t2=0.0;
	
	//para primer test
	for(int j=0;j<n_rows_y;j++)
	{
		for(int i=0;i<n_rows_x;i++)
		{
	//		if(direccion[0]==0) //Y<X
	//		{
				if(matrix_x[i][0]>matrix_y[j][0])
					sum_t1++;
				if(matrix_x[i][0]==matrix_y[j][0])
					sum_t1=sum_t1+0.5;
	//		}
	/*		else if(direccion[0]==1)
			{
				if(matrix_x[i][0]<matrix_y[j][0])
					sum_t1++;	
				if(matrix_x[i][0]==matrix_y[j][0])
					sum_t1=sum_t1+0.5;
			}	
	*/
		}
	}

/*
	if((sum_t1*constante)<0.5)
	{
		sum_t1=0.0;
		if(direccion[0]==0)
			direccion[0]=1;
		if(direccion[0]==1)
			direccion[0]=0;

		//para primer test
		for(int j=0;j<n_rows_y;j++)
		{
			for(int i=0;i<n_rows_x;i++)
			{
				if(direccion[0]==0) //Y<X
				{
					if(matrix_x[i][0]>matrix_y[j][0])
						sum_t1++;
					if(matrix_x[i][0]==matrix_y[j][0])
						sum_t1=sum_t1+0.5;
				}
				else if(direccion[0]==1)
				{
					if(matrix_x[i][0]<matrix_y[j][0])
						sum_t1++;	
					if(matrix_x[i][0]==matrix_y[j][0])
							sum_t1=sum_t1+0.5;
				}	
			}
		}
	}
*/
	//para segundo test
	for(int j=0;j<n_rows_y;j++)
	{
		for(int i=0;i<n_rows_x;i++)
		{
	//		if(direccion[1]==0) //Y<X
	//		{
				if(matrix_x[i][1]>matrix_y[j][1])
					sum_t2++;	
				if(matrix_x[i][1]==matrix_y[j][1])
					sum_t2=sum_t2+0.5;
	//		}
	/*		else if(direccion[1]==1)
			{
				if(matrix_x[i][1]<matrix_y[j][1])
					sum_t2++;	
				if(matrix_x[i][1]==matrix_y[j][1])
					sum_t2=sum_t2+0.5;
			}
	*/	
		}
	}
/*
	if(sum_t2*constante<0.5)
	{
		sum_t2=0.0;
		if(direccion[1]==0)
			direccion[1]=1;
		else if(direccion[1]==1)
			direccion[0]=0;
		//para segundo test
		for(int j=0;j<n_rows_y;j++)
		{
			for(int i=0;i<n_rows_x;i++)
			{
				if(direccion[1]==0) //Y<X
				{
					if(matrix_x[i][1]>matrix_y[j][1])
						sum_t2++;	
					if(matrix_x[i][1]==matrix_y[j][1])
						sum_t2=sum_t2+0.5;
				}
				else if(direccion[1]==1)
				{
					if(matrix_x[i][1]<matrix_y[j][1])
						sum_t2++;	
					if(matrix_x[i][1]==matrix_y[j][1])
						sum_t2=sum_t2+0.5;
				}	
			}
		}
	}
*/
	vector_estimates[0]=sum_t1*constante;
	vector_estimates[1]=sum_t2*constante;

	return vector_estimates;

}

void computeV10(double **V10, double **matrix_x, double **matrix_y, int n_rows_x, int n_rows_y, int *direccion)
{
	double sum_10=0;

	for(int k=0;k<2;k++)
	{
		for(int i=0;i<n_rows_x;i++)
		{
			for(int j=0;j<n_rows_y;j++)
			{
	//			if(direccion[k]==0)
	//			{
					if(matrix_x[i][k]>matrix_y[j][k])
						sum_10++;
					if(matrix_x[i][k]==matrix_y[j][k])
						sum_10=sum_10+0.5;
	//			}
	/*			else if(direccion[k]==1)
				{
					if(matrix_x[i][k]<matrix_y[j][k])
						sum_10++;
				}
	*/
			}
			V10[i][k]=sum_10/(double)n_rows_y;
			sum_10=0;
		}
	}

}

void computeV01(double **V01, double **matrix_x, double **matrix_y, int n_rows_x, int n_rows_y, int *direccion)
{
	double sum_01=0;

	for(int k=0;k<2;k++)
	{
		for(int j=0;j<n_rows_y;j++)
		{
			for(int i=0;i<n_rows_x;i++)
			{
		//		if(direccion[k]==0)
		//		{
					if(matrix_x[i][k]>matrix_y[j][k])
						sum_01++;
					if(matrix_x[i][k]==matrix_y[j][k])
						sum_01=sum_01+0.5;
		//		}
		/*		else if(direccion[k]==1)
				{
					if(matrix_x[i][k]<matrix_y[j][k])
						sum_01++;
				}
		*/
			}

			V01[j][k]=sum_01/(double)n_rows_x;
			sum_01=0;
		}
	}

}

//returns the transposed matrix of matrix
double **transpose(double **matrix, int n_rows, int n_cols)
{
	double **transposed_matrix;
	transposed_matrix=new double *[n_cols];

	for(int k=0; k< n_cols; k++)
		transposed_matrix[k]=new double[n_rows];

	for(int j=0; j< n_cols; j++)
	{
		for(int i=0;i<n_rows;i++)
			transposed_matrix[j][i]=matrix[i][j];
		
	}
	return transposed_matrix;
}

//calcula el producto de dos matrices
double **productMatrix(double **M1, double **M2, int n_rowsM1, int n_colsM1, int n_rowsM2, int n_colsM2)
{
	double **product=new double *[n_rowsM1];
	for(int i=0;i<n_colsM2;i++)
		product[i]=new double[n_colsM2];

	double sum=0.0;

	for(int m=0;m<n_rowsM1;m++)
	{
		for(int l=0;l<n_colsM2;l++)
		{
			for(int k=0;k<n_rowsM2;k++)
				sum=sum + M1[m][k]*M2[k][l];

			product[m][l]=sum;
			sum=0;
		}
	}
	return product;
}

void printMatrix(double **matrix, int nrows, int ncols, char *name_archivo)
{
	ofstream mat;
	mat.open(name_archivo);
	for(int i=0;i<nrows;i++)
	{
		for(int j=0;j<ncols;j++)
			mat << matrix[i][j] << "\t" ;	
		mat << endl;
	}
	mat.close();
}

void printMatrixResults(double **matrix, int nrows, int ncols, char *name_archivo, string names, double global_p)
{
	ofstream mat;
	mat.open(name_archivo);
	int index;
	string aux;

	mat << "Global test p-value: " ;

	if(global_p>=0 && global_p <=1)
	{
		mat << global_p << endl << endl;
	}

	else
	{
		mat << "Matrix LSL' is singular" << endl << endl;
	}


	mat << "\t"<< names << endl;
	for(int i=0;i<nrows;i++)
	{
		index=names.find("\t",0);
		aux=names.substr(0,index);
		mat << aux << "\t" ;
		names=names.substr(index+1,names.length());

		for(int j=0;j<ncols;j++)
		{
			if(i==j && j<ncols-1)
				mat << "N.A.\t";
			else if(i==j && j==ncols-1)
				mat << "N.A."<<endl;
			else
			{
				if(j<ncols-1)
					mat << matrix[i][j] << "\t" ;	
				else if(j==ncols-1)
					mat << matrix[i][j] << endl ;	
			}
		}
	}
	mat.close();
}

void printMatrixCov(double **matrix, int nrows, int ncols, char *name_archivo, string names)
{
	ofstream mat;
	mat.open(name_archivo);
	int index;
	string aux;

	mat << "\t"<< names << endl;
	for(int i=0;i<nrows;i++)
	{
		index=names.find("\t",0);
		aux=names.substr(0,index);
		mat << aux << "\t" ;
		names=names.substr(index+1,names.length());

		for(int j=0;j<ncols;j++)
		{
			if(j<ncols-1)
				mat << matrix[i][j] << "\t" ;	
			else if(j==ncols-1)
				mat << matrix[i][j] << endl ;	
		}
	}
	mat.close();
}

void printVectorAUC(double *vector,int largo, char *name_archivo, string names)
{
	ofstream mat;
	mat.open(name_archivo);
	mat << "TEST\tAUC" << endl;
	int index;
	string aux;
	
	for(int i=0;i<largo;i++)
	{
		index=names.find("\t",0);
		aux=names.substr(0,index);
		mat << aux << "\t" ;
		mat << vector[i] << endl;
		names=names.substr(index+1,names.length());
	}

	mat.close();

}

void printMatrixResultsSort(double **matrix, int nrows, int ncols, char *name_archivo, string names, double *AUC, int largo, double global_p)
{
	ofstream mat;
	mat.open(name_archivo);
	int index, indice;
	string aux;
	string sorted_names="";
	string aux_sorted;
	int *sorted_indexes_auc=new int[largo];
	double *AUC_aux=new double[largo];
	
	for(int i=0;i<largo;i++)
		AUC_aux[i]=AUC[i];
	
	int max=0;
	double max_v=0.0;

	for(int k=0;k<largo;k++)
	{
		for(int i=0;i<largo;i++)
		{
			if(max_v<AUC_aux[i])
			{
				max_v=AUC_aux[i];
				max=i;
			}
		}

		sorted_indexes_auc[k]=max;
		AUC_aux[max]=-1;
		max=0;
		max_v=0.0;
	}

	//en sorted_indexes_auc tenemos los indices de mayor a menor AUC
	//ahora hay que crear un "sorted_names"

	for(int i=0;i<largo;i++)
	{
		string save_names=names;

		for(int k=0;k<sorted_indexes_auc[i]+1;k++)
		{
			indice=save_names.find("\t",0);
			aux_sorted=save_names.substr(0,indice);
			save_names=save_names.substr(indice+1,save_names.length());

		}	
		sorted_names=sorted_names + aux_sorted;
		if(i==largo-1)
			sorted_names=sorted_names;
		else
			sorted_names=sorted_names + "\t";
	}
	//ahora hay que crear una matriz con los valores ordenados de acuerdo a sorted_indexes_auc

	double **sorted_matrix=new double *[ncols];

	for(int i=0;i<ncols;i++)
		sorted_matrix[i]=new double[ncols];

	for(int i=0;i<ncols;i++)
	{
		for(int j=i+1; j<ncols; j++)
		{
			if(sorted_indexes_auc[i]<=sorted_indexes_auc[j])
				sorted_matrix[i][j]=matrix[sorted_indexes_auc[i]][sorted_indexes_auc[j]];
			else if(sorted_indexes_auc[i]>sorted_indexes_auc[j])
				sorted_matrix[i][j]=matrix[sorted_indexes_auc[j]][sorted_indexes_auc[i]];

		}

	}

	for(int j=0;j<ncols;j++)
	{
		for(int i=j+1; i<ncols; i++)
		{
			if(sorted_indexes_auc[i]>sorted_indexes_auc[j])
				sorted_matrix[i][j]=matrix[sorted_indexes_auc[i]][sorted_indexes_auc[j]];
			else if(sorted_indexes_auc[i]<=sorted_indexes_auc[j])
				sorted_matrix[i][j]=matrix[sorted_indexes_auc[j]][sorted_indexes_auc[i]];
		}

	}

	mat << "Global test p-value: " ;

	if(global_p>=0 && global_p <=1)
	{
		mat << global_p << endl << endl;
	}

	else
	{
		mat << "Matrix LSL' is singular" << endl << endl;
	}

	mat << "\t"<< sorted_names << endl;
	for(int i=0;i<nrows;i++)
	{
		index=sorted_names.find("\t",0);
		aux=sorted_names.substr(0,index);
		mat << aux << "\t" ;
		sorted_names=sorted_names.substr(index+1,sorted_names.length());

		for(int j=0;j<ncols;j++)
		{
			if(i==j && j<ncols-1)
				mat << "N.A.\t";
			else if(i==j && j==ncols-1)
				mat << "N.A."<<endl;
			else
			{
				if(j<ncols-1)
					mat << sorted_matrix[i][j] << "\t" ;	
				else if(j==ncols-1)
					mat << sorted_matrix[i][j] << endl ;	
			}
		}
	}
	mat.close();
}

void printMatrixCovSort(double **matrix, int nrows, int ncols, char *name_archivo, string names, double *AUC, int largo)
{
	ofstream mat;
	mat.open(name_archivo);
	int index, indice;
	string aux;
	string sorted_names="";
	string aux_sorted;
	int *sorted_indexes_auc=new int[largo];
	double *AUC_aux=new double[largo];
	
	for(int i=0;i<largo;i++)
		AUC_aux[i]=AUC[i];
	
	int max=0;
	double max_v=0.0;

	for(int k=0;k<largo;k++)
	{
		for(int i=0;i<largo;i++)
		{
			if(max_v<AUC_aux[i])
			{
				max_v=AUC_aux[i];
				max=i;
			}
		}

		sorted_indexes_auc[k]=max;
		AUC_aux[max]=-1;
		max=0;
		max_v=0.0;
	}

	//en sorted_indexes_auc tenemos los indices de mayor a menor AUC
	//ahora hay que crear un "sorted_names"

	for(int i=0;i<largo;i++)
	{
		string save_names=names;

		for(int k=0;k<sorted_indexes_auc[i]+1;k++)
		{
			indice=save_names.find("\t",0);
			aux_sorted=save_names.substr(0,indice);
			save_names=save_names.substr(indice+1,save_names.length());

		}	
		sorted_names=sorted_names + aux_sorted;
		if(i==largo-1)
			sorted_names=sorted_names;
		else
			sorted_names=sorted_names + "\t";
	}
	//ahora hay que crear una matriz con los valores ordenados de acuerdo a sorted_indexes_auc

	double **sorted_matrix=new double *[ncols];

	for(int i=0;i<ncols;i++)
		sorted_matrix[i]=new double[ncols];

	for(int i=0;i<ncols;i++)
	{
		for(int j=i+1; j<ncols; j++)
		{
			if(sorted_indexes_auc[i]<=sorted_indexes_auc[j])
				sorted_matrix[i][j]=matrix[sorted_indexes_auc[i]][sorted_indexes_auc[j]];
			else if(sorted_indexes_auc[i]>sorted_indexes_auc[j])
				sorted_matrix[i][j]=matrix[sorted_indexes_auc[j]][sorted_indexes_auc[i]];

		}

	}

	for(int j=0;j<ncols;j++)
	{
		for(int i=0; i<ncols; i++)
				sorted_matrix[i][j]=matrix[sorted_indexes_auc[i]][sorted_indexes_auc[j]];
	}

	mat << "\t"<< sorted_names << endl;
	for(int i=0;i<nrows;i++)
	{
		index=sorted_names.find("\t",0);
		aux=sorted_names.substr(0,index);
		mat << aux << "\t" ;
		sorted_names=sorted_names.substr(index+1,sorted_names.length());

		for(int j=0;j<ncols;j++)
		{
			if(j<ncols-1)
				mat << sorted_matrix[i][j] << "\t" ;	
			else if(j==ncols-1)
				mat << sorted_matrix[i][j] << endl ;	
		}
	}
	mat.close();
}

string getHighestName(string names, double *AUCs, int largo)
{
	int index;
	int indice;
	string aux;
	double max=0.0;
	for(int i=0;i<largo; i++)
	{
		if(max<AUCs[i])
		{
			max=AUCs[i];
			index=i+1;
		}
	}

	for(int i=0;i<index;i++)
	{
		indice=names.find("\t",0);
		aux=names.substr(0,indice);
		names=names.substr(indice+1,names.length());
	}
	
	return aux;	
}

double getHighestValue(double *AUCs, int largo)
{
	int index;
	double max=0.0;
	for(int i=0;i<largo; i++)
	{
		if(max<AUCs[i])
		{
			max=AUCs[i];
			index=i;
		}
	}
	AUCs[index]=-1;
	return max;
	
}

void printVectorAUCSort(double *vector,int largo, char *name_archivo, string names)
{
	ofstream mat;
	mat.open(name_archivo);
	mat << "TEST\tAUC" << endl;
	int index;
	string aux;
	string n_highest;
	double v_highest;
	double *AUC_aux=new double[largo];
	
	for(int i=0;i<largo;i++)
		AUC_aux[i]=vector[i];
	
	for(int i=0;i<largo;i++)
	{
		n_highest=getHighestName(names, AUC_aux, largo);
		v_highest=getHighestValue(AUC_aux, largo);
		mat << n_highest << "\t" ;
		mat << v_highest << endl;
	}

	mat.close();
}



void printVector(double *vector,int largo)
{
	for(int i=0;i<largo;i++)
		cout << vector[i] << " ";

	cout << endl;

}

//returns the dot product of 2 vectors
double dotProduct(double *x, double *y, int number_elements)
{
	double sum=0;
	for(int i=0;i<number_elements;i++)
		sum=sum + x[i]*y[i];
	return sum;
}


void computeS10(double **S10, double *vector_estimates, double **V10, int n_rows_x)
{
	double **transpose_V10=transpose(V10,n_rows_x,2);
	double **mult_matrix=productMatrix(transpose_V10,V10, 2, n_rows_x, n_rows_x, 2);

	double **mult_vector=new double *[2];
	for(int i=0;i<2;i++)
		mult_vector[i]=new double[2];

	for(int i=0;i<2;i++)
	{
		for(int j=0;j<2;j++)
			mult_vector[i][j]=vector_estimates[i]*vector_estimates[j];
	}

	for(int i=0;i<2;i++)
	{
		for(int j=0;j<2;j++)
			S10[i][j]=(1.0/(double)(n_rows_x -1))*(mult_matrix[i][j] - n_rows_x*mult_vector[i][j]);

	}
}

void computeS01(double **S01, double *vector_estimates, double **V01, int n_rows_y)
{
	double **transpose_V01=transpose(V01,n_rows_y,2);
	double **mult_matrix=productMatrix(transpose_V01,V01, 2, n_rows_y, n_rows_y, 2);
	
	double **mult_vector=new double *[2];
	for(int i=0;i<2;i++)
		mult_vector[i]=new double[2];

	for(int i=0;i<2;i++)
	{
		for(int j=0;j<2;j++)
		mult_vector[i][j]=vector_estimates[i]*vector_estimates[j];
	}

	for(int i=0;i<2;i++)
	{
		for(int j=0;j<2;j++)
			S01[i][j]=(1.0/(double)(n_rows_y -1))*(mult_matrix[i][j] - n_rows_y*mult_vector[i][j]);

	}
}

void computeS(double **S, double **S10, double **S01,  int n_rows_x, int n_rows_y)
{
	for(int i=0;i<2;i++)
	{
		for(int j=0;j<2;j++)
			S[i][j]=(1.0/(double)n_rows_x)*S10[i][j] + (1.0/(double)n_rows_y)*S01[i][j];
	}
}

//funcion que calcula el producto de un vector de 1xN con una matriz de NxN, y luego eso por el vector transpuesto
double productVectMatVect(double *vector, double **matrix, int n)
{
	double sum;
	double *result=new double[n];
	double total=0.0;

	for(int j=0;j<n;j++)
	{
		sum=0.0;
		for(int i=0;i<n;i++)
		{
			sum=sum + vector[i]*matrix[i][j];
		}
		result[j]=sum;
	}
	for(int i=0;i<n;i++)
		total=total + result[i]*vector[i];

	return total;
	
}

//aplica el test no parametrico para comparar AUC's. Se pasa la memoria de AUC de manera de poder contar con los valores de las estimaciones de las AUC y así poder reportar la diferencia de ambas en el archivo final. Retorna el p-value obtenido con el test.

double *applyTest(double **matrix_x, double **matrix_y, int m, int n, double assigned_p_value)
{
	//determinamos si en general los Y < X o Y > X. Para eso calculamos el promedio de cada clase.
	double *average_x=getAverage(matrix_x,m,2);
	//cout << "PROMEDIOS"<< endl;
	//printVector(average_x,2);
	double *average_y=getAverage(matrix_y,n,2);
	//printVector(average_y,2);

	int *direccion=new int[2];

	for(int i=0;i<2;i++)
	{
		if(average_x[i]>average_y[i])
			direccion[i]=0; //Y<X
		else
			direccion[i]=1;//Y>X
	}

	//ahora calculamos el estimador de AUC para cada test
	double *AUC=computeMannWhitney(matrix_x, matrix_y, m, n, direccion);
	
	//ahora calculamos V_10 y V_01 para X e Y 
	double **V10=new double *[m];
	double **V01=new double *[n];
	
	for(int i=0;i<m;i++)
		V10[i]=new double[2];

	for(int i=0;i<n;i++)
		V01[i]=new double[2];

	computeV10(V10, matrix_x, matrix_y, m, n, direccion); //matriz de m x 2
	computeV01(V01, matrix_x, matrix_y, m, n, direccion); //matriz de n x 2

	double **S10=new double *[2];
	double **S01=new double *[2];
	double **S  =new double *[2];

	for(int i=0;i<2;i++)
	{
		S10[i]=new double[2];
		S01[i]=new double[2];
		  S[i]=new double[2];
	}	

	computeS10(S10, AUC, V10, m);
	computeS01(S01, AUC, V01, n);
	computeS(S, S10, S01,  m, n);

	double *contrast=new double[2];
	contrast[0]=1.0;
	contrast[1]=-1.0;

	double lt= productVectMatVect(contrast, S, 2);//LSL'
	double lt_1=1.0/lt; //(LSL')^{-1} para el test de hipotesis
	double lt_12=sqrt(lt);//(LSL')^{1/2} para el intervalo de confianza

	//calculamos el intervalo de confianza para la diferencia de las áreas
	double Ltheta_est=contrast[0]*AUC[0] + contrast[1]*AUC[1];

	double interval_factor=gsl_cdf_ugaussian_Qinv(assigned_p_value/2.0);

	double a= Ltheta_est - interval_factor*lt_12; 
	double b= Ltheta_est + interval_factor*lt_12;

	double chi=dotProduct(AUC, contrast, 2)*lt_1*dotProduct(contrast, AUC, 2);
	double df=1; //el rango de (LSL') pues es un numero

	double *results=new double[5];
	double p_value;
	if(isnan(chi))
	{
		if(Ltheta_est==0.0)
			p_value=1.0;
		else
			p_value=-1.0;
	}
	else
		p_value=gsl_cdf_chisq_Q(chi, df);


	results[0]=p_value;//p-valor
	results[1]=AUC[0];//AUC1
	results[2]=AUC[1];//AUC2
	results[3]=a;//MIN_IC
	results[4]=b;//MAX_IC

	return results;
}

string takeName(int index, string names)
{
	string aux;
	string names_aux=names;
	int ind;

	for(int i=0;i<index+1;i++)
	{
		ind=names_aux.find("\t",0);
		aux=names_aux.substr(0,ind);
		names_aux=names_aux.substr(ind+1,names_aux.length());
	}
	return aux;
}

void printVectorIntervals(double *diffAUC, double *Min_CI, double *Max_CI, int cols1, char *nombre_archivo,  string names)
{
	ofstream mat;
	mat.open(nombre_archivo);
	mat << "TEST1/TEST2\tAUC_DIFFERENCE\tCONFIDENCE_INTERVAL" << endl;
	string nombre1;
	string nombre2;
	int cont=0;
	
	for(int i=0;i<cols1;i++)
	{
		nombre1=takeName(i,names);

		for(int j=i+1;j<cols1;j++)
		{
			nombre2=takeName(j,names);
			mat << nombre1 << "/" << nombre2 << "\t" << diffAUC[cont] << "\t( "<< Min_CI[cont] << " , " << Max_CI[cont] << " )" << endl;

			cont++;
		}
	}
	mat.close();
}

double **getSubMatrix(double **matrix, int i, int j, int rows)
{
	double **submatrix=new double *[rows];
	for(int k=0;k<rows;k++)
		submatrix[k]=new double[2];

	for(int k=0;k<rows;k++)
	{		
		submatrix[k][0]=matrix[k][i];
		submatrix[k][1]=matrix[k][j];
	}
	return submatrix;
}



double computeGlobalTest(double **matrix_1, double **matrix_2, int cols, int rows1, int rows2, double **cov, double *MW_vector)
{
	double global_p;
	//first, get the covariance matrix and AUC vector
	for(int i=0;i<cols;i++)
	{
		for(int j=i+1;j<cols;j++)
		{
			
			double **matrix_x=getSubMatrix(matrix_1,i,j,rows1);
			double **matrix_y=getSubMatrix(matrix_2,i,j,rows2);

			//determinamos si en general los Y < X o Y > X. Para eso calculamos el promedio de cada clase.
			double *average_x=getAverage(matrix_x,rows1,2);
			double *average_y=getAverage(matrix_y,rows2,2);

			int *direccion=new int[2];

			for(int k=0;k<2;k++)
			{
				if(average_x[k]>average_y[k])
				direccion[k]=0; //Y<X
			else
				direccion[k]=1;//Y>X
			}

			double *AUC=computeMannWhitney(matrix_x, matrix_y, rows1, rows2, direccion);
			MW_vector[i]=AUC[0];
			MW_vector[j]=AUC[1];
			//ahora calculamos V_10 y V_01 para X e Y 
			double **V10=new double *[rows1];
			double **V01=new double *[rows2];
	
			for(int k=0;k<rows1;k++)
				V10[k]=new double[2];

			for(int k=0;k<rows2;k++)
				V01[k]=new double[2];
	
			computeV10(V10, matrix_x, matrix_y, rows1, rows2, direccion); //matriz de m x 2
			computeV01(V01, matrix_x, matrix_y, rows1, rows2, direccion); //matriz de n x 2

			double **S10=new double *[2];
			double **S01=new double *[2];
			double **S  =new double *[2];

			for(int k=0;k<2;k++)
			{
				S10[k]=new double[2];
				S01[k]=new double[2];
		 		S[k]=new double[2];
			}	

			computeS10(S10, AUC, V10, rows1);
			computeS01(S01, AUC, V01, rows2);
			computeS(S, S10, S01,  rows1, rows2);

			cov[i][i]=S[0][0];
			cov[j][j]=S[1][1];
			cov[i][j]=S[0][1];
			cov[j][i]=S[1][0];


			//free memory space

			for(int k=0; k<rows1;k++)
			{
				delete[] matrix_x[k];
				delete[] V10[k];
			}

			for(int k=0; k<rows2;k++)
			{
				delete[] matrix_y[k];
				delete[] V01[k];
			}

			for(int k=0;k<2;k++)
			{
				delete[] S01[k];
				delete[] S10[k];
				delete[] S[k];
			}

			delete []matrix_x;
			delete []matrix_y;
			delete []V10;
			delete []V01;
			delete []S10;
			delete []S01;
			delete []S;
			delete []AUC;
			delete []direccion;
		}
	}

	Matrix new_cov(cols,cols);
	Matrix MW(1,cols);
	Matrix MW_t(cols,1);

	

	for(int i=0;i<cols;i++)
	{
		MW(0,i)=MW_vector[i];
		MW_t(i,0)=MW_vector[i];	
		for(int j=0;j<cols;j++)
			new_cov(i,j)=cov[i][j];
	}

/*	cout << "Covariance Matrix\n";
	for(int i=0;i<cols;i++)
	{
		for(int j=0;j<cols;j++)
			cout << new_cov(i,j) << "\t";
		cout << endl;
	}
	cout << endl;

	for(int i=0;i<cols;i++)
		cout << MW(0,i) << "\t";
	cout << endl;

	for(int i=0;i<cols;i++)
		cout << MW_t(i,0) << "\t";
	cout << endl;
*/
	//second, we define the L matrix
	int rows_L=0;

	for(int i=cols-1;i>=1;i--)
	{
		rows_L+=i;
	}

	Matrix L(rows_L,cols);

	for(int i=0;i<rows_L;i++)
	{
		for(int j=0;j<cols;j++)
			L(i,j)=0;
	}




	int aux=cols;
	int sum=0;
	int i_aux,k;
	for(int j=0;j<cols;j++)
	{
		aux--;
		for(int i=0;i<aux;i++)
		{
			i_aux=i+sum;
			L(i_aux,j)=1;
			k=j+i+1;
			L(i_aux,k)=-1;
		}
		sum+=aux;	
	}

/*	cout << endl << "L Matrix: " << endl;

	for(int i=0;i<rows_L;i++)
	{
		for(int j=0;j<cols;j++)
			cout << L(i,j) << "\t";
		cout << endl;
	}
*/
	Matrix L_t(cols,rows_L);
	L_t=~L;

/*	cout << endl << "L transposed Matrix: " << endl;
	for(int i=0;i<cols;i++)
	{
		for(int j=0;j<rows_L;j++)
			cout << L_t(i,j) << "\t";
		cout << endl;
	}
*/
	Matrix left_to_invert(rows_L,cols);
	left_to_invert=L*new_cov;

/*	cout << endl << "left_side: " << endl;
	for(int i=0;i<rows_L;i++)
	{
		for(int j=0;j<cols;j++)
			cout << left_to_invert(i,j) << "\t";
		cout << endl;
	}
*/	
	Matrix to_invert(rows_L,rows_L);
	to_invert=left_to_invert*L_t;//LSL^t

/*	cout << endl << "to invert: " << endl;

	for(int i=0;i<rows_L;i++)
	{
		for(int j=0;j<rows_L;j++)
			cout << to_invert(i,j) << "\t";
		cout << endl;
	}
*/
	if(to_invert.IsSingular())
	{
		global_p=-1;
	}
	else
	{
		Matrix center_inverted(rows_L,rows_L);
		center_inverted=!to_invert;//(LSL^t)^-1
		int rank=rows_L;//a matrix is invertible iff has full rank

		Matrix left(1,rows_L);
		left=MW*L_t; //(1xcols) x (cols x rows_L) = (1 x rows_L)
		
		Matrix right(rows_L,1);//(rows_L x cols) x (cols x 1) = (rows_L x 1)
		right=L*MW_t;
		
		Matrix left_total(1,rows_L);
		left_total=left*center_inverted;
		Matrix total(1,1);

		
		total=left_total*right;
		double chi=total(0,0);

		//cout << "Chi (rank): " << chi << "(" << rank << ")" << endl << endl;
 
		global_p=gsl_cdf_chisq_Q(chi, rank);
	}

	return global_p;

}

int main(int argc, char *argv[])
{
	if(argc==1 || strcasecmp(argv[1],"--help")==0 || strcasecmp(argv[1],"-h")==0)
	{
		cout << "This program performs the non-parametric test for the difference of the Area Under the ROC Curves (AUC) for 2 classifiers, as reported in \"Comparing the Areas Under Two or More Correlated Receiver Operating Characteristic Curves: A Nonparametric Approach\", ER DeLong, DM DeLong and DL Clarke-Pearson, Biometrics 44,p. 837-845." << endl << endl;
		cout << "The mode of execution is: " << endl;
		cout << "./delong [--sort] class1.txt class2.txt alpha-value" << endl;
		return 0; 
	}
	//primero cuenta el numero de columnas por archivo y chequea que sean iguales
	int cols1, cols2, rows1, rows2;
	ifstream c1, c2;
	double assigned_p_value;

	if(strcasecmp(argv[1],"--sort")==0)
	{
		cols1=numberColumns(argv[2]);
		rows1=numberRows(argv[2])-1;//-1 pues hay que descartar la fila con los nombres
		cols2=numberColumns(argv[3]);	
		rows2=numberRows(argv[3])-1;//-1 pues hay que descartar la fila con los nombres
		c1.open(argv[2]);
		c2.open(argv[3]);
		assigned_p_value=atof(argv[4]);
	}
	else
	{
		cols1=numberColumns(argv[1]);
		rows1=numberRows(argv[1])-1;
		cols2=numberColumns(argv[2]);
		rows2=numberRows(argv[2])-1;
		c1.open(argv[1]);
		c2.open(argv[2]);
		assigned_p_value=atof(argv[3]);
	}

	if( assigned_p_value <= 0 || assigned_p_value >= 1)
	{
		cerr << "Alpha-value has to be any number greater than 0 and less than 1" << endl;
		return 0;
	}

	if(cols1!=cols2)
	{
		cerr << "The files should have the same number of classifiers/tests.\n";
		return 0;
	}

	if(!(c1.is_open()) || !(c2.is_open()))
	{
		cerr << "The files passed as input do not exist. Please check for existance of files and try again.\n";
		return 0;
	}

	string linea1, linea2;
	getline(c1,linea1); 
	getline(c2,linea2); 

	string names1=linea1; //nombres clasificadores archivo1
	string names2=linea2; //nombres clasificadores archivo2
	

	if(names1.compare(names2)!=0)
	{
		cerr << "Please check that the names of the test/classifiers in each file is exactly the same, and in the same order." << endl;
		c1.close();
		c2.close();
		return 0;
	}

	double **main_matrix_data1=getMatrix(&c1, "tab", rows1, cols1);
	double **main_matrix_data2=getMatrix(&c2, "tab", rows2, cols2);

	double **cov=new double *[cols1];
	for(int i=0;i<cols1;i++)
		cov[i]=new double[cols1];

	double *MW_vector=new double[cols1];	

	double global_p=computeGlobalTest(main_matrix_data1,main_matrix_data2,cols1,rows1,rows2, cov, MW_vector);
	//cout << "Global Test: " << global_p << endl;

	double *result;
	double **matrix=new double *[cols1];

	for(int i=0;i<cols1;i++)
		matrix[i]=new double[cols1];

	double *AUC=new double[cols1];
	double *diffAUC=new double[cols1*(cols1-1)/2];
	double *Min_CI=new double[cols1*(cols1-1)/2];
	double *Max_CI=new double[cols1*(cols1-1)/2];
	int contador_int=0;
	
	for(int i=0;i<cols1;i++)
	{
		for(int j=i+1;j<cols1;j++)
		{
			double **matrix_x=getSubMatrix(main_matrix_data1,i,j,rows1);
			double **matrix_y=getSubMatrix(main_matrix_data2,i,j,rows2);

			result=applyTest(matrix_x,matrix_y,rows1,rows2, assigned_p_value);
			matrix[i][j]=fabs(result[1]-result[2]);
			diffAUC[contador_int]=result[1]-result[2];
			AUC[i]=result[1];
			AUC[j]=result[2];
			matrix[j][i]=result[0];
			Min_CI[contador_int]=result[3];
			Max_CI[contador_int]=result[4];
			contador_int++;

			for(int k=0; k<rows1;k++)
				delete[] matrix_x[k];

			for(int k=0; k<rows2;k++)
				delete[] matrix_y[k];

			delete []matrix_x;
			delete []matrix_y;
			
		}
	}

	for(int i=0;i<cols1;i++)
		matrix[i][i]=-1;

	if(strcasecmp(argv[1],"--sort")==0)
	{
		printVectorIntervals(diffAUC, Min_CI, Max_CI, cols1, "conf_intervals.txt",names1);
		printMatrixResultsSort(matrix,cols1,cols2,"results_sorted.txt", names1, AUC, cols1, global_p);
		printVectorAUCSort(AUC, cols1,"auc_sorted.txt", names1);
		printMatrixCovSort(cov,cols1,cols2,"cov_matrix_sorted.txt",names1, AUC, cols1);

	}

	else
	{
		printMatrixResults(matrix,cols1,cols2,"results.txt", names1, global_p);
		printVectorIntervals(diffAUC, Min_CI, Max_CI, cols1, "conf_intervals.txt",names1);
		printVectorAUC(AUC, cols1,"auc.txt", names1);
		printMatrixCov(cov,cols1,cols2,"cov_matrix.txt",names1);
	}

	for(int i=0;i<cols1;i++)
		delete[] cov[i];
	
	delete []cov;

	return 0;
}
