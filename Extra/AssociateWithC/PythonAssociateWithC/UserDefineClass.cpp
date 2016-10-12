#include <iostream>

#include <Python.h>

int main( )
{
	Py_SetProgramName( L"UserDefineClass" );

	Py_Initialize( );

	PyObject* pModule = nullptr;
	PyObject* pClass = nullptr;
	PyObject* pList = nullptr;
	PyObject* pArgs = nullptr;
	PyObject* pInstance = nullptr;
	PyObject* pReturnObject = nullptr;

	PyRun_SimpleString(
		"import sys\n"
		"sys.path.append('.')\n"
	);

	pModule = PyImport_ImportModule( "Frequency" );
	assert( pModule );

	pClass = PyObject_GetAttrString( pModule, "FrequencyList" );
	assert( pClass );

	pList = PyList_New( 10 );
	assert( pList );

	for ( int i = 0; i < 10; ++i )
	{
		int number = rand( ) % 5;
		std::cout << number << std::endl;
		PyList_SetItem( pList, i, PyLong_FromLong( number ) );
	}

	std::cout << "-----------------------" << std::endl;

	pArgs = PyTuple_New( 1 );
	assert( pArgs );

	PyTuple_SetItem( pArgs, 0, pList );

	pInstance = PyObject_CallObject( pClass, pArgs );
	assert( pInstance );

	pReturnObject = PyObject_CallMethod( pInstance, "frequency", NULL );

	PyObject* pKeys = PyDict_Keys( pReturnObject );
	int listSize = PyList_Size( pKeys );

	for ( int i = 0; i < listSize; ++i )
	{
		PyObject *keyItem = PyList_GetItem( pKeys, i );
		assert( keyItem );
		PyObject *entryItem = PyDict_GetItem( pReturnObject, keyItem );
		assert( entryItem );

		std::cout << PyLong_AsLong( keyItem ) << " : " <<
			PyLong_AsLong( entryItem ) << std::endl;
	}
	Py_DECREF( pKeys );
	Py_DECREF( pModule );
	Py_DECREF( pClass );
	Py_DECREF( pArgs );
//	Py_DECREF( pList );
	Py_DECREF( pInstance );
	Py_DECREF( pReturnObject );

	Py_Finalize( );

	return 0;
}