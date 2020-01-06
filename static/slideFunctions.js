async function add_slide_google_slides(vm, params){
    //You have to make sure to close dialogflow querying.
    vm.openDialogQuery = false;
    var slide_name = params.fields.slide_name.stringValue;

    //querying and checking if there is a response
    var response = await call_google_api_functions("searchFileName", slide_name);
    if(!(checkResponse(vm, response, "There appears to be no documents with the name of '" + slide_name + "'"))){return}

    //let user select
    var slideRaw = await waitUserSelect(vm, response, "Choose the slide you want to add a slide to.");
    slide_id = slideRaw.id;


    try {
        responseFinal = await call_google_api_functions("createSingleSlide", slide_id);
        pushWinterText(vm, "Added a slide, boss.");
        // pushSelectChatbox(vm, calResponse);
        $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
      } catch(err) {
        alert(err); // TypeError: failed to fetch
      }
      //Opening dialogflow querying
      vm.openDialogQuery = true;
}