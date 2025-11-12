% Exercises from seminar 2
functor
import
   System
define
  % Exercise 1
  fun {Fact N}
    if N == 2 then 2
    else N * {Fact N-1}
    end
  end

  fun {Comb N K}
    {Fact N} div ({Fact K} * {Fact N-K})
  end

  fun {FactDecreasingUntil N K}
   % {System.show N}
    if N == K then K
    else N * {FactDecreasingUntil N-1 K}
    end
  end

  fun {CombA N K}
    if K == 0 then 1
    else ({FactDecreasingUntil N N-(K-1)} div {Fact K})
    end
  end

  fun {CombB N K}
    % {System.show N}
    % {System.show K}
    if K == 1.0 then N
    else (N / K) * {CombB N-1.0 K-1.0}
    end
  end

  % this didn't work
  % fun {CombB N K}
  %   if K == 0.0 then 1.0
  %   else 
  %     if K == 1.0 then N
  %     else ((N-K+1.0) / K) * {CombB N-1.0 K-1.0}
  %     end
  %   end
  % end

  {System.show {Comb 10 3}}
  {System.show {CombA 10 3}}
  {System.show {CombB 10.0 3.0}}

  % Exercise 2
  fun {Reverse List ReversedList}
    case List of 
      nil then ReversedList
      [] H|T then {Reverse T H|ReversedList} 
    end
  end
  {System.show {Reverse ['I' 'want' 2 go 'there'] nil}}

  % Exercise 3
  fun lazy {Filter L H}
    case L of
      nil then nil
      [] A|As then
        if (A mod H) == 0 then {Filter As H}
        else A|{Filter As H}
        end
    end
  end

  fun lazy {Gen N}
    N|{Gen N+1}
  end

  fun lazy {Sieve L}
    case L of
      nil then nil
      [] H|T then H|{Sieve {Filter T H}}
    end
  end

  fun {Prime}
    {Sieve {Gen 2}}
  end

  fun {FindNextGreater N List}
    case List of
      nil then ~1
      [] H|T then
        if H > N then H
        else {FindNextGreater N T}
        end
    end
  end

  LazyPrimeNumbersList = {Sieve {Gen 2}}

  fun {GetAfter N}
    {FindNextGreater N LazyPrimeNumbersList}
  end

  % {System.show {GetAfter 300}}

  % Exercise 4
  N2 = node(5 nil nil)
  N1 = node(3 nil N2)
  {System.show N1.1}
  {System.show N1.2}
  {System.show N1.3}

  fun {Insert BTree N}
    case BTree of
      nil then node(N nil nil)
      [] node(Val Left Right) then
        if N < Val then node(Val {Insert Left N} Right)
        elseif N > Val then node(Val Left {Insert Right N})
        else BTree
        end
      end
  end
  
  fun {Smallest BTree}
    case BTree of
      nil then nil
      [] node(Val Left Right) then
        if Left == nil then Val
        else {Smallest Left}
        end
    end
  end

  fun {Biggest BTree}
    case BTree of
      nil then nil
      [] node(Val Left Right) then
        if Right == nil then Val
        else {Biggest Right}
        end
    end
  end

  fun {IsSortedBST BTree}
    case BTree of
      nil then true
    [] node(Val Left Right) then
      if Left == nil then true else {Biggest Left} < Val end
      andthen
      if Right == nil then true else {Smallest Right} > Val end
      andthen
      {IsSortedBST Left} andthen {IsSortedBST Right}
    end
  end

  {System.show {Insert N1 10}}
  {System.show {Smallest {Insert N1 10}}}
  {System.show {Biggest {Insert N1 10}}}
  {System.show {IsSortedBST node(5 node(10 nil nil) node(3 nil nil))}}
  {System.show {IsSortedBST N1}}
end
