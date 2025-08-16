function out=problema3(v, k)
  C = nchoosek(v, k);
  linii = length(C);
  P1 = [];
  for(i = 1:linii)
    cuv = C(i,:);
    P2 = perms(cuv);
    P1 = [P1;P2];
  endfor
  P1
end

