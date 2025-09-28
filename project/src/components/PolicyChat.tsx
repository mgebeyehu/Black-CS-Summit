import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Policy, ChatMessage } from '../types';
import { Send, Mic, MicOff, Volume2, MessageSquare, ArrowLeft } from 'lucide-react';
import { apiClient } from '../services/api';

interface PolicyChatProps {
  policy: Policy;
  onBack: () => void;
  onTalkAboutIt: () => void;
  hasEngaged: boolean;
}

const PolicyChat: React.FC<PolicyChatProps> = ({ policy, onBack, onTalkAboutIt, hasEngaged }) => {
  const navigate = useNavigate();
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      text: `Hi! I'm here to help you understand "${policy.title}". Feel free to ask me anything about this policy or use one of the suggested questions below.`,
      isUser: false,
      timestamp: new Date()
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const suggestedQuestions = [
    "How does this policy affect me specifically?",
    "What are my rights under this policy?",
    "What should I do if this policy is violated?",
    "Are there any exceptions to this policy?",
    "How can I get help with this policy?",
    "What are the penalties for not following this policy?"
  ];

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      text: text.trim(),
      isUser: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');

    try {
      // Call the real API
      const chatResponse = await apiClient.chatWithAI({
        user_message: text.trim(),
        use_context: true,
        max_context_docs: 3
      });

      const aiResponse: ChatMessage = {
        id: (Date.now() + 1).toString(),
        text: chatResponse.answer,
        isUser: false,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiResponse]);
    } catch (error) {
      console.error('Chat API error:', error);
      // Fallback response
      const aiResponse: ChatMessage = {
        id: (Date.now() + 1).toString(),
        text: `I apologize, but I'm having trouble connecting to the AI service right now. Based on "${policy.title}", this is an important Chicago policy that affects residents. Please try again in a moment.`,
        isUser: false,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiResponse]);
    }
  };

  const handleSpeechToText = () => {
    if (!('webkitSpeechRecognition' in window)) {
      alert('Speech recognition not supported in this browser');
      return;
    }

    const recognition = new (window as any).webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;

    if (isListening) {
      recognition.stop();
      setIsListening(false);
    } else {
      recognition.start();
      setIsListening(true);

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setInputText(transcript);
        setIsListening(false);
      };

      recognition.onerror = () => {
        setIsListening(false);
      };
    }
  };

  const handleTextToSpeech = (text: string) => {
    if (isSpeaking) {
      speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    speechSynthesis.speak(utterance);
  };

  const handleTalkAboutItClick = () => {
    if (!hasEngaged && messages.length <= 1) {
      alert('Please get your facts straight before joining the discussion! Ask some questions about this policy first.');
      return;
    }
    onTalkAboutIt();
    navigate('/community');
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button
              onClick={onBack}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <ArrowLeft className="h-5 w-5" />
            </button>
            <div>
              <h1 className="text-xl font-semibold text-gray-900">{policy.title}</h1>
              <p className="text-sm text-gray-600">{policy.category}</p>
            </div>
          </div>
          <button
            onClick={handleTalkAboutItClick}
            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors flex items-center space-x-2"
          >
            <MessageSquare className="h-4 w-4" />
            <span>Talk About It!</span>
          </button>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 max-w-4xl mx-auto w-full p-4">
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 h-full flex flex-col">
          <div className="flex-1 p-6 overflow-y-auto">
            <div className="space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                      message.isUser
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-900'
                    }`}
                  >
                    <p>{message.text}</p>
                    {!message.isUser && (
                      <button
                        onClick={() => handleTextToSpeech(message.text)}
                        className="mt-2 p-1 hover:bg-gray-200 rounded transition-colors"
                      >
                        <Volume2 className={`h-4 w-4 ${isSpeaking ? 'text-blue-600' : 'text-gray-600'}`} />
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
            <div ref={messagesEndRef} />
          </div>

          {/* Suggested Questions */}
          {messages.length <= 2 && (
            <div className="p-4 border-t border-gray-100">
              <p className="text-sm text-gray-600 mb-3">Suggested questions:</p>
              <div className="flex flex-wrap gap-2">
                {suggestedQuestions.map((question, index) => (
                  <button
                    key={index}
                    onClick={() => handleSendMessage(question)}
                    className="text-sm bg-blue-50 text-blue-700 px-3 py-1 rounded-full hover:bg-blue-100 transition-colors"
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Input Area */}
          <div className="p-4 border-t border-gray-100">
            <div className="flex items-center space-x-2">
              <div className="flex-1 relative">
                <input
                  type="text"
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage(inputText)}
                  placeholder="Ask anything about this policy..."
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <button
                onClick={handleSpeechToText}
                className={`p-2 rounded-lg transition-colors ${
                  isListening ? 'bg-red-100 text-red-600' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {isListening ? <MicOff className="h-5 w-5" /> : <Mic className="h-5 w-5" />}
              </button>
              <button
                onClick={() => handleSendMessage(inputText)}
                disabled={!inputText.trim()}
                className="p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <Send className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PolicyChat;