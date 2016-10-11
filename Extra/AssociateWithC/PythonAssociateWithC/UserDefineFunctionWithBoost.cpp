#include <iostream>

#include <boost/python.hpp>

using namespace boost::python;

int main( )
{
	Py_SetProgramName( L"UserDefineFunction" );
	Py_Initialize( );

	object module;
	object func;
	object args;
	object returnValue;

	PyRun_SimpleString(
		"import sys\n"
		"sys.path.append('.')\n"
	);

	module = object( handle<>( PyImport_ImportModule( "Calc" ) ) );
	func = object( handle<>( PyObject_GetAttrString( module.ptr(), "add" ) ) );
	args = object( handle<>( PyTuple_New( 2 ) ) );

	// PyTuple_SetItem function steals a reference
	PyTuple_SetItem( args.ptr(), 0, PyLong_FromLong( 5 ) );
	PyTuple_SetItem( args.ptr(), 1, PyLong_FromLong( 10 ) );

	returnValue = object( handle<>( PyObject_CallObject( func.ptr(), args.ptr() ) ) );
	std::cout << extract<int>( returnValue ) << std::endl;

	Py_Finalize( );

	return 0;
}