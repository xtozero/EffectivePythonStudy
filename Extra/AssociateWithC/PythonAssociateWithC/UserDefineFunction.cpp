#include <iostream>

#include <Python.h>

int main( )
{
	Py_SetProgramName( L"UserDefineFunction" );
	Py_Initialize( );

	PyObject* pModule = nullptr;
	PyObject* pFunc = nullptr;
	PyObject* pArgs = nullptr;
	PyObject* pReturn = nullptr;

	PyRun_SimpleString(
		"import sys\n" 
		"sys.path.append('.')\n"
	);
	
	pModule = PyImport_ImportModule( "Calc" );
	assert( pModule );

	pFunc = PyObject_GetAttrString( pModule, "add" );
	assert( pFunc );

	pArgs = PyTuple_New( 2 );
	assert( pArgs );

	// PyTuple_SetItem function steals a reference
	PyTuple_SetItem( pArgs, 0, PyLong_FromLong( 5 ) );
	PyTuple_SetItem( pArgs, 1, PyLong_FromLong( 10 ) );

	pReturn = PyObject_CallObject( pFunc, pArgs );
	std::cout << PyLong_AsLong( pReturn ) << std::endl;
	
	// Release Objects
	Py_DECREF( pModule );
	Py_DECREF( pFunc );
	Py_DECREF( pArgs );
	Py_DECREF( pReturn );

	Py_Finalize( );

	return 0;
}