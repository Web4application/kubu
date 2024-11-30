#include "CRAXExpr.h"
#include <iostream>

int main() {
// Example usage of BaseOffsetExpr
auto base = klee::ConstantExpr::create(0x400000, klee::Expr::Int64);
auto offset = klee::ConstantExpr::create(0x1000, klee::Expr::Int64);
auto expr = klee::BaseOffsetExpr::alloc(base, offset, "base", "offset");

std::cout << "Expression: " << expr->toString() << std::endl;
return 0;
}
