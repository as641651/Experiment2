using MatrixGenerator

function operand_generator()
    X::Array{Float64,2} = generate((100,20), [Shape.General, Properties.Random(-1, 1)])
    M::Symmetric{Float64,Array{Float64,2}} = generate((100,100), [Shape.Symmetric, Properties.SPD])
    y::Array{Float64,1} = generate((100,1), [Shape.General, Properties.Random(-1, 1)])
    return (X, M, y,)
end