function [dxf] = Leer_DXF(nombre)
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here
% read file and plot
    dxf = DXFtool(nombre); 
    dxf.list;
end

