function [out] = operand_generator()
    import MatrixGenerator.*;
    out{ 1 } = generate([1100,1800], Shape.General(), Properties.Random([-1, 1]));
    out{ 2 } = generate([1100,1800], Shape.General(), Properties.Random([-1, 1]));
    out{ 3 } = generate([1100,1150], Shape.General(), Properties.Random([-1, 1]));
    out{ 4 } = generate([1100,1100], Shape.UpperTriangular(), Properties.Random([10, 11]));
    out{ 5 } = generate([1100,1100], Shape.UpperTriangular(), Properties.Random([10, 11]));
end