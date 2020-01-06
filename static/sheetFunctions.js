async function create_google_sheet(vm, params){
    //You have to make sure to close dialogflow querying.
    vm.openDialogQuery = false;
    var sheet_name = params.fields.sheet_name.stringValue;

    try {
        responseFinal = await call_google_api_functions("createSheets", sheet_name);
        pushWinterText(vm, "created google sheet!");
        // pushSelectChatbox(vm, calResponse);
        $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
      } catch(err) {
        alert(err); // TypeError: failed to fetch
      }
      //Opening dialogflow querying
      vm.openDialogQuery = true;
}


async function populate_google_sheet(vm, params){
    //You have to make sure to close dialogflow querying.
    vm.openDialogQuery = false;
    var sheet_name = params.fields.sheet_name.stringValue;
    //querying and checking if there is a response
    // pushWinterText(vm, "Select a google sheet.");
    var response = await call_google_api_functions("searchFileName", sheet_name);
    if(!(checkResponse(vm, response, "There appears to be no documents with the name of '" + sheet_name + "'"))){return}
    //let user select
    var SheetRaw = await waitUserSelect(vm, response, "Choose the sheet you'd like me to populate. ");
    sheet_id = SheetRaw.id;

    //let user select
    var user_input = await waitUserText(vm, "Type the data you want inputed in, '|' to deliminate columns, ',' by cell format. ");

    try {
        responseFinal = await call_google_api_functions("populateSheet", user_input, sheet_id);
        pushWinterText(vm, "I've added the data as you'd like.");
        // pushSelectChatbox(vm, calResponse);
        $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
      } catch(err) {
        alert(err); // TypeError: failed to fetch
      }
      //Opening dialogflow querying
      vm.openDialogQuery = true;
}



async function read_google_sheet(vm, params){
    //You have to make sure to close dialogflow querying.
    vm.openDialogQuery = false;
    var sheet_name = params.fields.sheet_name.stringValue;
    //querying and checking if there is a response
    // pushWinterText(vm, "Select a google sheet.");
    var response = await call_google_api_functions("searchFileName", sheet_name);
    if(!(checkResponse(vm, response, "There appears to be no documents with the name of '" + sheet_name + "'"))){return}
    //let user select
    var SheetRaw = await waitUserSelect(vm, response, "Choose the sheet you'd like me to populate. ");
    sheet_id = SheetRaw.id;

    try {
        responseFinal = await call_google_api_functions("readSheet", sheet_id);
        pushWinterText(vm, "Here you go");
        pushWinterText(vm, responseFinal);
        // pushSelectChatbox(vm, calResponse);
        $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
      } catch(err) {
        alert(err); // TypeError: failed to fetch
      }
      //Opening dialogflow querying
      vm.openDialogQuery = true;
}


async function rename_google_sheet(vm, params){
    //You have to make sure to close dialogflow querying.
    vm.openDialogQuery = false;
    var sheet_name = params.fields.query.stringValue;
    var rename = params.fields.rename.stringValue;
    //querying and checking if there is a response
    // pushWinterText(vm, "Select a google sheet.");
    var response = await call_google_api_functions("searchFileName", sheet_name);
    if(!(checkResponse(vm, response, "There appears to be no documents with the name of '" + sheet_name + "'"))){return}
    //let user select
    var SheetRaw = await waitUserSelect(vm, response, " Choose the sheet you'd like me to rename ");
    sheet_id = SheetRaw.id;

    try {
        responseFinal = await call_google_api_functions("renameSheet", rename, sheet_id);
        pushWinterText(vm, "I've added the data as you'd like.");
        // pushSelectChatbox(vm, calResponse);
        $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
      } catch(err) {
        alert(err); // TypeError: failed to fetch
      }
      //Opening dialogflow querying
      vm.openDialogQuery = true;
}
