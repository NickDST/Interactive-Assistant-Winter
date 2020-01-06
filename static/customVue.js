
document.addEventListener('DOMContentLoaded', function () {
  window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  const recognition = new SpeechRecognition();
  
  recognition.interimResults = true;
  
  // let p = document.createElement('p');
  
  // const words = document.querySelector('.words');
  // words.appendChild(p);


    new Vue({
      el: '#app',
      delimiters: ['[[', ']]'],
      mounted: function () {
        this.getFunctionList()
        console.log('mounted: got here')
      },
      // define data - initial display text
      data: {
        m1: "You got to let me know",
        message: "Proj. Winter",
        msg: "Empty",
        functionList: {},

        sidebarState: "",
        modalState: "",
        modal_values: [],
        function_response_values: [],
        select_modal_response: [],
        number_Modals: 0,

        chatbox_clicked_response: [],
        stored_followup_function: "",
        stored_input_text: "",

        loadingMessageWinter: false,
        openDialogQuery:  true,

        toggleQuery: 1,

        upcomingEvents: [],

        toggleVoice: false,


        messages: [{
          name: "Winter",
          message: "hey boss!",
        } ],
        user_message: "",
        user_name: "",
        message_type: "",
        user_speaking: false,

      },
      methods: {

        async getUpcomingEvents(){
          vm = this;
          try {
            upcomingEventsResult = await call_google_api_functions("calendarUpcoming", 5);
            vm.upcomingEvents = upcomingEventsResult;
            console.log(upcomingEventsResult)
          } catch(err) {
            alert(err); // TypeError: failed to fetch
          }

        },

        // **********************************
        getFunctionList() {
          var vm = this;
          const path = '/functionList';
          axios({
              method: 'get',
              url: path
            })
            .then((res) => {
              this.functionList = res.data;
              console.log(res.data);
            })
            .catch((error) => {
              //eslint-disable-next-line

              console.log(error)
            });
          // console.log(this.functionList);
        },
        // **********************************
        async submitMessage() {
          var vm = this;
          vm.messages.push({
            name: "Nick",
            message: vm.user_message,
            message_type: vm.message_type,
            message_box: ""
          });
          query = vm.user_message;
          
          vm.user_message = "";

          
          vm.loadingMessageWinter = true;
          $(".innerChat").stop().animate({ scrollTop: $(".innerChat")[0].scrollHeight}, 1000);

          console.log("dialogflow Listening:" + vm.openDialogQuery);
          if(vm.openDialogQuery){
            var response = await dialogFlow_query(query);

            pushWinterText(vm, response.data.fulfillmentText);

            //here I can add the speaking stuff
            if(vm.toggleVoice == true){
              winterSpeak(vm, response.data.fulfillmentText);
            }
            
  
            var allRequiredParamsPresent = response.data.allRequiredParamsPresent;
            var intent_name = response.data.intent.displayName;

            var params;
            
            console.log(allRequiredParamsPresent);
            console.log(response);

            if(intent_name && allRequiredParamsPresent === true){
              try {

                if(response.data.parameters){
                  params = response.data.parameters;
                }
                //sliding something in, not ideal but eh.
                if(intent_name == "schedule_event" || intent_name == "QueryFallbackIntent"){
                  params = response;
                }

                await window[intent_name](vm, params);
                } catch (err) {
                  console.log(err);
                }
            }
            
          }

          vm.loadingMessageWinter = false;
          if(next == false){
            vm.stored_input_text = query
            next = true;
          }


        },
        // **********************************
        callFunction() {
          var vm = this;
          const path = '/callFunction';
          axios({
              method: 'get',
              url: path,
              params: {
                function: vm.modalState.name,
                value1: vm.modal_values[0],
                value2: vm.modal_values[1],
                value3: vm.modal_values[2],
                value4: vm.modal_values[3],
              }
            })
            .then((res) => {
              // this.function_response_values.push(res.data);
              this.function_response_values = res.data;
              // console.log(res.data);
              vm.messages.push({
                name: "Winter",
                message: "Textbox",
                message_type: "thing",
                message_box: res.data,
              });
              console.log(this.function_response_values);

            })
            .catch((error) => {
              //eslint-disable-next-line
              console.log(error)
            });
        },

        // **********************************
        async testFunction(){

          var vm = this;
          await insert_text_google_doc(vm);
        },

        // **********************************
        async updatedSelectedModal(value){
          var vm = this;
          // $('#user-input').click(() => next = true) 
          // next = true;
          waitingSelectInput = true;
          if(vm.chatbox_clicked_response == "prompting..."){
            vm.chatbox_clicked_response = value; //insertTextDoc
          }
          
        },
        toggleClick(){
          console.log("Clicked")
          this.toggleQuery += 1
    
          if ((this.toggleQuery % 2) == 0) {
            // do this
              recognition.start();
              console.log('Ready to receive a color command.');
              recognition.addEventListener('end', recognition.start);
              console.log('Checked');
    
        } else {
            // do that
            console.log("resetting...");
            location.reload();
        }
        },    
        listenWinter(){
          vm = this;
        // this.getMessage();
        recognition.addEventListener('result', e => {
      //   console.log(e);
        const transcript = Array.from(e.results)
          .map(result => result[0])
          .map(result => result.transcript)
          .join('')
    
          // p.textContent = transcript;

      if(transcript.includes("dismissed") || transcript.includes("dismiss")){
        vm.user_speaking = false;
        if(e.results[0].isFinal){
          pushWinterText(vm, "Got it boss.");
        }
      }


      if(transcript.includes("break") || transcript.includes("break")){
        vm.toggleClick();
      }


      vm.msg = transcript;
      console.log(transcript);

      if(vm.user_speaking == true){
        vm.user_message = transcript;
      }

      if(e.results[0].isFinal && vm.user_speaking == true){
        vm.submitMessage();
      }




      // transcript.includes("winter")
      if(transcript.includes("winter")){
          console.log("WINTER HAS BEEN SUMMONED");
          vm.msg = "WINTER HAS BEEN SUMMONED";
          vm.user_speaking = true;
      }
    

    
    
    });
    }


      },
      created() {
        this.listenWinter();
        this.getUpcomingEvents();
      }
    })
  })
