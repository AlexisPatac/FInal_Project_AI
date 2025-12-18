// Chat bubble and panel toggle functionality
document.addEventListener('DOMContentLoaded', function() {
  const chatBubble = document.getElementById('chatBubble');
  const floatingChatPanel = document.getElementById('floatingChatPanel');
  const closeChat = document.getElementById('closeChat');
  const chatForm = document.getElementById('chatForm');
  const chatInput = document.getElementById('chatInput');
  const chatWindow = document.getElementById('chatWindow');

  // Toggle chat panel when bubble is clicked
  chatBubble.addEventListener('click', function() {
    floatingChatPanel.classList.toggle('active');
    if (floatingChatPanel.classList.contains('active')) {
      chatInput.focus();
    }
  });

  // Close chat panel when close button is clicked
  closeChat.addEventListener('click', function() {
    floatingChatPanel.classList.remove('active');
  });

  // Close chat panel when clicking outside of it
  document.addEventListener('click', function(event) {
    if (
      floatingChatPanel.classList.contains('active') &&
      !floatingChatPanel.contains(event.target) &&
      !chatBubble.contains(event.target)
    ) {
      floatingChatPanel.classList.remove('active');
    }
  });

  // Handle chat form submission
  chatForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const question = chatInput.value.trim();
    if (!question) return;

    // Add user message to chat
    addMessageToChat(question, 'user');
    chatInput.value = '';
    
    // Show loading indicator
    const loadingId = addLoadingMessage();

    try {
      // Send request to backend
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question }),
      });

      const data = await response.json();

      // Remove loading indicator
      removeLoadingMessage(loadingId);

      if (response.ok && data.answer) {
        // Add bot response to chat
        addMessageToChat(data.answer, 'bot');
      } else {
        // Show error message
        addMessageToChat(
          data.error || 'Sorry, there was an error processing your question.',
          'bot'
        );
      }
    } catch (error) {
      // Remove loading indicator
      removeLoadingMessage(loadingId);
      
      // Show error message
      addMessageToChat(
        'Sorry, there was an error connecting to the server. Please try again.',
        'bot'
      );
      console.error('Chat error:', error);
    }

    // Scroll to bottom
    scrollToBottom();
  });

  // Add message to chat window
  function addMessageToChat(text, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'bubble';
    bubbleDiv.textContent = text;
    
    messageDiv.appendChild(bubbleDiv);
    chatWindow.appendChild(messageDiv);
    
    scrollToBottom();
  }

  // Add loading message
  function addLoadingMessage() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot';
    messageDiv.id = 'loading-message';
    
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'bubble';
    bubbleDiv.innerHTML = '<span class="loading-dots">Thinking</span>';
    
    messageDiv.appendChild(bubbleDiv);
    chatWindow.appendChild(messageDiv);
    
    scrollToBottom();
    return 'loading-message';
  }

  // Remove loading message
  function removeLoadingMessage(id) {
    const loadingMsg = document.getElementById(id);
    if (loadingMsg) {
      loadingMsg.remove();
    }
  }

  // Scroll chat window to bottom
  function scrollToBottom() {
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  // Set current year in footer
  const yearElement = document.getElementById('year');
  if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
  }
});

