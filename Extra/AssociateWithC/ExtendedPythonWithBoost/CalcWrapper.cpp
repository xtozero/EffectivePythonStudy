#include <boost\python.hpp>

#include "Calc.h"

using namespace boost::python;

BOOST_PYTHON_MODULE( ExtendedPythonWithBoost )
{
	def( "Add", &Add );
	def( "Mul", &Mul );
	def( "Minus", &Minus );
	def( "Divide", &Divide );
}