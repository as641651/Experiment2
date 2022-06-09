using LinearAlgebra.BLAS
using LinearAlgebra

"""
    algorithm2(ml0::Array{Float64,2}, ml1::Array{Float64,2}, ml2::Array{Float64,2}, ml3::Array{Float64,2})

Compute
Y = (A B C D).

Requires at least Julia v1.0.

# Arguments
- `ml0::Array{Float64,2}`: Matrix A of size 100 x 100 with property Non-singular.
- `ml1::Array{Float64,2}`: Matrix B of size 100 x 100 with property Non-singular.
- `ml2::Array{Float64,2}`: Matrix C of size 100 x 100 with property Non-singular.
- `ml3::Array{Float64,2}`: Matrix D of size 100 x 100 with property Non-singular.
"""                    
function algorithm2(ml0::Array{Float64,2}, ml1::Array{Float64,2}, ml2::Array{Float64,2}, ml3::Array{Float64,2})
    # cost: 6e+06 FLOPs
    # A: ml0, full, B: ml1, full, C: ml2, full, D: ml3, full
    ml4 = Array{Float64}(undef, 100, 100)
    # tmp2 = (B C)
    gemm!('N', 'N', 1.0, ml1, ml2, 0.0, ml4)

    # A: ml0, full, D: ml3, full, tmp2: ml4, full
    ml5 = Array{Float64}(undef, 100, 100)
    # tmp4 = (A tmp2)
    gemm!('N', 'N', 1.0, ml0, ml4, 0.0, ml5)

    # D: ml3, full, tmp4: ml5, full
    ml6 = Array{Float64}(undef, 100, 100)
    # tmp6 = (tmp4 D)
    gemm!('N', 'N', 1.0, ml5, ml3, 0.0, ml6)

    # tmp6: ml6, full
    # Y = tmp6
    return (ml6)
end