using MatrixGenerator

{variants_includes}
include("operand_generator.jl")

function main()

    matrices = operand_generator()

    io = open("{runner_path}","w")
    write(io, "case:concept:name;concept:name;concept:flops;concept:operation;concept:kernel;timestamp:start;timestamp:end\n")

{runner_code}


end

main()