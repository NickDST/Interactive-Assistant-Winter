
async function upcoming_calendar_events(vm, params){
    //You have to make sure to close dialogflow querying.
    vm.openDialogQuery = false;
    //Extracting the variables from dialogflow
    var number = params.fields.number.numberValue;
    //querying and checking if there is a response
    var response = await call_google_api_functions("calendarsList");
    if(!(checkResponse(vm, response, "No Calendars found"))){return}
    vm.select_modal_response = "response";
    console.log(response);

    //let user select
    var calendar = await waitUserSelect(vm, response, "Choose a calendar you'd like me to use. ");
    console.log(calendar.summary);

    try {
        calResponse = await call_google_api_functions("calendarUpcoming", number, calendar.ID);
        pushWinterText(vm, "Loaded the events");
        pushSelectChatbox(vm, calResponse);
        $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
      } catch(err) {
        alert(err); // TypeError: failed to fetch
      }
      //Opening dialogflow querying
      vm.openDialogQuery = true;
}


async function list_calendars(vm, params){
    //You have to make sure to close dialogflow querying.
    vm.openDialogQuery = false;
    try {
        calResponse = await call_google_api_functions("calendarsList");
        pushWinterText(vm, "Loaded the calendars");
        pushSelectChatbox(vm, calResponse);
        $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);

      } catch(err) {
        alert(err); // TypeError: failed to fetch
      }
      //Opening dialogflow querying
      vm.openDialogQuery = true;
}


async function list_events_by_day(vm, params){
    // Gonna use default primary calendar
    vm.openDialogQuery = false;
    //Extracting the variables from dialogflow
    var date = params.fields.date.stringValue;
    try {
        calResponse = await call_google_api_functions("calendarListEventsDay", date);
        pushWinterText(vm, "Loaded the events for that day");
        pushSelectChatbox(vm, calResponse);
        $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);

      } catch(err) {
        alert(err); // TypeError: failed to fetch
      }

      //Opening dialogflow querying
      vm.openDialogQuery = true;
}



async function list_events_by_time(vm, params){
    // Gonna use default primary calendar
    vm.openDialogQuery = false;
    //Extracting the variables from dialogflow
    var start_date = params.fields.start_date.stringValue;
    var end_date = params.fields.end_date.stringValue;
    try {
        calResponse = await call_google_api_functions("calendarListEventsWithinTime", start_date, end_date);
        pushWinterText(vm, "Loaded the events for that timeframe");
        pushSelectChatbox(vm, calResponse);
        $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);

      } catch(err) {
        alert(err); // TypeError: failed to fetch
      }
      //Opening dialogflow querying
      vm.openDialogQuery = true;
}



async function schedule_event(vm, params){
    // Gonna use default primary calendar
    vm.openDialogQuery = false;
    //Extracting the variables from dialogflow
    var scheduling = params.data.queryText;

    var parsedSchedule = scheduling.replace('schedule',''); //This needs to be changed later

    try {
        calResponse = await call_google_api_functions("calendarQuickAdd", parsedSchedule);
        pushWinterText(vm, "Scheduled");
        $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
      } catch(err) {
        alert(err); // TypeError: failed to fetch
      }
      //Opening dialogflow querying
      vm.openDialogQuery = true;
}



async function delete_event(vm, params){
    // Gonna use default primary calendar
    vm.openDialogQuery = false;
    //Extracting the variables from dialogflow
    var event_name = params.fields.event_name.stringValue;

    //querying and checking if there is a response
    var response = await call_google_api_functions("calendarSearchEventByName", event_name);
    if(!(checkResponse(vm, response, "There appears to be no events with the name of '" + event_name + "'"))){return}

    //let user select
    var calendar_choice_Raw = await waitUserSelect(vm, response, "Choose a event you'd like me to remove. ");
    calendar_choice = calendar_choice_Raw.id;

    try {
        calResponse = await call_google_api_functions("calendarDelete", calendar_choice);
        pushWinterText(vm, "Removed!");
        $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
      } catch(err) {
        alert(err); // TypeError: failed to fetch
      }
      //Opening dialogflow querying
      vm.openDialogQuery = true;
}



async function add_reminder_event(vm, params){
    // Gonna use default primary calendar
    vm.openDialogQuery = false;

    //Extracting the variables from dialogflow
    var event_name = params.fields.event_name.stringValue;

    //querying and checking if there is a response
    var response = await call_google_api_functions("calendarSearchEventByName", event_name);
    if(!(checkResponse(vm, response, "There appears to be no events with the name of '" + event_name + "'"))){return}

    //let user select
    var calendar_choice_Raw = await waitUserSelect(vm, response, "Choose a event you'd like me to add a reminder to. ");
    event_id = calendar_choice_Raw.id;

    try {
        calResponse = await call_google_api_functions("calendarEmailPopUpReminders", event_id);
        pushWinterText(vm, "Reminder added");
        $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);
      } catch(err) {
        alert(err); // TypeError: failed to fetch
      }
      //Opening dialogflow querying
      vm.openDialogQuery = true;
}

