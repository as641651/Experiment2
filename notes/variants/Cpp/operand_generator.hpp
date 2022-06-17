#include <generator/generator.hpp>

template<typename Gen>
decltype(auto) operand_generator(Gen && gen)
{
    auto M1 = gen.generate({1100,1800}, generator::property::random{}, generator::shape::not_square{});
    auto M2 = gen.generate({1100,1800}, generator::property::random{}, generator::shape::not_square{});
    auto M3 = gen.generate({1100,1150}, generator::property::random{}, generator::shape::not_square{});
    auto M4 = gen.generate({1100,1100}, generator::shape::upper_triangular{}, generator::property::random{});
    auto M5 = gen.generate({1100,1100}, generator::shape::upper_triangular{}, generator::property::random{});
    return std::make_tuple(M1, M2, M3, M4, M5);
}