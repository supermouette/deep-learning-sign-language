function reconnaissance()
    nb_signes = 5;
    %d=1;
% centres_d_1_20 = cell(20);
% for d=1:20
%     sums = zeros(2*d,1);
%     centres_app = cell(nb_signes,1);
%     
%     signes = {'Doigt', 'Ok', 'Paume', 'Poing', 'Pouce'};
%     
% %%%%%% APPRENTISSAGE PROFILS EUCLIDIENS %%%%%%
% 
%     for s=1:nb_signes
%         folder = sprintf('Image/%s',signes{s});
%         a = dir([folder '/*.tif']);
%         nb_images_app = numel(a);
%         
%         for i=1:nb_images_app
%             path = sprintf('Image/%s/crop_bin_%d.tif',signes{s},i);
%             I = imread(path);
%         
%             sums = sums + dist_eucli(I, d);    
%         end
%         
%         sums = sums / nb_images_app;
%         
%         centres_app{s} = sums;
%     end
%     centres_d_1_20{d} = centres_app;
% end
    

%%%%%% APPRENTISSAGE KPPV %%%%%%
%     n=10;
%     m=10;
%     
%     zones_app = cell(nb_signes,1);
%     for s=1:nb_signes
%         folder = sprintf('Image/%s',signes{s});
%         a = dir([folder '/*.tif']);
%         nb_images_app = numel(a);
%         
%         zones = zeros(nb_images_app,n*m);
%         
%         for i=1:nb_images_app
%             path = sprintf('Image/%s/crop_bin_%d.tif',signes{s},i);
%             I = imread(path);
%             
%             zones(i,:) = zoning(I, n, m);
%         end
%         zones_app{s}=zones;
%     end

%%%%%% TEST PROFILS EUCLIDIENS %%%%%%
accuracy_eucli = zeros(20,1);
for d=1:20
    signes = {'doigt', 'ok', 'paume', 'poing', 'pouce'};
    file = load('dist_eucli_app_d_1_20.mat');
    centres_app = file.centres_d_1_20(d);
    centres_app = cell(centres_app{1,1});
    nb_images_test = 10;
    nb_correct = 0;
    for s=1:nb_signes
        for i=1:nb_images_test
            path = sprintf('image_test/test_%s_%d.tif',signes{s},i);
            I_test = imread(path);

            centre_test = dist_eucli(I_test, d);

            proba = zeros(nb_signes,1);
            for j=1:nb_signes       
                proba(j,1) = proba_distance(centres_app, centre_test, j, nb_signes);
            end
            
            [~, index] = max(proba);
            
            if index == s
                nb_correct = nb_correct + 1;
            end
        end
    end
    
    result = (nb_correct / (nb_images_test*5))*100;
    accuracy_eucli(d,1) = result;
end
plot(1:20,accuracy_eucli)


%%%%%% TEST KPPV %%%%%%
%     n=10;
%     m=10;
%     kppv=3;
%     signes = {'doigt', 'ok', 'paume', 'poing', 'pouce'};
%     file = load('kppv_app_m=10_n=10.mat');
%     zones_app = file.zones_app;
%     nb_images_test = 10;
%     nb_correct = 0;
%     %path = sprintf('Image/Poing/test_12.tif');
%     nb_total_images_app = 0;
%     for s=1:nb_signes
%         nb_total_images_app = nb_total_images_app + size(zones_app{s,1},1);
%     end
%     for s=1:nb_signes
%         for i=1:nb_images_test
%             dist_total = zeros(nb_total_images_app,2);
%             path = sprintf('image_test/test_%s_%d.tif',signes{s},i);
%             I_test = imread(path);
%             dist = dist_euc2(I_test, zones_app, n, m);
%             index=1;
%             for k=1:nb_signes
%                 dist_total(index:index-1+size(zones_app{k,1},1),1) = dist{k};
%                 dist_total(index:index-1+size(zones_app{k,1},1),2) = k;
%                 index = index + size(zones_app{k,1},1);
%             end
%             dist_total_sort = sortrows(dist_total,1);
%             
%             for j=1:kppv
%                 best_match(j) = dist_total_sort(j,2);
%             end
%             
%             for j=1:nb_signes
%                 correct = 0;
%                 for x=1:kppv
%                     
%                     if best_match(x) == j
%                         correct = correct +1;
%                     end
%                 end
%                 proba((i+(s-1)),j) = correct/kppv;
%             end
%             [~, index] = max(proba((i+(s-1)),:));
%             if index == s
%                 nb_correct = nb_correct +1;
%             end
%         end
%     end
%     result = (nb_correct / (nb_images_test*5))*100;




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

function proba = proba_distance(centres_app, c_test, n, nb_signes)
    tab_dist = zeros(10,1);
    sum_exp = 0;
    for i = 1:nb_signes
        tab_dist(i) = distance_centre(centres_app{i}, c_test);
        sum_exp = sum_exp + exp(-tab_dist(i));
    end
    proba = exp(-tab_dist(n))/sum_exp;

end

function distance = distance_centre(centre_app, c_test)
    m = 0;
    for i = 1:length(centre_app)
        m = m + power((centre_app(i) - c_test(i)),2);
    end
    distance = sqrt(m);
end

function [densite] = zoning(I, n, m)
    hauteur = size(I+1, 1);
    largeur = size(I+1, 2);
    
    nb_px_v = fix(largeur/n); %Nombre de pixel entre chaque lignes verticales
    nb_px_h = fix(hauteur/m); %Nombre de pixel entre chaque lignes horizontales
    
    densite_chiffre = zeros(1,n*m);
    
    digit = I;
    imshow(digit);
    for i=1:m
       line([1 largeur], [nb_px_h*(i) nb_px_h*(i)])
    end
    for i=1:n
       line([1+nb_px_v*(i) 1+nb_px_v*(i)],[1 hauteur])
    end
    
    for i=1:m
        for j=1:n
            coin_haut_gauche = [1+(j-1)*nb_px_v, 1+(i-1)*nb_px_h];
            coin_bas_droit = [j*nb_px_v, i*nb_px_h];
            zone = I((coin_haut_gauche(2):coin_bas_droit(2)),(coin_haut_gauche(1):coin_bas_droit(1)));
%             imshow(zone);
            [a,b] = size(zone);
            surface = a*b;
            densite_chiffre(1,i*j) = sum((zone(:)==0)/surface);
        end
    end
    
    densite = densite_chiffre;
    
end

function [dist] = dist_euc2(I_test, zones_app, n, m)
    dist = cell(size(zones_app));
    zones_test = zoning(I_test, n, m);

    for k = 1:size(zones_app)
        zones = zones_app{k,1};
        dist{k} = zeros(size(zones,1),1);
        for j = 1:size(zones,1)
            dist{k}(j,1) = sqrt(sum(zones(j,:)-zones_test).^2);
        end
    end
end