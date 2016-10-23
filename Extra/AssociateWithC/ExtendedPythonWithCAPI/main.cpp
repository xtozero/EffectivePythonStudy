#include <Python.h>

extern "C" PyObject* add( PyObject* self, PyObject* args )
{
	printf( "Function execute\n" );
	int lhs, rhs;
	if ( !PyArg_ParseTuple( args, "ii", &lhs, &rhs ) )
		return nullptr;

	int result = lhs + rhs;

	return Py_BuildValue( "i", result );
}

static PyMethodDef Methods[] = 
{
	{"add", add, METH_VARARGS, "add integer"},
	{nullptr, nullptr, 0, nullptr}
};

static struct PyModuleDef Module =
{
	PyModuleDef_HEAD_INIT,
	"Module",
	"Simple Add",
	-1, Methods
};

PyMODINIT_FUNC PyInit_Module( void )
{
	return PyModule_Create( &Module );
}