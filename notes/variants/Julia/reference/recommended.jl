using LinearAlgebra.BLAS
using LinearAlgebra

function recommended(M1::Array{Float64,2}, M2::Array{Float64,2}, M3::Array{Float64,2}, M4::UpperTriangular{Float64,Array{Float64,2}}, M5::UpperTriangular{Float64,Array{Float64,2}})
    start::Float64 = 0.0
    finish::Float64 = 0.0
    Benchmarker.cachescrub()
    start = time_ns()

    Y = (M1*transpose(M2)+M3*transpose(M3)+transpose(M4)+transpose(M5));

    finish = time_ns()
    return (tuple(Y), (finish-start)*1e-9)
end