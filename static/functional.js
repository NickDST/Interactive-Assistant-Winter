function testerFunction(param){
    console.log(param);
}


// this is an async timeout util (very useful indeed)
const timeout = async ms => new Promise(res => setTimeout(res, ms));


let next = false; // this is to be changed on user input
async function waitUserInput(vm) {
    while (next === false) await timeout(50); // pause script but avoid browser to freeze ;)
    next = false; // reset var
    console.log('user input detected');
    if(vm.stored_input_text == 'break'){
        pushWinterText(vm, "breakingg")
        return false;
    } else {
        return true
    }
}


let waitingSelectInput = false;
async function waitUserInputSelect(vm) {
    while (waitingSelectInput === false) await timeout(50); // pause script but avoid browser to freeze ;)
    waitingSelectInput = false; // reset var
    next = false;
    console.log('user input detected');
    if(vm.stored_input_text == 'break'){
        pushWinterText(vm, "breakingg Select")
        vm.openDialogQuery = true;
        return false;
    } else {
        return true;
    }
}


async function call_google_api_functions(functionName, value1=null, value2=null,value3=null,value4=null) {
    const path = '/callFunction';
    var res = await axios({
        method: 'get',
        url: path,
        params: {
            function: functionName,
            value1: value1,
            value2: value2,
            value3: value3,
            value4: value4,
          }
    })
    return res.data;
}

//this is a component query
async function search_drive_file(query){
    var response = await call_google_api_functions("searchFileName", query);
    return response;
}

async function insert_text_google_doc_component(vm, text, document_id){
    var response = await call_google_api_functions("insertTextDoc", text, document_id);
    pushWinterText(vm, "I've inserted the text as you wanted sir. ")
    return response;
}


function pushSelectChatbox(vm, response){
    vm.select_modal_response = "response";
    something_cachedValue = vm.chatbox_clicked_response;
    console.log("response " + response);
    vm.messages.push({
      name: "Winter",
      message: "Textbox",
      message_type: "thing",
      message_box: response,
    });
}

function pushWinterText(vm, text){
    vm.messages.push({
        name: "Winter",
        message: text,
        message_type: "",
        message_box: "",
      });
}


function testOutside(){
    const path = '/functionList';
    axios({
        method: 'get',
        url: path
    })
    .then((res) => {
        console.log(res.data);
    })
    .catch((error) => {
        //eslint-disable-next-line

        console.log(error)
    });
}



async function dialogFlow_query(query){
    const path = 'https://us-central1-winterbetav2-mergev1-nskpwt.cloudfunctions.net/dialogflowGateway';
    response = await axios({
        method: 'post',
        url: path,
        data: {
            "sessionId": "foo",
            "queryInput": {
                "text": {
                    "text": query,
                    "languageCode": "en-US"
                }
            }
        },
        headers: {'Access-Control-Allow-Origin': '*', 'Accept': '*/*', 'Content-type': 'application/json', 'Cache-Control': 'no-cache'}
    });
    return response;
}




//    var movingFileRaw = await waitUserSelect(vm, response, "Choose a document you'd like me to move. ");
async function waitUserSelect(vm, response, text){
    pushWinterText(vm, text);
    pushSelectChatbox(vm, response);
    vm.chatbox_clicked_response = "prompting...";
    waitingSelectInput = false; // reset var
    forward = await waitUserInputSelect(vm);
    if(!forward){
        pushWinterText(vm, "Got it boss. Pausing intent");
        vm.openDialogQuery = true;
        return null;
    }
    return vm.chatbox_clicked_response;
}


//    var movingFileRaw = await waitUserText(vm, response, "Choose a document you'd like me to move. ");
async function waitUserText(vm, text){
    next = false;
    pushWinterText(vm, text);
    waitingSelectInput = false; // reset var
    forward = await waitUserInput(vm);
    if(!forward){
        pushWinterText(vm, "Got it boss. Pausing intent");
        vm.openDialogQuery = true;
        return null;
    }
    return vm.stored_input_text;
}



// if(!(checkResponse(vm, response2, "There appears to be no folder with the name of '" + parent_folder + "'"))){return}
function checkResponse(vm, response, text){
    if(response === undefined || response.length == 0){
        pushWinterText(vm, text);
        $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
        vm.openDialogQuery = true;
        return false;
    } else {
        return true;
    }
}


