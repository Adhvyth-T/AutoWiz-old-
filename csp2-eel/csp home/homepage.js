  // Function to add a new message box with the message you send
  function loadingMessage(){
    const chatContainer = document.getElementById('chat_container');
    const LoadMsgBox = document.createElement('div');
    LoadMsgBox.classList.add('incoming_msg');
    LoadMsgBox.innerHTML=`
  <div class="incoming_msg_img"> <img src="robotics.png" alt="AIST"> </div>
  <div class="received_msg">
    <div id="loadingDiv">
      <div class="loader"></div>
      <p>Loading...</p>
  </div>
  </div>
  `
  chatContainer.appendChild(LoadMsgBox);
  }
  function fetchData(message) {
      try {
          const response =eel.chatjs(message);
          return response;
      } catch (error) {
          console.error('Error fetching data:', error);
      }
  }
  async function sendreq(message){
    const resp=await eel.chatjs(message)();
    if (resp){let p=document.getElementById("loadingDiv").parentNode;
    p.innerHTML="";
    p.innerHTML=`
    
        <div class="received_withd_msg">
        <p>${resp}</p>
        </div>
  `
  var aiMsg={};
  aiMsg.text=resp;
  outgoingMessages.push(aiMsg);
let aimes=document.querySelectorAll('.incoming_msg');
if (aimes.length>=3){
  parseMessages();
}

}
  }
  
  function addSentMessage() {
    const m=document.getElementById('messageinput');
    const messageBoxes = document.querySelectorAll('.outgoing_msg');
    
    let message=m.value;
    if (message==""){
      return
    }
    m.value="";
    if (messageBoxes.length>=3){
      alert("limit reached, start new chat")
      return
    }
    const chatContainer = document.getElementById('chat_container');
    const sentMsgBox = document.createElement('div');
    sentMsgBox.classList.add('outgoing_msg');
  
    // Message structure
    sentMsgBox.innerHTML = `
      <div class="sent_msg">
        <p>${message}</p>
      </div>
    `;
  sentMsg={};
  sentMsg.text=message;
  incomingMessages.push(sentMsg);
    // Append new message box to the chat container
    chatContainer.appendChild(sentMsgBox);
    loadingMessage();
    sendreq(message);
  }
  
// Define the event listener

var incomingMessages = [];
var outgoingMessages = [];
// Function to parse messages
function parseMessages() {

  if (incomingMessages.length==0 || outgoingMessages.length==0){
    return
  }
  // Print the JSON lists to console (for demonstration)
  console.log("Incoming Messages:", incomingMessages);
  console.log("Outgoing Messages:", outgoingMessages);
  let date= new Date();
  const arr=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  let DATE=arr[date.getMonth()]+" "+date.getDate();

  // Here, you can perform further actions like sending these lists to a server or storing them locally.
  eel.handle_messages(DATE,JSON.stringify(incomingMessages), JSON.stringify(outgoingMessages));
}


  // Function to clear the chat container
  function clearChatContainer() {
    const chatContainer = document.getElementById('chat_container');
    // Remove all child elements from the chat container
    while (chatContainer.firstChild) {
      chatContainer.removeChild(chatContainer.firstChild);
    }
    let aimes=document.querySelectorAll('.incoming_msg');
    if (aimes.length<3){
      parseMessages();
    }
  }
  function NewChat(){
    clearChatContainer()
  const chatcont= document.getElementById("chat-history-box");
  const newchat=document.createElement('div');
  let k = document.querySelectorAll('.active_chat');
  
  for (let i = 0; i < k.length; i++) {
    k[i].classList.remove('active_chat');
  }
  
  newchat.classList.add('chat_list');
  newchat.classList.add('active_chat');
  newchat.setAttribute('id', ChatID.ID());
  let cname="new chat";
  let date= new Date();
  const arr=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  let DATE=arr[date.getMonth()]+" "+date.getDate();
  
  newchat.innerHTML=`
  <div class="chat_people">
  <div class="chat_ib">
  <h5><span class="chat_date">${DATE}</span></h5>
  <p>${cname}</p>
  </div>
  </div>
  
  `;
  chatcont.insertBefore(newchat,chatcont.firstChild);
  }
  class ChatID {
    static identity = 0;
    
    static ID() {
        return String(ChatID.identity++);
    }
   
}

 

  