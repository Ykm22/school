function out=zileNastereIdentice(NrSim, n)
  found = 0;
  for i = 1 : NrSim
    arr = randi(365, 1, n);
    size1 = size(arr);
    uniq = unique(arr);
    size2 = size(uniq);
    if size1(1, 2) ~= size2(1, 2)
      found = found + 1;
    endif
  endfor
  out = found / NrSim;
end

