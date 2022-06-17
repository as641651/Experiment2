struct naive_eigen
{
template<typename Type_M1, typename Type_M2, typename Type_M3, typename Type_M4, typename Type_M5>
decltype(auto) operator()(Type_M1 && M1, Type_M2 && M2, Type_M3 && M3, Type_M4 && M4, Type_M5 && M5)
{
    auto Y = ((M1*(M2).transpose()+M3*(M3).transpose()+(M4).transpose()+(M5).transpose())).eval();

    typedef std::remove_reference_t<decltype(Y)> return_t;
    return return_t(Y);                         
}
};