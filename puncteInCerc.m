function out=puncteInCerc(N, cerinta)
  found = 0;
  clf; hold on; axis equal; grid on;
  rectangle('Position', [0, 0, 1, 1]);
  for i = 1 : N
    x = rand;
    y = rand;
    P = [x, y];
    O = [0.5, 0.5];
    dist = pdist([P; O]);
    if cerinta == 1
      if dist <= 0.5
        found = found + 1;
        plot(x, y, '*r');
      endif
    endif
    if cerinta == 2
      A = [0, 0];
      B = [0, 1];
      C = [1, 0];
      D = [1, 1];
      if pdist([P; O]) < pdist([P; A]) && pdist([P; O]) < pdist([P; B]) && pdist([P; O]) < pdist([P; C]) && pdist([P; O]) < pdist([P; D])
        found = found + 1;
        plot(x, y, '*r');
      endif
    endif
    if cerinta == 3
      %a^2 < b^2 + c^2
      %teorema lui pitagora generalizata
      %se compara perechi de puncte
    endif

  endfor

  out = found / N;
end
