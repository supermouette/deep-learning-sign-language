function reconnaissance()
    nb_signes = 5;
    nb_images_app = 12;
    d=5;
    sums = zeros(2*d,1);
    centres_app = cell(nb_signes,1);
    
    signes = {'Doigt', 'Ok', 'Paume', 'Poing', 'Pouce'};
    
    for s=1:nb_signes
        
        for i=1:nb_images_app
            path = sprintf('Image/%s/test_%d.tif',signes{s},i);
            I = imread(path);
        
            sums = sums + dist_eucli(I, d);    
        end
        
        sums = sums / nb_images_app;
        
        centres_app{s} = sums;
    end
    
    %path = sprintf('Image/Poing/test_12.tif');
    path = sprintf('Image/crop_bin_test.tif');
    I_test = imread(path);
    
    centre_test = dist_eucli(I_test, d);
    
    proba = zeros(nb_signes,1);
    for i=1:nb_signes       
        proba(i,1) = proba_chiffre_distance(centres_app, centre_test, i, nb_signes);
    end

end

function [profil] = dist_eucli(I, d)
    distance = zeros(d,2);

    count=1;
    
    %imshow(digit);
    %hold on
    %for i=1:d
    %    line([1 x2-x1+1], [1+nb_px*(i-1) 1+nb_px*(i-1)])
    %end
    %hold off
    
    hauteur = size(I, 1);
    largeur = size(I, 2);
    
    for i=1:(hauteur/(d-1)):hauteur
        index = ceil(i);
        sub_I = I(index,:);
        [~,x] = find(sub_I<1,1,'first'); %distance à gauche
        distance(count,1) = x/largeur;
        [~,x] = find(sub_I<1,1,'last');  %distance à droite
        distance(count,2) = (largeur-x)/largeur;
        count = count + 1;
    end
        
    profil = [distance(:,1) ; distance(:,2)];
end

function proba = proba_chiffre_distance(centres_app, c_chiffre, n, nb_signes)
    tab_dist = zeros(10,1);
    sum_exp = 0;
    for i = 1:nb_signes
        tab_dist(i) = distance_chiffre_centre(centres_app{i}, c_chiffre);
        sum_exp = sum_exp + exp(-tab_dist(i));
    end
    proba = exp(-tab_dist(n))/sum_exp;

end

function distance = distance_chiffre_centre(centre_app, c_chiffre)
    m = 0;
    for i = 1:length(centre_app)
        m = m + power((centre_app(i) - c_chiffre(i)),2);
    end
    distance = sqrt(m);
end