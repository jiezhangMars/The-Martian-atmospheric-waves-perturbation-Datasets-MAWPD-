function replace_the_line_contains_something(filename_ini,filename_new,new_contents,old_content)

fid=fopen(filename_ini);
replaceLine=0;

%% find the line of the selected content
while ~feof(fid)
   
replaceLine=replaceLine+1;
str = fgetl(fid);

if isempty(str)|str(1)=='!'
    continue;
end
if contains(str,old_content)
break;    
end
end
%% modify it
text_modify(filename_ini,filename_new,new_contents,replaceLine);
fclose(fid);
end