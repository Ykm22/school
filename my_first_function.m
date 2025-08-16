function out=my_first_function(in)
  %out = 1+1;
  out = NaN; %NaN = "not a number"
  if in~=1 %~= este operatorul diferit
    return
  else
    disp('Hello world!'); out = 1;
  endif
end

