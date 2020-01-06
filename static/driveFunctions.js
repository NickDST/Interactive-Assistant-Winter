function search_drive_file(vm, params){
    //You have to make sure to close dialogflow querying.
    vm.openDialogQuery = false;
    //Extracting the variables from dialogflow
    var query = params.fields.query.stringValue;

    //querying and checking if there is a response
    call_google_api_functions("searchFileName", query).then(async (response) => {
    vm.select_modal_response = "response";
    if(!(response === undefined || response.length == 0)){
      pushWinterText(vm, "Here are the documents from your google drive that I could find for '" + query + "'");
      pushSelectChatbox(vm, response);
      $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);

    } else {
      pushWinterText(vm, "There appears to be no documents with the name of '" + query + "'");
      $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
      vm.openDialogQuery = true;
      return;
    }
      //Opening dialogflow querying
      vm.openDialogQuery = true;
    });
}




function search_file_by_permissions(vm, params){
    //You have to make sure to close dialogflow querying.
    vm.openDialogQuery = false;
    //Extracting the variables from dialogflow
    var query = params.fields.query.stringValue;
    //querying and checking if there is a response
    call_google_api_functions("searchFilePermissions", query).then(async (response) => {
    vm.select_modal_response = "response";
    if(!(response === undefined || response.length == 0)){
      pushWinterText(vm, "Here are the files that '" + query + "' has access to.");
      pushSelectChatbox(vm, response);
      $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
    } else {
      pushWinterText(vm, "There appears to be no documents that '" + query + "' has access to.");
      $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
      vm.openDialogQuery = true;
      return;
    }
      //Opening dialogflow querying
      vm.openDialogQuery = true;
    });
}



function create_folder(vm, params){
    //You have to make sure to close dialogflow querying.
    vm.openDialogQuery = false;
    //Extracting the variables from dialogflow
    var folder_name = params.fields.folder_name.stringValue;
    //querying and checking if there is a response
    call_google_api_functions("createFolder", folder_name).then(async (response) => {
    vm.select_modal_response = "response";
    if(!(response === undefined || response.length == 0)){
      pushWinterText(vm, "The folder '" + folder_name + "' has been created");
    //   pushSelectChatbox(vm, response);
      $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
    } else {
      pushWinterText(vm, "Failed to create a folder with the name " + folder_name);
      $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
      vm.openDialogQuery = true;
      return;
    }
      //Opening dialogflow querying
      vm.openDialogQuery = true;
    });
}



async function move_file(vm, params){
    //You have to make sure to close dialogflow querying.
    vm.openDialogQuery = false;

    //Extracting the variables from dialogflow
    var query = params.fields.query.stringValue;
    var parent_folder = params.fields.parent_folder.stringValue;

    //querying and checking if there is a response
    var response = await call_google_api_functions("searchFileName", query);
    if(!(checkResponse(vm, response, "There appears to be no documents with the name of '" + query + "'"))){return}
    vm.select_modal_response = "response";


    pushWinterText(vm, "I'll search for documents with  '" + query + "'");

    //let user select
    var movingFileRaw = await waitUserSelect(vm, response, "Choose a document you'd like me to move. ");
    movingFile = movingFileRaw.id;


    //searching for parent folder
    var response2 = await call_google_api_functions("searchFileFolder", parent_folder);
    if(!(checkResponse(vm, response2, "There appears to be no folder with the name of '" + parent_folder + "'"))){return}


    //letting user select
    var chosen_parent_folderRaw = await waitUserSelect(vm, response2, "Choose the parent folder.");
    chosen_parent_folder = chosen_parent_folderRaw.id;


    try {
        await call_google_api_functions("moveFilesBetweenFolders", movingFile, chosen_parent_folder);
        pushWinterText(vm, "The file " + movingFileRaw + " has been moved to " + chosen_parent_folderRaw);
        $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);

      } catch(err) {
        alert(err); // TypeError: failed to fetch
      }

      //Opening dialogflow querying
      vm.openDialogQuery = true;
}



function upload_file(vm) {
    pushWinterText(vm, "Here you go!");
    vm.messages.push({
        name: "Winter",
        message: "upload",
        message_type: "upload",
        message_box: "",
      });

    pushWinterText(vm, "The page will reload after it successfully uploads btw.");
}







// function search_drive_file(vm, params){

//     //You have to make sure to close dialogflow querying.
//     vm.openDialogQuery = false;

    
//     //Extracting the variables from dialogflow
//     var query = params.fields.googleDocName.stringValue;

//     //querying and checking if there is a response
//     call_google_api_functions("searchFileName", query).then(async (response) => {
//     vm.select_modal_response = "response";
//     if(!(response === undefined || response.length == 0)){
//       pushSelectChatbox(vm, response);
//     } else {
//       pushWinterText(vm, "There appears to be no documents with the name of '" + query + "'");
//       $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
//       vm.openDialogQuery = true;
//       return;
//     }
    

//     //Typical way to take in user text
//     pushWinterText(vm, "Got it sir, please type the text you want inserted");
//     next = false;
//     var forward = await waitUserInput(vm);
//     if(!forward){
//         pushWinterText(vm, "Got it boss. Pausing intent");
//         return null;
//     }

//     //Waiting for input
//     pushWinterText(vm, "I'll search for documents with  '" + query + "'");
//     pushWinterText(vm, "Choose a document you'd like me to insert text into please. ");
//     vm.chatbox_clicked_response = "prompting...";
//     waitingSelectInput = false; // reset var
//     forward = await waitUserInputSelect(vm);
//     if(!forward){
//         pushWinterText(vm, "Got it boss. Pausing intent");
//         return null;
//     }

//       try {
//         await call_google_api_functions("insertTextDoc", text, document_id);
//         pushWinterText(vm, "I've inserted the text as you wanted sir. ")
//         $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
//       } catch(err) {
//         alert(err); // TypeError: failed to fetch
//       }

//       //Opening dialogflow querying
//       vm.openDialogQuery = true;
//     });
    
// }