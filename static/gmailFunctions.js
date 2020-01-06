user_email = 'me';


async function list_labels(vm, params){
    //You have to make sure to close dialogflow querying.
    vm.openDialogQuery = false;
    try {
        calResponse = await call_google_api_functions("callLabels");
        pushWinterText(vm, "Loading the gmail labels");
        pushSelectChatbox(vm, calResponse);
        $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
      } catch(err) {
        alert(err); // TypeError: failed to fetch
      }
      //Opening dialogflow querying
      vm.openDialogQuery = true;
}



async function create_draft(vm, params){
    //You have to make sure to close dialogflow querying.
    vm.openDialogQuery = false;
    var to = params.fields.email.stringValue;
    var sender = user_email;

    // let user select
    var draft_text = await waitUserText(vm, "Enter in the text you want to store into a draft.");

    // ahsdjlf
    var subject = await waitUserText(vm, "Enter in the subject.");

// create_save_draft(self, sender, to, subject, message_text):
    try {
        responseFinal = await call_google_api_functions("create_save_draft", sender, to, subject, draft_text);
        pushWinterText(vm, "Draft Prepped");
        // pushSelectChatbox(vm, calResponse);
        $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
      } catch(err) {
        alert(err); // TypeError: failed to fetch
      }
      //Opening dialogflow querying
      vm.openDialogQuery = true;
}




async function send_gmail(vm, params){
    //You have to make sure to close dialogflow querying.
    vm.openDialogQuery = false;
    var to = params.fields.email.stringValue;
    var sender = user_email;
    // let user select
    var draft_text = await waitUserText(vm, "Enter in the text you want to send...");
    // ahsdjlf
    var subject = await waitUserText(vm, "Enter in the subject.");

    try {
        responseFinal = await call_google_api_functions("create_send_message", sender, to, subject, draft_text);
        pushWinterText(vm, "Email Sent");
        // pushSelectChatbox(vm, calResponse);
        $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
      } catch(err) {
        alert(err); // TypeError: failed to fetch
      }
      //Opening dialogflow querying
      vm.openDialogQuery = true;
}


async function list_gmail_query(vm, params){
    //You have to make sure to close dialogflow querying.
    var query = params.fields.query.stringValue;

    vm.openDialogQuery = false;

    try {
        calResponse = await call_google_api_functions("ListMessagesMatchingQueryMore", query);
        pushWinterText(vm, "Messages that have " + query);
        pushSelectChatbox(vm, calResponse);
        console.log(calResponse);
        $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
      } catch(err) {
        alert(err); // TypeError: failed to fetch
      }
      //Opening dialogflow querying
      vm.openDialogQuery = true;

}

