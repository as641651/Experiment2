using MatrixGenerator

function operand_generator()
    M1::Array{Float64,2} = generate((1100,1800), [Shape.General, Properties.Random(-1, 1)])
    M2::Array{Float64,2} = generate((1100,1800), [Shape.General, Properties.Random(-1, 1)])
    M3::Array{Float64,2} = generate((1100,1150), [Shape.General, Properties.Random(-1, 1)])
    M4::UpperTriangular{Float64,Array{Float64,2}} = generate((1100,1100), [Shape.UpperTriangular, Properties.Random(10, 11)])
    M5::UpperTriangular{Float64,Array{Float64,2}} = generate((1100,1100), [Shape.UpperTriangular, Properties.Random(10, 11)])
    return (M1, M2, M3, M4, M5,)
end