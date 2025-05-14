function clearchatcont() {
    const chatContainer = document.getElementById('chat_container');
    // Remove all child elements from the chat container
    while (chatContainer.firstChild) {
      chatContainer.removeChild(chatContainer.firstChild);
    }
  }
  eel.expose(ChathistInsert);
  function ChathistInsert(chatName,chatDate){
    clearchatcont()
  const chatcont= document.getElementById("chat-history-box");
  const newchat=document.createElement('div');
  let k = document.querySelectorAll('.active_chat');
  
  for (let i = 0; i < k.length; i++) {
    k[i].classList.remove('active_chat');
  }
  
  newchat.classList.add('chat_list');
  newchat.classList.add('active_chat');
  newchat.setAttribute('id', ChatID.ID());
  let cname=chatName;
 
  let DATE=chatDate;
  
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
  var userChats = [];
  var aiChats = [];

  async function fetchChatData() {
      // Call the Python function to fetch chat data using Eel
      const chatDataJson = await eel.fetch_chat_rows()();

      // Parse the JSON data
      const chatData = JSON.parse(chatDataJson);

      // Extract user and AI chats from the fetched data
      chatData.forEach(chat => {
          userChats.push(chat.user_chat);
          aiChats.push(chat.ai_chat);
      });

      // You can access userChats and aiChats lists anywhere in your JavaScript code
      console.log("User Chats:", userChats);
      console.log("AI Chats:", aiChats);


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////


// Add click event listener to each chat list item
var cItems = document.querySelectorAll('.chat_list');

cItems.forEach(item => {
    item.addEventListener('click', function() {
        // Retrieve the id attribute of the clicked element
        clearchatcont()
        var clickedItemId = item.id;
        
        // Parse the ID as an integer
        var index = parseInt(clickedItemId);

        // Check if index is within the bounds of the lists
        if (index >= 0 && index < userChats.length && index < aiChats.length) {
            // Access user and AI chats at the specified position
            var userChat = userChats[index];
            var aiChat = aiChats[index];

            // Log userChat and aiChat to verify their types and contents
         
            // Check if userChat and aiChat are arrays
           // Check if userChat and aiChat are arrays
if (Array.isArray(userChat) && Array.isArray(aiChat)) {
    // Iterate through userChat and aiChat lists
    const maxLength = Math.max(userChat.length, aiChat.length);

    // Iterate over both arrays simultaneously
    for (let i = 0; i < maxLength; i++) {
        // Add user message if available
        if (userChat[i]) {
            addUserMsg(userChat[i].text); // Add user message to UI
        }

        // Add AI message if available
        if (aiChat[i]) {
            AddAImsg(aiChat[i].text); // Add AI message to UI
        }
    }
} else {
    // Handle the case where userChat or aiChat is not an array
    console.log("User Chat or AI Chat is not an array.");

    // Check if userChat and aiChat are JSON objects
    if (typeof userChat === 'object' && typeof aiChat === 'object') {
        // Log userChat and aiChat text directly
        addUserMsg(userChat.text); // Add user message to UI
        AddAImsg(aiChat.text); // Add AI message to UI
    } else {
        // Handle the case where userChat or aiChat is neither an array nor a JSON object
        console.log("User Chat or AI Chat is not an array or JSON object.");
    }
}

        } else {
            console.log("Invalid position ID.");
        }
    });
});
NewChat();
var chatItems = document.querySelectorAll('.chat_list');
chatItems.forEach(item => {
  if (item.hasAttribute('id')) {

  item.addEventListener('click', function() {
    document.getElementById('messageinput').disabled=true;
  })}})
  document.getElementsByClassName('active_chat')[0].addEventListener('click',function(){
    document.getElementById('messageinput').disabled=false;
    clearchatcont();
  })
  }
  function AddAImsg(msg){
    const chatContainer = document.getElementById('chat_container');
    const LoadMsgBox = document.createElement('div');
    LoadMsgBox.classList.add('incoming_msg');
    LoadMsgBox.innerHTML=`
  <div class="incoming_msg_img"> <img src="robotics.png" alt="AIST"> </div>
  <div class="received_msg">
  <div class="received_withd_msg">
        <p>${msg}</p>
        </div>
  </div>
  `
  chatContainer.appendChild(LoadMsgBox);
  }
  function addUserMsg(message) {
    const messageBoxes = document.querySelectorAll('.outgoing_msg');
    
   
    const chatContainer = document.getElementById('chat_container');
    const sentMsgBox = document.createElement('div');
    sentMsgBox.classList.add('outgoing_msg');
  
    // Message structure
    sentMsgBox.innerHTML = `
      <div class="sent_msg">
        <p>${message}</p>
      </div>
    `;
    chatContainer.appendChild(sentMsgBox);
}


  document.addEventListener('DOMContentLoaded',eel.getChathist());
  document.addEventListener('DOMContentLoaded',fetchChatData());
