function insert_text_google_doc(vm, params){

    vm.openDialogQuery = false;
    // console.log(vm.openDialogQuery + " This should be false");
    //this function is essentially the beginning of a query >> action function
    console.log(params);
    
    //Extracting the variables from dialogflow
    var query = params.fields.googleDocName.stringValue;

    //querying and checking if there is a response
    call_google_api_functions("searchFileName", query).then(async (response) => {
    vm.select_modal_response = "response";

    if((response === undefined || response.length == 0)){
    
      pushWinterText(vm, "There appears to be no documents with the name of '" + query + "'");
      $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
      vm.openDialogQuery = true;
      return;
    }
  
    pushWinterText(vm, "Got it sir, please type the text you want inserted");


    //Typical way to take in user text
    next = false;
    var forward = await waitUserInput(vm);
    if(!forward){
        pushWinterText(vm, "Got it boss. Pausing intent");
        return null;
    }

    //wait for user to input something
    pushWinterText(vm, "I'll search for documents with  '" + query + "'");
    pushWinterText(vm, "Choose a document you'd like me to insert text into please. ");
    pushSelectChatbox(vm, response);

    vm.chatbox_clicked_response = "prompting...";
    // vm.stored_followup_function = "insert_text_google_doc_component";

    //await
    waitingSelectInput = false; // reset var
    forward = await waitUserInputSelect(vm);
    if(!forward){
        pushWinterText(vm, "Got it boss. Pausing intent");
        return null;
    }


      var method_name = vm.stored_followup_function;
      var text_to_add = vm.stored_input_text;
      console.log(vm.messages);

      try {
        await call_google_api_functions("insertTextDoc", vm.stored_input_text,  vm.chatbox_clicked_response.id);
        pushWinterText(vm, "I've inserted the text as you wanted sir. ")
        // await window[method_name](vm, text_to_add , vm.chatbox_clicked_response.id); //figure out a way to dynamically add the arguments
        $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
        

      //   pushUpScroll()
      } catch(err) {
        alert(err); // TypeError: failed to fetch
      }

      vm.openDialogQuery = true;
    });
}


async function create_google_doc(vm, params){
  //You have to make sure to close dialogflow querying.
  vm.openDialogQuery = false;
  var doc_name = params.fields.doc_name.stringValue;

  try {
      responseFinal = await call_google_api_functions("createBlankDoc", doc_name);
      pushWinterText(vm, "created google doc. Dope");
      // pushSelectChatbox(vm, calResponse);
      $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
    } catch(err) {
      alert(err); // TypeError: failed to fetch
    }
    //Opening dialogflow querying
    vm.openDialogQuery = true;
}