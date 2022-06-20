using LinearAlgebra.BLAS
using LinearAlgebra

function algorithm79(ml0::Array{Float64,2}, ml1::Array{Float64,2}, ml2::Array{Float64,2}, ml3::Array{Float64,2}, ml4::Array{Float64,2})
    start::Float64 = 0.0
    finish::Float64 = 0.0
    Benchmarker.cachescrub()
    start = time_ns()

    # cost: 7.14e+09 FLOPs
    # M1: ml0, full, M2: ml1, full, M3: ml2, full, M4: ml3, full, M5: ml4, full
    ml5 = Array{Float64}(undef, 1100, 1100)
    # tmp1 = (M1 M2^T)
    gemm!('N', 'T', 1.0, ml0, ml1, 0.0, ml5)

    # M3: ml2, full, M4: ml3, full, M5: ml4, full, tmp1: ml5, full
    # tmp3 = (tmp1 + M5^T)
    ml5 .+= transpose(ml4)

    # M3: ml2, full, M4: ml3, full, tmp3: ml5, full
    # tmp4 = (tmp3 + M4^T)
    ml5 .+= transpose(ml3)

    # M3: ml2, full, tmp4: ml5, full
    # tmp5 = (tmp4 + (M3 M3^T))
    gemm!('N', 'T', 1.0, ml2, ml2, 1.0, ml5)

    # tmp5: ml5, full
    # Y = tmp5

    finish = time_ns()
    return (tuple(ml5), (finish-start)*1e-9)
end