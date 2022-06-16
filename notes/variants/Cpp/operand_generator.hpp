#include <generator/generator.hpp>

template<typename Gen>
decltype(auto) operand_generator(Gen && gen)
{
    auto X = gen.generate({100,20}, generator::property::random{}, generator::shape::not_square{});
    auto M = gen.generate({100,100}, generator::shape::self_adjoint{}, generator::property::spd{});
    auto y = gen.generate({100,1}, generator::property::random{}, generator::shape::col_vector{}, generator::shape::not_square{});
    return std::make_tuple(X, M, y);
}