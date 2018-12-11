clear
close all
clc

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Script permettant de binariser nos images d'entrées et de les rogner afin%
%d'optimiser le traitement par la suite. On enregistre les images         %
%binarisées et rognées dans le même dossier                               %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


nbimage = 12; %Nombre d'image par sous dossier
Images = cell(nbimage);
SE = [1 1 1;
      1 1 1;
      1 1 1];
seuil = 100; %Seuil retenu manuellement à partir de l'histogramme
  
  
for i=1:nbimage
    path = sprintf('Image/Pouce/%d.png',i);
    I = imread(path);
    %seuil = graythresh(I)*100;
    I_BW1 = im2bw(I,seuil/255);
    I_BW2 =~ I_BW1;

    I_BW_morph = imerode(I_BW2,SE);
    rect = boxing(I_BW_morph,1);
    I_crop = imcrop(I_BW_morph,[rect(1) rect(2) rect(3)-rect(1) rect(4)-rect(2)]);
    Images{i} = I_crop;
end

for i=1:nbimage
    figure('Name',sprintf('Image %d',i));
    imshow(Images{i});
    fname = sprintf('Image/Pouce/test_%d.tif',i);
    imwrite(Images{i},fname);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                    fullcoord = boxing(I,N)                     %
%Pour chaque chiffre, on réajuste sa hauteur pour les mettre dans%
%une "box"                                                       %
%                                                                %
%I : Image à traiter                                             %
%N : Nombre de chiffre par ligne                                 %
%fullcoord : Coordonnées des boxes (tableau 4 colonnes)          %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function fullcoord = boxing(I, N)
    %vx est la somme de tous les pixels noirs pour chaque ligne de l'image
    vx = sum(I<1,2);
    tabligne = searchline(I,vx);
    fullcoord = zeros(N,4);
    I0 = I((tabligne(1,1):tabligne(1,2)),:);
    vy = sum(I0<1,1);
    tabcol = searchcol(I0,vy,N);

    for m=1:N
            subI = I0(:,(tabcol(m,1):tabcol(m,2)));
            [~,y1] = find(subI'<50,1,'first');
            [~,y2] = find(subI'<50,1,'last');
            
            %line([tabcol(m,1) tabcol(m,2)], [y1+tabligne(k,1) y1+tabligne(k,1)]);
            %line([tabcol(m,1) tabcol(m,2)], [y2+tabligne(k,1) y2+tabligne(k,1)]);
            %line([tabcol(m,1) tabcol(m,1)], [y1+tabligne(k,1) y2+tabligne(k,1)]);
            %line([tabcol(m,2) tabcol(m,2)], [y1+tabligne(k,1) y2+tabligne(k,1)]);
            %hold off;

            fullcoord(m,1) = tabcol(m,1);         %abscisse du coin haut gauche
            fullcoord(m,2) = y1+tabligne(1,1)-1;  %ordonnée du coin haut gauche
            fullcoord(m,3) = tabcol(m,2);         %abscisse du coin bas droit
            fullcoord(m,4) = y2+tabligne(1,1)-1;  %ordonnée du coin bas droit
    end
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                tabligne = searchline(I,vx)                     %
%Permet de séparer les chiffres par bande                        %
%                                                                %
%I : Image à analyser                                            %
%vx : vecteur contenant le nombre de pixel noirs par ligne       %
%tabligne : tableau avec la hauteur de la bande (premier et      %
%           dernier pixel)                                       %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function tabligne = searchline(I, vx)
    innb = false;
    tabligne = zeros(1,2);
    l = 1;
    for i = 1:size(I,1)
    
    if vx(i) ~= 0 && innb == false
       %line([1 size(I,2)],[i i])
       tabligne(l,1) = i;
       innb = true;
    end
    if vx(i) == 0 && innb == true
        
       %line([1 size(I,2)],[i i])
       
       tabligne(l,2) = i-1;
       l = l+1;
       innb = false;
    end
    end
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                tabcol = searchcol(I0, vy, N)                   %
%Permet de séparer les chiffres verticalement                    %
%                                                                %
%I0 : Image à analyser (bande)                                   %
%vy : vecteur contenant le nombre de pixel noirs par ligne       %
%N : Nombre de chiffres par ligne                                %
%tabcol : tableau avec la largeur de chaque chiffre (premier et  %
%           dernier pixel)                                       %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function tabcol = searchcol(I0, vy, N)
    innb = false;
    tabcol = zeros(N,2);
    l = 1;
    for i = 1:size(I0,2)
        
        if vy(i) ~= 0 && innb == false
           tabcol(l,1) = i;
           innb = true;
        end
        if vy(i) == 0 && innb == true

           tabcol(l,2) = i-1;
           l = l+1;
           innb = false;
        end
    end
end