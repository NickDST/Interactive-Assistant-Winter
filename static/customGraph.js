var data = [ 
//     {
//     x: [], // in reality I have more values... 
//     y: [], 
//     type: ''
//     }
]; 


function adjustValue1(vm) {

    trace = {
        x: vm.xData,
        y: vm.yData,
        type: vm.graphType
    }
    if(vm.graphType == "scatter3d"){
        trace.mode = "markers";
        trace.marker = {
            color: 'rgb(Math.random()*127, Math.random()*127, Math.random()*127)',
            size: 12,
            symbol: 'circle',
            line: {
            color: 'rgb(Math.random()*204, Math.random()*204, Math.random()*204)',
            width: 1},
            opacity: 0.8};
        trace.z = vm.zData;
    }

    console.log(trace)
    data.push(trace)

    set_color = [];
    var parallel_data = [{

        type: 'parcoords',
        pad: [80, 80, 80, 80],
        line: {
          showscale: false,
          reversescale: true,
          colorscale: 'Jet',
          cmin: -4000,
          cmax: -100,
          color: set_color
        },
        dimensions: []
    }];

    if(vm.graphType == "coordinate_parallel"){

    for(var i = 0; i < vm.xData.length; i++){
        set_color.push(-(Math.random() * 4000));
    }
    



    xpart = Math.floor(vm.xData.length * 1.1);
    ypart = Math.floor(vm.yData.length * 1.1);
    zpart = Math.floor(vm.zData.length * 1.1);

    numberSort = function (a,b) {
        return a - b;
    };
    

    sorted_xData = vm.xData.slice(0).sort(numberSort); //do the slice(0) to create a new copy
    sorted_yData = vm.yData.slice(0).sort(numberSort);
    sorted_zData = vm.zData.slice(0).sort(numberSort);



    parallel_data[0].dimensions.push({
        label: vm.xCol,
        range: [Math.floor(sorted_xData[0] * 0.8), sorted_xData.filter(e => typeof e == 'number')[sorted_xData.filter(e => typeof e == 'number').length-1] * 1.1],
        values: vm.xData
      },
      {
        label: vm.yCol,
        range: [Math.floor(sorted_yData[0] * 0.8), sorted_yData.filter(e => typeof e == 'number')[sorted_yData.filter(e => typeof e == 'number').length-1] * 1.1],
        values: vm.yData
      },
      {
        label: vm.zCol,
        range: [Math.floor(sorted_zData[0] * 0.8), sorted_zData.filter(e => typeof e == 'number')[sorted_zData.filter(e => typeof e == 'number').length-1] * 1.1],
        values: vm.zData
      })

    data = parallel_data;
    // console.log(data);

    }
    console.log(data);
    // Plotly.plot('myDiv', data);

    console.log(vm.graphCreated);
    if(vm.graphCreated == 0){
        console.log("new")

        if(vm.graphType == "coordinate_parallel"){
            Plotly.plot('myDiv', data);
        } else {
            Plotly.newPlot('myDiv', data); 
        }

        
    } else {
        console.log("redraw")
        Plotly.redraw('myDiv');
    }
}

function clearData(vm){
    data = [];
    vm.graphCreated = 1;
    console.log("Data Cleared")
    Plotly.newPlot('myDiv', data);
}