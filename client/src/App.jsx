import { useState, useEffect, useRef } from "react";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef(null);

  // Auto-scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth"
    });
  }, [messages, loading]);


  const sendMessage = async (customMessage = null) => {

    const userMessage = (customMessage ?? message).trim();

    if (!userMessage || loading) return;


    // Save the current conversation BEFORE adding the new message
    const conversationHistory = messages.map((msg) => ({
      role: msg.sender === "user"
        ? "user"
        : "assistant",

      content: msg.text
    }));


    // Add user's message to UI
    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: userMessage
      }
    ]);

    setMessage("");
    setLoading(true);


    const controller = new AbortController();

    const timeout = setTimeout(() => {
      controller.abort();
    }, 120000);


    try {

      const response = await fetch(
        "http://localhost:5000/api/chat",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            message: userMessage,

            conversation: conversationHistory
          }),

          signal: controller.signal
        }
      );


      clearTimeout(timeout);


      if (!response.ok) {
        throw new Error(
          `Server returned status ${response.status}`
        );
      }


      const data = await response.json();


      // Add AI response
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text:
            data.reply ||
            "I couldn't generate a response."
        }
      ]);


    } catch (error) {

      clearTimeout(timeout);

      console.error(
        "Chat error:",
        error
      );


      let errorMessage =
        "Sorry, I couldn't connect to the server.";


      if (error.name === "AbortError") {

        errorMessage =
          "The AI is taking too long to respond. Please try a shorter question.";

      }


      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: errorMessage
        }
      ]);


    } finally {

      setLoading(false);

    }

  };


  // Start new conversation
  const newChat = () => {

    setMessages([]);
    setMessage("");
    setLoading(false);

  };


  return (
    <div className="app">


      {/* SIDEBAR */}

      <aside className="sidebar">

        <div className="brand">

          <div className="brand-icon">
            ✦
          </div>

          <span>
            Neura
          </span>

        </div>


        <button
          className="new-chat"
          onClick={newChat}
        >

          <span>
            ＋
          </span>

          New chat

        </button>


        <div className="sidebar-section">

          <p>
            RECENT
          </p>


          {messages.length > 0 && (

            <div className="history-item">

              <span>
                ◌
              </span>

              Current conversation

            </div>

          )}

        </div>


        <div className="sidebar-bottom">


          <div className="sidebar-item">

            <span>
              ⚙
            </span>

            Settings

          </div>


          <div className="sidebar-item">

            <span>
              ?
            </span>

            Help

          </div>


          <div className="profile">

            <div className="avatar">
              T
            </div>


            <div>

              <strong>
                User
              </strong>

              <small>
                Local AI
              </small>

            </div>

          </div>


        </div>

      </aside>



      {/* MAIN */}

      <main className="main">


        {/* TOPBAR */}

        <header className="topbar">

          <div>

            <h2>
              Neura
            </h2>


            <span className="status">

              <i></i>

              Online

            </span>

          </div>


          <button className="menu-button">

            •••

          </button>

        </header>



        {/* CHAT AREA */}

        <section className="chat-area">


          {messages.length === 0 ? (


            /* WELCOME */

            <div className="welcome">


              <div className="hero-icon">
                ✦
              </div>


              <h1>

                How can I help

                <span>
                  {" "}you today?
                </span>

              </h1>


              <p>

                Ask me anything. I'm your personal AI assistant.

              </p>


              <div className="suggestions">


                <button
                  onClick={() =>
                    sendMessage("Hello")
                  }
                  disabled={loading}
                >

                  <span>
                    👋
                  </span>

                  Say hello

                </button>


                <button
                  onClick={() =>
                    sendMessage(
                      "Help me with JavaScript"
                    )
                  }
                  disabled={loading}
                >

                  <span>
                    💻
                  </span>

                  Learn JavaScript

                </button>


                <button
                  onClick={() =>
                    sendMessage(
                      "Give me a workout"
                    )
                  }
                  disabled={loading}
                >

                  <span>
                    🏋️
                  </span>

                  Fitness advice

                </button>


                <button
                  onClick={() =>
                    sendMessage(
                      "I have an exam tomorrow"
                    )
                  }
                  disabled={loading}
                >

                  <span>
                    📚
                  </span>

                  Study help

                </button>


              </div>


            </div>


          ) : (


            /* MESSAGES */

            <div className="messages">


              {messages.map((msg, index) => (


                <div
                  key={index}
                  className={`message-row ${msg.sender}`}
                >


                  {msg.sender === "bot" && (

                    <div className="bot-avatar">
                      ✦
                    </div>

                  )}


                  <div className="message-content">


                    <div className="message-name">

                      {msg.sender === "user"
                        ? "You"
                        : "Neura"}

                    </div>


                    <div className="message-text">

                      {msg.text}

                    </div>


                  </div>


                </div>


              ))}


              {/* TYPING INDICATOR */}

              {loading && (

                <div className="message-row bot">


                  <div className="bot-avatar">
                    ✦
                  </div>


                  <div className="message-content">


                    <div className="message-name">
                      Neura
                    </div>


                    <div className="typing">

                      <span></span>
                      <span></span>
                      <span></span>

                    </div>


                  </div>


                </div>

              )}


              <div ref={messagesEndRef} />

            </div>

          )}

        </section>



        {/* INPUT */}

        <div className="input-wrapper">


          <div className="input-box">


            <button
              className="attach"
              type="button"
            >

              ＋

            </button>


            <input
              type="text"
              placeholder="Message Neura..."
              value={message}
              disabled={loading}

              onChange={(e) =>
                setMessage(e.target.value)
              }

              onKeyDown={(e) => {

                if (
                  e.key === "Enter" &&
                  !e.shiftKey
                ) {

                  e.preventDefault();

                  sendMessage();

                }

              }}

            />


            <button
              className="send"
              onClick={() => sendMessage()}

              disabled={
                loading ||
                !message.trim()
              }

              type="button"
            >

              ↑

            </button>


          </div>


          <p className="disclaimer">

            Neura can make mistakes. Check important
            information.

          </p>


        </div>


      </main>

    </div>
  );
}


export default App;