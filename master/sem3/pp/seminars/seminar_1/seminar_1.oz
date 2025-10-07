% Exercises from seminar 1
functor
import
   System
define
  % Exercise 1
  fun {Abs X}
    if {IsInt X} then
      if X < 0 then ~X else X end
    else
      if X < 0.0 then ~X else X end
    end
  end

  {System.show ['Exercise 1' 'Abs(1) = ' {Abs 1}]}
  {System.show ['Exercise 1' 'Abs(-1) = ' {Abs ~1}]}
  {System.show ['Exercise 1' 'Abs(1.123) = ' {Abs 1.123}]}
  {System.show ['Exercise 1' 'Abs(-1.123) = ' {Abs ~1.123}]}

  % Exercise 2
  fun {Pow N M}
    if M == 0 then 1
    else N * {Pow N (M-1)}
    end
  end

  {System.show ['Exercise 2' 'Pow(2, 5) = ' {Pow 2 5}]}

  % Exercise 3
  fun {Max N M}
    if N == 0 then M
    elseif M == 0 then N
    else 1 + {Max (N-1) (M-1)}
    end
  end

  {System.show ['Exercise 3' 'Max(2, 10) = '{Max 2 10}]}
end
