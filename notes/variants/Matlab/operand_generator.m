function [out] = operand_generator()
    import MatrixGenerator.*;
    out{ 1 } = generate([100,100], Shape.General(), Properties.Random([-1, 1]));
    out{ 2 } = generate([100,100], Shape.General(), Properties.Random([-1, 1]));
    out{ 3 } = generate([100,100], Shape.General(), Properties.Random([-1, 1]));
    out{ 4 } = generate([100,100], Shape.General(), Properties.Random([-1, 1]));
end