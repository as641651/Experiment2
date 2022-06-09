#include <generator/generator.hpp>

template<typename Gen>
decltype(auto) operand_generator(Gen && gen)
{
    auto A = gen.generate({100,100}, generator::property::random{});
    auto B = gen.generate({100,100}, generator::property::random{});
    auto C = gen.generate({100,100}, generator::property::random{});
    auto D = gen.generate({100,100}, generator::property::random{});
    return std::make_tuple(A, B, C, D);
}