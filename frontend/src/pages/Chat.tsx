import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  TextField,
  Button,
  Paper,
  Typography,
  Container,
  List,
  ListItem,
  ListItemText,
  Divider,
  CircularProgress,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import api from '../api';

interface Message {
  type: 'user' | 'bot';
  content: string;
  timestamp: Date;
}

interface ClaimData {
  ssn_last4?: string;
  employer?: string;
  separation_reason?: string;
  earnings?: string;
  employment_months?: string;
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      type: 'bot',
      content: "Hello! I'm Joy, your unemployment insurance assistant. Type 'start claim' to begin filing a new claim, or ask me any questions about unemployment benefits.",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [claimData, setClaimData] = useState<ClaimData>({});
  const [currentStep, setCurrentStep] = useState<string>('welcome');
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const addMessage = (content: string, type: 'user' | 'bot') => {
    setMessages(prev => [...prev, {
      type,
      content,
      timestamp: new Date(),
    }]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isProcessing) return;

    const userInput = input.trim();
    addMessage(userInput, 'user');
    setInput('');
    setIsProcessing(true);

    try {
      await processUserInput(userInput);
    } catch (error) {
      console.error('Error processing input:', error);
      addMessage("I apologize, but I'm having trouble processing your request right now. Please try again.", 'bot');
    } finally {
      setIsProcessing(false);
    }
  };

  const processUserInput = async (input: string) => {
    const lowerInput = input.toLowerCase();

    switch (currentStep) {
      case 'welcome':
        if (lowerInput.includes('start claim')) {
          setCurrentStep('ssn');
          addMessage("Great! Let's start filing your claim. Please provide the last 4 digits of your SSN.", 'bot');
        } else {
          handleGeneralQuery(input);
        }
        break;

      case 'ssn':
        if (/^\d{4}$/.test(input)) {
          setClaimData(prev => ({ ...prev, ssn_last4: input }));
          setCurrentStep('employer');
          addMessage("Thank you. What is the name of your employer?", 'bot');
        } else {
          addMessage("Please provide exactly 4 digits for your SSN.", 'bot');
        }
        break;

      case 'employer':
        setClaimData(prev => ({ ...prev, employer: input }));
        setCurrentStep('reason');
        addMessage("What was the reason for your separation from employment?", 'bot');
        break;

      case 'reason':
        setClaimData(prev => ({ ...prev, separation_reason: input }));
        setCurrentStep('earnings');
        addMessage("What were your total earnings in the last 6 months?", 'bot');
        break;

      case 'earnings':
        if (/^\d+(\.\d{1,2})?$/.test(input)) {
          setClaimData(prev => ({ ...prev, earnings: input }));
          setCurrentStep('months');
          addMessage("How many months were you employed?", 'bot');
        } else {
          addMessage("Please provide a valid number for your earnings.", 'bot');
        }
        break;

      case 'months':
        if (/^\d+$/.test(input)) {
          setClaimData(prev => ({ ...prev, employment_months: input }));
          await submitClaim();
        } else {
          addMessage("Please provide a valid number of months.", 'bot');
        }
        break;

      default:
        handleGeneralQuery(input);
    }
  };

  const handleGeneralQuery = (input: string) => {
    const lowerInput = input.toLowerCase();
    if (lowerInput.includes('eligibility') || lowerInput.includes('qualify')) {
      addMessage("To be eligible for unemployment benefits, you must:\n" +
        "1. Have earned at least $1,000 in the last 6 months\n" +
        "2. Have been employed for at least 3 months\n" +
        "3. Not have quit voluntarily\n" +
        "Would you like to start a claim?", 'bot');
    } else if (lowerInput.includes('status') || lowerInput.includes('check')) {
      addMessage("To check your claim status, please provide the last 4 digits of your SSN.", 'bot');
    } else {
      addMessage("I can help you with:\n" +
        "1. Filing a new claim (type 'start claim')\n" +
        "2. Checking claim status\n" +
        "3. Understanding eligibility requirements\n" +
        "What would you like to know more about?", 'bot');
    }
  };

  const submitClaim = async () => {
    try {
      addMessage("Processing your claim...", 'bot');
      const response = await api.post('/claims/submit', {
        ...claimData,
        earnings: parseFloat(claimData.earnings || '0'),
        employment_months: parseInt(claimData.employment_months || '0')
      });

      const { status, explanation, fraud_score } = response.data;
      addMessage(`Claim Status: ${status.toUpperCase()}\n\n${explanation}\n\nFraud Score: ${fraud_score}`, 'bot');
      
      // Reset for new claim
      setCurrentStep('welcome');
      setClaimData({});
      addMessage("Would you like to file another claim or ask any questions?", 'bot');
    } catch (error) {
      console.error('Error submitting claim:', error);
      addMessage("I apologize, but there was an error processing your claim. Please try again later.", 'bot');
      setCurrentStep('welcome');
      setClaimData({});
    }
  };

  return (
    <Container maxWidth="md" sx={{ height: '100vh', py: 4 }}>
      <Paper elevation={3} sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ p: 2, bgcolor: 'primary.main', color: 'white' }}>
          <Typography variant="h6">Chat with Joy</Typography>
        </Box>
        
        <List sx={{ flex: 1, overflow: 'auto', p: 2 }}>
          {messages.map((message, index) => (
            <React.Fragment key={index}>
              <ListItem
                sx={{
                  justifyContent: message.type === 'user' ? 'flex-end' : 'flex-start',
                }}
              >
                <Paper
                  elevation={1}
                  sx={{
                    p: 2,
                    maxWidth: '70%',
                    bgcolor: message.type === 'user' ? 'primary.light' : 'grey.100',
                    color: message.type === 'user' ? 'white' : 'text.primary',
                    whiteSpace: 'pre-line',
                  }}
                >
                  <ListItemText
                    primary={message.content}
                    secondary={message.timestamp.toLocaleTimeString()}
                  />
                </Paper>
              </ListItem>
              <Divider />
            </React.Fragment>
          ))}
          <div ref={messagesEndRef} />
        </List>

        <Box
          component="form"
          onSubmit={handleSubmit}
          sx={{
            p: 2,
            bgcolor: 'background.paper',
            borderTop: 1,
            borderColor: 'divider',
            display: 'flex',
            gap: 1,
          }}
        >
          <TextField
            fullWidth
            variant="outlined"
            placeholder={isProcessing ? "Processing..." : "Type your message..."}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isProcessing}
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={isProcessing}
            endIcon={isProcessing ? <CircularProgress size={20} color="inherit" /> : <SendIcon />}
          >
            Send
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default Chat; 