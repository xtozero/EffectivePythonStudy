#include <iostream>

#include <boost/python.hpp>

using namespace boost::python;

// 부스트는 파이썬 3에서 안됍니다....
int main( )
{
	//Py_SetProgramName( L"UserDefineFunctionWithBoost" );
	Py_Initialize( );

	PyRun_SimpleString(
		"import sys\n"
		"sys.path.append('.')\n"
	);

	object module = object( handle<>( PyImport_ImportModule( "Calc" ) ) );
	object func = object( handle<>( PyObject_GetAttrString( module.ptr(), "add" ) ) );
	object args = object( handle<>( PyTuple_New( 2 ) ) );

	// PyTuple_SetItem function steals a reference
	PyTuple_SetItem( args.ptr(), 0, PyLong_FromLong( 5 ) );
	PyTuple_SetItem( args.ptr(), 1, PyLong_FromLong( 10 ) );

	object returnValue = object( handle<>( PyObject_CallObject( func.ptr(), args.ptr() ) ) );
	std::cout << extract<long>( returnValue ) << std::endl;

	Py_Finalize( );

	return 0;
}