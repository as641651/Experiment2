using LinearAlgebra.BLAS
using LinearAlgebra

"""
    algorithm5(ml0::Array{Float64,2}, ml1::Array{Float64,2}, ml2::Array{Float64,2}, ml3::Array{Float64,2}, ml4::Array{Float64,2})

Compute
Y = ((M1 M2^T) + (M3 M3^T) + M4^T + M5^T).

Requires at least Julia v1.0.

# Arguments
- `ml0::Array{Float64,2}`: Matrix M1 of size 1100 x 1800 with property FullRank.
- `ml1::Array{Float64,2}`: Matrix M2 of size 1100 x 1800 with property FullRank.
- `ml2::Array{Float64,2}`: Matrix M3 of size 1100 x 1150 with property FullRank.
- `ml3::Array{Float64,2}`: Matrix M4 of size 1100 x 1100 with property UpperTriangular.
- `ml4::Array{Float64,2}`: Matrix M5 of size 1100 x 1100 with property UpperTriangular.
"""                    
function algorithm5(ml0::Array{Float64,2}, ml1::Array{Float64,2}, ml2::Array{Float64,2}, ml3::Array{Float64,2}, ml4::Array{Float64,2})
    # cost: 5.75e+09 FLOPs
    # M1: ml0, full, M2: ml1, full, M3: ml2, full, M4: ml3, full, M5: ml4, full
    ml5 = Array{Float64}(undef, 1100, 1100)
    # tmp2 = (M3 M3^T)
    syrk!('L', 'N', 1.0, ml2, 0.0, ml5)

    # M1: ml0, full, M2: ml1, full, M4: ml3, full, M5: ml4, full, tmp2: ml5, symmetric_lower_triangular
    for i = 1:1100-1;
        view(ml5, i, i+1:1100)[:] = view(ml5, i+1:1100, i);
    end;
    # tmp6 = (tmp2 + (M1 M2^T))
    gemm!('N', 'T', 1.0, ml0, ml1, 1.0, ml5)

    # M4: ml3, full, M5: ml4, full, tmp6: ml5, full
    # tmp10 = (tmp6 + M4^T)
    ml5 .+= transpose(ml3)

    # M5: ml4, full, tmp10: ml5, full
    # tmp5 = (tmp10 + M5^T)
    ml5 .+= transpose(ml4)

    # tmp5: ml5, full
    # Y = tmp5
    return (ml5)
end