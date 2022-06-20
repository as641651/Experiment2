using LinearAlgebra.BLAS
using LinearAlgebra

function algorithm13(ml0::Array{Float64,2}, ml1::Array{Float64,2}, ml2::Array{Float64,2}, ml3::Array{Float64,2}, ml4::Array{Float64,2})
    start::Float64 = 0.0
    finish::Float64 = 0.0
    Benchmarker.cachescrub()
    start = time_ns()

    # cost: 5.75e+09 FLOPs
    # M1: ml0, full, M2: ml1, full, M3: ml2, full, M4: ml3, full, M5: ml4, full
    ml5 = Array{Float64}(undef, 1100, 1100)
    # tmp1 = (M1 M2^T)
    gemm!('N', 'T', 1.0, ml0, ml1, 0.0, ml5)

    # M3: ml2, full, M4: ml3, full, M5: ml4, full, tmp1: ml5, full
    ml6 = Array{Float64}(undef, 1100, 1100)
    # tmp2 = (M3 M3^T)
    syrk!('L', 'N', 1.0, ml2, 0.0, ml6)

    # M4: ml3, full, M5: ml4, full, tmp1: ml5, full, tmp2: ml6, symmetric_lower_triangular
    for i = 1:1100-1;
        view(ml6, i, i+1:1100)[:] = view(ml6, i+1:1100, i);
    end;
    # tmp11 = (tmp2 + M4^T)
    ml6 .+= transpose(ml3)

    # M5: ml4, full, tmp1: ml5, full, tmp11: ml6, full
    # tmp9 = (tmp11 + M5^T)
    ml6 .+= transpose(ml4)

    # tmp1: ml5, full, tmp9: ml6, full
    # tmp5 = (tmp1 + tmp9)
    axpy!(1.0, ml5, ml6) # matrices

    # tmp5: ml6, full
    # Y = tmp5

    finish = time_ns()
    return (tuple(ml6), (finish-start)*1e-9)
end