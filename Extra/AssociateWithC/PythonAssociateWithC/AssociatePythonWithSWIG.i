// SWIG interface
%module AssociatePythonWithSWIG
%{
	extern int Add( int a, int b );
%}

int Add( int a, int b );