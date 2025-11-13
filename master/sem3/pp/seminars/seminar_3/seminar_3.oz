% Exercises from seminar 3
functor
import
   System
define
  % Exercise 1
  fun {Member Xs Y}
    case Xs of
      nil then false
      [] H|T then
        if H == Y then true
        else {Member T Y}
        end
    end
  end

  {System.show {Member [a b c] b}}
  {System.show {Member [a b c] d}}

  % Exercise 2
  fun {Take Xs N}
    if N == 0 then nil
    else
      case Xs of
        nil then nil
        [] H|T then H|{Take T N-1}
      end
    end
  end

  {System.show {Take [1 4 3 6 2] 3}}

  fun {Drop Xs N}
    if N == 0 then
       case Xs of
         nil then nil
         [] H|T then H|T
        end

    else
      case Xs of
        nil then nil
        [] H|T then {Drop T N-1}
      end
    end
  end
  {System.show {Drop [1 4 3 6 2] 3}}

  % Exercise 3
  fun {Zip Xs#Ys}
    case Xs#Ys of
      nil#nil then nil
      [] (X|Xr)#(Y|Yr) then X#Y|{Zip Xr#Yr}
    end
  end

  fun {UnZip List}
    case List of
      nil then nil#nil
      [] (X#Y)|T then
        case {UnZip T} of
          RestXs#RestYs then
            (X|RestXs)#(Y|RestYs)
          end
    end
  end
  {System.show {Zip [1 2 3]#[4 5 6]}}
  {System.show {UnZip [1#4 2#5 3#6]}}

  % Exercise 4
  fun {Position_1 Xs Y}
    case Xs of
      nil then 1
      [] H|T then
        if H == Y then 1
        else 1 + {Position_1 T Y}
        end
    end
  end
  {System.show {Position_1 [a b c] c}}

  fun {Position_2 Xs Y}
    case Xs of
      nil then 0
      [] H|T then
        if H == Y then 1
        else
          case {Position_2 T Y} of
            0 then 0
            [] SomePosition then SomePosition + 1
          end
        end
    end
  end
  {System.show {Position_2 [a b c] c}}

  % Exercise 5
  fun {Eval X#Y}
    case X of
      int then Y
      [] add then {Eval Y.1} + {Eval Y.2}
      [] mul then {Eval Y.1} * {Eval Y.2}
      else
        0
    end
  end

  {System.show {Eval add#((int#1)#(mul#((int#3)#(int#4))))}}
end
