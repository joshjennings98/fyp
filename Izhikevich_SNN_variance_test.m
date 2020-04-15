epochs = 1000; % simulation of 1000 ms
variances = [0; 0.01; 0.025; 0.05; 0.075; 0.1; 0.2; 0.3; 0.5; 0.75; 1; 1.1; 1.25; 1.5; 1.75; 2; 2.25; 2.5; 2.75; 3; 3.5; 4; 5; 6; 7; 8; 9; 10; 12; 15; 20; 25; 30; 40; 50; 60; 75; 100; 150; 200; 300; 400; 500; 750; 1000];

Ne=800;                     Ni=200;
re=rand(Ne,1);              ri=rand(Ni,1);

a=[0.02*ones(Ne,1);         0.02+0.08*ri];
b=[0.2*ones(Ne,1);          0.25-0.05*ri];
c=[-65+15*re.^2;            -65*ones(Ni,1)];
d=[8-6*re.^2;               2*ones(Ni,1)];
S=[0.5*rand(Ne+Ni,Ne),      -rand(Ne+Ni,Ni)];

for i=1:length(variances)
    fprintf("Run %d of %d.", i, length(variances));
    
    rng(123); % reset the seed for each test
    var = variances(i);
    
    v=-65*ones(Ne+Ni,1);        % Initial values of v
    u=b.*v;                     % Initial values of u
    firings=[];                 % spike timings
    quantity=zeros(epochs,1);   % Quantity of neurons firing per epoch
    
    for t=1:epochs
      I=[5*(var^0.5)*randn(Ne,1);2*(var^0.5)*randn(Ni,1)]; % thalamic input
      fired=find(v>=30);    % indices of spikes
      quantity(t) = length(fired);
      firings=[firings; t+0*fired,fired];
      v(fired)=c(fired);
      u(fired)=u(fired)+d(fired);
      I=I+sum(S(:,fired),2);
      v=v+0.5*(0.04*v.^2+5*v+140-u+I); % step 0.5 ms
      v=v+0.5*(0.04*v.^2+5*v+140-u+I); % for numerical
      u=u+a.*(b.*v-u);                 % stability
    end;
    
    f1 = figure;
    f2 = figure;
    
    figure(f1);
    plot(firings(:,1),firings(:,2),'.');
    title("When each neuron fires (σ²="+num2str(var)+")");
    xlabel("Epoch");
    ylabel("Neuron");
    xlim([0, epochs]);
    ylim([0, Ne+Ni]);
    exportgraphics(gcf,"when (σ²="+num2str(var)+").png",'Resolution',300);
    
    figure(f2);
    plot(quantity);
    title("Quantity of neurons firing per epoch (σ²="+num2str(var)+")");
    xlabel("Epoch");
    ylabel("Number of neurons that fire");
    xlim([0, epochs]);
    ylim([0, Ne+Ni]);
    exportgraphics(gcf,"quantity (σ²="+num2str(var)+").png",'Resolution',300);

end;

fprintf("Finished all runs.");