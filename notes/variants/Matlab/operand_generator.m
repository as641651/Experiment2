function [out] = operand_generator()
    import MatrixGenerator.*;
    out{ 1 } = generate([100,20], Shape.General(), Properties.Random([-1, 1]));
    out{ 2 } = generate([100,100], Shape.Symmetric(), Properties.SPD());
    out{ 3 } = generate([100,1], Shape.General(), Properties.Random([-1, 1]));
end