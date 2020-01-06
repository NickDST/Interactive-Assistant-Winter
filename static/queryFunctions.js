async function QueryFallbackIntent(vm, dialogResponse){

    //let user select
    // var answer = await waitUserText(vm, "Would you like for me to look it up?");
    
    // if(answer.includes("no") || answer.includes("pass") || answer.includes("I'm good")){
    //     pushWinterText(vm, "Undestood.");

    // } else if(answer.includes("yes") || answer.includes("sure") || answer.includes("ye")){
    //     pushWinterText(vm, "Undestood.");
    
    
    query = dialogResponse.data.queryText
    const path = '/WolframAlphaAPIs';
    var res = await axios({
        method: 'get',
        url: path,
        params: {
            query: query,
          }
    })
        pushWinterText(vm, res.data);
    // } else {
    //     pushWinterText(vm, "Not really sure I understand but I won't search.");
    // }
}


async function query_wikiepdia(vm, params){
    var query = params.fields.query.stringValue;
    
    const path = '/wikipediaQuery';
    var res = await axios({
        method: 'get',
        url: path,
        params: {
            query: query,
          }
    })

    pushWinterText(vm, res.data);
}