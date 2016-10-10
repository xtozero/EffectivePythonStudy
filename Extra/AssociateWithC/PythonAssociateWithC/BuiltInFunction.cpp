#include <Python.h>

int main( )
{
	Py_SetProgramName( L"Test Name" );
	Py_Initialize( );
	PyRun_SimpleString( "print(\'Hello World\')" );
	PyRun_SimpleString( "a = [1, 2, 3, 4, 5]" );
	PyRun_SimpleString( "print(a)" );
	Py_Finalize( );
}